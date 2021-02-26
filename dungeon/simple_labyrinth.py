from __future__ import annotations

from typing import List, TYPE_CHECKING

import tcod

from dungeon.rectangular_room import RectangularRoom
from dungeon.room_tunnel_base import RoomTunnelBase

if TYPE_CHECKING:
    from engine import Engine


class SimpleLabyrinth(RoomTunnelBase):
    def __init__(
            self,
            room_min_size: int,
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

    def _create_rooms(self) -> List[RectangularRoom]:
        rooms: List[RectangularRoom] = []

        bsp = tcod.bsp.BSP(x=0, y=0, width=self.map_width-1, height=self.map_height-1)
        bsp.split_recursive(
            depth=6,
            min_width=self.room_min_size,
            min_height=self.room_min_size,
            max_horizontal_ratio=1.2,
            max_vertical_ratio=1.2
        )

        # In pre order, leaf nodes are visited before the nodes that connect them.
        for node in bsp.pre_order():
            if node.children:
                # Ignore non leaves
                continue
            else:
                # "RectangularRoom" class makes rectangles easier to work with
                new_room = RectangularRoom(node.x, node.y, node.width, node.height)

                rooms.append(new_room)

        return rooms
