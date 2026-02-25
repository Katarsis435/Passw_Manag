import tkinter as tk
from tkinter import ttk


class SecureTable(ttk.Frame):
  def __init__(self, parent, columns, **kwargs):
    super().__init__(parent)

    self.columns = columns

    # Treeview
    self.tree = ttk.Treeview(self, columns=list(columns.keys()), show="headings", **kwargs)

    # Scrollbars
    v_scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
    h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)

    self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    # Настройка колонок
    for col_id, col_config in columns.items():
      self.tree.heading(col_id, text=col_config.get('label', col_id))
      self.tree.column(col_id, width=col_config.get('width', 100))

    # Размещение
    self.tree.grid(row=0, column=0, sticky='nsew')
    v_scroll.grid(row=0, column=1, sticky='ns')
    h_scroll.grid(row=1, column=0, sticky='ew')

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    # Привязка событий
    self.tree.bind('<Double-Button-1>', self.on_double_click)

  def add_item(self, values):
    return self.tree.insert('', tk.END, values=values)

  def get_selected(self):
    selection = self.tree.selection()
    if selection:
      return self.tree.item(selection[0])['values']
    return None

  def clear(self):
    for item in self.tree.get_children():
      self.tree.delete(item)

  def on_double_click(self, event):
    # Заглушка для редактирования
    pass
