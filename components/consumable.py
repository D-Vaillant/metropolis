from __future__ import annotations

from typing import Callable, Optional, TYPE_CHECKING, Union

import random

import actions
import color
import components.ai
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible
import forces
from input_handlers import SingleRangedAttackHandler

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Action) -> Optional[actions.Action]:
        """ try to return the action for this item """
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """ Invoke this item's ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns: Union[int, Callable]):
        if not isinstance(number_of_turns, int):
            number_of_turns = number_of_turns()
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        self.engine.event_handler = SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You can't see what's over there.")
        if not target:
            raise Impossible("You're not targeting anything.")
        if target is consumer:
            raise Impossible("You can't target yourself.")

        self.engine.message_log.add_message(
            f"{target.name} begins to stumble around, its eyes glassy.",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )
        self.consume()


class HealingConsumable(Consumable):
    def __init__(self,
                 amount: Union[int, Callable],
                 ):
        if not isinstance(amount, int):
            amount = amount()
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        healed_amount = self.amount

        if healed_amount == 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, but recover no health.",
                color.health_recovered,
            )
        amount_recovered = consumer.fighter.heal(healed_amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP.",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")


class RangedDamageConsumable(Consumable):
    def __init__(self,
                 damage: Union[int, Callable],
                 maximum_range: int):
        if not isinstance(damage, int):
            damage = damage()
        self.damage = damage
        self.damage_type = forces.Force
        self.maximum_range = maximum_range
        #self.message = "Energy strikes {target_name} for {damage} HP."
        self.message = self.damage_type.message

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            # If the actor isn't us, and is visible.
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                self.message.format(target_name=target.name, damage=self.damage)
            )
            target.fighter.take_damage(self.damage, self.damage_type)
            self.consume()
        else:
            raise Impossible("No enemy is near.")


class LightningDamageConsumable(RangedDamageConsumable):
    def __init__(self,
                 damage: Union[int, Callable],
                 maximum_range: int):
        super().__init__(damage, maximum_range)

        self.damage_type = forces.Lightning
        self.message = self.damage_type.message
        # self.message = "A crackle of electricity strikes {target_name} for {damage} HP.",
