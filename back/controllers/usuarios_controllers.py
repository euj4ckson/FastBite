from flask import Flask, request, redirect, url_for, flash, render_template,session,Blueprint
from models import Usuario
from database import db
from werkzeug.security import check_password_hash, generate_password_hash
from views import render_login, render_cadastro, render_usuarios, render_editar

def initt(app):
    # Funções de login / verificação
    def verificalogin():
        if 'logado' in session:
            if session['logado'] == 0:
                return False
            return True
    @app.route('/', methods=['GET', 'POST'])
    def login():
        session['logado'] = False
        logado_status = session.get('logado', 'Sessão não encontrada!')
        print(f'Status de logado: {logado_status}')

        if request.method == 'POST':
            print("ENTRANDO EM VERIFICAÇÃO")
            logado_status = session.get('logado', 'Sessão não encontrada!')
            print(f'Status de logado: {logado_status}')
            nome = request.form['nome']
            senha = request.form['senha']

            # Verifica se o usuário existe
            usuario = Usuario.query.filter_by(nome=nome).first()
            
            if usuario and check_password_hash(usuario.senha, senha):
                global id_logado
                id_logado = usuario.id
                flash('Login realizado com sucesso!')
                session['logado'] = True
                # Aqui você pode redirecionar para a página inicial ou outra página
                return listar_usuarios()  # Mantenha o retorno conforme desejado
            else:
                flash('Email ou senha incorretos. Tente novamente.')

        return render_login()  # Retorno para renderizar a página de login

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        
        redirecionar = verificalogin()
        if redirecionar is not True:
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            session['logado'] = 0
            senha = generate_password_hash(request.form['senha'])
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário cadastrado com sucesso!')
            return redirect(url_for('login'))
        
        return render_cadastro()

    @app.route('/usuarios', methods=['GET'])
    def listar_usuarios():
        redirecionar = verificalogin()
        if redirecionar is not True:
            return redirect(url_for('login'))
        usuarios = Usuario.query.all()
        return render_usuarios(usuarios)

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        redirecionar = verificalogin()
        if redirecionar is not True:
            return redirect(url_for('login'))
        usuario = Usuario.query.get_or_404(id)
        if request.method == 'POST':
            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            db.session.commit()
            flash('Usuário atualizado com sucesso!')
            return redirect(url_for('listar_usuarios'))
        return render_editar(usuario)

    @app.route('/deletar/<int:id>', methods=['GET', 'POST'])
    def deletar_usuario(id):
        redirecionar = verificalogin()
        if redirecionar is not True:
            return redirect(url_for('login'))
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário deletado com sucesso!')
        return redirect(url_for('listar_usuarios'))
