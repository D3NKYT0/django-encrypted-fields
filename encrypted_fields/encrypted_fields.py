from django.db import models
from datetime import datetime
from .encrypted_field_mixin import EncryptedFieldMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.functional import cached_property
from django.db.backends.base.operations import BaseDatabaseOperations


class EncryptedIntegerField(EncryptedFieldMixin, models.IntegerField):
    """
    Campo criptografado para valores inteiros.
    """
    @cached_property
    def validators(self) -> list[MinValueValidator | MaxValueValidator]:
        # These validators can't be added at field initialization time since
        # they're based on values retrieved from `connection`.
        validators_ = [*self.default_validators, *self._validators]
        internal_type = models.IntegerField().get_internal_type()
        min_value, max_value = BaseDatabaseOperations.integer_field_ranges[
            internal_type
        ]
        if min_value is not None and not any(
            (
                isinstance(validator, MinValueValidator)
                and (
                    validator.limit_value()
                    if callable(validator.limit_value)
                    else validator.limit_value
                )
                >= min_value
            )
            for validator in validators_
        ):
            validators_.append(MinValueValidator(min_value))
        if max_value is not None and not any(
            (
                isinstance(validator, MaxValueValidator)
                and (
                    validator.limit_value()
                    if callable(validator.limit_value)
                    else validator.limit_value
                )
                <= max_value
            )
            for validator in validators_
        ):
            validators_.append(MaxValueValidator(max_value))
        return validators_

    def cast_value(self, value):
        return int(value)


class EncryptedFloatField(EncryptedFieldMixin, models.FloatField):
    """
    Campo criptografado para valores flutuantes (float).
    """
    def cast_value(self, value):
        return float(value)


class EncryptedBooleanField(EncryptedFieldMixin, models.BooleanField):
    """
    Campo criptografado para valores booleanos.
    """
    def cast_value(self, value):
        return value.lower() == 'true'


class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    """
    Campo criptografado para strings.
    """
    def cast_value(self, value):
        return value  # Strings não precisam de conversão adicional


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    """
    Campo criptografado para strings.
    """
    def cast_value(self, value):
        return value  # Strings não precisam de conversão adicional


class EncryptedDateField(EncryptedFieldMixin, models.DateField):
    """
    Campo criptografado para datas.
    """
    def cast_value(self, value):
        if isinstance(value, str):
            # Supondo que o formato da data armazenada seja 'YYYY-MM-DD'
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value  # Se já for uma instância de `date`, não é necessário converter


class EncryptedDateTimeField(EncryptedFieldMixin, models.DateTimeField):
    """
    Campo criptografado para valores de data e hora.
    """
    def cast_value(self, value):
        if isinstance(value, str):
            # Supondo que o formato seja 'YYYY-MM-DD HH:MM:SS'
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return value


class EncryptedTimeField(EncryptedFieldMixin, models.TimeField):
    """
    Campo criptografado para valores de hora.
    """
    def cast_value(self, value):
        if isinstance(value, str):
            # Supondo que o formato seja 'HH:MM:SS'
            return datetime.strptime(value, '%H:%M:%S').time()
        return value


class EncryptedDecimalField(EncryptedFieldMixin, models.DecimalField):
    """
    Campo criptografado para valores decimais.
    """
    def cast_value(self, value):
        from decimal import Decimal
        return Decimal(value)


class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
    """
    Campo criptografado para endereços de e-mail.
    """
    def cast_value(self, value):
        return value  # Strings de e-mail não precisam de conversão adicional


class EncryptedURLField(EncryptedFieldMixin, models.URLField):
    """
    Campo criptografado para URLs.
    """
    def cast_value(self, value):
        return value  # Strings de URL não precisam de conversão adicional


class EncryptedUUIDField(EncryptedFieldMixin, models.UUIDField):
    """
    Campo criptografado para valores UUID.
    """
    def cast_value(self, value):
        import uuid
        if isinstance(value, str):
            return uuid.UUID(value)
        return value


class EncryptedJSONField(EncryptedFieldMixin, models.JSONField):
    """
    Campo criptografado para valores JSON.
    """
    def cast_value(self, value):
        import json
        if isinstance(value, str):
            return json.loads(value)
        return value  # Assume que já é um dicionário ou lista
