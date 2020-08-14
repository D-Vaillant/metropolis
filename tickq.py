from collections import deque
from typing import Any

class TurnQueue(deque):
    def register(self, obj: Any):
        self.append(obj)
        obj.action_points = 0

    def release(self, obj: Any):
        self.remove(obj)

    def tick(self) -> Any:
        if len(self) > 0:
            obj = self[0]
            self.rotate()
            while obj.action_points >= 0:
                obj.action_points -= obj.perform()
