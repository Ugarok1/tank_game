#!/usr/bin/env python3

import pygame
import random
import time

backgroundColor = (0, 191, 200)

windowSize = (1200, 900)

keyMoveRight = pygame.K_RIGHT
keyMoveLeft = pygame.K_LEFT
keyMoveUp = pygame.K_UP
keyMoveDown = pygame.K_DOWN
keySpace = pygame.K_SPACE

###############
# BASE VALUES #
###############
baseTankSpeed = 4
baseBulletSpeed = 14
baseBulletScale = (4, 2)
baseSize = 6

################
# TANK OBJECTS #
################
mainTank = {
    "position": (windowSize[0] / 2, windowSize[1] - 150),
    "sprite": "images/main_tank.png",
    "direction": 0,
    "health": 3,
    "speed": baseTankSpeed * 20,
    "size": baseSize,
    "scale": (12, 10),
    "exist": True,
}

enemyTank1 = {
    "position": [windowSize[0] / 2 - 50, 70],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "health": 5,
    "speed": baseTankSpeed / 3,
    "size": baseSize * 1.5,
    "scale": (12, 10),
    "collide": 4,
    "exist": True,
}
enemyTank2 = {
    "position": [windowSize[0] / 2, 20],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "health": 3,
    "speed": baseTankSpeed / 1.7,
    "size": baseSize,
    "scale": (12, 10),
    "exist": True,
}
enemyTank3 = {
    "position": [windowSize[0] / 2 + 50, 20],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "health": 1,
    "speed": baseTankSpeed * 1.1,
    "size": baseSize / 1.5,
    "scale": (12, 10),
    "exist": True,
}
# array of objects
# obstacle object have values similar to rectangle values, meaning ((x, y), (sizeX, sizeY))
obstacles = [
    ((windowSize[0] / 5, windowSize[1] * 2 / 3), (windowSize[0] * 3 / 5, 90)),
    (
        (windowSize[0] / 10, windowSize[1] / 10),
        (windowSize[0] / 10, windowSize[1] / 10),
    ),
    (
        (windowSize[0] - 2 * windowSize[0] / 10, windowSize[1] / 10),
        (windowSize[0] / 10, windowSize[1] / 10),
    ),
]


#####################
# UTILITY FUNCTIONS #
#####################


# return scalled object size for object direction
def getSize(object):
    objectSize = (
        object["scale"][0] * object["size"],
        object["scale"][1] * object["size"],
    )
    if object["direction"] == 0 or object["direction"] == 2:
        objectSize = (
            object["scale"][1] * object["size"],
            object["scale"][0] * object["size"],
        )
    return objectSize


# return true if object pass border on newPosition and change object position to nearest to border
def checkBorder(object, newPosition):
    objectScalledSize = getSize(object)
    if newPosition[0] + objectScalledSize[0] > windowSize[0]:
        object["position"] = (
            windowSize[0] - objectScalledSize[0],
            object["position"][1],
        )
        return True
    if newPosition[0] < 0:
        object["position"] = (0, object["position"][1])
        return True
    if newPosition[1] < 0:
        object["position"] = (object["position"][0], 0)
        return True
    if newPosition[1] + objectScalledSize[1] > windowSize[1]:
        object["position"] = (
            object["position"][0],
            windowSize[1] - objectScalledSize[1],
        )
        return True


# return true if object have collision with array of objects "obstacles"
def checkCollision(object, newPosition):
    objectScalledSize = getSize(object)
    objectRect = (newPosition, objectScalledSize)
    answer = False
    for obstacle in obstacles:
        answer = pygame.Rect(objectRect).colliderect(pygame.Rect(obstacle))
        if answer:
            return True
    return answer


def drawObstacles(window):
    for obstacle in obstacles:
        pygame.draw.rect(window, (0, 0, 0), obstacle)


# change object position to new
# if new object possition collide or pass border - do nothing
def changeObjectPosition(object, newPosition):
    collision = checkCollision(object, newPosition)
    passBorder = checkBorder(object, newPosition)
    if collision or passBorder:
        return
    object["position"] = newPosition


######################
# BULLET LOGIC BLOCK #
######################
bullets = []


