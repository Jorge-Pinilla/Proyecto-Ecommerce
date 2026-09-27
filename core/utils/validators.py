# core/utils/validators.py
import re
from django.core.exceptions import ValidationError

def validate_rut(value):
    rut = value.upper().replace(".", "").replace("-", "")
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        raise ValidationError("Formato de RUT inválido.")
    cuerpo = rut[:-1]
    dv = rut[-1]
    suma = 0
    multiplo = 2
    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1
    res = 11 - (suma % 11)
    dvr = 'K' if res == 10 else '0' if res == 11 else str(res)
    if dvr != dv:
        raise ValidationError("RUT o Dígito Verificador incorrecto.")