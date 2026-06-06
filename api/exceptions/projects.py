class ProjectInvalidOs(Exception):

    def __init__(self, message: str = "Numero da OS invalido"):
        super().__init__(message)
        self.status_code = 400

class ProjectNotFound(Exception):

    def __init__(self, message: str = "Projeto nao encontrado"):
        super().__init__(message)
        self.status_code = 404


