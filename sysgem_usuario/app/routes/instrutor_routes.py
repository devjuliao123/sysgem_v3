from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.services import instrutor_service

instrutor_bp = Blueprint('instrutores', __name__, url_prefix='/instrutores')

@instrutor_bp.route('/')
def list_instrutores():
    instrutores = instrutor_service.get_all()
    return render_template('instrutores.html', instrutores=instrutores)

@instrutor_bp.route('/criar', methods=['POST'])
def create_instrutor():
    nome = request.form.get('nome')
    if nome:
        instrutor_service.create(nome)
        flash(f'INSTRUTOR {nome.upper()} CADASTRADO COM SUCESSO!', 'success')
    else:
        flash('ERRO AO CADASTRAR INSTRUTOR.', 'danger')
    return redirect(url_for('instrutores.list_instrutores'))

@instrutor_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_instrutor(id):
    if instrutor_service.delete(id):
        flash('INSTRUTOR REMOVIDO COM SUCESSO!', 'success')
    return redirect(url_for('instrutores.list_instrutores'))
