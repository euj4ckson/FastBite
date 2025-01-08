from flask import render_template

def render_login():
    return render_template('login.html')  # Template de login

def render_cadastro():
    return render_template('cadastro.html')  # Template de cadastro
def render_cadastro_pedido(produtos):
    return render_template('cadastrar_pedidos.html', produtos = produtos)  # Template de cadastro pedidos

def render_usuarios(usuarios):
    return render_template('usuarios.html', usuarios=usuarios)  # Template para listar usuários
def render_pedidos(pedidos):
    return render_template('pedidos.html', pedidos=pedidos)  # Template para listar pedidos

def render_editar(usuario):
    return render_template('editar.html', usuario=usuario)  # Template para editar usuário


def render_editar_pedido(pedidos):
    return render_template('editar_evento.html', pedidos=pedidos)  # Template para editar usuário
