class Aluno:
    def __init__(self, id, nome, instrumento_id, instrutor_id):
        self.id = id
        self.nome = nome.upper()
        self.instrumento_id = instrumento_id
        self.instrutor_id = instrutor_id

class Instrutor:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome.upper()

class Instrumento:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome.upper()

class Aula:
    def __init__(self, id, aluno_id, instrutor_id, instrumento_id, data, observacao):
        self.id = id
        self.aluno_id = aluno_id
        self.instrutor_id = instrutor_id
        self.instrumento_id = instrumento_id
        self.data = data
        self.observacao = observacao.upper()
