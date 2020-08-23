from __future__ import annotations

import random
import logging
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np  # type: ignore
import tcod

from actions import (
    Action,
    BumpAction,
    MeleeAction,
    MovementAction,
    WaitAction
)

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """ Compute and return a path to the target position.

        If no valid path exists, return the empty list.
        """
        # can specify different walkable tiles for an entity or basecomponent
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Adds costs to blocked positions.
                # Low means crowded hallways, high means players will try to
                # surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # initial position

        # compute path to destination, remove starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]]
        return [(index[0], index[1]) for index in path]


class ConfusedEnemy(BaseAI):
    """
    A confused enemy stumbles around aimlessly, swinging at anything
    in its way.

    Has a chance to avoid hitting allies.
    """
    def __init__(self,
         entity: Actor,
         previous_ai: Optional[BaseAI],
         turns_remaining: int,
    ):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining
        
    def perform(self) -> None:
        # Revert AI back to original state once effect expires.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            self.turns_remaining -= 1
            # pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # NW
                    (0, -1),   # N
                    (1, -1),   # NE
                    (-1, 0),   # W
                    (1, 0),    # E
                    (-1, 1),   # SW
                    (0, 1),    # S
                    (1, 1),    # SE
                ]
            )
            # Chance to not hit allies.
            target_x = self.entity.x + direction_x,
            target_y = self.entity.y + direction_y
            target_entity = self.engine.game_map.get_blocking_entity_at_location(target_x, target_y)
            if not (target_entity is self.engine.player):
                # 50% chance of not hitting allies
                # TODO: Tie into allegiances, intelligence.
                r = random.random()
                if r <= 0.5:
                    return WaitAction(self.entity)
            return BumpAction(self.entity, direction_x, direction_y,).perform()

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))   # Chebyshev distance
        logging.info("{} is {} spaces away.".format(self.entity, distance))

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            logging.info("{} sees us.".format(self.entity))
            if distance <= 1:
                logging.info("{} is going to try to hit us.".format(self.entity))
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            logging.info("{} is moving towards us.".format(self.entity))
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            ).perform()

        # logging.info("{} is waiting.".format(self.entity))
        return WaitAction(self.entity).perform()
