from __future__ import division
from tile import *
from vector import *

class Surface:
    def __init__ (self, world):
        self.world = world
        self.tiles = []
        self.border = Border(self)
        
        self.tiles_genesis()
        self.tiles_setup()

        print '== Surface Report =='
        print 'Length Tiles: %i' %len(self.tiles)
        print '== End Report ==\n'

    def tiles_genesis (self):
        count = self.world.get_count()
        x, y = count.pygame
        x_base = Vector3D(1, 0, 0)
        y_base = Vector3D(0, 1, 0)
        size = self.world.get_tile_size()

        print 'Tile genesis beginning. Tiles to be made: %i' %(x * y)
        for i in range(x):
            for j in range(y):
                x_coor = x_base * i * size
                y_coor = y_base * j * size
                position = x_coor + y_coor
                index = Vector(i, j)
                tile = Tile(self, index, position, size)
                self.tiles.append(tile)
        print 'Tile genesis complete. %i Tiles made.\n' %len(self.tiles)

    def tiles_setup (self):
        print 'Setting up Tiles. This may take awhile.'
        search_list = set(self.tiles)
        
        step = 2
        processed = 0
        total = len(search_list)
        percents = []
        for i in range(int(100 / step) + 1):
            percents.append(i * step)

        for tile in self.tiles:
            tile.setup_neighbors(search_list)
            search_list.remove(tile)

            processed += 1
            temp_percent = 100.0 * processed / total
            percent = temp_percent - temp_percent % 1
            if percent in percents:
                print '%i%% complete.' %(percent)
                percents.remove(percent)

        print 'Tile setup complete\n'

    def update (self, time):
        for tile in self.tiles:
            tile.update(time)

    def find_tile (self, target=None, index=None, tile_list=None):
        # target is a vector3D. index is a 2D vector of integers.
        # Exactly one of either target or index must be provided.
        # tile_list is the list that will be searched.
        if tile_list is None:
            tile_list = self.tiles

        if target is None and not index is None:
            for tile in tile_list:
                tile_index = tile.get_index()
                if tile_index == index:
                    return tile
        elif index is None and not target is None:
            tile_size = self.world.get_tile_size()

            half_side = tile_size / 2.0
            max_contained_squared = 2 * half_side**2

            for tile in tile_list:
                position = tile.get_position()

                difference = position - target
                flat = Vector.from_vector3D (difference, strip = 'z')

                if max_contained_squared >= flat.magnitude_squared:
                    x, y = flat.__abs__().tuple

                    if x <= half_side and y <= half_side:
                        return tile
        return None

    def get_world (self): return self.world
    def get_tiles (self): return self.tiles
    def get_border (self): return self.border
