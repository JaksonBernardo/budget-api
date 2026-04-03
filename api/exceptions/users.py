class UserNotFound(Exception):

    def __init__(self, message: str = "Usuário não encontrado"):
        super().__init__(message)
        self.status_code = 404


class UserAlreadyExists(Exception):

    def __init__(self, message: str = "E-mail já cadastrado"):
        super().__init__(message)
        self.status_code = 409


class UserAccessDenied(Exception):

    def __init__(self, message: str = "Acesso negado ao usuário"):
        super().__init__(message)
        self.status_code = 403


class InvalidUserId(Exception):

    def __init__(self, message: str = "ID do usuário inválido"):
        super().__init__(message)
        self.status_code = 400
