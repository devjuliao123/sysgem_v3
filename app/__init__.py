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

    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

    # Logging
    logging.basicConfig(level=logging.INFO)

    if db_instance:
        db = db_instance
    else:
        # Database Configuration
        db_password = os.getenv("DB_PASSWORD")

        DB_CONFIG = {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": db_password if db_password is not None else "",
            "database": os.getenv("DB_NAME", "db_gem")
        }

        if db_password is None:
             logging.warning("!!!" + "="*50)
             logging.warning("AVISO: A variável DB_PASSWORD não está definida no seu ambiente ou arquivo .env")
             logging.warning("Se o seu PostgreSQL exige senha, a conexão irá falhar.")
             logging.warning("!!!" + "="*50)

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

    # Global schema validation for all operational routes
    @app.before_request
    def global_validate_schema():
        from flask import request, abort, current_app, g
        import re

        # Check if the request is for an operational route (starting with /app/)
        if request.path.startswith('/app/'):
            parts = request.path.split('/')
            if len(parts) > 2:
                schema = parts[2]
                # Security: Strict schema name validation
                if not re.match(r'^org_\d{4}$', schema):
                    abort(400, "Schema inválido")

                # Check if organization exists
                org_service = current_app.config['ORG_SERVICE']
                if not org_service.schema_exists(schema):
                    abort(404, "Organização não encontrada")

                g.schema = schema

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
