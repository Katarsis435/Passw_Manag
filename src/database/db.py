import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from ..core.config import config
from .models import Models


class Database:
  def __init__(self):
    self.db_path = config.get('database_path')
    self._local = threading.local()
    self._init_database()

  def _init_database(self):
    db_dir = Path(self.db_path).parent
    db_dir.mkdir(exist_ok=True)

    with self.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('PRAGMA user_version')
      version = cursor.fetchone()[0]

      if version == 0:
        Models.create_tables(conn)
        cursor.execute('PRAGMA user_version = 1')

  @contextmanager
  def get_connection(self):
    if not hasattr(self._local, 'connection'):
      self._local.connection = sqlite3.connect(
        self.db_path,
        timeout=10,
        check_same_thread=False
      )
      self._local.connection.execute('PRAGMA foreign_keys = ON')

    try:
      yield self._local.connection
    except Exception as e:
      self._local.connection.rollback()
      raise e
    else:
      self._local.connection.commit()

  def close_all(self):
    if hasattr(self._local, 'connection'):
      self._local.connection.close()
      delattr(self._local, 'connection')

  def backup(self, backup_path: str):
    # Заглушка для Sprint 8
    pass

  def restore(self, backup_path: str):
    # Заглушка для Sprint 8
    pass


db = Database()
