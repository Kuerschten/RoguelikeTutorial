from __future__ import annotations

from typing import TYPE_CHECKING

from dungeon.bsp import BSP
from dungeon.diffusion_limited_aggregation import DiffusionLimitedAggregation
from dungeon.diffusion_limited_aggregation_2 import DiffusionLimitedAggregation2
from dungeon.drunkards_walk import DrunkardsWalk
from dungeon.simple import Simple
from dungeon.simple_labyrinth import SimpleLabyrinth
from game_map import GameMap


if TYPE_CHECKING:
    from engine import Engine


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine
) -> GameMap:
    """
    generator = Simple(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """

    """
    generator = BSP(
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """

    """
    generator = SimpleLabyrinth(
        room_min_size=room_min_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """

    """
    generator = DrunkardsWalk(
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """

    """
    generator = DiffusionLimitedAggregation(
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """

    generator = DiffusionLimitedAggregation2(
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )

    return generator.generate_dungeon()
