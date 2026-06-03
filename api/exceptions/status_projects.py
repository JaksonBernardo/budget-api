
class StatusProjectInvalidName(Exception):

    def __init__(self, message: str = "Nome do status não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class StatusProjectNotFound(Exception):

    def __init__(self, message: str = "Status não encontrado"):
        super().__init__(message)
        self.status_code = 404

class StatusProjectIsCompletedAlreadyExists(Exception):

    def __init__(self, message: str = "Já existe um status de finalização configurado para esta empresa"):
        super().__init__(message)
        self.status_code = 400

class StatusProjectAccesDenied(Exception):

    def __init__(self, message: str = "Acesso negado aos status do projeto"):
        super().__init__(message)
        self.status_code = 403
