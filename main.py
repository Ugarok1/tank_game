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
keyShoot = pygame.K_SPACE

keyQuit = pygame.K_q
keyPause = pygame.K_p

KEYS = {"singular": set(keyShoot, keyQuit, keyPause),
        "continious": set(keyMoveLeft, keyMoveUp, keyMoveDown, keyMoveRight)
        }
keys = set()

# Directions
N = 0
E = 1
S = 2
W = 3


BULLET_SPEED = 10
BULLET_SIZE = 3

########################
# template for objects #
########################
# If, for ex. movement is None, then object can't be moved
Object = {
        "type": None,  # Type of object
        "name": "",  # Name of object for debug
        "position": None,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "movement": None,  # Will contain seed, that will determine
                           # how object will move
        "logic": None,  # Will contain pointer to function
                        # how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": [],  # List of bonuses affecting object
        "team": 0  # If obj frendly(1), hostile(2) or neutral(0), bonus(3)
        }

Turret = {
        "reload": None,  # Time between succesive shoots
        "timeout": 0,  # Countdown from the last shot
        }

Position = {
        "rect": pygame.Rectangle(),
        "direction": 0,
        "sprite": None,  # init
        "size": None,  # init int size of square
        }

Lives = {
        "hp": None,
        "max_hp": None,  # init
        "lives": None,  # init, number of respawns,
                        # TODO: decide starts with 0 or 1
        }

Movement = {
        "speed": 0,  # Current speed in direction of object, may be negative
        "max_speed": None,  # init
        }


# N. Beliy s2604210
def new_bullet(obj):
    """
    Create a new bullet object in the direction of shooter
    Bullet is created just outside of shooter box.

    To avoid collision with shooter, bullet must be moved
    after it's creation

    Parameters:
    -----------
        obj: dict
            Shooter object

    Returns:
    --------
        Bullet object
    """
    bullet = {}
    bullet["type"] = "bullet"
    bullet["name"] = obj["name"] + "_bullet"
    # fix position
    obj_pos = obj["position"]
    if obj_pos["direction"] == N:
        point = obj_pos["rect"].midtop
        point = (point[0] - 0.5 * BULLET_SIZE,
                 point[1] - BULLET_SIZE)
    elif obj_pos["direction"] == E:
        point = obj_pos["rect"].midright
        point = (point[0],
                 point[1] - 0.5 * BULLET_SIZE)
    elif obj_pos["direction"] == S:
        point = obj_pos["rect"].midright
        point = (point[0] - 0.5 * BULLET_SIZE,
                 point[1])
    elif obj_pos["direction"] == W:
        point = obj_pos["rect"].midright
        point = (point[0] - BULLET_SIZE,
                 point[1] - 0.5 * BULLET_SIZE)
    else:
        raise Exception("[{}] Invalid direction: {}"
                        .format(obj["name"], obj_pos["direction"]))

    bullet["position"] = {
            "rect": pygame.Rect((point), (BULLET_SIZE, BULLET_SIZE)),
            "direction": obj_pos["direction"],
            "sprite": "images/bullet.png",
            "size": BULLET_SIZE
            }

    bullet["health"] = {"hp": 1, "max_hp": 1, "lives": 0}
    bullet["movement"] = {"seed": BULLET_SPEED,
                          "max_speed": BULLET_SPEED}
    bullet["logic"] = None
    bullet["turret"] = None,
    bullet["bonuses"] = []
    bullet["team"] = obj["team"]  # TODO: Decide on friendly fire
    return bullet

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


def moveObject(obj):
    """
    Detect if object can move in given direction, then if possible move it
    """
    pass

# N. Beliy s2604210
def shoot(obj):
    """
    Checks if object can shoot (has turret and not reloading)
    and create a new bullet.

    Created bullet is moved immediatly and returned.

    Parameters:
    -----------
        obj: Object
            shooter

    Returns:
    --------
        Bullet or None
    """
    if obj["turret"] is None or obj["turret"]["timeout"] > 0:
        # Object can't shoot
        return None

    obj["turret"]["timeout"] = obj["turret"]["reload"]
    bullet = new_bullet(obj)

    # TODO: Adding to the list during iteration may cause problems
    # TODO: Avoid double move
    moveObject(bullet)
    return bullet

# N. Beliy s2604210
def parseKeys(events):
    """
    Detect pressed keys and put seleted ones in the global keys
    For continious keys, it also detect unpressing of key.

    Parameters:
    -----------
        events: list
            List of events of pygame
    """
    for event in events:
        if event.type == pygame.QUIT:
            keys.add(keyQuit)
        elif event.type == pygame.KEYDOWN:
            if event.key in KEYS["singular"] or event.key in KEYS["continious"]:
                keys.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in KEYS["continious"]:
                keys.discard(event.key)

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
