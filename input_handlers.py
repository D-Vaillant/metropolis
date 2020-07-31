from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction

class EventHandler(tcod.event.EventDispatch[Action]):
    keymap = {
            tcod.event.K_UP: MovementAction(dx=0, dy=-1),
            tcod.event.K_DOWN: MovementAction(dx=0, dy=1),
            tcod.event.K_LEFT: MovementAction(dx=-1, dy=0),
            tcod.event.K_RIGHT: MovementAction(dx=1, dy=0),
            tcod.event.K_ESCAPE: EscapeAction()
            }
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        action = self.keymap.get(key, None)

        return action

