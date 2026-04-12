
class InvalidNameCompany(Exception):

    def __init__(self, message: str = "Nome nao pode ser vazio"):
        super().__init__(message)
        self.status_code = 400

class CnpjAlreadyExists(Exception):

    def __init__(self, message: str = "CNPJ ja cadastrado na plataforma"):
        super().__init__(message)
        self.status_code = 400

class NameAlreadyExists(Exception):

    def __init__(self, message: str = "Nome da empresa ja existente"):
        super().__init__(message)
        self.status_code = 400


class InvalidTypeCompanyId(Exception):

    def __init__(self, message: str = "ID Company deve ser do tipo inteiro"):
        super().__init__(message)
        self.status_code = 400

class ZeroCompanyId(Exception):

    def __init__(self, message: str = "ID Company não pode ser menor ou igual a zero"):
        super().__init__(message)
        self.status_code = 400


class CompanyNotFound(Exception):

    def __init__(self, message: str = "Company não encontrada"):
        super().__init__(message)
        self.status_code = 404
