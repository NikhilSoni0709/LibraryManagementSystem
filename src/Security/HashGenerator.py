# built-in
from passlib.context import CryptContext

class HashGenerator:
    crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def generate(plain_text: str) -> str:
        return HashGenerator.crypt_context.hash(plain_text)
    
    @staticmethod
    def verify(plain_text: str, hashed_text: str) -> bool:
        if HashGenerator.crypt_context.verify(plain_text, hashed_text):
            return True
        return False
