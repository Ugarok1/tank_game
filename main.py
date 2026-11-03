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
# BASE BALUES #
###############
base_speed = 5
base_size = 5
base_health = 3
bonus_sprite = "image/bonus.png"

########################
# template for objects #
########################
# If, for ex. movement is None, then object can't be moved
Object = {
    "position": None,  # Will contain position dict for drawing object
    "health": None,  # Will containg health and life/respawn info
    "movement": None,  # Will contain seed, that will determine how object will move
    "logic": None,  # Will contain pointer to function how object will behave
    "turrets": [],  # List of turrets associated to object
    "bonuses": [],  # List of bonuses affecting object
    "team": 0,  # If obj frendly, hostile or neutral
}

Turret = {
    "direction": 0,  # Direction w.r.t. object orientation
    "reload": None,  # Time between succesive shoots
    "salvo": 1,  # Number of bullets per shot
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
    "accel": None,  # init
}

#########################
# Global object holders #
#########################
objects = []  # List of objects
keys = []  # List/set of pressed keys
bonuses = []  # List of not-activated bonuses


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


###########
# OBJECTS #
###########
# Autor: Myka
def create_tank(
    basePosition, size, sprite, maxHealth, lives, team, speed, reloadSpeed, logic=None
):
    turret = {
        "direction": 0,
        "reload": reloadSpeed,
        "timeout": 0,  # set at reloadSpeed on shoot, then every second -1 till 0, when 0 can shoot again
    }
    position = {
        "rect": [basePosition, (10, 10)],
        "direction": 0,
        "sprite": sprite,
        "size": size,
    }
    lives = {"hp": maxHealth, "max_hp": maxHealth, "lives": lives}
    mouvement = {"speed": 0, "max_speed": speed}
    object = {
        "position": position,
        "health": lives,
        "mouvement": mouvement,
        "logic": logic,
        "turrets": turret,
        "bonuses": None,
        "team": team,  # team 0 - obstacles, team 1 - player, team 2 enemy, team 3 - bonuses
    }
    return object


def create_bonus(basePosition, size, lifetime):
    position = {
        "rect": [basePosition, (10, 10)],
        "direction": 0,
        "sprite": bonus_sprite,
        "size": size,
    }
    lives = {"hp": lifetime, "max_hp": lifetime, "lives": 1}
    mouvement = {"speed": 0, "max_speed": 0}
    object = {
        "position": position,
        "health": lives,
        "movement": mouvement,
        "logic": None,
        "turrets": [],
        "bonuses": [],
        "team": 3,
    }
    return object


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
