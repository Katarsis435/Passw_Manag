from datetime import datetime, timedelta


class StateManager:
  def __init__(self):
    self.is_locked = True
    self.current_user = None
    self.clipboard_content = None
    self.clipboard_timer = None
    self.last_activity = datetime.now()

  def login(self, user_id: str):
    self.is_locked = False
    self.current_user = user_id
    self.update_activity()

  def logout(self):
    self.is_locked = True
    self.current_user = None
    self.clear_clipboard()

  def lock(self):
    self.is_locked = True
    self.clear_clipboard()

  def unlock(self, user_id: str):
    self.is_locked = False
    self.current_user = user_id
    self.update_activity()

  def update_activity(self):
    self.last_activity = datetime.now()

  def set_clipboard(self, content: str, timeout: int = 30):
    self.clipboard_content = content
    if self.clipboard_timer:
      self.clipboard_timer.cancel()

    from threading import Timer
    self.clipboard_timer = Timer(timeout, self.clear_clipboard)
    self.clipboard_timer.daemon = True
    self.clipboard_timer.start()

  def clear_clipboard(self):
    self.clipboard_content = None
    if self.clipboard_timer:
      self.clipboard_timer.cancel()
      self.clipboard_timer = None

  def check_inactivity(self, timeout_minutes: int) -> bool:
    if self.is_locked:
      return True
    inactive = datetime.now() - self.last_activity
    return inactive.total_seconds() > (timeout_minutes * 60)


state_manager = StateManager()
