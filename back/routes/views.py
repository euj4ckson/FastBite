from flask import render_template

def render_login():
    return render_template('login.html')  # Template de login

def render_cadastro():
    return render_template('cadastro.html')  # Template de cadastro

def render_cadastro_pedido(produtos):
    return render_template('pedidos/cadastrar_pedidos.html', produtos = produtos)  # Template de cadastro pedidos

def render_usuarios(usuarios):
    return render_template('usuarios.html', usuarios=usuarios)  # Template para listar usuários
def render_pedidos(pedidos):
    return render_template('pedidos/pedidos.html', pedidos=pedidos)  # Template para listar pedidos

def render_editar(usuario):
    return render_template('pedidos/editar.html', usuario=usuario)  # Template para editar usuário


def render_editar_pedido(pedidos):
    return render_template('editar_evento.html', pedidos=pedidos)  # Template para editar usuário

#PRODUTOS

def render_produtos(produtos):
    return render_template('produtos/listar_produtos.html', produtos=produtos)  # Template para editar usuário

def render_cadastro_produto():
    return render_template('produtos/cadastrar_produto.html')  # Template de cadastro produtos


# PEDIDO CLIENTE
def render_cadastrarpedido_cliente():
    return render_template('pedidos/cadastrarpedido_cliente.html')  # Template de cadastro produtos
def render_acompanhamentopedido_cliente(pedido):
    return render_template('pedidos/acompanhamento.html',pedido=pedido)  # Template de cadastro produtos
