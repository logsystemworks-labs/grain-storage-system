# app/__init__.py

from flask import Flask
from app.db.extensions import db, migrate
from flask_cors import CORS


def create_app():
    """Factory pattern para criar app Flask"""

    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:53616d75@localhost:5432/silos_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False

    # Inicializa extensões COM o app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Permite requisições do front-end

    # ⚠️ IMPORTANTE: Importa models ANTES de registrar blueprints
    # (senão os blueprints não vão achar os models)
    from app.models.movements import Movements
    from app.models.storage_silo import Storage

    # Importa blueprints
    from app.routes.silos_bp import silos_bp
    from app.routes.moves_bp import moves_bp

    # Registra blueprints
    app.register_blueprint(silos_bp, url_prefix='/api/silos')
    app.register_blueprint(moves_bp, url_prefix='/api/movements')

    # Rota raiz
    @app.route('/')
    def index():
        return {
            'message': 'API Sistema de Armazenagem - Log System Works',
            'status': 'online',
            'endpoints': {
                'silos': '/api/silos',
                'movements': '/api/movements'
            }
        }

    # Cria tabelas (se não existirem)
    with app.app_context():
        db.create_all()

    return app