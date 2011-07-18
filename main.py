from __future__ import division

import sys
from world import World
from gui import Gui

import pygame
from pygame.locals import *

clock  = pygame.time.Clock()
frequency = 40

world = World()
gui = Gui(world)

while world.is_running():
    time = clock.tick(frequency) / 1000

    world.update(time)
    gui.update(time)

print "Have a nice day!"
