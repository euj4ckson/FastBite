from flask import Flask, request, redirect, url_for, flash, render_template
from models import Usuario
from database import db
from werkzeug.security import generate_password_hash
from views import render_login, render_cadastro, render_usuarios, render_editar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://teste:novasenha@127.0.0.1:3306/minha_aplicacao'
app.config['SECRET_KEY'] = 'sua_chave_secreta'
db.init_app(app)

@app.route('/')
def home():
    print("Acessando a página inicial")  # Para debug
    return render_template('index.html')  # Página inicial

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('login'))
    
    return render_cadastro()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_login()

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_usuarios(usuarios)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('listar_usuarios'))
    
    return render_editar(usuario)

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado com sucesso!')
    return redirect(url_for('listar_usuarios'))

if __name__ == '__main__':
    app.run(debug=True)  # Ative o modo de debug
