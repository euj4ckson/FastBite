from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint,jsonify
from models import Usuario
from werkzeug.security import check_password_hash
def init_login(app):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']

            # Verificar se o usuário existe no banco
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                session['usuario_id'] = usuario.id
                session['usuario_nome'] = usuario.nome
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('listar_pedidos'))  # Substitua pela rota desejada após login
            else:
                flash('Email ou senha inválidos.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('usuario_id', None)
        session.pop('usuario_nome', None)
        flash('Você saiu da sua conta.', 'info')
        return redirect(url_for('login'))