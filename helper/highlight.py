from typing import Tuple

import tcod

import color


def highlight(
        console: tcod.Console,
        xy: Tuple[int, int],
        *,
        fg: Tuple[int, int, int] = color.black,
        bg: Tuple[int, int, int] = color.white
) -> None:
    try:
        x, y = xy

        if x >= 0 and y >= 0:
            console.tiles_rgb["bg"][xy] = bg
            console.tiles_rgb["fg"][xy] = fg
    except IndexError:
        pass  # Ignore to write out of index.
