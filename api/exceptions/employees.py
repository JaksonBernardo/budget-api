
class EmployeeNotFound(Exception):

    def __init__(self, message: str = "Colaborador não encontrado"):
        super().__init__(message)
        self.status_code = 404

class EmployeeAccessDenied(Exception):

    def __init__(self, message: str = "Operação não permitida"):
        super().__init__(message)
        self.status_code = 403

class EmployeeInvalidData(Exception):

    def __init__(self, message: str = "Dados do colaborador inválidos"):
        super().__init__(message)
