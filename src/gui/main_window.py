import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ..core.config import config
from ..core.state_manager import state_manager
from ..core.events import event_bus, EventType
from .widgets.password_entry import PasswordEntry
from .widgets.secure_table import SecureTable


class MainWindow:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("CryptoSafe Manager")
    self.root.geometry("900x600")

    self._create_menu()
    self._create_toolbar()
    self._create_main_content()
    self._create_statusbar()

    # Подписка на события
    event_bus.subscribe(EventType.USER_LOGGED_IN, self.on_login)
    event_bus.subscribe(EventType.USER_LOGGED_OUT, self.on_logout)

    # Проверка первого запуска
    if not self._check_first_run():
      self.show_login()

  def _create_menu(self):
    menubar = tk.Menu(self.root)
    self.root.config(menu=menubar)

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New Database", command=self.new_database)
    file_menu.add_command(label="Open Database", command=self.open_database)
    file_menu.add_separator()
    file_menu.add_command(label="Backup", command=self.backup_database)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=self.root.quit)

    # Edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Add Entry", command=self.add_entry)
    edit_menu.add_command(label="Edit Entry", command=self.edit_entry)
    edit_menu.add_command(label="Delete Entry", command=self.delete_entry)

    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Audit Log", command=self.show_audit_log)
    view_menu.add_command(label="Settings", command=self.show_settings)

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=self.show_about)

  def _create_toolbar(self):
    toolbar = ttk.Frame(self.root)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    ttk.Button(toolbar, text="Add", command=self.add_entry).pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text="Edit", command=self.edit_entry).pack(side=tk.LEFT, padx=2)
    ttk.Button(toolbar, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=2)
    ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
    ttk.Button(toolbar, text="Search").pack(side=tk.LEFT, padx=2)

  def _create_main_content(self):
    # Основной контейнер
    main = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
    main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Левая панель - таблица
    left_frame = ttk.Frame(main)
    main.add(left_frame, weight=3)

    columns = {
      'title': {'label': 'Title', 'width': 150},
      'username': {'label': 'Username', 'width': 150},
      'url': {'label': 'URL', 'width': 200},
      'updated': {'label': 'Updated', 'width': 120}
    }

    self.table = SecureTable(left_frame, columns)
    self.table.pack(fill=tk.BOTH, expand=True)

    # Правая панель - детали (заглушка)
    right_frame = ttk.LabelFrame(main, text="Details")
    main.add(right_frame, weight=1)

    ttk.Label(right_frame, text="Select an entry to view details").pack(pady=20)

  def _create_statusbar(self):
    statusbar = ttk.Frame(self.root)
    statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    self.status_label = ttk.Label(statusbar, text="Ready")
    self.status_label.pack(side=tk.LEFT, padx=5)

    self.lock_status = ttk.Label(statusbar, text="● Locked", foreground="red")
    self.lock_status.pack(side=tk.RIGHT, padx=5)

  def _check_first_run(self):
    # Проверка первого запуска
    import os
    db_path = config.get('database_path')
    return os.path.exists(db_path)

  def show_login(self):
    dialog = tk.Toplevel(self.root)
    dialog.title("Login")
    dialog.geometry("300x150")
    dialog.transient(self.root)
    dialog.grab_set()

    ttk.Label(dialog, text="Master Password:").pack(pady=10)
    password_entry = PasswordEntry(dialog, show="*")
    password_entry.pack(pady=5, padx=10, fill=tk.X)

    def login():
      # Заглушка для проверки пароля
      state_manager.login("user")
      event_bus.publish(EventType.USER_LOGGED_IN, "user")
      dialog.destroy()

    ttk.Button(dialog, text="Login", command=login).pack(pady=10)

  def on_login(self, data):
    self.lock_status.config(text="● Unlocked", foreground="green")
    self.status_label.config(text=f"Logged in as {data}")
    self._load_sample_data()

  def on_logout(self, data):
    self.lock_status.config(text="● Locked", foreground="red")
    self.status_label.config(text="Ready")
    self.table.clear()

  def _load_sample_data(self):
    # Заглушка для демо
    self.table.add_item(["Google", "user@gmail.com", "https://google.com", "2024-01-01"])
    self.table.add_item(["GitHub", "dev@github.com", "https://github.com", "2024-01-01"])

  def new_database(self):
    messagebox.showinfo("New Database", "This will be implemented in Sprint 2")

  def open_database(self):
    messagebox.showinfo("Open Database", "This will be implemented in Sprint 2")

  def backup_database(self):
    messagebox.showinfo("Backup", "This will be implemented in Sprint 8")

  def add_entry(self):
    if state_manager.is_locked:
      messagebox.showwarning("Locked", "Please unlock the database first")
      return
    messagebox.showinfo("Add Entry", "This will be implemented in Sprint 2")

  def edit_entry(self):
    if state_manager.is_locked:
      messagebox.showwarning("Locked", "Please unlock the database first")
      return
    messagebox.showinfo("Edit Entry", "This will be implemented in Sprint 2")

  def delete_entry(self):
    if state_manager.is_locked:
      messagebox.showwarning("Locked", "Please unlock the database first")
      return
    messagebox.showinfo("Delete Entry", "This will be implemented in Sprint 2")

  def show_audit_log(self):
    messagebox.showinfo("Audit Log", "This will be implemented in Sprint 5")

  def show_settings(self):
    messagebox.showinfo("Settings", "This will be implemented in Sprint 3")

  def show_about(self):
    messagebox.showinfo(
      "About CryptoSafe Manager",
      "CryptoSafe Manager\nVersion 0.1 (Sprint 1)\n\nSecure password manager"
    )

  def run(self):
    self.root.mainloop()


def main():
  app = MainWindow()
  app.run()


if __name__ == "__main__":
  main()
