from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import tcod

from dungeon.base_dungeon_generator import BaseDungeonGenerator
from dungeon.rectangular_room import RectangularRoom
from dungeon.constants import max_items_by_floor, max_monsters_by_floor, enemy_chances, item_chances
from entity import Actor
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class RoomTunnelBase(BaseDungeonGenerator):
    def __init__(
            self,
            map_width: int,
            map_height: int,
            engine: Engine
    ):
        self.map_width = map_width
        self.map_height = map_height
        self.engine = engine

    def _connect_rooms(
            self,
            rooms: List[RectangularRoom],
            dungeon: GameMap) -> None:
        for i in range(0, len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]

            for x, y in self._tunnel_between(room1.random_field, room2.random_field):
                dungeon.tiles[x, y] = tile_types.floor

    def _get_max_value_for_floor(
            self,
            max_value_by_floor: List[Tuple[int, int]], floor: int
    ) -> int:
        current_value = 0

        for floor_minimum, value in max_value_by_floor:
            if floor_minimum > floor:
                break
            else:
                current_value = value

        return current_value

    def _get_entities_at_random(
            self,
            weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
            number_of_entities: int,
            floor: int,
    ) -> List[Entity]:
        entity_weighted_chances = {}

        for key, values in weighted_chances_by_floor.items():
            if key > floor:
                break
            else:
                for value in values:
                    entity = value[0]
                    weighted_chance = value[1]

                    entity_weighted_chances[entity] = weighted_chance

        entities = list(entity_weighted_chances.keys())
        entity_weighted_chance_values = list(entity_weighted_chances.values())

        chosen_entities = random.choices(
            entities, weights=entity_weighted_chance_values, k=number_of_entities
        )

        return chosen_entities

    def _tunnel_between(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int]
    ) -> Iterator[Tuple[int, int]]:
        """Return an L-shaped tunnel between these two points."""
        x1, y1 = start
        x2, y2 = end
        if random.random() < 0.5:  # 50% chance.
            # Move horizontally, then vertically.
            corner_x, corner_y = x2, y1
        else:
            # Move vertically, then horizontally.
            corner_x, corner_y = x1, y2

        # Generate the coordinates for this tunnel.
        for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
            yield x, y

    def _get_random_room(
            self,
            rooms: List[RectangularRoom]
    ) -> RectangularRoom:
        return rooms[random.randrange(0, len(rooms))]

    def _place_downstairs(
            self,
            rooms: List[RectangularRoom],
            dungeon: GameMap
    ):
        center_of_room = self._get_random_room(rooms).random_field

        dungeon.tiles[center_of_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_room

    def _place_player(
            self,
            player: Actor,
            rooms,
            dungeon
    ) -> None:
        room = self._get_random_room(rooms)
        player.place(*room.random_field, dungeon)

    def _place_entities(
            self,
            rooms: List[RectangularRoom],
            dungeon: GameMap,
            floor_number: int
    ) -> None:
        for room in rooms:
            self._place_entities_room(room, dungeon, floor_number)

    def _place_entities_room(
            self,
            room: RectangularRoom,
            dungeon: GameMap,
            floor_number: int
    ) -> None:
        number_of_monsters = random.randint(
            0, self._get_max_value_for_floor(max_monsters_by_floor, floor_number)
        )
        number_of_items = random.randint(
            0, self._get_max_value_for_floor(max_items_by_floor, floor_number)
        )

        monsters: List[Entity] = self._get_entities_at_random(
            enemy_chances, number_of_monsters, floor_number
        )
        items: List[Entity] = self._get_entities_at_random(
            item_chances, number_of_items, floor_number
        )

        for entity in monsters + items:
            x, y = room.random_field

            if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
                entity.spawn(dungeon, x, y)

    def _dig_out_rooms(
            self,
            dungeon: GameMap,
            rooms: List[RectangularRoom]
    ) -> None:
        for room in rooms:
            dungeon.tiles[room.inner] = tile_types.floor

    def _create_rooms(self) -> List[RectangularRoom]:
        raise NotImplementedError()

    def generate_dungeon(self) -> GameMap:
        """Generate a new dungeon map."""
        player = self.engine.player
        dungeon = GameMap(self.engine, self.map_width, self.map_height, entities=[player])

        rooms = self._create_rooms()

        self._dig_out_rooms(dungeon, rooms)

        self._connect_rooms(rooms, dungeon)

        self._place_player(player, rooms, dungeon)

        self._place_downstairs(rooms, dungeon)

        self._place_entities(rooms, dungeon, self.engine.game_world.current_floor)

        return dungeon
