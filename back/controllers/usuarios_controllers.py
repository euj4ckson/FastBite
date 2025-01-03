from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models import Usuario
from database import db
from werkzeug.security import check_password_hash, generate_password_hash
 

def init_usuarios(app):
    #SELECT USUARIOS
    @app.route('/usuarios', methods=['GET'])
    def listar_usuarios():
        try:
            usuarios = Usuario.query.all()
            if not usuarios:
                return jsonify({"message": "Nenhum usuário encontrado"}), 404
            lista_usuarios = [usuario.to_dict() for usuario in usuarios]
            return jsonify(lista_usuarios), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    #INSERT USUARIOS
    @app.route('/inserir_usuario', methods=['POST'])
    def criar_usuario():
        try:
            dados = request.json
            novo_usuario = Usuario(
                nome=dados.get('nome'),
                email=dados.get('email'),
                senha=dados.get('senha')
            )
            db.session.add(novo_usuario)
            db.session.commit()
            return jsonify(novo_usuario.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500       
    @app.route('/editar_usuario', methods=['POST'])
    def atualizar_usuario(id):
        try:
            dados = request.json
            usuario = Usuario.query.get(id)
            if not usuario:
                return jsonify({"message": "Usuário não encontrado"}), 404
            usuario.nome = dados.get('nome', usuario.nome)
            usuario.email = dados.get('email', usuario.email)
            usuario.senha = dados.get('senha', usuario.senha)
            db.session.commit()
            return jsonify(usuario.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route('/deletar_usuario/<int:id>', methods=['GET', 'POST'])
    def deletar_usuario(id):
        try:
            usuario = Usuario.query.get(id)
            if not usuario:
                return jsonify({"message": "Usuário não encontrado"}), 404
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"message": "Usuário deletado com sucesso"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500