class MaterialInvalidName(Exception):

    def __init__(self, message: str = "Nome do material não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class MaterialNotFound(Exception):

    def __init__(self, message: str = "Material não encontrado"):
        super().__init__(message)
        self.status_code = 404

class MaterialInvalidClassification(Exception):

    def __init__(self, message: str = "Classificação Inválida"):
        super().__init__(message)
        self.status_code = 409

