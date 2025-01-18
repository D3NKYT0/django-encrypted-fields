from django.db import models

from encrypted_fields.encrypted_fields import *
from encrypted_fields.encrypted_files import *


# Create your models here.
class SecureDataModel(models.Model):
    """
    Modelo que utiliza campos criptografados para diferentes tipos de dados.
    """
    # Campos básicos
    encrypted_text = EncryptedCharField(max_length=255, verbose_name="Texto Criptografado", null=True, blank=True)
    encrypted_integer = EncryptedIntegerField(verbose_name="Inteiro Criptografado", null=True, blank=True)
    encrypted_float = EncryptedFloatField(verbose_name="Float Criptografado", null=True, blank=True)
    encrypted_boolean = EncryptedBooleanField(verbose_name="Booleano Criptografado", null=True, blank=True)

    # Uploads
    encrypted_file = EncryptedFileField(upload_to="uploads/files/", verbose_name="Arquivo Criptografado", null=True, blank=True)
    encrypted_image = EncryptedImageField(upload_to="uploads/images/", verbose_name="Imagem Criptografada", null=True, blank=True)

    def __str__(self):
        return f"SecureDataModel #{self.pk}"
    
    class Meta:
        verbose_name = 'Modelo Encriptado'
        verbose_name_plural = 'Modelo Encriptado'
