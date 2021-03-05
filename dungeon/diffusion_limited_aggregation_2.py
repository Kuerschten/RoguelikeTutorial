from __future__ import annotations

import random
from typing import Set, Tuple, TYPE_CHECKING

from dungeon.particles_base import ParticlesBase

if TYPE_CHECKING:
    from engine import Engine


def _should_stuck(
        particles: Set[Tuple[int, int]],
        *,
        x: int,
        y: int
) -> bool:
    north = (x + 1, y)
    south = (x - 1, y)
    east = (x, y + 1)
    west = (x, y - 1)

    return north in particles or south in particles or east in particles or west in particles


class DiffusionLimitedAggregation2(ParticlesBase):
    def __init__(
            self,
            *,
            map_width: int,
            map_height: int,
            entity_rooms: int = 10,
            floor_tile_rate: float = 0.25,
            engine: Engine):
        super().__init__(
            map_width=map_width,
            map_height=map_height,
            entity_rooms=entity_rooms,
            floor_tile_rate=floor_tile_rate,
            engine=engine
        )

    def _should_break(
            self,
            step: int
    ) -> bool:
        multiply_border = self.map_width * self.map_height * self.floor_tile_rate
        sum_border = (self.map_width + self.map_height) * 2
        border = max(multiply_border, sum_border)

        return step > border

    def _create_particles(self) -> Set[Tuple[int, int]]:
        particle_x = int(self.map_width / 2)
        particle_y = int(self.map_height / 2)

        particles: Set[Tuple[int, int]] = {(particle_x, particle_y)}

        cross_x_stretch = int(self.map_width * self.floor_tile_rate * 0.25)
        cross_y_stretch = int(self.map_height * self.floor_tile_rate * 0.25)

        for i in range(-cross_x_stretch, cross_x_stretch + 1):
            particles.add((particle_x + i, particle_y))

        for i in range(-cross_y_stretch, cross_y_stretch + 1):
            particles.add((particle_x, particle_y + i))

        while len(particles) < self.map_height * self.map_width * self.floor_tile_rate:
            particle_x = target_x = random.randint(1, self.map_width - 2)
            particle_y = target_y = random.randint(1, self.map_height - 2)

            # Starting from edge
            starting_direction_x, starting_direction_y = self._get_random_direction()

            if starting_direction_x < 0:
                particle_x = target_x = 1
            elif starting_direction_x > 0:
                particle_x = target_x = self.map_width - 2
            elif starting_direction_y < 0:
                particle_y = target_y = 1
            else:
                particle_y = target_y = self.map_height - 2

            step = 0
            add_particle = True

            while not _should_stuck(particles, x=particle_x, y=particle_y):
                step += 1

                if 0 < target_x < self.map_width - 1 and 0 < target_y < self.map_height - 1:
                    particle_x, particle_y = target_x, target_y

                direction_x, direction_y = self._get_random_direction()

                target_x = particle_x + direction_x
                target_y = particle_y + direction_y

                if self._should_break(step):
                    # Break if stray and try again
                    add_particle = False
                    break

            if add_particle:
                particles.add((particle_x, particle_y))

        return particles
