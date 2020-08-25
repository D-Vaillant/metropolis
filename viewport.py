from typing import Tuple, TYPE_CHECKING, Optional

from exceptions import InstantiationError
from render_functions import *

import tcod
from tcod.map import compute_fov
from engine import Engine



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

    def render_hp(
        self,
        current_value: int,
        maximum_value: int,
        total_width: int,
        x: int = 0,
        y: int = 45,
    ) -> None:
        """ Renders a bar. """
        bar_width = int(float(current_value) / maximum_value * total_width)

        self.console.draw_rect(x=x, y=y, width=20, height=1, ch=1, bg=color.bar_empty)

        if bar_width > 0:
            self.console.draw_rect(
                x=x, y=y, width=bar_width, height=1, ch=1, bg=color.bar_filled
            )

        # lol at x=x+1
        self.console.print(
            x=x+1, y=y, string=f"HP: {current_value}/{maximum_value}", fg=color.bar_text
        )

    def render_names_at_mouse_location(
        self,
        x: int,
        y: int,
    ) -> None:
        # yup, this is easy to understand
        names_at_mouse_location = self.engine.game_map.get_names_at_location(*self.engine.mouse_location)

        self.console.print(x=x, y=y, string=names_at_mouse_location)

    def update_fov(self) -> None:
        """ Recompute visible area based on player's point of view. """
        self.engine.game_map.visible[:] = compute_fov(
            transparency=self.engine.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,)
        # If a tile is visible, it should be marked as explored.
        self.engine.game_map.explored |= self.engine.game_map.visible

    def render_game_map(self) -> None:
        """ Renders whatever the engine's active map is. """
        """
        There's multiple things here:
        1. We want to render what the player sees, centering the map on the player.
            We can write it with an arbitrary BaseAI, anything which implements a Map thing.

        """
        map = self.engine.game_map

        self.console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
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
