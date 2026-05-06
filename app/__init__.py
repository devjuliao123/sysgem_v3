from flask import Flask, redirect, url_for
import os
import logging
from app.core.database import Database
from app.admin.organization_service import OrganizationService
from app.modules.aluno.aluno_service import AlunoService
from app.modules.instrutor.instrutor_service import InstrutorService
from app.modules.instrumento.instrumento_service import InstrumentoService
from app.modules.aula.aula_service import AulaService
from app.modules.comum.comum_service import ComumService

def create_app(db_instance=None):
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')

    app.secret_key = os.urandom(24)

    # Logging
    logging.basicConfig(level=logging.INFO)

    if db_instance:
        db = db_instance
    else:
        # Database Configuration
        DB_CONFIG = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
            "database": os.getenv("DB_NAME", "db_gem")
        }
        db = Database(DB_CONFIG)

    # Services
    org_service = OrganizationService(db)
    aluno_service = AlunoService(db)
    instrutor_service = InstrutorService(db)
    instrumento_service = InstrumentoService(db)
    aula_service = AulaService(db)
    comum_service = ComumService(db)

    # App Config Store
    app.config['DB'] = db
    app.config['ORG_SERVICE'] = org_service
    app.config['ALUNO_SERVICE'] = aluno_service
    app.config['INSTRUTOR_SERVICE'] = instrutor_service
    app.config['INSTRUMENTO_SERVICE'] = instrumento_service
    app.config['AULA_SERVICE'] = aula_service
    app.config['COMUM_SERVICE'] = comum_service

    # Blueprints
    from app.admin.organization_routes import admin_org_bp
    from app.modules.main_routes import gem_main_bp
    from app.modules.aluno.aluno_routes import aluno_bp
    from app.modules.instrutor.instrutor_routes import instrutor_bp
    from app.modules.instrumento.instrumento_routes import instrumento_bp
    from app.modules.aula.aula_routes import aula_bp

    app.register_blueprint(admin_org_bp)
    app.register_blueprint(gem_main_bp)
    app.register_blueprint(aluno_bp)
    app.register_blueprint(instrutor_bp)
    app.register_blueprint(instrumento_bp)
    app.register_blueprint(aula_bp)

    # Admin Main Route
    from flask import Blueprint, render_template
    admin_main_bp = Blueprint('admin_main', __name__, url_prefix='/admin')

    @admin_main_bp.route('/')
    def index():
        return render_template('admin_index.html')

    app.register_blueprint(admin_main_bp)

    @app.route('/')
    def root():
        return redirect(url_for('admin_main.index'))

    return app
