from fastapi import status

class PaymentConditionNotFound(Exception):
    def __init__(self, message: str = "Condição de pagamento não encontrada"):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message)

class PaymentConditionAccesDenied(Exception):
    def __init__(self, message: str = "Acesso negado para esta condição de pagamento"):
        self.message = message
        self.status_code = status.HTTP_403_FORBIDDEN
        super().__init__(self.message)

class PaymentConditionAssociatedWithBudget(Exception):
    def __init__(self, message: str = "Condição de pagamento associada a um orçamento não pode ser excluída"):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message)

class PaymentConditionInvalidName(Exception):
    def __init__(self, message: str = "Nome da condição de pagamento inválido"):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message)

class PaymentConditionNameAlreadyExists(Exception):
    def __init__(self, message: str = "Já existe uma condição de pagamento com este nome para esta empresa"):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message)
