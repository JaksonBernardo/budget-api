class SupplierNotFound(Exception):

    def __init__(self, message: str = "Fornecedor não encontrado"):
        super().__init__(message)
        self.status_code = 404

class ZeroSupplierId(Exception):

    def __init__(self, message: str = "ID Supplier não pode ser menor ou igual a zero"):
        super().__init__(message)
        self.status_code = 400

class SupplierAccesDenied(Exception):

    def __init__(self, message: str = "Acesso negado ao fornecedor"):
        super().__init__(message)
        self.status_code = 403
