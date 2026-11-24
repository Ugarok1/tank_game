#!/usr/bin/env python3
# help

import math

import pygame
import random
import time

DEBUG = True

backgroundColor = (0, 191, 200)


# windowSize = (1200, 900)
windowSize = (840, 600)

# Keys
keyMoveRight = pygame.K_RIGHT
keyMoveLeft = pygame.K_LEFT
keyMoveUp = pygame.K_UP
keyMoveDown = pygame.K_DOWN
keyShoot = pygame.K_SPACE
keyQuit = pygame.K_q
keyPause = pygame.K_p

# Directions
N = 0
E = 1
S = 2
W = 3

# Bullets parameters
BULLET_SPEED = 5
BULLET_SIZE = 5

#########################
# Global object holders #
#########################
objects = []  # List of objects
bonuses = []  # List of not-activated bonuses

KEYS = {
    "singular": set([keyShoot, keyQuit, keyPause]),
    "continious": set([keyMoveLeft, keyMoveUp, keyMoveDown, keyMoveRight]),
}
keys = set()

#############
# MOUVEMENT #
#############


# Mykhailo Sutyrin S2601127
# take index and new rectangle. Test collision with all objestc, return bool(True collide ; False not collide) and index of collision
def test_collision(oper_ind, nex_pos):
    """
    Test collision with all objestc

    Parameters:
    ---
        oper_ind - index of object we work with
        new_pos - new rectangle of object

    Returns:
    ---
        bool(True collide ; False not collide)
        index of collided object
    """
    answer = False
    for ind in range(len(objects)):
        if oper_ind != ind:
            rect2 = objects[ind]["position"]["rect"]
            answer = nex_pos.colliderect(rect2)
            if answer:
                return answer, ind
    return answer, None


# N. Beliy s2604210
def moveObject(ind):
    """
    Try to move object at index ind, if movement results in collision
    do appropriate action.

    Parameters:
    -----------
        ind: int
            index of object to move in objects list
    #MAIN_LOOP
    """
    obj = objects[ind]

    if objects[ind] is None:
        return

    if "mouvement" not in obj or obj["mouvement"] is None:
        return

    speed = obj["mouvement"]["speed"]
    pos = obj["position"]["rect"]
    direction = obj["position"]["direction"]

    if speed == 0:
        return

    if obj["name"] == "user_bullet":
        print("Moving {} ({}) by {} pixels in direction {}"
              .format(obj["name"], obj["type"], speed, direction))

    dx = 0
    dy = 0
    if direction == N:
        dy = -speed
    elif direction == S:
        dy = speed
    elif direction == E:
        dx = speed
    elif direction == W:
        dx = -speed
    else:
        print(
            "{}({}): Can't move object -- invalid direction {}".format(
                obj["name"], obj["type"], direction
            )
        )
        return
    new_rect = pos.move(dx, dy)

    collision, index = test_collision(ind, new_rect)
    if collision:
        if obj["name"] == "user_bullet":
            print("{} ({}) collides with {} ({})"
                  .format(obj["name"], obj["type"],
                          objects[index]["name"],
                          objects[index]["type"]))
        new_rect = apply_collide_logic(ind, index, new_rect)

    obj["position"]["rect"] = new_rect
    print(new_rect.topleft)
    print(new_rect.bottomright)


# Mykhailo SUTYRIN S2601127
def apply_collide_logic(oper_index, index, new_rect):
    """
    Apply collision logic to operated object and type of collision.

    Parameters:
    ---
        oper_index - index of operated object
        index - index of object in collision
        new_rect - new rectangle of operated object
    """
    if objects[oper_index] is None:
        return

    operated_object = objects[oper_index]
    object = objects[index]

    oper_rect = operated_object["position"]["rect"]
    rect = object["position"]["rect"]

    operated_type = operated_object["type"]
    operated_team = operated_object["team"]

    type = object["type"]
    team = object["team"]

    # First, move operated_object close to collided object
    dx = 0
    dy = 0
    direction = operated_object["position"]["direction"]
    if direction == N:
        dy = rect.bottom - oper_rect.top
    elif direction == S:
        dy = rect.top - oper_rect.bottom
    elif direction == E:
        dx = rect.left - oper_rect.right
    elif direction == W:
        dx = rect.right - oper_rect.left
    oper_rect = oper_rect.move(dx, dy)

    enemy = True
    if operated_team == 0 or team == 0:
        enemy = False

    if operated_team == team:
        # No frendly fire
        enemy = False

    if operated_type == "tank" and enemy:
        print("Hurting operated tank")
        hurt(1, operated_object)

    if type == "tank" and enemy:
        print("Hurting static tank")
        hurt(1, object)

    if operated_type == "bullet" or operated_type == "bonus":
        hurt(1, operated_object)
        print("Removing bullet")

    if type == "bullet" or type == "bonus":
        hurt(1, object)

    return oper_rect


