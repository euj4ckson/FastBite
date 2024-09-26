from flask import render_template

def render_login():
    return render_template('login.html')  # Template de login

def render_cadastro():
    return render_template('cadastro.html')  # Template de cadastro

def render_usuarios(usuarios):
    return render_template('usuarios.html', usuarios=usuarios)  # Template para listar usuários

def render_editar(usuario):
    return render_template('editar.html', usuario=usuario)  # Template para editar usuário
