class Cell:
    """A single maze cell, tracking whether each of its four walls
    (north, east, south, west) is present (1) or open (0)."""

    def __init__(self, north: int, east: int, south: int, west: int,
                 pos: tuple[int, int]):
        """Create a cell at grid position `pos` with the given wall
        states, all walls closed by default and marked as unvisited."""
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.pos = pos

    def get_hex(self) -> str:
        """Encode the cell's four walls as a 4-bit binary number
        (N,E,S,W) and return it as a single hexadecimal digit."""
        walls = [str(self.north), str(self.east), str(self.south),
                 str(self.west)]
        num = hex(int("".join(walls), 2))[2].capitalize()
        return num
