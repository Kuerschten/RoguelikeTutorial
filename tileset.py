import tcod


class TilesetFactory:
    @staticmethod
    def get_tileset(tileset_type=tcod.tileset.CHARMAP_TCOD) -> tcod.tileset.Tileset:
        if tileset_type == tcod.tileset.CHARMAP_TCOD:
            return tcod.tileset.load_tilesheet(
                "fonts/tcod/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
            )
        else:
            return tcod.tileset.load_tilesheet(
                "fonts/cp437/terminal16x16_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437
            )
