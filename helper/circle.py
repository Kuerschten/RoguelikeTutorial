import tcod

import math
from typing import Tuple

import color
from helper.highlight import highlight


def is_in(
        *,
        center_xy: Tuple[int, int],
        radius: int,
        target_xy: Tuple[int, int]
) -> bool:
    center_x, center_y = center_xy
    target_x, target_y = target_xy

    distance = math.sqrt((center_x - target_x) ** 2 + (center_y - target_y) ** 2)

    return distance <= radius + 0.5


def draw_circle(
        console: tcod.Console,
        center_xy: Tuple[int, int],
        radius: int,
        *,
        fg: Tuple[int, int, int] = color.black,
        bg: Tuple[int, int, int] = color.white

) -> None:
    center_x, center_y = center_xy

    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            target_xy = (center_x + i, center_y + j)

            if is_in(center_xy=center_xy, radius=radius, target_xy=target_xy):
                highlight(console, target_xy, fg=fg, bg=bg)
                