#################
# CREATE OBJECT #
#################


# Lesquir Jules s2601624
# create obstacles (block,...) on the stage
def create_obstacle(BLOCK_LENGHT, BLOCK_WIDTH, sprite, position):
    if sprite is not None:
        sprite = pygame.image.load(sprite)
        sprite = pygame.transform.scale(sprite, (BLOCK_LENGHT, BLOCK_WIDTH))
    Position = {
        "rect": pygame.Rect(position, [BLOCK_LENGHT, BLOCK_WIDTH]),
        "direction": None,
        "sprite": sprite,
        "size": (BLOCK_LENGHT, BLOCK_WIDTH),
    }
    object = {
        "position": Position,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "mouvement": None,  # Will contain seed, that will determine how object will move
        "logic": None,  # Will contain pointer to function how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": None,  # List of bonuses affecting object
        "team": 0,  # If obj frendly(1), hostile(2) or neutral(0), bonus(3)
        "type": "obstacle",
        "name": ""
    }
    return object


# N. Beliy s2604210
def create_bullet(obj):
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
        point = (obj_pos["rect"].centerx - int(BULLET_SIZE / 2),
                 obj_pos["rect"].top - BULLET_SIZE)
    elif obj_pos["direction"] == E:
        point = (obj_pos["rect"].right,
                 obj_pos["rect"].centery - int(BULLET_SIZE / 2))
    elif obj_pos["direction"] == S:
        point = (obj_pos["rect"].centerx - int(BULLET_SIZE / 2),
                 obj_pos["rect"].bottom)
    elif obj_pos["direction"] == W:
        point = (obj_pos["rect"].left - BULLET_SIZE,
                 obj_pos["rect"].centery - int(BULLET_SIZE / 2))
    else:
        raise Exception(
            "[{}] Invalid direction: {}".format(obj["name"], obj_pos["direction"])
        )

    sprite = pygame.image.load("images/bullet2.png")
    sprite = pygame.transform.scale(sprite, (BULLET_SIZE, BULLET_SIZE))
    bullet["position"] = {
        "rect": pygame.Rect((point), (BULLET_SIZE, BULLET_SIZE)),
        "direction": obj_pos["direction"],
        "sprite": sprite,
        "size": BULLET_SIZE,
    }

    bullet["health"] = {"hp": 1, "max_hp": 1, "lives": 1}
    bullet["mouvement"] = {"speed": BULLET_SPEED, "max_speed": BULLET_SPEED}
    bullet["logic"] = None
    bullet["turret"] = (None,)
    bullet["bonuses"] = []
    bullet["team"] = obj["team"]  # TODO: Decide on friendly fire
    return bullet


# Mykhailo SUTYRIN S2601127
def create_bonus(basePosition, size, lifetime):
    """
    Create bonus object.

    Parameters:
    ---
        basePosition: initial position of the object
        size: size of object
        lifetime: amount of seconds bonus will live
    Returns:
    ---
        bonus object
    """
    position = {
        "rect": pygame.Rect(basePosition, (10, 10)),
        "direction": 0,
        "sprite": None,
        "size": size,
    }
    lives = {"hp": lifetime, "max_hp": lifetime, "lives": 1}
    mouvement = {"speed": 0, "max_speed": 0}
    object = {
        "position": position,
        "health": lives,
        "mouvement": mouvement,
        "logic": None,
        "turrets": [],
        "bonuses": [],
        "team": 3,
        "type": "bonus",
        "name": ""
    }
    return object


