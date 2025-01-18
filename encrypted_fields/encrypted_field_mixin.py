from cryptography.fernet import Fernet
from django.conf import settings


class EncryptedFieldMixin:
    """
    Mixin genérico para adicionar criptografia/descriptografia a campos do Django.
    """
    def __init__(self, *args, **kwargs):
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            raise ValueError("ENCRYPTION_KEY must be set in your environment.")
        self.cipher = Fernet(settings.ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """
        Criptografa o valor antes de salvar no banco de dados.
        """
        if value is not None:
            value = str(value).encode()  # Converte o valor para string e depois para bytes
            return self.cipher.encrypt(value).decode()  # Criptografa e retorna string
        return value

    def from_db_value(self, value, expression, connection):
        """
        Descriptografa o valor ao recuperar do banco de dados.
        """
        if value is not None:
            value = value.encode()  # Converte para bytes
            decrypted = self.cipher.decrypt(value).decode()  # Descriptografa para string
            return self.cast_value(decrypted)  # Converte o valor de volta ao tipo original
        return value

    def cast_value(self, value):
        """
        Sobrescreva este método para converter o valor descriptografado no tipo correto.
        """
        return value  # O padrão é string

    def to_python(self, value):
        """
        Garante que o valor seja descriptografado ao acessá-lo.
        """
        if isinstance(value, str):
            try:
                return self.cast_value(self.cipher.decrypt(value.encode()).decode())
            except Exception:
                return value
        return value

    def get_internal_type(self):
        return "TextField"
