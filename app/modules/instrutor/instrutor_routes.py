from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

instrutor_bp = Blueprint('instrutores', __name__, url_prefix='/app/<schema>/instrutores')

def get_services():
    return (
        current_app.config['INSTRUTOR_SERVICE'],
        current_app.config['INSTRUMENTO_SERVICE'],
        current_app.config['COMUM_SERVICE']
    )

@instrutor_bp.route('/')
def list_instrutores(schema):
    instrutor_service, instrumento_service, comum_service = get_services()

    instrutores = instrutor_service.get_all(schema)
    instrumentos = instrumento_service.get_all(schema)
    comuns = comum_service.get_all(schema)
    columns = instrutor_service.get_columns(schema)

    for i in instrutores:
        inst = next((ins for ins in instrumentos if ins['id'] == i.get('instrumento_id')), None)
        i['instrumento_nome'] = inst['nome'] if inst else 'N/A'

    return render_template('instrutores.html',
                           schema=schema,
                           instrutores=instrutores,
                           instrumentos=instrumentos,
                           comuns=comuns,
                           columns=columns)

@instrutor_bp.route('/criar', methods=['POST'])
def create_instrutor(schema):
    instrutor_service, _, _ = get_services()
    data = request.form.to_dict()
    try:
        instrutor_service.create(data, schema)
        flash('INSTRUTOR CADASTRADO COM SUCESSO!', 'success')
    except Exception as e:
        flash(f'ERRO: {str(e)}', 'danger')
    return redirect(url_for('instrutores.list_instrutores', schema=schema))

@instrutor_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_instrutor(schema, id):
    instrutor_service, _, _ = get_services()
    instrutor_service.delete(id, schema)
    flash('INSTRUTOR REMOVIDO!', 'success')
    return redirect(url_for('instrutores.list_instrutores', schema=schema))
