from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from .encrypted_file_mixin import EncryptedFileMixin
from django.core.files.storage import default_storage
from PIL import Image
import os


class EncryptedFileField(models.FileField):
    """
    Um campo de arquivo criptografado.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cryptographer = EncryptedFileMixin()  # Instanciando o EncryptedFileMixin para usá-lo

    def pre_save(self, model_instance, add):
        image = getattr(model_instance, self.attname)

        if image:
            if image.size == 0:
                model_instance.__dict__[self.attname] = None
            else:
                # Corrige o nome do arquivo
                image.name = os.path.basename(image.name)
                encrypted_image = self._encrypt_image(image)
                model_instance.__dict__[self.attname] = encrypted_image
        else:
            model_instance.__dict__[self.attname] = None

        return super().pre_save(model_instance, add)

    def _encrypt_file(self, file):
        """
        Função para criptografar o arquivo antes de ser salvo.
        """
        content = file.read()  # Lê o conteúdo do arquivo
        encrypted_content = self.cryptographer.encrypted(content)  # Chama o método encrypted() da instância

        if isinstance(encrypted_content, bytes):
            encrypted_file = BytesIO(encrypted_content)
            encrypted_file.name = file.name  # Mantém o nome original do arquivo
            encrypted_file.size = len(encrypted_content)  # Ajusta o tamanho do arquivo
            encrypted_file.seek(0)  # Posiciona o ponteiro do arquivo no início
            return ContentFile(encrypted_file.read(), name=file.name)  # Retorna o arquivo criptografado como ContentFile
        else:
            raise ValueError("A criptografia falhou, o conteúdo não é um tipo de dado esperado.")

    def from_db_value(self, value, expression, connection, context=None):
        """
        Descriptografa o arquivo ao ser acessado do banco de dados.
        Se o valor for vazio ou None, retorna None.
        """
        if value is None or value == b'' or value == '':  # Verifica se o valor é vazio ou None
            return None

        file_path = value  # Supondo que o valor seja uma string representando o caminho do arquivo
        
        if default_storage.exists(file_path):
            # Lê o conteúdo do arquivo como bytes
            with default_storage.open(file_path, 'rb') as encrypted_file:  # Abre o arquivo para leitura binária
                return self._decrypt_file(encrypted_file)  # Passa os bytes para descriptografia
        else:
            raise ValueError(f"O arquivo no caminho {file_path} não existe.")

    def _decrypt_file(self, encrypted_file):
        """
        Função para descriptografar o conteúdo criptografado.
        """

        encrypted_content = encrypted_file.read()  # Lê todo o conteúdo como bytes
        decrypted_content = self.cryptographer.decrypted(encrypted_content)

        if isinstance(decrypted_content, bytes):
            # Cria um arquivo em memória com o conteúdo descriptografado
            decrypted_file = BytesIO(decrypted_content)
            decrypted_file.name = encrypted_file.name  # Mantém o nome original do arquivo
            decrypted_file.size = len(decrypted_content)  # Ajusta o tamanho do arquivo
            decrypted_file.seek(0)  # Posiciona o ponteiro do arquivo no início
            # Retorna o arquivo descriptografado como ContentFile
            return ContentFile(decrypted_file.read(), name=encrypted_file.name)
        else:
            raise ValueError("A decriptação falhou, o conteúdo não é um tipo de dado esperado.")


class EncryptedImageField(models.ImageField):
    """
    Um campo de imagem criptografado.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cryptographer = EncryptedFileMixin()  # Instanciando o EncryptedFileMixin para usá-lo
    
    def pre_save(self, model_instance, add):
        image = getattr(model_instance, self.attname)

        if image:
            if image.size == 0:
                model_instance.__dict__[self.attname] = None
            else:
                # Corrige o nome do arquivo
                image.name = os.path.basename(image.name)
                encrypted_image = self._encrypt_image(image)
                model_instance.__dict__[self.attname] = encrypted_image
        else:
            model_instance.__dict__[self.attname] = None

        return super().pre_save(model_instance, add)

    def _encrypt_image(self, image):
        """
        Função para criptografar a imagem antes de ser salva.
        """
        content = image.read()  # Lê o conteúdo da imagem
        encrypted_content = self.cryptographer.encrypted(content)  # Criptografa o conteúdo

        if isinstance(encrypted_content, bytes):
            encrypted_image = BytesIO(encrypted_content)
            encrypted_image.name = image.name  # Mantém o nome original do arquivo
            encrypted_image.size = len(encrypted_content)  # Ajusta o tamanho do arquivo
            encrypted_image.seek(0)  # Posiciona o ponteiro no início
            return ContentFile(encrypted_image.read(), name=image.name)  # Retorna a imagem criptografada como ContentFile
        else:
            raise ValueError("A criptografia falhou, o conteúdo não é um tipo de dado esperado.")

    def from_db_value(self, value, expression, connection, context=None):
        """
        Descriptografa a imagem ao ser acessada do banco de dados.
        Se o valor for vazio ou None, retorna None.
        """
        if value is None or value == b'' or value == '':  # Verifica se o valor é vazio ou None
            return None

        file_path = value  # Supondo que o valor seja uma string representando o caminho do arquivo

        if default_storage.exists(file_path):
            # Lê o conteúdo do arquivo como bytes
            with default_storage.open(file_path, 'rb') as encrypted_file:  # Abre o arquivo para leitura binária
                return self._decrypt_image(encrypted_file)  # Passa os bytes para descriptografia
        else:
            raise ValueError(f"O arquivo no caminho {file_path} não existe.")

    def _decrypt_image(self, encrypted_file):
        """
        Função para descriptografar o conteúdo criptografado da imagem.
        """
        encrypted_content = encrypted_file.read()  # Lê todo o conteúdo como bytes
        decrypted_content = self.cryptographer.decrypted(encrypted_content)  # Descriptografa o conteúdo

        if isinstance(decrypted_content, bytes):
            # Cria uma imagem em memória com o conteúdo descriptografado
            decrypted_image = BytesIO(decrypted_content)
            decrypted_image.name = encrypted_file.name  # Mantém o nome original do arquivo
            decrypted_image.seek(0)  # Posiciona o ponteiro no início

            # Valida se o conteúdo é uma imagem válida
            try:
                Image.open(decrypted_image).verify()
                decrypted_image.seek(0)  # Reposiciona o ponteiro após a verificação
            except Exception as e:
                raise ValueError(f"A decriptação falhou, o conteúdo não é uma imagem válida: {e}")

            # Retorna a imagem descriptografada como ContentFile
            return ContentFile(decrypted_image.read(), name=encrypted_file.name)
        else:
            raise ValueError("A decriptação falhou, o conteúdo não é um tipo de dado esperado.")
