class Cell:
    def __init__(self, north: int, east: int, south: int, west: int,
                 pos: tuple[int, int]):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_visited = False
        self.pos = pos

    def get_hex(self) -> str:
        walls = [str(self.north), str(self.east), str(self.south),
                 str(self.west)]
        num = hex(int("".join(walls), 2))
        return num
