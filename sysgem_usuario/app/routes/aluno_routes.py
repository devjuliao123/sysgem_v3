from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.services import aluno_service, instrumento_service, instrutor_service

aluno_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@aluno_bp.route('/')
def list_alunos():
    alunos = aluno_service.get_all()
    instrumentos = instrumento_service.get_all()
    instrutores = instrutor_service.get_all()

    enriched_alunos = []
    for a in alunos:
        instrumento = instrumento_service.get_by_id(a.instrumento_id)
        instrutor = instrutor_service.get_by_id(a.instrutor_id)
        enriched_alunos.append({
            'id': a.id,
            'nome': a.nome,
            'instrumento': instrumento.nome if instrumento else 'N/A',
            'instrutor': instrutor.nome if instrutor else 'N/A'
        })

    return render_template('alunos.html', alunos=enriched_alunos, instrumentos=instrumentos, instrutores=instrutores)

@aluno_bp.route('/criar', methods=['POST'])
def create_aluno():
    nome = request.form.get('nome')
    instrumento_id = request.form.get('instrumento_id')
    instrutor_id = request.form.get('instrutor_id')
    if nome and instrumento_id and instrutor_id:
        aluno_service.create(nome, instrumento_id, instrutor_id)
        flash(f'ALUNO {nome.upper()} CADASTRADO COM SUCESSO!', 'success')
    else:
        flash('ERRO AO CADASTRAR ALUNO. VERIFIQUE OS CAMPOS.', 'danger')
    return redirect(url_for('alunos.list_alunos'))

@aluno_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_aluno(id):
    if aluno_service.delete(id):
        flash('ALUNO REMOVIDO COM SUCESSO!', 'success')
    return redirect(url_for('alunos.list_alunos'))
