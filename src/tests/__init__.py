# src/core/crypto/abstract.py
"""
Абстрактный базовый класс для сервисов шифрования.
Определяет интерфейс, который должны реализовать все конкретные реализации.
"""
from abc import ABC, abstractmethod
from typing import Protocol


class EncryptionService(ABC):
  """
  Абстрактный класс, определяющий контракт для всех сервисов шифрования.
  Позволяет легко заменять реализацию шифрования без изменения остального кода.
  """

  @abstractmethod
  def encrypt(self, data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные с использованием предоставленного ключа.

    Args:
        data: Данные для шифрования в байтах
        key: Ключ шифрования в байтах

    Returns:
        Зашифрованные данные в байтах
    """
    pass

  @abstractmethod
  def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные с использованием предоставленного ключа.

    Args:
        ciphertext: Зашифрованные данные в байтах
        key: Ключ шифрования в байтах

    Returns:
        Расшифрованные данные в байтах
    """
    pass
