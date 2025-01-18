from django.contrib import admin
from .models import *


class SecureDataModelAdmin(admin.ModelAdmin):
    """
    Admin personalizado para o modelo SecureDataModel.
    """
    list_display = (
        "id",
        "encrypted_text_preview",
        "encrypted_integer",
        "encrypted_float",
        "encrypted_boolean",
    )
    fieldsets = (
        ("Campos Básicos", {
            "fields": (
                "encrypted_text",
                "encrypted_integer",
                "encrypted_float",
                "encrypted_boolean",
            ),
        }),
        ("Uploads Criptografados", {
            "fields": (
                "encrypted_file",
                "encrypted_image",
            ),
        })
    )

    def encrypted_text_preview(self, obj):
        """
        Mostra uma prévia do texto criptografado.
        """
        return obj.encrypted_text[:20] + "..." if len(obj.encrypted_text) > 20 else obj.encrypted_text

    encrypted_text_preview.short_description = "Texto Criptografado (Prévia)"


admin.site.register(SecureDataModel, SecureDataModelAdmin)
