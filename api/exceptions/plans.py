class PlanInvalidName(Exception):

    def __init__(self, message: str = "Nome do plano não pode ser inválido ou vazio"):
        super().__init__(message)
        self.status_code = 400

class PlanNotFound(Exception):

    def __init__(self, message: str = "Plano não encontrado"):
        super().__init__(message)
        self.status_code = 404

class PlanNegativePrice(Exception):

    def __init__(self, message: str = "Plano nao pode ter o valor menor ou igual a zero"):
        super().__init__(message)
        self.status_code = 400

class PlanAlreadyExists(Exception):

    def __init__(self, message: str = "Plano ja existente"):
        super().__init__(message)
        self.status_code = 409

class PlanHaveCompanys(Exception):

    def __init__(self, message: str = "Existem clientes com essa assinatura"):
        super().__init__(message)
        self.status_code = 403

