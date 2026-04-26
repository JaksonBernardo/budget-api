class ServiceInvalidName(Exception):

    def __init__(self, message: str = "Nome do servico não pode ser inválido ou vazio"):
        super().__init__(message)

class ServiceNotFound(Exception):

    def __init__(self, message: str = "Servico não encontrado"):
        super().__init__(message)
        self.status_code = 404

class ServiceAccesDenied(Exception):

    def __init__(self, message: str = "Operação não permitida"):
        super().__init__(message)
        self.status_code = 403