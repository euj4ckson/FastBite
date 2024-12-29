import sys
import os
from flask import Flask
from flask_cors import CORS
# from flask_migrate import Migrate


# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models import db

# Adiciona o diretório 'controllers' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'controllers')))

# Agora você pode importar os controllers
from controllers.usuarios_controllers import init_usuarios
from controllers.pedidos_controllers import init_pedidos
from controllers.produtos_controllers import init_produtos

app = Flask(
    __name__, 
    template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'front', 'templates'),
    static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'front', 'static')
)
CORS(app)
# migrate = migrate(app, db)

# Envia o app para os controllers
init_usuarios(app)
init_pedidos(app)
init_produtos(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/minha_aplicacao'
app.config['SECRET_KEY'] = '1q2w3e4rr4e3w2q1'
db.init_app(app)

if __name__ == '__main__':
    # Definir o host e a porta
    host = '0.0.0.0'
    port = 8000
    # Imprimir a URL de acesso
    print(f"A aplicação Flask está rodando em http://{host}:{port}")
    # Iniciar o servidor
    app.run(debug=True, host=host, port=port)

