import unittest
import os
from src.core.crypto.placeholder import AES256Placeholder
from src.core.key_manager import KeyManager


class TestCrypto(unittest.TestCase):
  def setUp(self):
    self.crypto = AES256Placeholder()
    self.key_manager = KeyManager()

  def test_encrypt_decrypt(self):
    data = b"test data"
    key = b"12345678901234567890123456789012"

    encrypted = self.crypto.encrypt(data, key)
    decrypted = self.crypto.decrypt(encrypted, key)

    self.assertEqual(data, decrypted)

  def test_key_derivation(self):
    password = "test_password"
    key, salt = self.key_manager.derive_key(password)

    self.assertEqual(len(key), 32)
    self.assertEqual(len(salt), 16)

    key2, _ = self.key_manager.derive_key(password, salt)
    self.assertEqual(key, key2)


if __name__ == '__main__':
  unittest.main()
