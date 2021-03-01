from __future__ import annotations

import math
import random
from typing import Set, Tuple, TYPE_CHECKING

from dungeon.particles_base import ParticlesBase

if TYPE_CHECKING:
    from engine import Engine


class DiffusionLimitedAggregation(ParticlesBase):

    def __init__(
            self,
            *,
            map_width: int,
            map_height: int,
            entity_rooms: int,
            floor_tile_rate: float,
            engine: Engine):
        super().__init__(
            map_width=map_width,
            map_height=map_height,
            entity_rooms=entity_rooms,
            floor_tile_rate=floor_tile_rate,
            engine=engine
        )

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

            i = 0
            add_particle = True

            while (target_x, target_y) not in particles:
                i += 1

                if 0 < target_x < self.map_width - 1 and 0 < target_y < self.map_height - 1:
                    particle_x, particle_y = target_x, target_y

                direction_x, direction_y = self._get_random_direction()

                target_x = particle_x + direction_x
                target_y = particle_y + direction_y

                if i > self.map_width * self.map_height * self.floor_tile_rate:
                    # Break if stray and try again
                    add_particle = False
                    break

            if add_particle:
                particles.add((particle_x, particle_y))

        return particles