# M. Sutyrin S2601127
def create_tank(
    basePosition, size, sprite, maxHealth, lives, team, speed, reloadSpeed, logic=None
):
    """
    Create new tank object.

    Parameters:
    ---
        basePosition: initial position ([int,int])
        size: size of tank (int)
        sprite: sprite of tank
        maxHealth: hp maximum de tank
        lives: number of lives
        team: team of the tank
        speed: speed of the tank
        reloadSpeed: number of seconds object need to shoot again
        logc: function of logic
    Returns:
    ---
        tank object
    """
    turret = {
        "direction": 0,
        "reload": reloadSpeed,
        "timeout": 0,  # set at reloadSpeed on shoot, then every second -1 till 0, when 0 can shoot again
    }

    sprite = pygame.image.load(sprite)
    sprite = pygame.transform.scale(sprite, (size, size))
    position = {
        "rect": pygame.Rect(basePosition, (size, size)),
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
        "type": "tank",
        "name": ""
    }
    return object


################
# TANK ACTIONS #
################


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
    """
    if obj.get("turrets") is None or obj["turrets"]["timeout"] > 0:
        # Object can't shoot
        print("Can't shoot: {}".format(obj["turrets"]["timeout"]))
        return None

    obj["turrets"]["timeout"] = obj["turrets"]["reload"]
    bullet = create_bullet(obj)
    objects.append(bullet)
    moveObject(len(objects) - 1)
    print("Shooting done")


# TODO: create func
def add_bonus(tank):
    return


# N. Beliy s2604210
def applyLogic(ind):
    """
    Decide what object must do (move, shoot, etc...) based
    on environment or user input

    Parameters:
    -----------
        ind: int
            index of object in object list
    """
    obj = objects[ind]

    if obj is None or obj.get("logic") is None:
        return

    obj["logic"](obj)


# N. Beliy s2604210
def user_control(obj):
    """
    Reads user commands and apply them to selected tank
    """

    # Selecting direction
    direction = None
    if keyMoveRight in keys:
        direction = E
    elif keyMoveLeft in keys:
        direction = W
    elif keyMoveUp in keys:
        direction = N
    elif keyMoveDown in keys:
        direction = S

    if direction is None:
        # No direction keys pressed: stop object
        obj["mouvement"]["speed"] = 0
    else:
        # Move object in given direction
        obj["position"]["direction"] = direction
        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]

    if keyShoot in keys:
        print("Shooting...")
        keys.discard(keyShoot)
        shoot(obj)


###########
# UTILITY #
###########


# Lesquir Jules s2601624
# Draw objects based on their "type"


def draw_object(obj):
    if obj is None:
        return
    if obj["type"] == "obstacle":
        if obj["position"]["sprite"] is not None:
            image = obj["position"]["sprite"].convert_alpha(mainWindow)
            mainWindow.blit(image, obj["position"]["rect"].topleft)
        

    elif obj["type"] == "tank" or obj["type"] == "bullet":
        image = obj["position"]["sprite"].convert_alpha(mainWindow)
        image = pygame.transform.rotate(image, -90 * obj["position"]["direction"])
        mainWindow.blit(image, obj["position"]["rect"].topleft)

    else:
        image = obj["position"]["sprite"].convert_alpha(mainWindow)
        image = pygame.transform.rotate(image, -90 * obj["position"]["direction"])
        mainWindow.blit(image, obj["position"]["rect"].topleft)

    if DEBUG:
        color = (255, 0, 0)
        pygame.draw.rect(mainWindow, color, obj["position"]["rect"], width=1)


# S2601624, Lesquir, Jules
# Reduce hp based on the damages
def hurt(damage, obj):
    obj["health"]["hp"] -= damage


# N. Beliy s2604210
def update_coundown(obj, clock):
    """
    Recursively updates all countdowns related to object
    (for ex. timeout of turrets).
    #MAIN_LOOP

    Parameters:
    -----------
        obj: dict
            object to update
        clock: pygame.time.Clock
            clock object
    """
    if obj is None:
        return

    for key, val in obj.items():
        if key == "timeout" and val > 0:
            # get_time returns in miliseconds
            obj[key] -= clock.get_time() / 1000
        elif isinstance(val, dict):
            update_coundown(val, clock)
        elif isinstance(val, list):
            for v in val:
                # Danger: may crash on list of not dict
                update_coundown(v, clock)


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
            print("Quitting...")
        elif event.type == pygame.KEYDOWN:
            if event.key in KEYS["singular"] or event.key in KEYS["continious"]:
                keys.add(event.key)
                print("Key {} pressed".format(event.key))
        elif event.type == pygame.KEYUP:
            if event.key in KEYS["continious"]:
                keys.discard(event.key)
                print("Key {} unpressed".format(event.key))


# S. Mykhailo S2601127
def clean_objects():
    """
    Clean objects with no life and remove life if no hp left.
    """
    global objects
    for i in range(len(objects)):
        health = objects[i].get("health")
        if health is not None:
            if objects[i]["health"]["hp"] <= 0:
                objects[i]["health"]["lives"] -= 1
            if objects[i]["health"]["lives"] <= 0:
                objects[i] = None
    objects = [obj for obj in objects
               if obj is not None]

###################
# ENEMY LOGIC(AI) #
###################


# S. Mykhailo S2601127
# TODO: possible bug if walls aren't fat enough
def dist2(obj1, obj2):
    """
    Return squared distance between 2 objects.

    Parameters:
    ---
        obj1: first object
        obj2: second object

    Returns:
    ---
        float distance
    """
    center1 = obj1["position"]["rect"].center
    center2 = obj2["position"]["rect"].center

    distance = (center1[0] - center1[0]) ** 2 +\
            (center1[1] - center1[1]) ** 2
    return distance


# N. Beliy s2604210
def awarness(obj, radius):
    """
    Check if any other object is within radius; objects are searched within
    4 cardinal directions (N, S, E, W). Found closest objects are plased
    in return list:
        [obj at N, obj at E, obj at S, obj at W]

    It is intended to be used by computer controlled entities

    Parameters:
    -----------
        obj: object to test
        radius: radius

    Returns:
    --------
        list of found objects
    """
    obj_pos = obj["position"]["rect"]
    projections = [
        pygame.Rect(obj_pos.left, obj_pos.top + radius, obj_pos.width, radius),
        pygame.Rect(obj_pos.right + radius, obj_pos.top, radius, obj_pos.height),
        pygame.Rect(obj_pos.left, obj_pos.bottom, obj_pos.width, radius),
        pygame.Rect(obj_pos.left - radius, obj_pos.top, radius, obj_pos.height),
    ]

    results = [None, None, None, None]

    for test_obj in objects:
        test_rect = test_obj["position"]["rect"]
        # gives 0,1,2,3
        for i in range(4):
            if projections[i].colliderect(test_rect):
                if results[i] is None or dist2(obj, results[i]) > dist2(obj, test_obj):
                    results[i] = test_obj
    return results


# S. Mykhailo S2601127
def do_wander(obj):
    """
    Wander randomly around, don't move in direction where is an obstacle.

    Parameters:
    ---
        obj - object to wander
    """
    random.seed()

    near = awarness(obj, 20)
    # standart direction pool
    standart_direction_pool = [0, 1, 2, 3]
    tmp = 0
    obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
    # randomly change direction if current direction face an obstacle
    for i in near:
        if not (i is None):
            standart_direction_pool.remove(tmp)
            tmp += 1
            if obj["position"]["direction"] == tmp:
                obj["position"]["direction"] = random.randint(
                    0, len(standart_direction_pool) - 1
                )
                return
    # randomly change direction, or leave previous direction
    rand = random.randint(0, 10)
    for i in standart_direction_pool:
        if rand == i:
            obj["position"]["direction"] = i
            return


# S. Mykhailo S2601127
def standart_logic(obj):
    """
    Scan in range for enemy tanks, shoot and move to them. Stop mouvement if distance is less then number of pixels.

    Moves randomly if no enemy in range, bypass obstacles with left hand rule.

    Parameters:
    ---
        obj: object to apply
    """
    vision = awarness(obj, 50)
    tmp = 0
    for i in vision:
        # scan for enemy shoot and move to it
        if not (i is None) and i["type"] == "tank" and i["team"] != obj["team"]:
            match tmp:
                # enemy detected North
                case 0:
                    if obj["position"]["rect"].x > i["position"]["rect"].x:
                        obj["position"]["direction"] = 1
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].x < i["position"]["rect"].x:
                        obj["position"]["direction"] = 3
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 0
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected East
                case 1:
                    if obj["position"]["rect"].y > i["position"]["rect"].y:
                        obj["position"]["direction"] = 0
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].y < i["position"]["rect"].y:
                        obj["position"]["direction"] = 2
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 1
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected South
                case 2:
                    if obj["position"]["rect"].x > i["position"]["rect"].x:
                        obj["position"]["direction"] = 1
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].x < i["position"]["rect"].x:
                        obj["position"]["direction"] = 3
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 2
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected West
                case 3:
                    if obj["position"]["rect"].y > i["position"]["rect"].y:
                        obj["position"]["direction"] = 0
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].y < i["position"]["rect"].y:
                        obj["position"]["direction"] = 2
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 3
                        obj["mouvement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
    do_wander(obj)


####################
# START GAME BLOCK #
####################

pygame.init()

BLOCK_SIZE = 60
#S2601624, Lesquir, Jules
#create the obstacles, (BLOCK_LENGHT, BLOCK_WICTH, (x, y))
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 3, BLOCK_SIZE * 3))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 3, BLOCK_SIZE * 6))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 4, BLOCK_SIZE * 2))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 4, BLOCK_SIZE * 7))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 9, BLOCK_SIZE * 2))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 9, BLOCK_SIZE * 7))
        )

objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 10, BLOCK_SIZE * 3))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 10, BLOCK_SIZE * 6))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        ((BLOCK_SIZE/2) * 13, (BLOCK_SIZE/2) * 9))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (0, 0))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (0, BLOCK_SIZE * 9))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 13, 0))
        )
objects.append(
        create_obstacle(BLOCK_SIZE, BLOCK_SIZE, "images/wall.png",
                        (BLOCK_SIZE * 13, BLOCK_SIZE * 9))
        )

objects.append(
        create_tank((BLOCK_SIZE * 2, BLOCK_SIZE), BLOCK_SIZE, "images/enemy_tank.png",
                    3, 1, 2, 3, 3, standart_logic)
        )
objects.append(
        create_tank((BLOCK_SIZE * 11, BLOCK_SIZE), BLOCK_SIZE, "images/enemy_tank.png",
                    3, 1, 2, 3, 3, standart_logic)
        )

objects.append(
        create_tank((BLOCK_SIZE * 7, BLOCK_SIZE * 8), BLOCK_SIZE, "images/main_tank.png",
                    3, 1, 1, 3, 3, user_control)
        )

#block outside window to stop the player from going too far
objects.append(
    create_obstacle(1, windowSize[1], None,
                    (-1, 0))
)
objects.append(
    create_obstacle(1, windowSize[1], None,
                    (windowSize[0] + 1, 0))
)
objects.append(
    create_obstacle(windowSize[0], 1, None,
                    (0, -1))
)
objects.append(
    create_obstacle(windowSize[0], 1, None,
                    (0, windowSize[1] + 1))
)
objects[-1]["name"] = "user"

mainWindow = pygame.display.set_mode(windowSize)

mainWindow.fill(backgroundColor)

time1 = pygame.time.Clock()

running = True

while running:
    parseKeys(pygame.event.get())

    mainWindow.fill(backgroundColor)
    for i in range(len(objects)):
        update_coundown(objects[i], time1)
        applyLogic(i)
        moveObject(i)

    for i in range(len(objects)):
        draw_object(objects[i])
    clean_objects()

    pygame.display.flip()
    time1.tick(50)


pygame.display.quit()
pygame.quit()
