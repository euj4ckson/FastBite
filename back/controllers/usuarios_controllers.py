from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models import Usuario
from database import db
from werkzeug.security import check_password_hash, generate_password_hash
 

def init_usuarios(app):
        # LISTA USUARIOS
        @app.route('/usuarios', methods=['GET'])
        def listar_Usuario(): 
            usuarios = Usuario.query.all()
            lista_Usuario = [usuario.to_dict() for usuario in usuarios]  # Corrigido uso de "produto" (minúsculo)
            return jsonify(lista_Usuario), 200

