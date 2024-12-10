from werkzeug.security import check_password_hash
from flask import Flask, request, redirect, url_for, flash, render_template,session
from back.models import Usuario,Produto,pedido_itens,Pedidos
from back.database import db
from werkzeug.security import generate_password_hash
from back.views import render_login, render_cadastro, render_usuarios,render_pedidos, render_editar,render_editar_pedido
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/minha_aplicacao'
app.config['SECRET_KEY'] = '1q2w3e4rr4e3w2q1'
db.init_app(app)

id_logado = 0
# FUNÇÕES DE LOGIN / VERIFICAÇÃO

def verificalogin():
    if 'logado' in session:
        print('VERIFICAÇÃO LOGIN')
        if session['logado'] == 0:
            print('FOI =0')
            return False
        print('FOI =1')    
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

# FUNÇÕES DE USUARIOS (CRUD)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    redirecionar = verificalogin()
    if redirecionar is not True:
        print('redirecionando')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        session['logado']= 0
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
        print('redirecionando')
        return redirect(url_for('login'))
    usuarios = Usuario.query.all()
    return render_usuarios(usuarios)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    redirecionar = verificalogin()
    if redirecionar is not True:
        print('redirecionando')
        return redirect(url_for('login'))
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('listar_usuarios'))
    
    return render_editar(usuario)

@app.route('/deletar/<int:id>', methods=['GET','POST'])
def deletar_usuario(id):
    redirecionar = verificalogin()
    if redirecionar is not True:
        print('redirecionando')
        return redirect(url_for('login'))
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado com sucesso!')
    return redirect(url_for('listar_usuarios'))

# FUNÇÕES DE pedidoS (CRUD)

@app.route('/pedidos', methods=['GET'])

def listar_pedidos():
    redirecionar = verificalogin()
    if redirecionar is not True:
        print('redirecionando')
        return redirect(url_for('login'))
    global id_logado
    print(id_logado)
    pedidos = Pedidos.query.all()
 

    return render_pedidos(pedidos)


@app.route('/cadastro_pedido', methods=['GET', 'POST'])
def cadastro_pedido():
    if request.method == 'POST':
        cliente_nome = request.form['cliente_nome']
        total_pedido = 0.00

        # Obter os itens do formulário
        itens = []
        for key in request.form.keys():
            if key.startswith('itens['):  # Capturar apenas os campos relacionados aos itens
                itens.append(key)

        parsed_itens = {}
        for item_key in itens:
            # Extrair índice e tipo do campo (produto ou quantidade)
            match = re.match(r'itens\[(\d+)\]\[(\w+)\]', item_key)
            if match:
                index, field = match.groups()
                if index not in parsed_itens:
                    parsed_itens[index] = {}
                parsed_itens[index][field] = request.form[item_key]

        # Processar os itens e calcular o total
        for _, item_data in parsed_itens.items():
            produto_id = int(item_data['produto'])
            quantidade = int(item_data['quantidade'])
            produto = Produto.query.get(produto_id)
            if produto:
                total_pedido += produto.valor * quantidade

        # Criar o pedido
        novo_pedido = Pedidos(cliente_nome=cliente_nome, valor_total=total_pedido)
        db.session.add(novo_pedido)
        db.session.commit()

        # Criar itens do pedido
        for _, item_data in parsed_itens.items():
            produto_id = int(item_data['produto'])
            quantidade = int(item_data['quantidade'])
            novo_item = pedido_itens(pedido_id=novo_pedido.id, produto_id=produto_id, quantidade=quantidade)
            db.session.add(novo_item)

        db.session.commit()

        flash('Pedido cadastrado com sucesso!')
        return redirect(url_for('listar_pedidos'))

    # Pegar a lista de produtos para o formulário
    produtos = Produto.query.all()
    return render_template('cadastro_pedido.html', produtos=produtos)

