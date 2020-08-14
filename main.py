#!/usr/bin/env python3
import copy
import traceback
from typing import TYPE_CHECKING

import tcod

import color
from engine import Engine
import entity_factories
from procgen import generate_dungeon
from apartment import generate_apartment_floor

if TYPE_CHECKING:
    from game_map import GameMap


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    hallway_width = 10

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

    starting_apartment = generate_apartment_floor(
        max_apartments=5,
        room_min_size=5,
        room_max_size=5,
        map_width=map_width,
        map_height=map_height,
        hallway_width=hallway_width,
        engine=engine,
    )


    engine.game_map: GameMap = starting_apartment

    engine.update_fov()

    engine.message_log.add_message(
        "You wake up in a cold room. The floor is stone.", color.welcome_text
    )

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Roguelike Tutorial",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:
                traceback.print_exc()
                # print error to the message log
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
