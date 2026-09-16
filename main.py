#!/usr/bin/env python3

import pygame

colorBlue = (0, 191, 200)
colorYellow = (255, 255, 0)

windowSize = (1200, 900)

bulletRadius = 3

windowSize = (windowSize[0], windowSize[1])

pygame.init()

mainWindow = pygame.display.set_mode(windowSize)

mainWindow.fill(colorBlue)

time = pygame.time.Clock()

end = False


# draw a tank on position coords, center of the tank is on position ; position is a array of 2 int numbers
# size take int values and defines the size of drawn tank
def drawTank(position, size):
    square1Width = 20 * size
    square1Height = 20 * size
    square1Color = (255, 255, 255)
    square1Coords = [position[0] - square1Width // 2, position[1] - square1Height // 2]
    pygame.draw.rect(
        mainWindow, square1Color, (square1Coords, (square1Height, square1Width))
    )
    squareLeftWidth = 3 * size
    squareLeftHeight = 20 * size
    squareLeftColor = (0, 0, 0)
    squareLeftCoords = [square1Coords[0] - squareLeftWidth, square1Coords[1]]
    pygame.draw.rect(
        mainWindow,
        squareLeftColor,
        (squareLeftCoords, (squareLeftWidth, squareLeftHeight)),
    )
    squareRightWidth = 3 * size
    squareRightHeight = 20 * size
    squareRightColor = (0, 0, 0)
    squareRightCoords = [position[0] + square1Width // 2, square1Coords[1]]
    pygame.draw.rect(
        mainWindow,
        squareRightColor,
        (squareRightCoords, (squareRightWidth, squareRightHeight)),
    )
    circleRadius = 4 * size
    circleColor = (255, 0, 255)
    pygame.draw.circle(mainWindow, circleColor, position, circleRadius)

    rectGunColor = (255, 0, 0)
    rectGunWidth = 2 * size
    rectGunHeight = 15 * size
    rectGunCoords = [position[0] - rectGunWidth // 2, position[1] - rectGunHeight]
    pygame.draw.rect(
        mainWindow, rectGunColor, (rectGunCoords, (rectGunWidth, rectGunHeight))
    )
    pygame.display.flip()


while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
    drawTank((windowSize[0] // 2, windowSize[1] // 2), 5)


pygame.display.quit()
pygame.quit()
