#!/usr/bin/env python3
# help

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

###########
# OBJECTS #
###########
def createBaseObject(name):
    object = {name: }
    return

mainTank = {
    "position": (windowSize[0] / 2, windowSize[1] - 150),
    "oldPosition": (windowSize[0] / 2, windowSize[1] - 150),
    "sprite": "images/main_tank.png",
    "direction": 0,
    "oldDirection": 0,
    "health": 3,
    "speed": baseTankSpeed * 5,
    "size": baseSize,
    "scale": (12, 10),
    "exist": True,
}

enemyTank1 = {
    "position": [windowSize[0] / 2 - 50, 70],
    "oldPosition": [windowSize[0] / 2 - 50, 70],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "oldDirection": 0,
    "health": 5,
    "speed": baseTankSpeed / 3,
    "size": baseSize * 1.5,
    "scale": (12, 10),
    "collide": 4,
    "exist": True,
}
enemyTank2 = {
    "position": [windowSize[0] / 2, 20],
    "oldPosition": [windowSize[0] / 2, 20],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "oldDirection": 0,
    "health": 3,
    "speed": baseTankSpeed / 1.7,
    "size": baseSize,
    "scale": (12, 10),
    "exist": True,
}
enemyTank3 = {
    "position": [windowSize[0] / 2 + 50, 20],
    "oldPosition": [windowSize[0] / 2 + 50, 20],
    "sprite": "images/enemy_tank.png",
    "direction": 0,
    "oldDirection": 0,
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


# get scalled object size, but with specific direction
def getSizeDirection(direction, object):
    objectSize = (
        object["scale"][0] * object["size"],
        object["scale"][1] * object["size"],
    )
    if direction == 0 or direction == 2:
        objectSize = (
            object["scale"][1] * object["size"],
            object["scale"][0] * object["size"],
        )
    return objectSize


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


# return true if object pass border and direction where met border. Else return false
def checkBorder(object, newPosition):
    objectScalledSize = getSize(object)
    if newPosition[0] + objectScalledSize[0] > windowSize[0]:
        return True, 3
    elif newPosition[0] < 0:
        return True, 1
    elif newPosition[1] + objectScalledSize[1] > windowSize[1]:
        return True, 2
    elif newPosition[1] < 0:
        return True, 0
    else:
        return False, 0


# return true, obstacle and direction of collision if object have collision with array []obstacles
# newPosition shouldn't been changed for horizontal and verical axes at the same time
def checkCollision(object, newPosition):
    objectScalledSize = getSize(object)
    posDifference = (
        object["position"][0] - newPosition[0],
        object["position"][1] - newPosition[1],
    )
    objectRect = (newPosition, objectScalledSize)
    collide = False
    for obstacle in obstacles:
        collide = pygame.Rect(objectRect).colliderect(pygame.Rect(obstacle))
        if collide:
            collisionPosition = (0, 0)
            if posDifference[0] < 0:
                collisionPosition = (
                    obstacle[0][0] - objectScalledSize[0],
                    object["position"][1],
                )
            if posDifference[0] > 0:
                collisionPosition = (
                    obstacle[0][0] + obstacle[1][0],
                    object["position"][1],
                )
            if posDifference[1] < 0:
                collisionPosition = (
                    object["position"][0],
                    obstacle[0][1] - objectScalledSize[1],
                )
            if posDifference[1] > 0:
                collisionPosition = (
                    object["position"][0],
                    obstacle[0][1] + obstacle[1][1],
                )
            return True, obstacle, collisionPosition
    return collide, 0, 0


# draw obstacles defined in []obstacles array
def drawObstacles(window):
    for obstacle in obstacles:
        pygame.draw.rect(window, (0, 0, 0), obstacle)


# change object position to new
# if new object possition collide or pass border - change position to closest to border or obstacle
def changeObjectPosition(object, newPosition):
    objectScalledSize = getSize(object)
    collision, _, collisionPosition = checkCollision(object, newPosition)
    passBorder, border = checkBorder(object, newPosition)
    if passBorder:
        match border:
            case 0:
                object["position"] = (object["position"][0], 0)
            case 1:
                object["position"] = (0, object["position"][1])
            case 2:
                object["position"] = (
                    object["position"][0],
                    windowSize[1] - objectScalledSize[1],
                )
            case 3:
                object["position"] = (
                    windowSize - objectScalledSize[0],
                    object["position"][1],
                )
        return

    if collision:
        object["position"] = collisionPosition
        return

    object["position"] = newPosition


# draw object on position, takes care about direction and scaling
def drawObject(object, window):
    imagePath = object["sprite"]
    image = pygame.image.load(imagePath).convert_alpha(window)
    object_size = getSize(object)
    image = pygame.transform.rotate(image, 90 * object["direction"])
    image = pygame.transform.scale(image, object_size)
    window.blit(image, object["position"])


######################
# BULLET LOGIC BLOCK #
######################
bullets = []


# draw bullet
# only difference with drawObject is sprite source
def drawBullet(object, window):
    imagePath = "images/bullet.png"
    image = pygame.image.load(imagePath).convert_alpha(window)
    object_size = getSize(object)
    image = pygame.transform.rotate(image, 90 * object["direction"])
    image = pygame.transform.scale(image, object_size)
    window.blit(image, object["position"])


# create new object bullet with position depending on parent tank position
# append new bullet to []bullets array
def shootBullet(object):
    # get direction of object and set same direction to bullet
    objectDirecton = object["direction"]
    # objectSize only for calculating right position
    objectScalledSize = getSize(object)
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
            object["position"][0] + objectScalledSize[0] / 2 - bulletScalledSize[0] / 2,
            object["position"][1] - bulletScalledSize[1],
        )
    elif objectDirecton == 1:
        bulletPosition = (
            object["position"][0] - bulletScalledSize[0],
            object["position"][1] + objectScalledSize[1] / 2 - bulletScalledSize[1] / 2,
        )
    elif objectDirecton == 2:
        bulletPosition = (
            object["position"][0] + objectScalledSize[0] / 2 - bulletScalledSize[0] / 2,
            object["position"][1] + objectScalledSize[1] + bulletScalledSize[1],
        )
    else:
        bulletPosition = (
            object["position"][0] + objectScalledSize[0] + bulletScalledSize[0],
            object["position"][1] + objectScalledSize[1] / 2 - bulletScalledSize[1] / 2,
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
    collision, _, _ = checkCollision(bullet, newBulletPosition)
    passBorder, _ = checkBorder(bullet, newBulletPosition)

    # WORK IF HAVE TIME
    # if passBorder:
    #     match border:
    #         case 0:
    #             bullet["position"] = (bullet["position"][0], 0)
    #         case 1:
    #             bullet["position"] = (0, bullet["position"][1])
    #         case 2:
    #             bullet["position"] = (bullet["position"][0], windowSize[1]-objectScalledSize[1])
    #         case 3:
    #             bullet["position"] = (windowSize - objectScalledSize[0], bullet["position"][1])
    #     return
    #
    # if collision:
    #     object["position"] = collisionPosition
    #     return

    if collision or passBorder:
        bulletExplode(bullet, time.time(), window)
        return False
    bullet["position"] = newBulletPosition
    return True


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
# and delete bullet from canvas and []bullets array
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


# if exposioin was create less then 3 seconds before: do nothing
# else: delete explosion object from canvas and []explosions array
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
def moveTankUp(object, window):
    object["oldDirection"] = object["direction"]
    object["direction"] = 0
    changeObjectPosition(
        object,
        (
            object["position"][0],
            object["position"][1] - object["speed"],
        ),
    )


def moveTankDown(object, window):
    object["oldDirection"] = object["direction"]
    object["direction"] = 2
    changeObjectPosition(
        object,
        (
            object["position"][0],
            object["position"][1] + object["speed"],
        ),
    )


def moveTankRight(object, window):
    object["oldDirection"] = object["direction"]
    object["direction"] = 3
    changeObjectPosition(
        object,
        (
            object["position"][0] + object["speed"],
            object["position"][1],
        ),
    )


def moveTankLeft(object, window):
    object["oldDirection"] = object["direction"]
    object["direction"] = 1
    changeObjectPosition(
        object,
        (
            object["position"][0] - object["speed"],
            object["position"][1],
        ),
    )


# add to main loop
# render tank to canvas
def animateTank(object, window):
    oldTankDirection = object["oldDirection"]

    oldTankPosition = object["oldPosition"]
    oldTankScalledSize = getSizeDirection(oldTankDirection, object)

    rectValues = (oldTankPosition, oldTankScalledSize)

    pygame.draw.rect(window, backgroundColor, rectValues)
    drawObject(object, window)
    object["oldPosition"] = object["position"]


###############
# ENEMY LOGIC #
###############
# check collision for object with selected direction and new position
# return true if collision, else false
def checkCollisionDirection(direction, object, newPosition):
    objectScalledSize = getSizeDirection(direction, object)
    objectRect = (newPosition, objectScalledSize)
    answer = False
    for obstacle in obstacles:
        answer = pygame.Rect(objectRect).colliderect(pygame.Rect(obstacle))
        if answer:
            return True
    return answer


# for each tryMove:
# set newPosition based on object coords and object speed
# if newPositoin collide with []obstacles: save collision directoin to object
# else: move tank
def tryMoveRight(object, window):
    newPosition = (object["position"][0] + object["speed"], object["position"][1])
    collision = checkCollisionDirection(3, object, newPosition)
    if collision:
        object["collide"] = 3
    else:
        moveTankRight(object, window)


def tryMoveLeft(object, window):
    newPosition = (object["position"][0] - object["speed"], object["position"][1])
    collision = checkCollisionDirection(1, object, newPosition)
    if collision:
        object["collide"] = 1
    else:
        moveTankLeft(object, window)


def tryMoveUp(object, window):
    newPosition = (object["position"][0], object["position"][1] - object["speed"])
    collision = checkCollisionDirection(0, object, newPosition)
    if collision:
        object["collide"] = 0
    else:
        moveTankUp(object, window)


def tryMoveDown(object, window):
    newPosition = (object["position"][0], object["position"][1] + object["speed"])
    collision = checkCollisionDirection(2, object, newPosition)
    if collision:
        object["collide"] = 2
    else:
        moveTankDown(object, window)


# move tank1 most effectively to mainTank
# on collision with obstacle try to get around that obstacle (always by left)
# for more precise comprehension - read the function
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
            collision = checkCollisionDirection(collisionSide, enemyTank1, newPosition)
            if not collision:
                tryMoveUp(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 1:
            tryMoveDown(enemyTank1, window)
            newPosition = (tank1Position[0] - enemyTank1["speed"], tank1Position[1])
            collision = checkCollisionDirection(collisionSide, enemyTank1, newPosition)
            if not collision:
                tryMoveLeft(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 2:
            tryMoveRight(enemyTank1, window)
            newPosition = (tank1Position[0], tank1Position[1] + enemyTank1["speed"])
            collision = checkCollisionDirection(collisionSide, enemyTank1, newPosition)
            if not collision:
                tryMoveDown(enemyTank1, window)
                enemyTank1["collide"] = 4
        if collisionSide == 3:
            tryMoveUp(enemyTank1, window)
            newPosition = (tank1Position[0] + enemyTank1["speed"], tank1Position[1])
            collision = checkCollisionDirection(collisionSide, enemyTank1, newPosition)
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
    animateTank(enemyTank1, mainWindow)
    animateTank(mainTank, mainWindow)
    startTank1AI(mainWindow)
    drawObstacles(mainWindow)
    pygame.display.flip()
    time1.tick(30)

pygame.display.quit()
pygame.quit()
