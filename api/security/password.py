from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Gera o hash argon2 de uma senha."""
    return _ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Verifica se a senha informada corresponde ao hash armazenado."""
    try:
        _ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
