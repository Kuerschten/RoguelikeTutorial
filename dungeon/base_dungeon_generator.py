from game_map import GameMap


class BaseDungeonGenerator:
    def generate_dungeon(self) -> GameMap:
        raise NotImplementedError()
