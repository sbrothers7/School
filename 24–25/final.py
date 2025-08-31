import pygame
from pygame.locals import *

pygame.init()

WIDTH = 800
HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project")

import math
import random

shadowSurf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (250, 200, 150)
MGRAY = (150, 150, 150)
DGRAY = (70, 70, 70)
GREEN = (80, 120, 80)
LGRAY = (180, 180, 180)

# sky colors (stored in lists instead of tuples)
skyColors = [
    [[120, 150, 200], [220, 150, 110]],
    [[60, 90, 180], [120, 150, 200]],
    [[120, 150, 200], [220, 150, 110]],
    [[20, 20, 30], [30, 50, 80]],
]
# sun -> normal -> sun -> night

# other colors
cloudColor = [255, 255, 255, 140]
lightColor = [235, 235, 175]
riverColor = [90, 120, 150]

# current index of skyColors
skyState = 0

# other variables
angle = 0
angleIncrement = -(math.pi / 1024)
r = 320
rh = 15  # road height
yb = HEIGHT - 150  # y base value
step = 0
cycleTotal = (math.pi * 2) / abs(angleIncrement)
transition = 200  # value can't go under largest color value difference
starR = 400
cloudX = [100, 400, 700]  # inital locations of clouds

# window dimensions
wh = 14
ww = 10
wp = 3

shadowAlpha = 80


