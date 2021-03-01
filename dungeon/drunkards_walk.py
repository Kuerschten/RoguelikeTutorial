from __future__ import annotations

from typing import Set, Tuple, TYPE_CHECKING

from dungeon.particles_base import ParticlesBase

if TYPE_CHECKING:
    from engine import Engine


class DrunkardsWalk(ParticlesBase):

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

        while len(particles) < self.map_height * self.map_width * self.floor_tile_rate:
            direction_x, direction_y = self._get_random_direction()

            target_x = particle_x + direction_x
            target_y = particle_y + direction_y

            if 0 < target_x < self.map_width - 1 and 0 < target_y < self.map_height - 1:
                particles.add((target_x, target_y))
                particle_x, particle_y = target_x, target_y

        return particles
