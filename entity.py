from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    parent: Union[GameMap, Inventory]

    def __init__(
            self,
            parent: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255,255,255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
            render_order: RenderOrder = RenderOrder.FLOOR,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If we don't have one, set it later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def overlaps(self, x, y) -> bool:
        return (self.x == x and self.y == y)

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location. """
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """ place entity at a new location. allows moving across GameMaps. """
        self.x = x
        self.y = y
        # if we specify a gamemap, we can do things
        if gamemap:
            if hasattr(self, "parent"):  # might not exist
                # if the entity exists on a gamemap, remove it first
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap  # and then account for moving between gamemaps
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy



class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        fighter: Fighter,
        inventory: Inventory,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )


        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self


    @property
    def is_alive(self) -> bool:
        """ return True as long as this actor can perform actions """
        return bool(self.ai)


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Consumable,
    ):
        super().__init__(
            x=x, y=y,
            char=char, color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.consumable.parent = self
