import unittest
import tempfile
import os
from src.database.db import Database
from src.core.config import config


class TestDatabase(unittest.TestCase):
  def setUp(self):
    self.temp_db = tempfile.NamedTemporaryFile(delete=False)
    config.set('database_path', self.temp_db.name)
    self.db = Database()

  def tearDown(self):
    self.db.close_all()
    os.unlink(self.temp_db.name)

  def test_connection(self):
    with self.db.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
      tables = cursor.fetchall()

      table_names = [t[0] for t in tables]
      self.assertIn('vault_entries', table_names)
      self.assertIn('audit_log', table_names)
      self.assertIn('settings', table_names)
      self.assertIn('key_store', table_names)

  def test_insert_vault_entry(self):
    with self.db.get_connection() as conn:
      cursor = conn.cursor()
      cursor.execute('''
                INSERT INTO vault_entries (title, username, created_at, updated_at)
                VALUES (?, ?, datetime('now'), datetime('now'))
            ''', ('Test', 'testuser'))

      cursor.execute('SELECT * FROM vault_entries WHERE title = ?', ('Test',))
      row = cursor.fetchone()

      self.assertIsNotNone(row)
      self.assertEqual(row[1], 'Test')


if __name__ == '__main__':
  unittest.main()
