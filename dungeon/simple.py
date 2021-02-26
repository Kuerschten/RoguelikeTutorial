from __future__ import annotations

import random
from typing import List, TYPE_CHECKING


from dungeon.room_tunnel_base import RoomTunnelBase
from dungeon.rectangular_room import RectangularRoom


if TYPE_CHECKING:
    from engine import Engine


class Simple(RoomTunnelBase):
    def __init__(
            self,
            max_rooms: int,
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
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

    def _create_rooms(self) -> List[RectangularRoom]:
        rooms: List[RectangularRoom] = []

        for r in range(self.max_rooms):
            room_width = random.randint(self.room_min_size, self.room_max_size)
            room_height = random.randint(self.room_min_size, self.room_max_size)

            x = random.randint(0, self.map_width - room_width - 1)
            y = random.randint(0, self.map_height - room_height - 1)

            # "RectangularRoom" class makes rectangles easier to work with
            new_room = RectangularRoom(x, y, room_width, room_height)

            # Run through the other rooms and see if they intersect with this one.
            if any(new_room.intersects(other_room) for other_room in rooms):
                continue  # This room intersects, so go to the next attempt.
            # If there are no intersections then the room is valid.

            rooms.append(new_room)

        return rooms
