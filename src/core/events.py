from enum import Enum
from typing import Callable, Dict, List, Any


class EventType(Enum):
  ENTRY_ADDED = "entry_added"
  ENTRY_UPDATED = "entry_updated"
  ENTRY_DELETED = "entry_deleted"
  USER_LOGGED_IN = "user_logged_in"
  USER_LOGGED_OUT = "user_logged_out"
  CLIPBOARD_COPIED = "clipboard_copied"
  CLIPBOARD_CLEARED = "clipboard_cleared"


class EventBus:
  def __init__(self):
    self._subscribers: Dict[EventType, List[Callable]] = {}

  def subscribe(self, event_type: EventType, callback: Callable):
    if event_type not in self._subscribers:
      self._subscribers[event_type] = []
    self._subscribers[event_type].append(callback)

  def publish(self, event_type: EventType, data: Any = None, sync: bool = True):
    if event_type not in self._subscribers:
      return

    for callback in self._subscribers[event_type]:
      if sync:
        callback(data)
      else:
        import threading
        threading.Thread(target=callback, args=(data,)).start()


# Глобальный экземпляр
event_bus = EventBus()
