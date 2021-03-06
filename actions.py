from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity  # actions are attached to Agents

    @property
    def engine(self) -> Engine:
        """ Return the engine that this action belongs to. """
        return self.entity.gamemap.engine   # Entities (and so Agents) are attached to Engine

    def schedule(self, interval: int, value: Any) -> Ticket:
        """ Harmless wrapper function. """
        return self.engine.turn_queue.schedule(interval=interval, value=value)


    def perform(self) -> None:
        """ Perform this action with the objects required.

        `self.engine` is the scope that the actions are performed in

        `self.entity` is the object performing the action

        Must be overwritten.
        """
        raise NotImplementedError()



class WaitAction(Action):
    def perform(self) -> None:
        self.engine.schedule(value=self.entity, interval=self.entity.base_ticks)
        pass


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        """ An action that's also instantiated with a coordinate pair.
        It corresponds to offset from the Actor doing the Action. """
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """ Returns this action's destination. 
        Here's where we do something with that offset. """
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """ Return blocking entity at this action's destination.
        We're asking the game map about blocking. """
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """ Return the actor at this action's destination. """
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            self.engine.schedule(value=self.entity, interval=0)
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        self.engine.schedule(value=self.entity, interval=self.entity.attack_ticks)
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk
        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc}, but the blow is deflected harmlessly.", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        default_interval = 0 if self.entity == self.engine.player else 2
        # TODO I hate exceptions.Impossible.
        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # destination out of bounds
            self.engine.schedule(value=self.entity, interval=default_interval)
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # can't move through walls
            self.engine.schedule(value=self.entity, interval=default_interval)
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # destination blocked by entity
            self.engine.schedule(value=self.entity, interval=default_interval)
            raise exceptions.Impossible("That way is blocked.")

        self.engine.schedule(value=self.entity, 
                             interval=self.entity.movement_ticks)
        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()

class PickupAction(Action):
    """ picks up and adds to inventory if possible """
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if item.overlaps(actor_location_x, actor_location_y):
                if len(inventory.items) >= inventory.capacity:
                    self.engine.schedule(value=self.entity, interval=0)
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.schedule(value=self.entity, interval=15)
                self.engine.message_log.add_message(f"You picked up the {item.name}.")
                return

        self.engine.turn_queue.schedule(value=self.entity, interval=0)
        self.engine.message_log.add_message("There is nothing here to pick up.")
        return



class ItemAction(Action):
    def __init__(
        self,
        entity: Actor,  # Actions belong to some Actor.
        item: Item,  # And they reference their item.
        target_xy: Optional[Tuple[int, int]] = None   # We can specify coordinates.
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy
        self.use_time = 30

    @property
    def target_actor(self) -> Optional[Actor]:
        """ Return the actor at this action's destination. """
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the item's ability."""
        self.engine.schedule(value=self.entity, interval=self.use_time)
        self.item.consumable.activate(self)



class DropItem(ItemAction):
    def perform(self) -> None:
        self.engine.schedule(value=self.entity, interval=15)
        self.entity.inventory.drop(self.item)
