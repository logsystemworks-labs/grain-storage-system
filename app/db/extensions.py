# app/db/extensions.py

"""  Extensões de conexão com o banco de dados  """
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
