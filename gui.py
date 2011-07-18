import sys
import pygame
from pygame.locals import *

from shapes import *
from vector import *
import gui_settings

class Gui:
    # Constructor {{{1
    def __init__ (self, world):
        self.world = world

        pygame.init()

        # In meters
        self.map_volume = world.get_map_volume()
        self.size = Vector.from_vector3D(self.map_volume, strip='z')
        
        radius = int(world.get_tile_size() / 2.0)
        self.world_offset = Vector3D(radius, radius, 0)

        self.screen = pygame.display.set_mode(self.size.pygame)

        self.font = pygame.font.Font(None, 20)

        self.selected = None

        print '== Gui Report =='
        print 'Map volume: ', self.map_volume
        print 'Map size: ', self.size
        print '== End Report ==\n'
    # }}}1

    # Updates {{{1
    def update (self, time):
        self.react (time)
        self.draw (time)

    def react (self, time):
        # React to input. {{{2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif not self.selected is None:
                    new = None
                    if event.key == K_UP:
                        new = self.selected.get_adjacent('north')
                    elif event.key == K_DOWN:
                        new = self.selected.get_adjacent('south')
                    elif event.key == K_RIGHT:
                        new = self.selected.get_adjacent('east')
                    elif event.key == K_LEFT:
                        new = self.selected.get_adjacent('west')
                    if not new is None:
                        self.selected = new


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = self.flip_y(event.pos)
                    location = Vector3D(x, y, 0) - self.world_offset
                    surface = self.world.get_surface()
                    self.selected = surface.find_tile(location)
        # }}}2
    def draw (self, time):
        # Draw {{{2
        tile_color = gui_settings.tile_color
        selected_color = gui_settings.selected_color
        background_color = gui_settings.background_color
        text_color = gui_settings.text_color
        direction_color = gui_settings.direction_color

        world = self.world
        surface = world.get_surface()

        size = world.get_tile_size()
        radius = int(size / 2.0)
        world_offset = Vector.from_vector3D(self.world_offset)
        position = None

        screen = self.screen
        screen.fill(background_color)

        screen.lock()
        for tile in surface.get_tiles():
            # Draw a circle for each tile
            index = tile.get_index() * size + world_offset

            py_location = self.flip_y(index.pygame)
            if tile is self.selected:
                pygame.draw.circle(screen, selected_color, py_location, radius)
            else:
                pygame.draw.circle(screen, tile_color, py_location, radius)
        """
            # Draw the neighbor connections.
            for name in 'north', 'south', 'east', 'west':
                neighbor = tile.get_neighbor(name)
                if neighbor.is_implemented():
                    neighbor_offset = neighbor.get_offset()
                    start_point = position
                    end_point = start_point + neighbor_offset / 2.0
                    line_color = direction_color[name]

                    py_start = self.flip_y(start_point.pygame)
                    py_end = self.flip_y(end_point.pygame)
                    pygame.draw.line(screen, line_color, py_start, py_end)
        """
        screen.unlock()

        # Show frame rate:
        frame_rate = 1.0 / time
        rate_text = 'Frame rate: %f.2' % frame_rate
        rate_image = self.font.render(rate_text, True, text_color, background_color)
        rate_position = 0, 0
        screen.blit(rate_image, rate_position)

        # Finish the update.
        pygame.display.flip()
        # }}}2
    # }}}1
    def flip_y (self, tuple):
        x = tuple[0]
        y = int(self.size.y) - tuple[1]
        return x, y