def shootBullet(object):
    # get direction of object and set same direction to bullet
    objectDirecton = object["direction"]
    # objectSize only for calculating right position
    objectSize = getSize(object)
    bulletSize = object["size"]
    # bulletScalledSize only for calculating right position
    if objectDirecton == 1 or objectDirecton == 3:
        bulletScalledSize = (
            bulletSize * baseBulletScale[0],
            bulletSize * baseBulletScale[1],
        )
    else:
        bulletScalledSize = (
            bulletSize * baseBulletScale[1],
            bulletSize * baseBulletScale[0],
        )

    # propositional block for setting right position to bullet
    if objectDirecton == 0:
        bulletPosition = (
            object["position"][0] + objectSize[0] / 2 - bulletScalledSize[0] / 2,
            object["position"][1] - bulletScalledSize[1],
        )
    elif objectDirecton == 1:
        bulletPosition = (
            object["position"][0] - bulletScalledSize[0],
            object["position"][1] + objectSize[1] / 2 - bulletScalledSize[1] / 2,
        )
    elif objectDirecton == 2:
        bulletPosition = (
            object["position"][0] + objectSize[0] / 2 - bulletScalledSize[0] / 2,
            object["position"][1] + objectSize[1] + bulletScalledSize[1],
        )
    else:
        bulletPosition = (
            object["position"][0] + objectSize[0] + bulletScalledSize[0],
            object["position"][1] + objectSize[1] / 2 - bulletScalledSize[1] / 2,
        )
    # create bullet speed
    bulletSpeed = (0, 0)
    if objectDirecton == 0:
        bulletSpeed = (0, -baseBulletSpeed)
    if objectDirecton == 1:
        bulletSpeed = (-baseBulletSpeed, 0)
    if objectDirecton == 2:
        bulletSpeed = (0, baseBulletSpeed)
    if objectDirecton == 3:
        bulletSpeed = (baseBulletSpeed, 0)

    # declaration of bullet object
    bullet = {
        "direction": objectDirecton,
        "position": bulletPosition,
        "speed": bulletSpeed,
        "size": bulletSize,
        "scale": baseBulletScale,
    }
    # append bullet object to array
    bullets.append(bullet)


# move bullet with it's speed
# return False if collide with obstacle or pass border, and explode bullet
# return True if moved bullet
def moveBullet(bullet, window):
    newBulletPosition = (
        bullet["position"][0] + bullet["speed"][0],
        bullet["position"][1] + bullet["speed"][1],
    )
    collision = checkCollision(bullet, newBulletPosition)
    passBorder = checkBorder(bullet, newBulletPosition)
    if collision or passBorder:
        bulletExplode(bullet, time.time(), window)
        return False
    bullet["position"] = newBulletPosition
    return True


def drawBullet(bullet, window):
    image = pygame.image.load("images/bullet.png").convert_alpha(window)
    object_size = getSize(bullet)
    image = pygame.transform.rotate(image, 90 * bullet["direction"])
    image = pygame.transform.scale(image, object_size)
    window.blit(image, bullet["position"])


# add to main loop
def animateBullets(window):
    for bullet in bullets:
        scalledBulletSize = getSize(bullet)
        rectValues = (bullet["position"], scalledBulletSize)
        pygame.draw.rect(window, backgroundColor, rectValues)
        canMove = moveBullet(bullet, window)
        if canMove:
            drawBullet(bullet, window)


###################
# EXPLOSION LOGIC #
###################
explosions = []
explosionRadius = 11
explosionColor = (255, 127, 0)


# create explosion object for parent bullet object
# and delete bullet from canvas and bullets array
def bulletExplode(bullet, currentTime, window):
    bullets.remove(bullet)
    scalledBulletSize = getSize(bullet)
    rectValues = (bullet["position"], scalledBulletSize)
    pygame.draw.rect(window, backgroundColor, rectValues)
    explosionPosition = (
        bullet["position"][0] + scalledBulletSize[0] / 2 + bullet["speed"][0],
        bullet["position"][1] + scalledBulletSize[1] / 2 + bullet["speed"][1],
    )
    explosionTime = currentTime
    explosion = {"position": explosionPosition, "time": explosionTime}
    explosions.append(explosion)


def animateExplosion(explosion, window):
    explosionTime = explosion["time"]
    if explosionTime + 3 <= time.time():
        explosions.remove(explosion)
        pygame.draw.circle(
            window, backgroundColor, explosion["position"], explosionRadius
        )
        return
    pygame.draw.circle(window, explosionColor, explosion["position"], explosionRadius)


# add in main loop
def animateExplosions(window):
    for explosion in explosions:
        animateExplosion(explosion, window)


#######################
# TANK MOVEMENT BLOCK #
#######################
def drawTank(object, window):
    image = pygame.image.load(object["sprite"]).convert_alpha(window)
    object_size = getSize(object)
    image = pygame.transform.rotate(image, 90 * object["direction"])
    image = pygame.transform.scale(image, object_size)
    window.blit(image, object["position"])


def moveTankUp(object, window):
    oldTankSize = getSize(object)
    object["direction"] = 0
    rectValues = (object["position"], oldTankSize)
    pygame.draw.rect(window, backgroundColor, rectValues)
    changeObjectPosition(
        object,
        (
            object["position"][0],
            object["position"][1] - object["speed"],
        ),
    )
    drawTank(object, window)


