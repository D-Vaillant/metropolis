from typing import Optional

import tcod.event

from actions import Action, EscapeAction, BumpAction

class EventHandler(tcod.event.EventDispatch[Action]):
    keymap = {
            # up
            tcod.event.K_UP: BumpAction(dx=0, dy=-1),
            tcod.event.K_k: BumpAction(dx=0, dy=-1),
            # down
            tcod.event.K_DOWN: BumpAction(dx=0, dy=1),
            tcod.event.K_j: BumpAction(dx=0, dy=1),
            # left
            tcod.event.K_LEFT: BumpAction(dx=-1, dy=0),
            tcod.event.K_h: BumpAction(dx=-1, dy=0),
            # right
            tcod.event.K_RIGHT: BumpAction(dx=1, dy=0),
            tcod.event.K_l: BumpAction(dx=1, dy=0),
            # diagonals
            tcod.event.K_u: BumpAction(dx=-1, dy=-1),
            tcod.event.K_i: BumpAction(dx=1, dy=-1),
            tcod.event.K_n: BumpAction(dx=-1, dy=1),
            tcod.event.K_m: BumpAction(dx=1, dy=1),
            # escape
            tcod.event.K_ESCAPE: EscapeAction()
            }
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        action = self.keymap.get(key, None)

        return action

