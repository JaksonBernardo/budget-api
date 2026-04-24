class PriceInvalidName(Exception):

    def __init__(self, message: str = "Nome do Price não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class PriceNotFound(Exception):

    def __init__(self, message: str = "Price não encontrado"):
        super().__init__(message)
        self.status_code = 404

class PriceInvalidValue(Exception):

    def __init__(self, message: str = "Price nao pode ter nenhuma taxa negativa"):
        super().__init__(message)
        self.status_code = 400

class PriceExceedValue(Exception):

    def __init__(self, message: str = "Price nao pode ter a soma das taxas maior que 100"):
        super().__init__(message)
        self.status_code = 400
