from typing import Tuple, TYPE_CHECKING, Optional

from exceptions import InstantiationError
from render_functions import *

from tcod import Console
from engine import Engine



class AbstractViewport:
    def __init__(self,
                 width: int,
                 height: int):
        self.width = width
        self.height = height

    def update_fov(self) -> None:
        """ Recompute visible area based on player's point of view. """
        self.engine.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is visible, it should be marked as explored.
        self.engine.game_map.explored |= self.engine.game_map.visible

    def render(self, console: Console) -> None:
        raise NotImplementedError()


class Viewport(AbstractViewport):
    def __init__(self,
                 width: int,
                 height: int,
                 engine: Engine):

        super().__init__(width, height)

        self.engine = engine
        self.player = self.engine.player

    @property
    def player_location(self) -> Tuple[int, int]:
        return player.x, player.y

    def render(self, console: Console) -> None:
        self.engine.game_map.render(console)
        self.engine.message_log.render(console=console,
                                       x=21,
                                       y=45,
                                       width=self.width,
                                       height=self.height,)
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fight.max_hp,
            total_width=20,
        )
        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
