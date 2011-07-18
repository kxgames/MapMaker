import managers
import settings
from vector import *

class World:
    def __init__ (self):
        self.running = True

        # In meters
        self.tile_size = settings.tile_size
        self.map_volume = settings.map_volume * 1000.0

        # Number of tiles on xy plane
        count = Vector.from_vector3D(self.map_volume, strip='z')
        self.count = count / self.tile_size

        self.surface = managers.Surface(self)
        #self.subsurface = managers.Subsurface(self)

        print '== World Report =='
        print 'Tile_size: %f' %self.tile_size
        print 'Map volume: ', self.map_volume
        print 'Count: ', self.count
        print '== End Report ==\n'

    def update (self, time):
        #self.subsurface.update(time)
        self.surface.update(time)
    
    def is_running(self): return self.running
    def get_surface (self): return self.surface
    #def get_subsurface (self): return self.subsurface
    def get_count (self): return self.count
    def get_tile_size (self): return self.tile_size
    def get_map_volume (self): return self.map_volume
