from __future__ import annotations

from typing import TYPE_CHECKING

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

class Engine:
    game_map: GameMap

    def __init__(self,
                 player: Actor):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.turn_queue = TurnQueue()
        # For the sake of laziness
        self.schedule = self.turn_queue.schedule

    def handle_enemy_turns(self) -> None:
        while True:
            print(self.turn_queue)
            ticket = self.turn_queue.next()

            entity_to_act = ticket.value
            if entity_to_act is self.player:
                return
            else:
                break

        # I took out the Impossible exception part...
        if entity_to_act.ai:
            entity_to_act.ai.perform()


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
