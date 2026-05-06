from flask import Blueprint, render_template, current_app, g, abort
import re

gem_main_bp = Blueprint('gem_main', __name__, url_prefix='/app/<schema>')

@gem_main_bp.url_value_preprocessor
def pull_schema(endpoint, values):
    g.schema = values.pop('schema', None)


@gem_main_bp.route('/inicio')
def inicio():
    schema = g.schema
    db = current_app.config['DB']

    # Quick stats
    conn = db.get_connection(schema=schema)
    cur = db.get_cursor(conn)
    stats = {}
    try:
        cur.execute("SELECT COUNT(*) as total FROM tb_aluno")
        stats['alunos'] = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM tb_instrutor")
        stats['instrutores'] = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM tb_instrumento")
        stats['instrumentos'] = cur.fetchone()['total']
        cur.execute("SELECT COUNT(*) as total FROM tb_aula")
        stats['aulas'] = cur.fetchone()['total']
    finally:
        cur.close()
        conn.close()

    # Org info
    conn = db.get_connection()
    cur = db.get_cursor(conn)
    try:
        cur.execute("SELECT nome, schema FROM public.tb_organizacao WHERE schema = %s", (schema,))
        org_info = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    return render_template('inicio.html',
                           schema=schema,
                           org_info=org_info,
                           stats=stats)
