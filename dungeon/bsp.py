from __future__ import annotations

import random
from typing import List, TYPE_CHECKING

import tcod

from dungeon.rectangular_room import RectangularRoom
from dungeon.room_tunnel_base import RoomTunnelBase

if TYPE_CHECKING:
    from engine import Engine


class BSP(RoomTunnelBase):
    def __init__(
            self,
            room_min_size: int,
            room_max_size: int,
            map_width: int,
            map_height: int,
            engine: Engine
    ):
        super().__init__(
            map_width=map_width,
            map_height=map_height,
            engine=engine
        )
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

    def _create_rooms(self) -> List[RectangularRoom]:
        rooms: List[RectangularRoom] = []

        bsp = tcod.bsp.BSP(x=0, y=0, width=self.map_width, height=self.map_height)
        bsp.split_recursive(
            depth=5,
            min_width=self.room_max_size + 1,
            min_height=self.room_max_size + 1,
            max_horizontal_ratio=1.5,
            max_vertical_ratio=1.5
        )

        # In pre order, leaf nodes are visited before the nodes that connect them.
        for node in bsp.pre_order():
            if node.children:
                # Ignore non leaves
                continue
            else:
                room_width = random.randint(self.room_min_size, self.room_max_size)
                room_height = random.randint(self.room_min_size, self.room_max_size)

                x = random.randint(node.x, node.x + node.width - room_width - 1)
                y = random.randint(node.y, node.y + node.height - room_height - 1)

                # "RectangularRoom" class makes rectangles easier to work with
                new_room = RectangularRoom(x, y, room_width, room_height)

                rooms.append(new_room)

        return rooms
