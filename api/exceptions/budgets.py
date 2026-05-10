

class BudgetNotFound(Exception):

    def __init__(self, message: str = "Orcamento não encontrado"):
        super().__init__(message)
        self.status_code = 404

