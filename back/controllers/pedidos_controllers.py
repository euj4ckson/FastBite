from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models.models import Pedidos, Produto, pedido_itens
from models.database import db
from routes.views import render_cadastro_pedido, render_acompanhamentopedido_cliente
from datetime import datetime, timedelta
from flask import request, jsonify
import re

def init_pedidos(app):
    @app.route('/pedidos', methods=['GET'])
    def listar_pedidos():
    # Capturar os parâmetros de data
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        apenas_nao_finalizados = request.args.get('entregues') == 'on'   
 
        query = Pedidos.query
 
        if data_inicio:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')   
                query = query.filter(Pedidos.criado_em >= data_inicio)
            except ValueError:
                raise ValueError("Formato inválido para data_inicio. Use o formato YYYY-MM-DD.")

        if data_fim:
            try:
                
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
                query = query.filter(Pedidos.criado_em <= data_fim)
            except ValueError:
                raise ValueError("Formato inválido para data_fim. Use o formato YYYY-MM-DD.")

        query = query.order_by(Pedidos.criado_em.desc())
        if apenas_nao_finalizados:
            query = query.filter(Pedidos.entregue == False)  

      
        pedidos = query.all()


        # Calcular o valor do caixa com os pedidos filtrados
        valor_caixa = sum(pedido.valor_total for pedido in pedidos)

        # Renderizar a página
        return render_template('pedidos/listar_pedidos.html', pedidos=pedidos, valor_caixa=valor_caixa)
    @app.route('/api/pedidos', methods=['GET'])
    def api_listar_pedidos():
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        apenas_nao_finalizados = request.args.get('entregues') == 'on'   

        query = Pedidos.query

        if data_inicio:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')   
                query = query.filter(Pedidos.criado_em >= data_inicio)
            except ValueError:
                return jsonify({"erro": "Formato inválido para data_inicio"}), 400

        if data_fim:
            try:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
                query = query.filter(Pedidos.criado_em <= data_fim)
            except ValueError:
                return jsonify({"erro": "Formato inválido para data_fim"}), 400

        if apenas_nao_finalizados:
            query = query.filter(Pedidos.entregue == False)  

        pedidos = query.order_by(Pedidos.criado_em.desc()).all()

        pedidos_json = [{
            "id": pedido.id,
            "cliente_nome": pedido.cliente_nome,
            "valor_total": float(pedido.valor_total) if pedido.valor_total else 0, 
            "criado_em": pedido.criado_em.strftime('%d/%m/%Y %H:%M'),
            "entregue": pedido.entregue
        } for pedido in pedidos]

        return jsonify({"pedidos": pedidos_json})

    @app.route('/api/pedido/<int:id>', methods=['GET'])
    def obter_detalhes_pedido(id):
        pedido = Pedidos.query.get_or_404(id)
        pedido_dict = pedido.to_dict()
        for item in pedido_dict['itens']:
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
            observacao = request.form['observacao']
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
            novo_pedido = Pedidos(cliente_nome=cliente_nome, valor_total=total_pedido, observacao= observacao)
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
        
        produtos = [produto.to_dict() for produto in Produto.query.all()]
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
        
        produtos = [produto.to_dict() for produto in Produto.query.all()]

        pedido_itens_lista = pedido_itens.query.filter_by(pedido_id=pedido.id).all()
        return render_template('pedidos/editar_pedidos.html', pedido=pedido, produtos=produtos, pedido_itens=pedido_itens_lista)

    @app.route('/deletar_pedido/<int:id>', methods=['GET', 'POST'])
    def deletar_pedido(id):  
        pedido = Pedidos.query.get_or_404(id)
        pedido_itensdeletados = pedido_itens.query.filter_by(pedido_id=pedido.id).all()
        for item in pedido_itensdeletados:
            db.session.delete(item)
        db.session.delete(pedido)
        db.session.commit()
        return redirect(url_for('listar_pedidos'))
    @app.route('/confirmar_pedido/<int:id>', methods=['GET', 'POST'])
    def confirmar_pedido(id):
        pedido = Pedidos.query.get_or_404(id)
        pedido.entregue = 1  # Atualiza o status para entregue
        db.session.commit()
        flash('Pedido marcado como finalizado com sucesso!')
        return redirect(url_for('listar_pedidos'))
    @app.route('/Entregar_pedido/<int:id>', methods=['GET', 'POST'])
    def Entregar_pedido(id):
        pedido = Pedidos.query.get_or_404(id)
        pedido.entregue = 2  # Atualiza o status para entregue
        db.session.commit()
        return redirect(url_for('acompanhamento_pedido', pedido_id=id))
    @app.route('/cadastrarpedido_clientes', methods=['GET','POST'])
    def cadastrarpedido_clientes():
        data = request.get_json()  # <-- Aqui pegamos os dados JSON

        if not data:
            return jsonify({"error": "Dados inválidos!"}), 400

        cliente_nome = data.get('cliente_nome')
        observacao = data.get('observacao', '')
        endereco = data.get('endereco','')  # Obter o endereço do JSON
        itens = data.get('itens', [])
        forma_pagamento = data.get('forma_pagamento')
        valor_entregue = data.get('valor_entregue')  # pode ser None se não for dinheiro


        if not cliente_nome or not itens or not endereco:  # Verificar se o endereço foi informado
            return jsonify({"error": "Nome do cliente, endereço e itens são obrigatórios!"}), 400

        total_pedido = 0.00
        for item in itens:
            produto_id = int(item['produto'])
            quantidade = int(item['quantidade'])
            produto = Produto.query.get(produto_id)
            if produto:
                total_pedido += produto.valor * quantidade

        novo_pedido = Pedidos(cliente_nome=cliente_nome, valor_total=total_pedido, observacao=observacao, endereco=endereco,forma_pagamento=forma_pagamento,valor_entregue=valor_entregue)  # Passar o endereço
        db.session.add(novo_pedido)
        db.session.commit()

        for item in itens:
            produto_id = int(item['produto'])
            quantidade = int(item['quantidade'])
            novo_item = pedido_itens(pedido_id=novo_pedido.id, produto_id=produto_id, quantidade=quantidade)
            db.session.add(novo_item)

        db.session.commit()

        return jsonify({"message": "Obrigado pelo seu pedido! Ele foi cadastrado com sucesso.", "pedido_id": novo_pedido.id}), 201
 
    @app.route('/acompanhamento/<int:pedido_id>', methods=['GET'])
    
    def acompanhamento_pedido(pedido_id):
        pedido = db.session.execute(db.select(Pedidos).filter_by(id=pedido_id)).scalar_one_or_none()

        if not pedido:
            return render_template("erro.html", mensagem="Pedido não encontrado"), 404

        return render_acompanhamentopedido_cliente(pedido)
    @app.route('/api/acompanhamento/<int:pedido_id>', methods=['GET'])
    def acompanhamento_api(pedido_id):
        pedido = db.session.execute(db.select(Pedidos).filter_by(id=pedido_id)).scalar_one_or_none()
        if not pedido:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        return jsonify({
            'id': pedido.id,
            'cliente_nome': pedido.cliente_nome,
            'endereco': pedido.endereco,
            'observacao': pedido.observacao or "Nenhuma",
            'entregue': pedido.entregue  # Status do pedido (0 = em andamento, 1 = a caminho, 2 = finalizado)
        })
