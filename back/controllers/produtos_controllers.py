from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models import Pedidos, Produto, pedido_itens,Usuario
from database import db
from flask import jsonify

def init_produtos(app):
    #SELECT PRODUTOS
    @app.route('/produtos', methods=['GET'])
    def listar_produtos(): 
        try:
            produtos = Produto.query.all()
            if not produtos:
                return jsonify({"message": "Nenhum produto encontrado"}), 404
            lista_produtos = [produto.to_dict() for produto in produtos]
            return jsonify(lista_produtos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    #CRIAR PRODUTO
    @app.route('/criar_produto', methods=['POST'])
    def criar_produto():
        try:
            dados = request.json
            novo_produto = Produto(
                nome=dados.get('nome'),
                valor=dados.get('valor')
            )
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify(novo_produto.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500  
    #UPDATE PRODUTOS
    @app.route('/put_produto/<int:id>', methods=['PUT'])
    def atualizar_produto(id):
        try:
            dados = request.json
            produto = Produto.query.get(id)
            if not produto:
                return jsonify({"message": "Produto não encontrado"}), 404
            produto.nome = dados.get('nome', produto.nome)
            produto.valor = dados.get('valor', produto.valor)
            db.session.commit()
            return jsonify(produto.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
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
 