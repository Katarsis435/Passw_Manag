from .abstract import EncryptionService
import secrets


class AES256Placeholder(EncryptionService):
  def encrypt(self, data: bytes, key: bytes) -> bytes:
    # Простой XOR для Sprint 1
    key_bytes = key[:len(data)] if len(key) >= len(data) else key * (len(data) // len(key) + 1)
    return bytes([a ^ b for a, b in zip(data, key_bytes[:len(data)])])

  def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
    return self.encrypt(ciphertext, key)  # XOR симметричен
