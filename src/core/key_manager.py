import hashlib
import os
import secrets


class KeyManager:
  @staticmethod
  def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    if salt is None:
      salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key, salt

  @staticmethod
  def store_key(key: bytes, key_id: str) -> None:
    # Заглушка для Sprint 2
    pass

  @staticmethod
  def load_key(key_id: str) -> bytes:
    # Заглушка для Sprint 2
    return b''

  @staticmethod
  def zero_memory(data: bytearray) -> None:
    for i in range(len(data)):
      data[i] = 0
