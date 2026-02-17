# app/__init__.py

from flask import Flask
from app.db.extensions import db, migrate
from flask_cors import CORS
from flask_login import LoginManager

login_manager = LoginManager()

"""Factory pattern para criar app Flask"""
def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:53616d75@localhost:5432/silos_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'daeb0afeb1b37226c94e56512b5963b8c08b241c2bd9819bef786cf89007284b'

    # Inicializa extensões COM o app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Permite requisições do front-end
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # ⚠️ IMPORTANTE: Importa models ANTES de registrar blueprints
    # (senão os blueprints não vão achar os models)
    from app.models.movements import Movements
    from app.models.storage_silo import Storage
    from app.models.tenant import Tenant
    from app.models.user import User


    # Importa blueprints
    from app.routes.silos_bp import silos_bp
    from app.routes.moves_bp import moves_bp
    from app.routes.auth_bp import auth_bp

    # Registra blueprints
    app.register_blueprint(silos_bp, url_prefix='/api/silos')
    app.register_blueprint(moves_bp, url_prefix='/api/movements')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Rota raiz
    @app.route('/')
    def index():
        return {
            'message': 'API Sistema de Armazenagem - Log System Works',
            'status': 'online',
            'endpoints': {
                'silos': '/api/silos',
                'movements': '/api/movements',
                'auth': '/auth'
            }
        }

    # Cria tabelas (se não existirem)
    with app.app_context():
        db.create_all()

    return app