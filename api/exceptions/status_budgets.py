
class StatusBudgetInvalidName(Exception):

    def __init__(self, message: str = "Nome do status não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class StatusBudgetNotFound(Exception):

    def __init__(self, message: str = "Status não encontrado"):
        super().__init__(message)
        self.status_code = 404

