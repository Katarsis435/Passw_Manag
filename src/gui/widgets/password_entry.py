import tkinter as tk
from tkinter import ttk


class PasswordEntry(ttk.Frame):
  def __init__(self, parent, label_text="Password:", **kwargs):
    super().__init__(parent)

    self.show_password = tk.BooleanVar(value=False)

    ttk.Label(self, text=label_text).pack(side=tk.LEFT, padx=(0, 5))

    self.entry = ttk.Entry(self, show="*", **kwargs)
    self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    self.toggle_btn = ttk.Button(
      self,
      text="Show",
      command=self.toggle_show,
      width=6
    )
    self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0))

  def toggle_show(self):
    if self.show_password.get():
      self.entry.config(show="*")
      self.toggle_btn.config(text="Show")
    else:
      self.entry.config(show="")
      self.toggle_btn.config(text="Hide")
    self.show_password.set(not self.show_password.get())

  def get(self):
    return self.entry.get()

  def set(self, value):
    self.entry.delete(0, tk.END)
    self.entry.insert(0, value)
