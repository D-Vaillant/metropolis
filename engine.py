from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

#from actions import EscapeAction, MovementAction
import exceptions
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location
from tqueue import TurnQueue

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap
    from input_handlers import EventHandler
    from viewport import Viewport

class Engine:
    game_maps: List[GameMap]

    def __init__(self,
                 player: Actor,):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.map_index = 0
        self.game_maps = []
        self.turn_queue = TurnQueue()
        # For the sake of laziness
        self.schedule = self.turn_queue.schedule

    def handle_enemy_turns(self) -> None:
        while True:
            # print(self.turn_queue)
            ticket = self.turn_queue.next()

            entity_to_act = ticket.value
            if entity_to_act is self.player:
                return
            elif entity_to_act.ai:
                # I took out the Impossible exception part...
                tick_cost = entity_to_act.ai.perform()
                if tick_cost is None:
                    raise exceptions.Impossible("An action occurred without a tick cost.")
                self.schedule(value=entity_to_act, interval=tick_cost)




    @property
    def game_map(self) -> Optional[GameMap]:
        """ Maps are accessed by using an index. """
        try:
            return self.game_maps[self.map_index]
        except IndexError:
            return None

    @game_map.setter
    def game_map(self, new_map) -> None:
        """ Either we switch to an already existing map, or we add it to the list. """
        try:
            map_index = self.game_maps.index(new_map)
        except ValueError:  # game not in list already
            self.game_maps.append(new_map)
            map_index = len(self.game_maps) - 1
        self.map_index = map_index

    def update_fov(self) -> None:
        """ Recompute visible area based on player's point of view. """
        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.tiles["transparent"],
            pov=(self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is visible, it should be marked as explored.
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
