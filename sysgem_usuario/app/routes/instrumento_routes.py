from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.services import instrumento_service

instrumento_bp = Blueprint('instrumentos', __name__, url_prefix='/instrumentos')

@instrumento_bp.route('/')
def list_instrumentos():
    instrumentos = instrumento_service.get_all()
    return render_template('instrumentos.html', instrumentos=instrumentos)

@instrumento_bp.route('/criar', methods=['POST'])
def create_instrumento():
    nome = request.form.get('nome')
    if nome:
        instrumento_service.create(nome)
        flash(f'INSTRUMENTO {nome.upper()} CADASTRADO COM SUCESSO!', 'success')
    else:
        flash('ERRO AO CADASTRAR INSTRUMENTO.', 'danger')
    return redirect(url_for('instrumentos.list_instrumentos'))

@instrumento_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_instrumento(id):
    if instrumento_service.delete(id):
        flash('INSTRUMENTO REMOVIDO COM SUCESSO!', 'success')
    return redirect(url_for('instrumentos.list_instrumentos'))
