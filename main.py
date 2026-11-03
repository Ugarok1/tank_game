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
        "position": None,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "movement": None,  # Will contain seed, that will determine how object will move
        "logic": None,  # Will contain pointer to function how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": [],  # List of bonuses affecting object
        "team": 0  # If obj frendly, hostile or neutral
        }

Turret = {
        "reload": None,  # Time between succesive shoots
        "timeout": 0,  # Countdown from the last shot
        }

Position = {
        "rect": Pygame.Rectangle(),
        "direction": 0,
        "sprite": None,  # init
        "size": None,  # init
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
