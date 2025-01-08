from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models import Pedidos, Produto, pedido_itens
from database import db
from views import render_cadastro_pedido,render_pedidos
from usuarios_controllers import init_usuarios
import re

def init_pedidos(app):
    @app.route('/pedidos', methods=['GET'])
    def listar_pedidos():
        try:
            pedidos = Pedidos.query.all()
            return render_template('listar_pedidos.html', pedidos=pedidos)
        except Exception as e:
            flash('Erro ao listar pedidos: ' + str(e))
            return redirect(url_for('listar_pedidos'))

    @app.route('/api/pedido/<int:id>', methods=['GET'])
    def obter_detalhes_pedido(id):
        pedido = Pedidos.query.get_or_404(id)
        pedido_dict = pedido.to_dict()
        for item in pedido_dict['itens']:
            print(pedido_dict)
            produto = Produto.query.get(item['produto_id'])
            item['produto'] = {
                'nome': produto.nome,
                'valor': produto.valor
            }
        return jsonify(pedido_dict)

    @app.route('/cadastro_pedido', methods=['GET', 'POST'])
    def cadastro_pedido():
        if request.method == 'POST':
            cliente_nome = request.form['cliente_nome']
            total_pedido = 0.00
            itens = []
            for key in request.form.keys():
                if key.startswith('itens['):
                    itens.append(key)
            parsed_itens = {}
            for item_key in itens:
                match = re.match(r'itens\[(\d+)\]\[(\w+)\]', item_key)
                if match:
                    index, field = match.groups()
                    if index not in parsed_itens:
                        parsed_itens[index] = {}
                    parsed_itens[index][field] = request.form[item_key]
            for _, item_data in parsed_itens.items():
                produto_id = int(item_data['produto'])
                quantidade = int(item_data['quantidade'])
                produto = Produto.query.get(produto_id)
                if produto:
                    total_pedido += produto.valor * quantidade
            novo_pedido = Pedidos(cliente_nome=cliente_nome, valor_total=total_pedido)
            db.session.add(novo_pedido)
            db.session.commit()
            for _, item_data in parsed_itens.items():
                produto_id = int(item_data['produto'])
                quantidade = int(item_data['quantidade'])
                novo_item = pedido_itens(pedido_id=novo_pedido.id, produto_id=produto_id, quantidade=quantidade)
                db.session.add(novo_item)
            db.session.commit()
            flash('Pedido cadastrado com sucesso!')
            return redirect(url_for('listar_pedidos'))
        
        produtos = Produto.query.all()
        return render_cadastro_pedido(produtos)

    @app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
    def editar_pedido(id):
        pedido = Pedidos.query.get_or_404(id)
        if request.method == 'POST':
            pedido.cliente_nome = request.form['cliente_nome']
            itens_data = []
            for key, value in request.form.items():
                if key.startswith('itens[') and key.endswith('][produto]'):
                    index = key.split('[')[1].split(']')[0]
                    produto_id = int(value)
                    quantidade = int(request.form.get(f'itens[{index}][quantidade]', 0))
                    itens_data.append({'produto': produto_id, 'quantidade': quantidade})
            novos_itens_ids = []
            novo_valor_total = 0
            for item_data in itens_data:
                produto_id = item_data['produto']
                quantidade = item_data['quantidade']
                produto = Produto.query.get_or_404(produto_id)
                item_existente = pedido_itens.query.filter_by(pedido_id=pedido.id, produto_id=produto_id).first()
                if item_existente:
                    item_existente.quantidade = quantidade
                    db.session.add(item_existente)
                else:
                    novo_item = pedido_itens(pedido_id=pedido.id, produto_id=produto_id, quantidade=quantidade)
                    db.session.add(novo_item)
                novo_valor_total += produto.valor * quantidade
                novos_itens_ids.append(produto_id)
            itens_antigos = pedido_itens.query.filter(pedido_itens.pedido_id == pedido.id).all()
            for item_antigo in itens_antigos:
                if item_antigo.produto_id not in novos_itens_ids:
                    db.session.delete(item_antigo)
            pedido.valor_total = novo_valor_total
            db.session.commit()
            flash('Pedido atualizado com sucesso!')
            return redirect(url_for('listar_pedidos'))
        
        produtos = Produto.query.all()
        pedido_itens_lista = pedido_itens.query.filter_by(pedido_id=pedido.id).all()
        return render_template('editar_pedidos.html', pedido=pedido, produtos=produtos, pedido_itens=pedido_itens_lista)

    @app.route('/deletar_pedido/<int:id>', methods=['GET', 'POST'])
    def deletar_pedido(id):  
        pedido = Pedidos.query.get_or_404(id)
        pedido_itensdeletados = pedido_itens.query.filter_by(pedido_id=pedido.id).all()
        for item in pedido_itensdeletados:
            db.session.delete(item)
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido e itens associados deletados com sucesso!')
        return redirect(url_for('listar_pedidos'))