def moveTankDown(object, window):
    oldTankSize = getSize(object)
    object["direction"] = 2
    rectValues = (object["position"], oldTankSize)
    pygame.draw.rect(window, backgroundColor, rectValues)
    changeObjectPosition(
        object,
        (
            object["position"][0],
            object["position"][1] + object["speed"],
        ),
    )
    drawTank(object, window)


def moveTankRight(object, window):
    oldTankSize = getSize(object)
    object["direction"] = 3
    rectValues = (object["position"], oldTankSize)
    pygame.draw.rect(window, backgroundColor, rectValues)
    changeObjectPosition(
        object,
        (
            object["position"][0] + object["speed"],
            object["position"][1],
        ),
    )
    drawTank(object, window)


def moveTankLeft(object, window):
    oldTankSize = getSize(object)
    object["direction"] = 1
    rectValues = (object["position"], oldTankSize)
    pygame.draw.rect(window, backgroundColor, rectValues)
    changeObjectPosition(
        object,
        (
            object["position"][0] - object["speed"],
            object["position"][1],
        ),
    )
    drawTank(object, window)


###############
# ENEMY LOGIC #
###############
def tryMoveRight(object, window):
    newPosition = (object["position"][0] + object["speed"], object["position"][1])
    collision = checkCollision(object, newPosition)
    if collision:
        object["collide"] = object["direction"]
    else:
        moveTankRight(object, window)


def tryMoveLeft(object, window):
    newPosition = (object["position"][0] - object["speed"], object["position"][1])
    collision = checkCollision(object, newPosition)
    if collision:
        object["collide"] = object["direction"]
    else:
        moveTankLeft(object, window)


def tryMoveUp(object, window):
    newPosition = (object["position"][0], object["position"][1] - object["speed"])
    collision = checkCollision(object, newPosition)
    if collision:
        object["collide"] = object["direction"]
    else:
        moveTankUp(object, window)


def tryMoveDown(object, window):
    newPosition = (object["position"][0], object["position"][1] + object["speed"])
    collision = checkCollision(object, newPosition)
    if collision:
        object["collide"] = object["direction"]
    else:
        moveTankDown(object, window)


def startTank1AI(window):
    tank1Position = enemyTank1["position"]
    mainTankPosition = mainTank["position"]
    collisionSide = enemyTank1["collide"]
    if collisionSide == 4:
        difference = (
            mainTankPosition[0] - tank1Position[0],
            mainTankPosition[1] - tank1Position[1],
        )
        if abs(difference[0]) >= abs(difference[1]):
            if difference[0] > 0:
                tryMoveRight(enemyTank1, window)
            else:
                tryMoveLeft(enemyTank1, window)
        else:
            if difference[1] > 0:
                tryMoveDown(enemyTank1, window)
            else:
                tryMoveUp(enemyTank1, window)
    else:
        if collisionSide == 0:
            tryMoveLeft(enemyTank1, window)
            newPosition = (tank1Position[0], tank1Position[1] - enemyTank1["speed"])
            collision = checkCollision(enemyTank1, newPosition)
            if not collision:
                tryMoveUp(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 1:
            tryMoveDown(enemyTank1, window)
            newPosition = (tank1Position[0] - enemyTank1["speed"], tank1Position[1])
            collision = checkCollision(enemyTank1, newPosition)
            if not collision:
                tryMoveLeft(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 2:
            tryMoveRight(enemyTank1, window)
            newPosition = (tank1Position[0], tank1Position[1] + enemyTank1["speed"])
            collision = checkCollision(enemyTank1, newPosition)
            if not collision:
                tryMoveDown(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 3:
            tryMoveUp(enemyTank1, window)
            newPosition = (tank1Position[0] + enemyTank1["speed"], tank1Position[1])
            collision = checkCollision(enemyTank1, newPosition)
            if not collision:
                tryMoveRight(enemyTank1, window)
                enemyTank1["collide"] = 4


####################
# START GAME BLOCK #
####################

pygame.init()
pygame.key.set_repeat(200, 25)

mainWindow = pygame.display.set_mode(windowSize)

mainWindow.fill(backgroundColor)

time1 = pygame.time.Clock()

end = False

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        elif event.type == pygame.KEYDOWN:
            if event.key == keyMoveDown:
                moveTankDown(mainTank, mainWindow)
            if event.key == keyMoveUp:
                moveTankUp(mainTank, mainWindow)
            if event.key == keyMoveRight:
                moveTankRight(mainTank, mainWindow)
            if event.key == keyMoveLeft:
                moveTankLeft(mainTank, mainWindow)
            if event.key == keySpace:
                shootBullet(mainTank)
    animateExplosions(mainWindow)
    animateBullets(mainWindow)
    startTank1AI(mainWindow)
    drawObstacles(mainWindow)
    pygame.display.flip()
    time1.tick(60)

pygame.display.quit()
pygame.quit()
