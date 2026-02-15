from flask import Flask

""" Instância de aplicação e configurações """
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/silos_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    return app
