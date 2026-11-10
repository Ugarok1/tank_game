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

########################
# template for objects #
########################
# If, for ex. movement is None, then object can't be moved




Object = {
        "type": None,  # Type of object
        "name": "",  # Name of object for debug
        "position": None,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "movement": None,  # Will contain seed, that will determine how object will move
        "logic": None,  # Will contain pointer to function how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": [],  # List of bonuses affecting object
        "team": 0  # If obj frendly(1), hostile(2) or neutral(0), bonus(3)


        }

Turret = {
        "reload": None,  # Time between succesive shoots
        "timeout": 0,  # Countdown from the last shot
        }

Position = {
        "rect": [[x, y],[width, lenght]],
        "direction": 0,
        "sprite": None,  # init
        "size": None,  # init int size of square
        }

Lives = {
        "hp": None,
        "max_hp": None,  # init
        "lives": None,  # init, number of respawns
        }

Movement = {
        "speed": 0,  # Current speed in direction of object, may be negative
        "max_speed": None,  # init
        }

#########################
# Global object holders #
#########################
objects = []  # List of objects
keys = []  # List/set of pressed keys
bonuses = [] # List of not-activated bonuses

def spawn(obj):
    """
    Put created object into game
    """
    pass

def action(obj):
    """
    Executes object logic if defined, for player-controlled object
    executes action for pressed keys, for AI-controlled, executes the logic

    Essentualy moves and shoots.
    """
    if obj["logic"] is None:
        return
    obj["logic"]()

def test_collision(index, obj):
    """
    Tests if current object collides with any of other objects

    If collision is detected, apply collision logic based of
    nature of colliding objects (ex. bullet with tank)
    """
    pass

def update_coundown(obj):
    """
    Updates all countdowns related to object (for ex. timeout of turrets)
    """
    pass

def draw(obj):
    """
    Redraw current object
    """
    pass

def draw_score():
    """
    Draws user score and other infos
    """
    pass

def clean_objects():
    """
    Removes destroed objects and bonuses from global list
    """
    pass

def init():
    """
    Declaration des objet
    """
    pass

def moveObject(obj, direction):
    """
    Detect if object can move in given direction, then if possible move it
    """
    pass

def shoot(obj):
    """
    Create a bullet in direction of object
    """
    pass

def parseKeys():
    """
    Detect pressed keys
    """

def logicPlayer(obj, keys):
    """
    Move and shoot based on player input
    """
    pass

def logicEnemy(obj):
    """
    Move AI tank based on environment

    Variants:
        random: change direction at random at obstacle
                and after minimum distance
        hunter: Actively following player
        target_shoot: shoot if can hurt player tank
    """
    pass

def spawnBonus():
    """
    Create a new bonus after timeout and if no bonuses of screen
    """
    pass

def hurt(obj, ball):
    """
    Reduce hp of object, destroy ball, create collision explosion
    Check if object is destroyed
    """
    pass

def respawn(obj, pos):
    """
    Recreate destryed object at given position
    """
    pass

#block on the stage (S2601624, Lesquir, Jules)
def create_obstacle(BLOCK_LENGHT, BLOCK_WIDTH, position):
        Position = {
            "rect" : [position, [BLOCK_LENGHT, BLOCK_WIDTH]],
            "direction" : None
            "sprite" : None
            "size" : None

        }
        object = {
        "position": Position,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "movement": None,  # Will contain seed, that will determine how object will move
        "logic": None,  # Will contain pointer to function how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": [],  # List of bonuses affecting object
        "team": 0  # If obj frendly(1), hostile(2) or neutral(0), bonus(3)
        
        }
        return object

#Draw objects based on their "type" (S2601624, Lesquir, Jules)
def draw_for_object(obj):
    if obj["type"] == "obstacle":
        color = (   0,   0,   0)
        pygame.draw.rect(mainWindow, color, obj["position"]["rect"])

    elif obj["type"] == "tank" or obj["type"] =="bullet":
        imagePath = obj["position"]["sprite"]
        image = pygame.image.load(imagePath).convert_alpha(mainWindow)
        image = pygame.transform.rotate(image, 90 * obj["position"]["direction"])
        image = pygame.transform.scale(image, ["position"]["rect"][1])
        mainWindow.blit(image, obj["position"]["rect"][0])

    else:
        imagePath = obj["position"]["sprite"]
        image = pygame.image.load(imagePath).convert_alpha(mainWindow)
        image = pygame.transform.scale(image, ["position"]["rect"][1])
        mainWindow.blit(image, obj["position"]["rect"][0])

#Reduce hp when hit with the bullet
def hurt(obj, ball):
    #si collision, alors -hp (pas détruire) SEULEMENT !!! attention ! python veut pas laisser effacer (traduction : POURQUOI ???)
    hp = hp - 1
    
    #NOT FINISHED YET !!!


####################
# START GAME BLOCK #
####################

pygame.init()
pygame.key.set_repeat(200, 25)

mainWindow = pygame.display.set_mode(windowSize)

mainWindow.fill(backgroundColor)

time1 = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        pass
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
