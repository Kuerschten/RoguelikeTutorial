from __future__ import annotations

import random
from typing import Dict, List, Set, Tuple, TYPE_CHECKING

from dungeon.base_dungeon_generator import BaseDungeonGenerator
from dungeon.constants import max_items_by_floor, max_monsters_by_floor, enemy_chances, item_chances
from entity import Actor
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


def _random_particle(
        particles: Set[Tuple[int, int]]
) -> Tuple[int, int]:
    return random.choice(list(particles))


def _dig_out_particles(
        dungeon: GameMap,
        particles: Set[Tuple[int, int]]
) -> None:
    for particle in particles:
        dungeon.tiles[particle] = tile_types.floor


def _place_player(
        player: Actor,
        particles: Set[Tuple[int, int]],
        dungeon: GameMap
) -> None:
    particle = _random_particle(particles)
    player.place(*particle, gamemap=dungeon)


def _place_downstairs(
        particles: Set[Tuple[int, int]],
        dungeon: GameMap
):
    particle = _random_particle(particles)

    dungeon.tiles[particle] = tile_types.down_stairs
    dungeon.downstairs_location = particle


def _get_max_value_for_floor(
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


def _place_entities_internal(
        particles: Set[Tuple[int, int]],
        dungeon: GameMap,
        floor_number: int
) -> None:
    number_of_monsters = random.randint(
        0, _get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, _get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = _get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = _get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x, y = _random_particle(particles)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


class ParticlesBase(BaseDungeonGenerator):
    def __init__(
            self,
            *,
            map_width: int,
            map_height: int,
            entity_rooms: int,
            floor_tile_rate: float,
            engine: Engine
    ):
        self.map_width = map_width
        self.map_height = map_height
        self.entity_rooms = entity_rooms
        self.floor_tile_rate = floor_tile_rate
        self.engine = engine

    def _get_random_direction(self) -> Tuple[int, int]:
        directions = [
            (0, -1),  # North
            (0, 1),   # South
            (1, 0),   # East
            (-1, 0),  # West
        ]

        weights = [self.map_height, self.map_height, self.map_width, self.map_width]

        return random.choices(
            directions,
            weights=weights,
            k=1
        )[0]

    def _should_break(
            self,
            step: int
    ) -> bool:
        multiply_border = self.map_width * self.map_height * self.floor_tile_rate
        sum_border = (self.map_width + self.map_height) * 2
        border = max(multiply_border, sum_border)

        return step > border

    def _place_entities(
            self,
            particles: Set[Tuple[int, int]],
            dungeon: GameMap,
            floor_number: int,
    ) -> None:
        for i in range(self.entity_rooms):
            _place_entities_internal(particles, dungeon, floor_number)

    def _create_particles(self) -> Set[Tuple[int, int]]:
        raise NotImplementedError()

    def generate_dungeon(self) -> GameMap:
        """Generate a new dungeon map."""
        player = self.engine.player
        dungeon = GameMap(self.engine, self.map_width, self.map_height, entities=[player])

        particles = self._create_particles()

        _dig_out_particles(dungeon, particles)

        _place_player(player, particles, dungeon)

        _place_downstairs(particles, dungeon)

        self._place_entities(particles, dungeon, self.engine.game_world.current_floor)

        return dungeon
