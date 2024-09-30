from flask import render_template

def render_login():
    return render_template('login.html')  # Template de login

def render_cadastro():
    return render_template('cadastro.html')  # Template de cadastro
def render_cadastro_evento():
    return render_template('cadastro_evento.html')  # Template de cadastro eventos

def render_usuarios(usuarios):
    return render_template('usuarios.html', usuarios=usuarios)  # Template para listar usuários
def render_eventos(eventos):
    return render_template('eventos.html', eventos=eventos)  # Template para listar eventos

def render_editar(usuario):
    return render_template('editar.html', usuario=usuario)  # Template para editar usuário


def render_editar_evento(eventos):
    return render_template('editar_evento.html', eventos=eventos)  # Template para editar usuário
