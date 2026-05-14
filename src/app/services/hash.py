import hashlib
import json


def hash_dict(data: dict) -> str:
    """Generar un hash SHA-256 de un diccionario"""
    # convertir el diccionario a una cadena JSON y luego a bytes
    data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    # calcular el hash SHA-256
    hash_object = hashlib.sha256(data_bytes)
    return hash_object.hexdigest()
