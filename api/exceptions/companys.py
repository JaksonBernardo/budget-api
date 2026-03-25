
class InvalidTypeCompanyId(Exception):

    def __init__(self, message: str = "ID Company deve ser do tipo inteiro"):
        super().__init__(message)


class ZeroCompanyId(Exception):

    def __init__(self, message: str = "ID Company não pode ser menor ou igual a zero"):
        super().__init__(message)


class CompanyNotFound(Exception):

    def __init__(self, message: str = "Company não encontrada"):
        super().__init__(message)
        self.status_code = 404
