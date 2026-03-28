
class ClientNotFound(Exception):

    def __init__(self, message: str = "Cliente não encontrado"):
        super().__init__(message)
        self.status_code = 404


class ClientAccesDenied(Exception):

    def __init__(self, message: str = "Acesso negado ao cliente"):
        super().__init__(message)
        self.status_code = 403




