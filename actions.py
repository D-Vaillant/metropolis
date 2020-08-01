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


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return  # no entity found

        print(f"You kick the {target.name} harmlessly.")

class MovementAction(ActionWithDirection):
    def perform(self, engine, entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # can't leave the map
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return  # can't move through walls
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return  # destination blocked by entity

        entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
