import json
import os
from pathlib import Path


class Config:
  def __init__(self):
    self.config_dir = Path.home() / ".cryptosafe"
    self.config_file = self.config_dir / "config.json"
    self._config = self._load()

  def _load(self):
    if self.config_file.exists():
      with open(self.config_file, 'r') as f:
        return json.load(f)
    return self._defaults()

  def _defaults(self):
    return {
      "database_path": str(self.config_dir / "vault.db"),
      "encryption": {
        "algorithm": "AES256",
        "key_derivation": "PBKDF2"
      },
      "security": {
        "clipboard_timeout": 30,
        "auto_lock_minutes": 5
      },
      "appearance": {
        "theme": "default",
        "language": "en"
      }
    }

  def save(self):
    self.config_dir.mkdir(exist_ok=True)
    with open(self.config_file, 'w') as f:
      json.dump(self._config, f, indent=2)

  def get(self, key, default=None):
    keys = key.split('.')
    value = self._config
    for k in keys:
      if isinstance(value, dict):
        value = value.get(k)
      else:
        return default
    return value if value is not None else default

  def set(self, key, value):
    keys = key.split('.')
    target = self._config
    for k in keys[:-1]:
      if k not in target:
        target[k] = {}
      target = target[k]
    target[keys[-1]] = value
    self.save()


config = Config()
