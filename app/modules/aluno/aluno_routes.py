from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app

aluno_bp = Blueprint('alunos', __name__, url_prefix='/app/<schema>/alunos')

def get_services():
    return (
        current_app.config['ALUNO_SERVICE'],
        current_app.config['INSTRUMENTO_SERVICE'],
        current_app.config['INSTRUTOR_SERVICE']
    )

@aluno_bp.route('/')
def list_alunos(schema):
    aluno_service, instrumento_service, instrutor_service = get_services()

    alunos = aluno_service.get_all(schema)
    instrumentos = instrumento_service.get_all(schema)
    instrutores = instrutor_service.get_all(schema)

    # Get columns for dynamic form
    columns = aluno_service.get_columns(schema)

    # Enrichment for list display (optional but helpful)
    for a in alunos:
        instrumento = next((i for i in instrumentos if i['id'] == a.get('instrumento_id')), None)
        instrutor = next((i for i in instrutores if i['id'] == a.get('instrutor_id')), None)
        a['instrumento_nome'] = instrumento['nome'] if instrumento else 'N/A'
        a['instrutor_nome'] = instrutor['nome'] if instrutor else 'N/A'

    return render_template('alunos.html',
                           schema=schema,
                           alunos=alunos,
                           instrumentos=instrumentos,
                           instrutores=instrutores,
                           columns=columns)

@aluno_bp.route('/criar', methods=['POST'])
def create_aluno(schema):
    aluno_service, _, _ = get_services()

    # Request form is a ImmutableMultiDict, convert to regular dict
    data = request.form.to_dict()

    try:
        aluno_service.create(data, schema)
        flash(f'ALUNO CADASTRADO COM SUCESSO!', 'success')
    except Exception as e:
        flash(f'ERRO AO CADASTRAR ALUNO: {str(e)}', 'danger')

    return redirect(url_for('alunos.list_alunos', schema=schema))

@aluno_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_aluno(schema, id):
    aluno_service, _, _ = get_services()
    if aluno_service.delete(id, schema):
        flash('ALUNO REMOVIDO COM SUCESSO!', 'success')
    return redirect(url_for('alunos.list_alunos', schema=schema))
