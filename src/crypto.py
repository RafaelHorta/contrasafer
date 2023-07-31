from cryptography.fernet import Fernet

class Crypto:

    def __init__(self, key: str = None) -> None:
        self._key = Fernet.generate_key() if key is None else key
        self.objFernet = Fernet(self._key)

    def encrypt(self, text: str) -> str:
        text_encrypt = self.objFernet.encrypt(text.encode())

        return text_encrypt.decode()

    def decrypt(self, token : str) -> str:
        text_decrypt = self.objFernet.decrypt(token)

        return text_decrypt.decode()

    @property
    def get_key(self) -> str:
        return self._key.decode()