stars = []
# init stars
for i in range(200):
    stars.append(
        [
            random.randint(-WIDTH // 2 - starR, WIDTH // 2 + starR),
            random.randint(-starR, yb + starR),
            random.randint(50, 255),
        ]
    )
# stored in [x, y, alpha] format


def drawPoly(color, coords, outline=0):
    pygame.draw.polygon(DISPLAYSURF, color, coords, 0)
    if outline != 0:
        pygame.draw.polygon(DISPLAYSURF, BLACK, coords, outline)


def drawRect(color, coords, outline=0):
    pygame.draw.rect(DISPLAYSURF, color, coords, 0)
    if outline != 0:
        pygame.draw.rect(DISPLAYSURF, BLACK, coords, outline)


def createColorDiffList(a, b):
    diff = []
    for i in range(3):
        diff.append(a[i] - b[i])
    return diff


def generateGradient(color1, color2):
    diff = createColorDiffList(color1, color2)

    color = list(color1)
    for i in range(yb):
        for j in range(3):
            # print("color: " + str(j) + ", res: " + str(i % (yb // abs(diff[j]))))
            if (diff[j] != 0) and (i % (yb // abs(diff[j])) == 0):
                if diff[j] < 0:
                    color[j] += 1
                else:
                    color[j] -= 1
                # print(color)

        drawRect(color, (0, i, WIDTH, 1))


currColors = [[x for x in skyColors[0][0]], [x for x in skyColors[0][1]]]
cd = []  # color difference


def setCd():
    global cd

    cd = [
        createColorDiffList(currColors[0], skyColors[skyState][0]),
        createColorDiffList(currColors[1], skyColors[skyState][1]),
    ]


def colorComp(a, b):
    for i in range(3):
        if a[i] != b[i]:
            return False
    return True


def sky():
    global skyState

    if step % cycleTotal > round(cycleTotal * 0.5):
        skyState = 3
        setCd()
    elif step % cycleTotal > round(cycleTotal * 0.4):
        skyState = 2
        setCd()
    elif step % cycleTotal > round(cycleTotal * 0.1):
        skyState = 1
        setCd()
    elif step % cycleTotal > 0:
        skyState = 0
        setCd()

    target = skyColors[skyState]
    color1 = currColors[0]
    color2 = currColors[1]

    if not (colorComp(color1, target[0]) or colorComp(color2, target[1])):
        for i in range(3):
            for j in range(len(cd)):
                if (cd[j][i] != 0) and (step % (transition // abs(cd[j][i])) == 0):
                    if cd[j][i] < 0:
                        currColors[j][i] += 2
                        if currColors[j][i] > target[j][i]:
                            currColors[j][i] = target[j][i]
                    else:
                        currColors[j][i] -= 2
                        if currColors[j][i] < target[j][i]:
                            currColors[j][i] = target[j][i]

    generateGradient(color1, color2)

    if skyState == 3:
        for x in stars:
            pygame.draw.circle(
                DISPLAYSURF,
                (255, 255, 255, x[2]),
                (
                    math.cos((angle) - math.pi) * starR + x[0] + WIDTH // 2,
                    math.sin((angle) - math.pi) * starR + x[1] + HEIGHT // 2,
                ),
                1,
            )


def celestialObject():
    pygame.draw.circle(
        DISPLAYSURF,
        (230, 230, 100),
        (
            (math.cos(angle) * r) + WIDTH // 2,
            (math.sin(angle) * r) + HEIGHT // 2 + 150,
        ),
        20,
    )
    pygame.draw.circle(
        DISPLAYSURF,
        (240, 240, 240),
        (
            (math.cos(angle - math.pi) * r) * 1.15 + WIDTH // 2,
            (math.sin(angle - math.pi) * r) * 1.1 + HEIGHT // 2 + 150,
        ),
        15,
    )


def rectBoundsGen(x, y, w, h):
    return ((x, y), (x + w, y), (x + w, y + h), (x, y + h))


def windowBoundsGen(coords):
    x = coords[-2][0] - coords[-1][0]

    # only get y coordinates
    temp = []
    for coord in coords:
        temp.append(list(coord))

    # same thing as set(temp) but we're not allowed to use sets :(
    ycoords = []
    for a in temp:
        if not a[1] in ycoords:
            ycoords.append(a[1])

    # print(ycoords)
    tempY = max(ycoords)
    if len(ycoords) > 2:
        ycoords.remove(tempY)
        y = tempY - max(ycoords)
    else:
        y = tempY - min(ycoords)

    return [x, y]


# buildings
# [color, coordinates, outline thickness (optional)]
buildingsBack = [
    [(200, 200, 210), rectBoundsGen(25, yb - 70, 32, 70)],
    [BEIGE, rectBoundsGen(100, yb - 100, 57, 100)],
    [MGRAY, rectBoundsGen(165, yb - 120, 70, 120)],
    [
        LGRAY,
        (
            (250, yb - 230),
            (300, yb - 220),
            (333, yb - 200),
            (333, yb),
            (250, yb),
        ),
    ],
    [MGRAY, rectBoundsGen(350, yb - 150, 71, 150)],
    [LGRAY, rectBoundsGen(450, yb - 200, 58, 200)],
    [(220, 140, 100), rectBoundsGen(560, yb - 140, 70, 140)],
    [BEIGE, rectBoundsGen(650, yb - 50, 45, 50)],
    [MGRAY, rectBoundsGen(710, yb - 80, 58, 80)],
]

buildingsFront = [
    [
        (250, 250, 240),
        (
            (130, yb - 39),
            (170, yb - 39),
            (170, yb - 30),
            (202, yb - 30),
            (202, yb),
            (130, yb),
        ),
    ],
    [BEIGE, ((230, yb - 50), (270, yb - 50), (288, yb - 40), (288, yb), (230, yb))],
    [
        (220, 140, 100),
        ((310, yb - 90), (382, yb - 120), (382, yb), (310, yb)),
    ],
    [BEIGE, rectBoundsGen(500, yb - 100, 45, 100)],
]


def city():
    # 남산타워
    drawRect(WHITE, (WIDTH // 2, yb - 180 - 80, 10, 80))
    drawRect(LGRAY, (WIDTH // 2 - 10, yb - 180 - 100, 30, 20))
    drawRect(LGRAY, (WIDTH // 2 - 5, yb - 180 - 115, 20, 15))
    drawRect(WHITE, (WIDTH // 2 + 3, yb - 180 - 145, 4, 30))

    # mountain
    drawPoly(
        GREEN,
        (
            (0, yb),
            (70, yb - 50),
            (WIDTH // 3, yb - 100),
            (WIDTH // 2, yb - 200),
            (WIDTH // 2 + 100, yb - 180),
            (WIDTH - 70, yb - 50),
            (WIDTH, yb),
        ),
    )

    global riverColor

    for building in buildingsBack + buildingsFront:
        windowColor = []

        if skyState == 3:  # night
            riverColor = [40, 70, 100]
            shadowAlpha = 20

            temp = []
            for x in building[0]:
                temp.append(x - 50)

            drawPoly(temp, building[1])
            windowColor = [235, 235, 180]
        else:
            riverColor = [90, 120, 150]

            drawPoly(building[0], building[1])

            for i in range(3):
                color = max(building[0][i] - 50, 0)
                windowColor.append(color)

        wBounds = windowBoundsGen(building[1])
        xOffset = building[1][-1][0]

        # window bounds calc & drawing
        for y in range(rh, wBounds[1] - 5, wh + wp):
            for x in range(5, wBounds[0] - 5, ww + wp):
                drawRect(windowColor, (xOffset + x, yb - y, ww, wh))

    # boat
    # road
    drawRect(DGRAY, (0, yb, WIDTH, rh))


def river():
    drawRect(riverColor, (0, yb + rh, WIDTH, HEIGHT))


def shadows():
    if skyState == 3:
        return 0

    offset = ((step % (cycleTotal / 2)) / (cycleTotal / 2)) * 100 - 50
    for x in buildingsBack:
        coords = list(x[1])
        # print(coords)
        for i in range(len(coords) - 2):
            temp = list(coords[i])
            # print((math.cos(angle % math.pi)))
            h = (yb - temp[1]) - 40
            coords[i] = [
                temp[0] + math.cos(angle % (math.pi)) * h,
                (yb + h),
            ]

        pygame.draw.polygon(shadowSurf, (0, 0, 0, shadowAlpha), coords, 0)

    for x in buildingsFront:
        coords = list(x[1])
        for i in range(len(coords)):
            temp = list(coords[i])
            h = (yb - temp[1]) * 0.8
            coords[i] = [temp[0] + math.cos(angle % (math.pi)) * h, (yb + h)]

        pygame.draw.polygon(shadowSurf, (0, 0, 0, shadowAlpha), coords, 0)


def clouds():
    for i in range(len(cloudX)):
        cloudX[i] += 0.2
        if cloudX[i] > WIDTH + 50:  # add 50 to account for radii
            cloudX[i] = -100  # make sure cloud first generates off screen

    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[0], 100), 20)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[0] + 30, 90), 30)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[0] + 50, 95), 25)

    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[1], 120), 30)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[1] + 40, 110), 40)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[1] + 80, 115), 25)

    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[2], 105), 30)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[2] + 30, 100), 40)
    pygame.draw.circle(shadowSurf, cloudColor, (cloudX[2] + 65, 105), 25)


clock = pygame.time.Clock()

while True:
    step += 1

    pygame.event.clear()
    DISPLAYSURF.fill(WHITE)
    shadowSurf.fill((0, 0, 0, 0))

    angle += angleIncrement
    sky()
    celestialObject()
    clouds()
    city()
    river()
    shadows()

    # necessary for opacity
    DISPLAYSURF.blit(shadowSurf, (0, 0))
    pygame.display.flip()

    # frames
    pygame.display.update()
    # pygame.time.delay(10)
    # use built in function over manual time delays
    clock.tick(120)  # 120 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
