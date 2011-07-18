from vector import *

class Neighbor:
    # Constructor {{{1
    def __init__ (self, parent, name, direction):
        self.parent = parent
        self.name = name
        self.direction = direction
        self.offset = direction * parent.get_size()

        self.implemented = False
        self.neighbor = None
        self.slope = Vector3D.null()

    def setup (self, adjacent):
        target_name = ''
        if 'north' == self.name:
            target_name = 'south'
        if 'south' == self.name:
            target_name = 'north'
        if 'east' == self.name:
            target_name = 'west'
        if 'west' == self.name:
            target_name = 'east'

        neighbor = adjacent.get_neighbor(target_name)

        my_position = self.parent.get_position()
        your_position = neighbor.get_position()
        slope = your_position - my_position

        neighbor.greet(self, slope)

        self.neighbor = neighbor
        self.slope = slope

        self.implemented = True

    def greet (self, neighbor, slope):
        self.neighbor = neighbor
        self.slope = slope

        self.implemented = True
    #}}}

    # Update {{{1
    def update (self, time):
        if self.implemented:
            my_position = self.parent.get_position()
            your_position = self.neighbor.get_position()
            my_slope = your_position - my_position
            if not self.slope == my_slope:
                self.neighbor.refresh(my_slope)
                self.slope = my_slope

    # Methods {{{1
    def refresh (self, your_slope):
        self.slope = -your_slope
        self.parent.set_update(True)
    # }}}1

    # Operators {{{1
    def __eq__ (self, other):
        return self.neighbor is other and other.get_slope() == -self.slope
    # }}}1

    # Attributes {{{1
    def is_implemented (self): return self.implemented
    def get_parent (self): return self.parent
    def get_name(self): return self.name
    def get_direction (self): return self.direction
    def get_offset (self): return self.offset
    def get_slope (self): return self.slope
    def get_position (self): return self.parent.get_position()
    def get_adjacent (self):
        if self.neighbor is None: return None
        else: return self.neighbor.get_parent()
