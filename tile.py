import random

from vector import *
from neighbor import Neighbor

class Tile:
    # Constructor {{{1
    def __init__ (self, surface, index, position, width):
        self.surface = surface
        self.index = index
        self.position = position
        self.size = width

        self.refresh = False
        self.edge = False

        self.north = Neighbor(self, 'north', Vector3D( 0,  1, 0))
        self.south = Neighbor(self, 'south', Vector3D( 0, -1, 0))
        self.east = Neighbor(self, 'east',   Vector3D( 1,  0, 0))
        self.west = Neighbor(self, 'west',   Vector3D(-1,  0, 0))

        self.neighbors = (self.north, self.south, self.east, self.west)

        self.down = Neighbor(self, 'down', Vector3D(0, 0, -1))


    def setup_neighbors(self, search_list):
        find = self.surface.find_tile
        for neighbor in self.neighbors:
            if not neighbor.is_implemented():
                target_index = self.index + neighbor.get_direction()

                #target_pos = self.position + neighbor.get_offset()
                #adjacent = find(target=target_pos, tile_list=search_list)
                adjacent = find(index=target_index, tile_list=search_list)
                if adjacent is None:
                    if not self.edge:
                        self.surface.get_border().add_edge(self)
                        self.edge = True
                else:
                    neighbor.setup (adjacent)
    # }}}1
    # Update {{{1
    def update (self, time):
        if self.refresh:
            print 'refreshing'
            for neighbor in self.neighbors:
                neighbor.update(time)
            self.refresh = False

    def set_update(self, bool):
        self.refresh = bool
    # }}}1

    # Attributes {{{1
    def get_neighbor (self, name):
        if 'north' == name: return self.north
        if 'south' == name: return self.south
        if 'east' == name: return self.east
        if 'west' == name: return self.west

    def get_adjacent (self, name):
        neighbor = self.get_neighbor(name)
        return neighbor.get_adjacent()

    def get_position (self): return self.position
    def get_size(self): return self.size
    def get_index(self): return self.index
    # }}}1

class Border:
    def __init__ (self, surface):
        self.surface = surface
        self.edge_tiles = []
        #self.neighbors = []

    def add_edge (self, tile):
        self.edge_tiles.append(tile)


