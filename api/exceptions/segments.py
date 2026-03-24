
class SegmentInvalidName(Exception):

    def __init__(self, message: str = "Nome do segmento não pode ser inválido ou vazio"):
        super().__init__(message)




