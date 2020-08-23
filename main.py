#!/usr/bin/env python3
import copy
import logging
import traceback
from typing import TYPE_CHECKING

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon
from viewport import Viewport

if TYPE_CHECKING:
    from game_map import GameMap


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    # okay, logger should be ok now
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2
    max_items_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
            # why 32/8?
            "static/dejavu12x12.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    starting_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.game_map: GameMap = starting_map

    logger.info("Entering context.")
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Roguelike Tutorial",
            vsync=True,
    ) as context:
        viewport = Viewport(screen_width, screen_height, order="F", engine=engine)
        viewport.update_fov()

        engine.message_log.add_message(
            "You wake up in a cold room. The floor is stone.", color.welcome_text
        )

        logger.info("Starting loop.")
        while True:   # Why are we looping this?
            viewport.clear()
            engine.event_handler.on_render(viewport=viewport)
            context.present(viewport.console)

            try:
                for event in tcod.event.wait():
                    logger.info("event: {}".format(event))
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
                    viewport.update_fov()
            except Exception:
                traceback.print_exc()
                # print error to the message log
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
