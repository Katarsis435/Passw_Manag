import sqlite3
from datetime import datetime


class Models:
  @staticmethod
  def create_tables(conn):
    cursor = conn.cursor()

    # vault_entries
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                username TEXT,
                encrypted_password BLOB,
                url TEXT,
                notes TEXT,
                tags TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')

    # audit_log
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                timestamp TIMESTAMP,
                entry_id INTEGER,
                details TEXT,
                signature TEXT
            )
        ''')

    # settings
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                encrypted BOOLEAN DEFAULT 0
            )
        ''')

    # key_store
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_type TEXT NOT NULL,
                salt BLOB,
                hash BLOB,
                params TEXT
            )
        ''')

    # Индексы
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_vault_title ON vault_entries(title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)')

    conn.commit()
