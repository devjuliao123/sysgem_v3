from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.services import aula_service, aluno_service, instrutor_service, instrumento_service

aula_bp = Blueprint('aulas', __name__, url_prefix='/aulas')

@aula_bp.route('/')
def list_aulas():
    aulas = aula_service.get_all()
    alunos = aluno_service.get_all()
    instrutores = instrutor_service.get_all()
    instrumentos = instrumento_service.get_all()

    enriched_aulas = []
    for a in aulas:
        aluno = aluno_service.get_by_id(a.aluno_id)
        instrutor = instrutor_service.get_by_id(a.instrutor_id)
        instrumento = instrumento_service.get_by_id(a.instrumento_id)
        enriched_aulas.append({
            'id': a.id,
            'aluno': aluno.nome if aluno else 'N/A',
            'instrutor': instrutor.nome if instrutor else 'N/A',
            'instrumento': instrumento.nome if instrumento else 'N/A',
            'data': a.data,
            'observacao': a.observacao
        })

    return render_template('aulas.html', aulas=enriched_aulas, alunos=alunos, instrutores=instrutores, instrumentos=instrumentos)

@aula_bp.route('/criar', methods=['POST'])
def create_aula():
    aluno_id = request.form.get('aluno_id')
    instrutor_id = request.form.get('instrutor_id')
    instrumento_id = request.form.get('instrumento_id')
    data = request.form.get('data')
    observacao = request.form.get('observacao')

    if aluno_id and instrutor_id and instrumento_id and data:
        aula_service.create(aluno_id, instrutor_id, instrumento_id, data, observacao)
        flash('AULA REGISTRADA COM SUCESSO!', 'success')
    else:
        flash('ERRO AO REGISTRAR AULA. VERIFIQUE OS DADOS.', 'danger')
    return redirect(url_for('aulas.list_aulas'))

@aula_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_aula(id):
    if aula_service.delete(id):
        flash('AULA REMOVIDA COM SUCESSO!', 'success')
    return redirect(url_for('aulas.list_aulas'))
