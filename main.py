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
        "rect": Pygame.Rectangle(),
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


def new_bullet(obj):
    bullet = Object.copy()
    bullet["bonuses"] = []
    bullet["type"] = "bullet"
    bullet["movement"] = {"seed": BULLET_SPEED,
                          "max_speed": BULLET_SPEED}
    # fix position
    return bullet

#########################
# Global object holders #
#########################
objects = []  # List of objects
keys = []  # List/set of pressed keys
bonuses = [] # List of not-activated bonuses

# 
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

# myka
def test_collision(index, obj):
    """
    Tests if current object collides with any of other objects

    If collision is detected, apply collision logic based of
    nature of colliding objects (ex. bullet with tank)
    """
    pass

# nikita
def update_coundown(obj):
    """
    Updates all countdowns related to object (for ex. timeout of turrets)
    """
    pass

# lesqu
def draw(obj):
    """
    Redraw current object
    """
    pass

# nikita
def draw_score():
    """
    Draws user score and other infos
    """
    pass

# myka
def clean_objects():
    """
    Removes destroed objects and bonuses from global list
    """
    pass

# myka
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

# meme que create_bullet, nikita
def shoot(obj):
    """
    Create a bullet in direction of object
    """
    pass

# nikita
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

# myka
def spawnBonus():
    """
    Create a new bonus after timeout and if no bonuses of screen
    """
    pass

# lesqu
def hurt(obj, ball):
    """
    Reduce hp of object, destroy ball, create collision explosion
    Check if object is destroyed
    """
    pass

# myka
def respawn(obj, pos):
    """
    Recreate destryed object at given position
    """
    pass


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
