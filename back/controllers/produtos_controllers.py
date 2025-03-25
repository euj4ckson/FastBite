from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models.models import  Produto
from models.database import db
from routes.views import render_produtos,render_cadastro_produto
from flask import jsonify

def init_produtos(app):
    #SELECT PRODUTOS
    @app.route('/produtos', methods=['GET'])
    def listar_produtos(): 
        try:
            produtos = Produto.query.all()
            print(produtos)
            if not produtos:
                return jsonify({"message": "Nenhum produto encontrado"}), 404
            return render_produtos(produtos)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    #CRIAR PRODUTO
    @app.route('/cadastrar_produto', methods=['GET', 'POST'])
    def cadastrar_produto():
        if request.method == 'POST':
            try:
                dados = request.form  # Mude para request.form, já que é um formulário HTML normal
                nome = dados.get('nome')
                valor = dados.get('valor')

                # Verificar se os dados são válidos
                if not nome or not valor:
                    return jsonify({"error": "Nome e valor são obrigatórios!"}), 400

                # Criando um novo produto
                novo_produto = Produto(nome=nome, valor=float(valor))

                # Adicionando ao banco de dados
                db.session.add(novo_produto)
                db.session.commit()

                return redirect(url_for('listar_produtos'))
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        return render_template('produtos/cadastrar_produto.html')

    #UPDATE PRODUTOS
    @app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
    def editar_produto(id):
        # Buscar o produto pelo ID
        produto = Produto.query.get(id)
        if not produto:
            return jsonify({"message": "Produto não encontrado"}), 404

        if request.method == 'POST':
            try:
                # Captura os dados do formulário
                nome = request.form['nome']
                valor = request.form['valor']

                # Atualiza os dados do produto
                produto.nome = nome
                produto.valor = float(valor)

                # Salva as alterações no banco de dados
                db.session.commit()

                # Redireciona para a página de produtos após a atualização
                return redirect(url_for('listar_produtos'))

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # Caso seja um GET, renderize o formulário com os dados do produto
        return render_template('produtos/editar_produto.html', produto=produto)

    #DELETE PRODUTO
    @app.route('/deletar_produto/<int:id>', methods=['GET', 'POST'])
    def deletar_produto(id):
        try:
            produto = Produto.query.get(id)
            if not produto:
                return jsonify({"message": "Produto não encontrado"}), 404
            db.session.delete(produto)
            db.session.commit()
            return jsonify({"message": "Produto deletado com sucesso"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
 