from typing import Tuple, TYPE_CHECKING, Optional

from exceptions import InstantiationError
from render_functions import *
from engine import Engine

import tcod
from tcod.map import compute_fov



class AbstractViewport:
    def __init__(self,
                 width: int,
                 height: int,
                 order: str = "F"):
        self.console_width = width
        self.console_height = height
        # deprecate this
        self.width = width
        self.height = height
        self.console = tcod.Console(self.width, self.height, order)

    def clear(self):
        self.console.clear()

    def render(self) -> None:
        raise NotImplementedError()


class Viewport(AbstractViewport):
    def __init__(self,
                 width: int,
                 height: int,
                 engine: Engine,
                 order: str = "F"):

        super().__init__(width, height, order)

        self.engine = engine
        self.player = self.engine.player

    @property
    def player_location(self) -> Tuple[int, int]:
        return player.x, player.y

    def update_fov(self) -> None:
        """ Recompute visible area based on player's point of view. """
        self.engine.game_map.visible[:] = compute_fov(
            transparency=self.engine.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,)
        # If a tile is visible, it should be marked as explored.
        self.engine.game_map.explored |= self.engine.game_map.visible

    def render(self) -> None:
        self.engine.game_map.render(self.console)
        self.engine.message_log.render(console=self.console,
                                       x=21,
                                       y=45,
                                       width=self.width,
                                       height=self.height,)
        render_bar(
            console=self.console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )
        render_names_at_mouse_location(console=self.console, x=21, y=44, engine=self.engine)
