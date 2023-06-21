from cryptography.fernet import Fernet

class Crypt:

    def __init__(self, key = None):
        self._key = Fernet.generate_key() if key is None else key
        self.objFernet = Fernet(self._key)

    def encrypt_text(self, text):
        text_encrypt = self.objFernet.encrypt(str.encode(text))

        return text_encrypt.decode()

    def decrypt_text(self, token):
        text_decrypt = self.objFernet.decrypt(token)

        return text_decrypt.decode()

    @property
    def get_key(self):
        return self._key.decode()
