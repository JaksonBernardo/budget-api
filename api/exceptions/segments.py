
class SegmentInvalidName(Exception):

    def __init__(self, message: str = "Nome do segmento não pode ser inválido ou vazio"):
        super().__init__(message)

class SegmentNotFound(Exception):

    def __init__(self, message: str = "Segmento não encontrado"):
        super().__init__(message)
        self.status_code = 404

class SegmentAccesDenied(Exception):

    def __init__(self, message: str = "Operação não permitida"):
        super().__init__(message)
        self.status_code = 403