@app.route('/editar_pedido/<int:id>', methods=['GET', 'POST'])
def editar_pedido(id):
    pedido = Pedidos.query.get_or_404(id)

    # Log do pedido original
    print(f"Pedido original: {pedido.cliente_nome}, Valor Total: {pedido.valor_total}")

    if request.method == 'POST':
        # Log dos dados do formulário
        print(f"Dados do formulário recebidos: {request.form}")

        # Atualizar informações do cliente
        pedido.cliente_nome = request.form['cliente_nome']
        print(f"Nome do cliente atualizado para: {pedido.cliente_nome}")

        # Processar itens do pedido enviados no formulário
        itens_data = []
        for key, value in request.form.items():
            if key.startswith('itens[') and key.endswith('][produto]'):
                index = key.split('[')[1].split(']')[0]  # Extrai o índice do item
                produto_id = int(value)
                quantidade = int(request.form.get(f'itens[{index}][quantidade]', 0))
                itens_data.append({'produto': produto_id, 'quantidade': quantidade})

        # Log dos itens processados
        print(f"Itens processados: {itens_data}")

        novos_itens_ids = []
        novo_valor_total = 0

        # Processar os itens do formulário
        for item_data in itens_data:
            produto_id = item_data['produto']
            quantidade = item_data['quantidade']

            # Obter produto relacionado
            produto = Produto.query.get_or_404(produto_id)
            print(f"Produto selecionado: {produto.nome}, ID: {produto.id}, Preço: {produto.valor}")

            # Tentar encontrar o item existente
            item_existente = pedido_itens.query.filter_by(pedido_id=pedido.id, produto_id=produto_id).first()
            print(f"Item existente: {item_existente} para Produto ID {produto_id}")

            if item_existente:
                # Atualizar item existente
                item_existente.quantidade = quantidade
                db.session.add(item_existente)
                print(f"Item atualizado: Produto ID {produto_id}, Nova Quantidade: {quantidade}")
            else:
                # Adicionar novo item
                novo_item = pedido_itens(pedido_id=pedido.id, produto_id=produto_id, quantidade=quantidade)
                db.session.add(novo_item)
                print(f"Novo item adicionado: Produto ID {produto_id}, Quantidade: {quantidade}")

            # Adicionar o preço do item ao total do pedido
            novo_valor_total += produto.valor * quantidade
            print(f"Novo valor total acumulado: {novo_valor_total}")

            # Adicionar o id do produto à lista de itens processados
            novos_itens_ids.append(produto_id)

        # Excluir itens antigos que não estão mais no pedido
        itens_antigos = pedido_itens.query.filter(pedido_itens.pedido_id == pedido.id).all()
        print(f"Itens antigos: {[item.produto_id for item in itens_antigos]}")
        for item_antigo in itens_antigos:
            if item_antigo.produto_id not in novos_itens_ids:
                db.session.delete(item_antigo)
                print(f"Item excluído: Produto ID {item_antigo.produto_id}")

        # Atualizar o valor total do pedido
        pedido.valor_total = novo_valor_total
        print(f"Valor total do pedido atualizado: {pedido.valor_total}")

        # Salvar alterações no banco de dados
        try:
            db.session.commit()
            print("Alterações salvas no banco de dados com sucesso.")
            flash('Pedido atualizado com sucesso!')
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar alterações no banco de dados: {e}")
            flash('Erro ao atualizar o pedido. Tente novamente.', 'error')

        return redirect(url_for('listar_pedidos'))

    # Carregar lista de produtos e itens do pedido para o formulário
    produtos = Produto.query.all()
    pedido_itens_lista = pedido_itens.query.filter_by(pedido_id=pedido.id).all()

    return render_template(
        'editar_pedido.html',
        pedido=pedido,
        produtos=produtos,
        pedido_itens=pedido_itens_lista,
    )

@app.route('/deletar_pedido/<int:id>', methods=['GET', 'POST'])
def deletar_pedido(id):
    # Verificar login antes de prosseguir
    redirecionar = verificalogin()
    if redirecionar is not True:
        print('Redirecionando para login')
        return redirect(url_for('login'))
    
    # Buscar o pedido ou retornar erro 404
    pedido = Pedidos.query.get_or_404(id)
    
    # Buscar e deletar os itens relacionados ao pedido
    pedido_itensdeletados = pedido_itens.query.filter_by(pedido_id=pedido.id).all()
    for item in pedido_itensdeletados:
        db.session.delete(item)
    
    # Deletar o próprio pedido
    db.session.delete(pedido)
    db.session.commit()
    
    flash('Pedido e itens associados deletados com sucesso!')
    return redirect(url_for('listar_pedidos'))


if __name__ == '__main__':
    app.run(debug=True)   
