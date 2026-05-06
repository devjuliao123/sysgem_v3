from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

instrumento_bp = Blueprint('instrumentos', __name__, url_prefix='/app/<schema>/instrumentos')

@instrumento_bp.route('/')
def list_instrumentos(schema):
    service = current_app.config['INSTRUMENTO_SERVICE']
    instrumentos = service.get_all(schema)
    columns = service.get_columns(schema)
    return render_template('instrumentos.html', schema=schema, instrumentos=instrumentos, columns=columns)

@instrumento_bp.route('/criar', methods=['POST'])
def create_instrumento(schema):
    service = current_app.config['INSTRUMENTO_SERVICE']
    data = request.form.to_dict()
    service.create(data, schema)
    flash('INSTRUMENTO CADASTRADO!', 'success')
    return redirect(url_for('instrumentos.list_instrumentos', schema=schema))

@instrumento_bp.route('/deletar/<int:id>', methods=['POST'])
def delete_instrumento(schema, id):
    service = current_app.config['INSTRUMENTO_SERVICE']
    service.delete(id, schema)
    flash('INSTRUMENTO REMOVIDO!', 'success')
    return redirect(url_for('instrumentos.list_instrumentos', schema=schema))
