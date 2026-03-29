class SupplierNotFound(Exception):

    def __init__(self, message: str = "Fornecedor não encontrado"):
        super().__init__(message)
        self.status_code = 404


class SupplierAccesDenied(Exception):

    def __init__(self, message: str = "Acesso negado ao fornecedor"):
        super().__init__(message)
        self.status_code = 403
