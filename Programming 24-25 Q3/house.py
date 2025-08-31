import pygame
from pygame.locals import *
import math

pygame.init()
WIDTH = 800
HEIGHT = 600
# DISPLAYSURF=pygame.display.set_mode((WIDTH,HEIGHT))
# Make Pygame use the fullscreen in CODIO (Which is 800x600)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
roofColor = (98, 28, 19)

pi = math.pi

DEG30 = pi / 6
DEG45 = pi / 4
DEG60 = pi / 3
DEG90 = pi / 2
DEG180 = pi
DEG360 = 2 * pi

# house dimensions
hx = 100
hy = 100
hh = 100
hw = 100
hd = 50  # house z distance
rh = 50  # roof height

# z axis
a = DEG30

# outline thickness (actual thickness is twice the value)
thickness = 1

# ---------------------------------------#
# the main program begins here          #
# ---------------------------------------#
while True:
    pygame.event.clear()
    DISPLAYSURF.fill(WHITE)

    def setPadding(outer, padding):
        inner = []
        cx = cy = 0
        # more efficient to use one loop instead of two loops when calculating center
        for x, y in outer:
            cx += x
            cy += y
        cx /= 3
        cy /= 3

        for x, y in outer:
            dx = cx - x
            dy = cx - y
            s = 1 - (2 * padding / max(hw, rh))  # scaling towards centroid
            for x, y in outer:
                inner.append((cx + (x - cx) * s, cy + (y - cy) * s))

        return inner

    def generate3D(coords, angle, distance):
        res = [(x, y) for x, y in reversed(coords)]
        for x, y in coords:
            res.append((x + distance, y - math.tan(angle) * distance))

        return res

    def generateRectVertices(x, y, w, h):
        return ((x, y), (x + w, y), (x + w, y + h), (x, y + h))

    def drawFilledOutline(color, coords):
        surface = DISPLAYSURF
        pygame.draw.polygon(surface, color, coords, 0)
        pygame.draw.polygon(surface, GREY, coords, thickness)

    roofCoords = [(hx, hy), (hx + hw / 2, hy - rh), (hx + hw, hy)]

    innerRoofCoords = setPadding(roofCoords, 10)
    houseBounds = generateRectVertices(hx, hy, hw, hh)

    drawFilledOutline((208, 66, 48), houseBounds)

    # 3D
    drawFilledOutline(roofColor, generate3D((roofCoords[0], roofCoords[1]), a, hd))
    drawFilledOutline(roofColor, generate3D((roofCoords[1], roofCoords[2]), a, hd))
    drawFilledOutline(roofColor, generate3D((houseBounds[1], houseBounds[2]), a, hd))
    # roof (overengineered)
    drawFilledOutline(roofColor, roofCoords)
    drawFilledOutline((242, 229, 184), innerRoofCoords)

    # -----------------------------------#
    pygame.display.update()  # display must be updated, in order
    # to show the drawings
    # Check for Quit
    for event in pygame.event.get():  # this loop is required to determine
        if event.type == QUIT:  # if the user closed the window
            pygame.quit()
            exit()  # which will cause the program to quit
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # hit ESCAPE to quit
                pygame.quit()
                exit()
