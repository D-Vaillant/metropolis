from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class GameMap:
    def __init__(
            self, engine: Engine,  width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        # Map layers.
        # We could "register" layers onto a dict.
        ## Ideally, dynamically deleting/updating them?
        self._layers = dict()

        self._layers["visible"] = np.full(
            (width, height), fill_value=False, order="F"
        )  # tiles the player can see
        self._layers["explored"] = np.full(
            (width, height), fill_value=False, order="F"
        )  # tiles the player has seen

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over living actors."""
        yield from (
            entity for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (
            entity for entity in self.entities
            if isinstance(entity, Item)
        )

    @property
    def explored(self):
        return self._layers["explored"]

    @explored.setter
    def explored(self, map):
        self._layers["explored"] = map

    @explored.deleter
    def explored(self, map):
        del(self._layers["explored"])

    @property
    def visible(self):
        return self._layers["visible"]

    @visible.setter
    def visible(self, map):
        self._layers["visible"] = map

    @visible.deleter
    def visible(self, map):
        del(self._layers["visible"])

    def get_layer(self, layer_name: str) -> np.ndarray:
        try:
            return self._layers[layer_name]
        except KeyError as K:
            # Create an empty layer, maybe?
            raise K

    def set_layer(self, layer_name: str, layer_contents: np.ndarray) -> None:
        # Check to see if the layer actually... fits.
        assert layer_contents.shape == self.tiles.shape
        self._layers[layer_name] = layer_contents

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """ returns True if x and y are inside the bounds of the map """
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If the tile is in the "visible" array, draw it with the "light" color.
        Otherwise, if it's in the "explored" array, draw it with the "dark" color.
        Otherwise, use "SHROUD".
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # print entities in POV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
