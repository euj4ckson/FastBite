import sys
import os
from flask import Flask
from flask_cors import CORS
from waitress import serve
# from flask_migrate import Migrate


# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models.models import db

# Adiciona o diretório 'controllers' ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'controllers')))

# importar os controllers
from controllers.usuarios_controllers import init_usuarios
from controllers.pedidos_controllers import init_pedidos
from controllers.produtos_controllers import init_produtos
from controllers.login_controllers import init_login
from controllers.cupom_controller import initcupom

app = Flask(
    __name__, 
    template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'front','templates' ),
    static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'front', 'src','static')
)
CORS(app)
# migrate = migrate(app, db)

# Envia o app para os controllers
init_usuarios(app)
init_pedidos(app)
init_produtos(app)
init_login(app)
initcupom(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gpQEgnKhEixOpMYwCuHgEHfZNVxiXlFD@nozomi.proxy.rlwy.net:12713/minha_aplicacao'
app.config['SECRET_KEY'] = 'a3f1c9d7e4b5c6a8f2e9d1b7c0a5e6f4d3b2c1a7f8e9d6c5a4b3c2d1e7f9g8h'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gpQEgnKhEixOpMYwCuHgEHfZNVxiXlFD@nozomi.proxy.rlwy.net:12713/minha_aplicacao?charset=utf8mb4'

db.init_app(app)

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 8000))
    
    print(f"A aplicação Flask está rodando em http://{host}:{port}")
    serve(app, host=host, port=port)
