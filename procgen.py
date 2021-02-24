from __future__ import annotations

from typing import TYPE_CHECKING

from dungeon.simple import generate_dungeon as generate_simple_dungeon
from dungeon.bsp import generate_dungeon as generate_bsp_dungeon
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
    return generate_bsp_dungeon(
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
