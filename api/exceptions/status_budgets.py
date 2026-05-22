
class StatusBudgetInvalidName(Exception):

    def __init__(self, message: str = "Nome do status não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class StatusBudgetNotFound(Exception):

    def __init__(self, message: str = "Status não encontrado"):
        super().__init__(message)
        self.status_code = 404

class StatusBudgetIsSaleAlreadyExists(Exception):

    def __init__(self, message: str = "Já existe um status de venda configurado para esta empresa"):
        super().__init__(message)
        self.status_code = 400

