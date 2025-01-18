from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.apps import apps
from django.http import HttpResponse
from django.db.models.fields.files import FieldFile
from mimetypes import guess_type
from django.core.cache import cache

from encrypted_fields.encrypted_fields import *
from encrypted_fields.encrypted_files import *


# Create your views here.
def serve_decrypted_file(request, app_name, model_name, field_name, uuid):
    """
    View para descriptografar e retornar o arquivo (imagem ou qualquer outro) com cache de 5 minutos.
    """
    try:
        # Tenta recuperar o arquivo do cache
        cache_key = f"{app_name}_{model_name}_{field_name}_{uuid}"
        cached_file = cache.get(cache_key)

        if cached_file:
            return cached_file  # Retorna o arquivo cacheado se disponível

        # Valida se o app existe
        if app_name not in apps.app_configs:
            return HttpResponse("App não encontrado.", status=404)

        # Obtém o modelo dinamicamente a partir do nome
        model = apps.get_model(app_name, model_name)
        if not model:
            return HttpResponse("Modelo não encontrado.", status=404)
        
        # Busca o objeto pelo ID (pk)
        obj = model.objects.filter(uuid=uuid).first()
        if not obj:
            return HttpResponse("Objeto não encontrado.", status=404)
        
        # Obtém o campo do objeto dinamicamente
        file_field = getattr(obj, field_name, None)
        if not file_field:
            return HttpResponse("Campo não encontrado.", status=404)
        
        # Verifica se o campo é do tipo EncryptedFileField ou EncryptedImageField
        if isinstance(file_field, (EncryptedFileField, EncryptedImageField)):
            # Chama a descriptografia via from_db_value
            decrypted_file = file_field.from_db_value(file_field.name, None, None)
            if not decrypted_file:
                return HttpResponse("Erro ao descriptografar o arquivo.", status=500)
        elif isinstance(file_field, (FieldFile)):
            # Se for um FileField ou ImageField normal, abre o arquivo associado
            decrypted_file = file_field.file
        else:
            return HttpResponse("Campo não é do tipo FieldFile.", status=400)

        # Determina o tipo MIME do arquivo
        mime_type, _ = guess_type(decrypted_file.name)
        
        # Cria a resposta com o arquivo
        response = HttpResponse(decrypted_file.read(), content_type=mime_type)
        response['Content-Disposition'] = f'inline; filename="{decrypted_file.name}"'

        # Armazena a resposta no cache por 5 minutos
        cache.set(cache_key, response, timeout=300)

        return response
        
    except Exception as e:
        return HttpResponse(f"Erro: {e}", status=500)
