from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirect to /inicio as requested
    from flask import redirect, url_for
    return redirect(url_for('main.inicio'))

@main_bp.route('/inicio')
def inicio():
    return render_template('inicio.html')
