from models import Pedidos, Produto, pedido_itens,Usuario
from flask import jsonify

def init_produtos(app):
    @app.route('/produtos', methods=['GET'])
    # LISTA PRODUTOS
    def listar_produtos(): 
        produtos = Produto.query.all()
        lista_produtos = [produto.to_dict() for produto in produtos]  # Corrigido uso de "produto" (minúsculo)
        return jsonify(lista_produtos), 200

    