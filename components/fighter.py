from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    """ Has stats, can die. """
    parent: Actor

    def __init__(
        self,
        body: int,
        agility: int,
        reflexes: int,
        strength: int,
        charisma: int,
        intuition: int,
        logic: int,
        willpower: int,
    ) -> None:
        # unused
        self.body = body
        self.agility = agility
        self.reflexes = reflexes
        self.strength = strength

        self.charisma = charisma
        self.intuition = intuition
        self.logic = logic
        self.willpower = willpower

        self.equipment = {
            "head": None,
            "neck": None,
            "chest": None,
            "hands": None,
            "legs": None,
            "feet": None,
        }
        self.feats = defaultdict(int)

        self._hp = self.max_hp

    @property
    def max_hp(self) -> int:
        base_hp = 10 * self.body
        base_hp += 5 * self.willpower 
        base_hp += 15 * self.feats["Toughness"]
        return base_hp

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def power(self) -> int:
        return 2 * self.strength

    @property
    def defense(self) -> int:
        pv = 0
        for v in self.equipment.values():
            try:
                pv += v.protection
            except AttributeError:
                continue
        return pv

    @property
    def dodge(self) -> int:
        """ not sure how I want to proceed this """
        return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died..."
            death_message_color = color.player_die
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} is dead."
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount
        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp
        self.hp = new_hp_value
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
