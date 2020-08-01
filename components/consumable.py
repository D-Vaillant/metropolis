from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import random

import actions
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible

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



class HealingConsumable(Consumable):
    def __init__(self, amount: int, max_amount: Optional[int] = None):
        self.amount = amount
        if max_amount is None:
            self.max_amount = self.amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        healed_amount = random.randint(self.amount, self.max_amount)

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
