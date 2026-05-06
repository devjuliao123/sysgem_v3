from app.modules.base_service import BaseService

class InstrutorService(BaseService):
    def __init__(self, db):
        super().__init__(db, "tb_instrutor")
