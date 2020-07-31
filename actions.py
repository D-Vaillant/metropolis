from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """ Perform this action with the objects required.

        `engine` is the scope that the actions are performed in

        `entity` is the object performing the action

        Must be overwritten.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine, entity):
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine, entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # can't leave the map
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # can't move through walls

        entity.move(self.dx, self.dy)
