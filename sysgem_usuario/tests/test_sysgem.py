import pytest
from app import create_app
from app.services.services import aluno_service, instrutor_service, instrumento_service, aula_service

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_inicio_route(client):
    response = client.get('/inicio')
    assert response.status_code == 200
    assert b"SysGEM Cloud" in response.data

def test_redirect_to_inicio(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/inicio'

def test_instrumento_creation():
    instrumento = instrumento_service.create("Violão")
    assert instrumento.nome == "VIOLÃO"
    assert len(instrumento_service.get_all()) > 0

def test_instrutor_creation():
    instrutor = instrutor_service.create("João")
    assert instrutor.nome == "JOÃO"
    assert len(instrutor_service.get_all()) > 0

def test_aluno_creation():
    # Need instrument and instructor first
    inst = instrumento_service.create("Piano")
    teacher = instrutor_service.create("Maria")
    aluno = aluno_service.create("Pedro", inst.id, teacher.id)
    assert aluno.nome == "PEDRO"
    assert aluno.instrumento_id == inst.id
    assert aluno.instrutor_id == teacher.id

def test_aula_creation():
    aluno = aluno_service.get_all()[0]
    inst = instrumento_service.get_all()[0]
    teacher = instrutor_service.get_all()[0]
    aula = aula_service.create(aluno.id, teacher.id, inst.id, "2025-05-20", "Primeira aula")
    assert aula.observacao == "PRIMEIRA AULA"
