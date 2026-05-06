from app.models.models import Aluno, Instrutor, Instrumento, Aula

class BaseService:
    def __init__(self):
        self.data = []
        self.current_id = 1

    def get_all(self):
        return self.data

    def get_by_id(self, id):
        return next((item for item in self.data if item.id == id), None)

    def delete(self, id):
        self.data = [item for item in self.data if item.id != id]
        return True

class AlunoService(BaseService):
    def create(self, nome, instrumento_id, instrutor_id):
        aluno = Aluno(self.current_id, nome, int(instrumento_id), int(instrutor_id))
        self.data.append(aluno)
        self.current_id += 1
        return aluno

class InstrutorService(BaseService):
    def create(self, nome):
        instrutor = Instrutor(self.current_id, nome)
        self.data.append(instrutor)
        self.current_id += 1
        return instrutor

class InstrumentoService(BaseService):
    def create(self, nome):
        instrumento = Instrumento(self.current_id, nome)
        self.data.append(instrumento)
        self.current_id += 1
        return instrumento

class AulaService(BaseService):
    def create(self, aluno_id, instrutor_id, instrumento_id, data, observacao):
        aula = Aula(self.current_id, int(aluno_id), int(instrutor_id), int(instrumento_id), data, observacao)
        self.data.append(aula)
        self.current_id += 1
        return aula

# Instantiate services (Singletons for in-memory storage)
aluno_service = AlunoService()
instrutor_service = InstrutorService()
instrumento_service = InstrumentoService()
aula_service = AulaService()
