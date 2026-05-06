from flask import Flask
import os

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.urandom(24)

    from app.routes.main import main_bp
    from app.routes.aluno_routes import aluno_bp
    from app.routes.instrutor_routes import instrutor_bp
    from app.routes.instrumento_routes import instrumento_bp
    from app.routes.aula_routes import aula_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(instrutor_bp)
    app.register_blueprint(instrumento_bp)
    app.register_blueprint(aula_bp)

    return app
