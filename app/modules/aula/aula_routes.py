from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

aula_bp = Blueprint('aulas', __name__, url_prefix='/app/<schema>/aulas')

def get_services():
    return (
        current_app.config['AULA_SERVICE'],
        current_app.config['ALUNO_SERVICE'],
        current_app.config['INSTRUTOR_SERVICE'],
        current_app.config['INSTRUMENTO_SERVICE']
    )

@aula_bp.route('/')
def list_aulas(schema):
    aula_service, aluno_service, instrutor_service, instrumento_service = get_services()

    aulas = aula_service.get_all(schema)
    alunos = aluno_service.get_all(schema)
    instrutores = instrutor_service.get_all(schema)
    instrumentos = instrumento_service.get_all(schema)
    columns = aula_service.get_columns(schema)

    for a in aulas:
        aluno = next((al for al in alunos if al['id'] == a.get('aluno_id')), None)
        a['aluno_nome'] = aluno['nome'] if aluno else 'N/A'

    return render_template('aulas.html',
                           schema=schema,
                           aulas=aulas,
                           alunos=alunos,
                           instrutores=instrutores,
                           instrumentos=instrumentos,
                           columns=columns)

@aula_bp.route('/criar', methods=['POST'])
def create_aula(schema):
    aula_service, _, _, _ = get_services()
    data = request.form.to_dict()
    aula_service.create(data, schema)
    flash('AULA REGISTRADA!', 'success')
    return redirect(url_for('aulas.list_aulas', schema=schema))

@aula_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_aula(schema, id):
    aula_service, _, _, _ = get_services()
    aula_service.delete(id, schema)
    flash('AULA REMOVIDA!', 'success')
    return redirect(url_for('aulas.list_aulas', schema=schema))
