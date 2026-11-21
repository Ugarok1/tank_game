#!/usr/bin/env python3
# help

import math

import pygame
import random
import time

backgroundColor = (0, 191, 200)


windowSize = (1200, 900)

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
BULLET_SPEED = 10
BULLET_SIZE = 3

#########################
# Global object holders #
#########################
objects = []  # List of objects
keys = []  # List/set of pressed keys
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

    if "movement" not in obj:
        return
    speed = obj["movement"]["speed"]
    pos = obj["position"]["rect"]
    direction = obj["position"]["direction"]

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
        apply_collide_logic(ind, index, new_rect)
        return


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

    operated_type = object["type"]
    operated_team = object["team"]

    type = object["type"]
    team = object["team"]
    if operated_type == "tank" or operated_type == "obstacle":
        if type == "tank":
            oper_obj_size = (oper_rect.width, oper_rect.height)
            obj_size = (rect.width, rect.height)
            if operated_object["position"]["direction"][0] == N:
                oper_rect.move_ip(oper_rect.x, rect.bottim + 1)
            elif operated_object["position"]["direction"][0] == E:
                oper_rect.move_ip(rect.right + 1, oper_rect.y)
            elif operated_object["position"]["direction"][0] == S:
                oper_rect.move_ip(oper_rect.x, rect.top - oper_rect.height - 1)
            elif operated_object["position"]["direction"][0] == W:
                oper_rect.move_ip(rect.left, oper_rect.y)
            else:
                print("ERROR, unexpected value of position")
            if operated_type == "tank" and type == "tank" and operated_team != team:
                operated_object["Lives"]["hp"] -= 1
                object["Lives"]["hp"] -= 1
        if operated_type == "tank" and type == "bullet" and team != operated_team:
            operated_object["Lives"]["hp"] -= 1
        if operated_type == "tank" and type == "bonus":
            add_bonus(operated_object)
    if operated_type == "bullet" or operated_type == "bonus":
        objects.remove(operated_object)


#################
# CREATE OBJECT #
#################


# Lesquir Jules s2601624
# create obstacles (block,...) on the stage
def create_obstacle(BLOCK_LENGHT, BLOCK_WIDTH, position):
    Position = {
        "rect": pygame.Rect(position, [BLOCK_LENGHT, BLOCK_WIDTH]),
        "direction": None,
        "sprite": None,
        "size": None,
    }
    object = {
        "position": Position,  # Will contain position dict for drawing object
        "health": None,  # Will containg health and life/respawn info
        "movement": None,  # Will contain seed, that will determine how object will move
        "logic": None,  # Will contain pointer to function how object will behave
        "turret": None,  # Parameters of cannon
        "bonuses": None,  # List of bonuses affecting object
        "team": 0,  # If obj frendly(1), hostile(2) or neutral(0), bonus(3)
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
        point = obj_pos["rect"].midtop
        point = (point[0] - 0.5 * BULLET_SIZE, point[1] - BULLET_SIZE)
    elif obj_pos["direction"] == E:
        point = obj_pos["rect"].midright
        point = (point[0], point[1] - 0.5 * BULLET_SIZE)
    elif obj_pos["direction"] == S:
        point = obj_pos["rect"].midright
        point = (point[0] - 0.5 * BULLET_SIZE, point[1])
    elif obj_pos["direction"] == W:
        point = obj_pos["rect"].midright
        point = (point[0] - BULLET_SIZE, point[1] - 0.5 * BULLET_SIZE)
    else:
        raise Exception(
            "[{}] Invalid direction: {}".format(obj["name"], obj_pos["direction"])
        )

    bullet["position"] = {
        "rect": pygame.Rect((point), (BULLET_SIZE, BULLET_SIZE)),
        "direction": obj_pos["direction"],
        "sprite": "images/bullet.png",
        "size": BULLET_SIZE,
    }

    bullet["health"] = {"hp": 1, "max_hp": 1, "lives": 0}
    bullet["movement"] = {"seed": BULLET_SPEED, "max_speed": BULLET_SPEED}
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
        "movement": mouvement,
        "logic": None,
        "turrets": [],
        "bonuses": [],
        "team": 3,
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
    position = {
        "rect": pygame.Rect(basePosition, (10, 10)),
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

    Returns:
    --------
        Bullet or None
    """
    if obj["turret"] is None or obj["turret"]["timeout"] > 0:
        # Object can't shoot
        return None

    obj["turret"]["timeout"] = obj["turret"]["reload"]
    bullet = create_bullet(obj)

    # TODO: Adding to the list during iteration may cause problems
    # TODO: Avoid double move
    moveObject(bullet)
    return bullet


# TODO: create func
def add_bonus(tank):
    return


###########
# UTILITY #
###########


# Lesquir Jules s2601624
# Draw objects based on their "type"


def draw_object(obj):
    """
    #MAIN_LOOP
    """
    if obj["type"] == "obstacle":
        color = (0, 0, 0)
        pygame.draw.rect(mainWindow, color, obj["position"]["rect"])

    elif obj["type"] == "tank" or obj["type"] == "bullet":
        imagePath = obj["position"]["sprite"]
        image = pygame.image.load(imagePath).convert_alpha(mainWindow)
        image = pygame.transform.rotate(image, 90 * obj["position"]["direction"])
        image = pygame.transform.scale(image, obj["position"]["rect"][1])
        mainWindow.blit(image, obj["position"]["rect"][0])

    else:
        imagePath = obj["position"]["sprite"]
        image = pygame.image.load(imagePath).convert_alpha(mainWindow)
        image = pygame.transform.scale(image, obj["position"]["rect"][1])
        mainWindow.blit(image, obj["position"]["rect"][0])


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
    for key, val in obj.items():
        if key == "timeout" and val > 0:
            val -= clock.get_time()
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
        elif event.type == pygame.KEYDOWN:
            if event.key in KEYS["singular"] or event.key in KEYS["continious"]:
                keys.add(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in KEYS["continious"]:
                keys.discard(event.key)


# S. Mykhailo S2601127
def clean_objects():
    """
    Clean objects with no life and remove life if no hp left.
    #MAIN_LOOP
    """
    for i in range(len(objects)):
        if objects[i]["Lives"]["hp"] <= 0:
            objects[i]["Lives"]["lives"] -= 1
        if objects[i]["Lives"]["lives"] <= 0:
            objects.remove(i)


###################
# ENEMY LOGIC(AI) #
###################


# S. Mykhailo S2601127
# TODO: possible bug if walls aren't fat enough
def dist2(obj1, obj2):
    """
    Return distance between 2 objects.

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

    distance = math.sqrt(
        (center1[0] - center1[0]) ** 2 + (center1[1] - center1[1]) ** 2
    )
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
def apply_AI():
    """
    Apply logic to tanks, if they have one.
    #MAIN_LOOP
    """
    for object in objects:
        if object["type"] == "tank" and not (object["logic"] is None):
            object["logic"](object)


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
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].x < i["position"]["rect"].x:
                        obj["position"]["direction"] = 3
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 0
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected East
                case 1:
                    if obj["position"]["rect"].y > i["position"]["rect"].y:
                        obj["position"]["direction"] = 0
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].y < i["position"]["rect"].y:
                        obj["position"]["direction"] = 2
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 1
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected South
                case 2:
                    if obj["position"]["rect"].x > i["position"]["rect"].x:
                        obj["position"]["direction"] = 1
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].x < i["position"]["rect"].x:
                        obj["position"]["direction"] = 3
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 2
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
                # enemy detected West
                case 3:
                    if obj["position"]["rect"].y > i["position"]["rect"].y:
                        obj["position"]["direction"] = 0
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    elif obj["position"]["rect"].y < i["position"]["rect"].y:
                        obj["position"]["direction"] = 2
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        return
                    else:
                        obj["position"]["direction"] = 3
                        obj["movement"]["speed"] = obj["mouvement"]["max_speed"]
                        shoot(obj)
                        return
    do_wander(obj)


####################
# START GAME BLOCK #
####################

pygame.init()
pygame.key.set_repeat(200, 25)

# S2601624, Lesquir, Jules
# create the obstacles, (BLOCK_LENGHT, BLOCK_WICTH, (x, y))
create_obstacle(
    windowSize[0] / 8, windowSize[1] / 6, (windowSize[0] / 4, windowSize[1] / 3)
)

create_obstacle(
    windowSize[0] / 8, windowSize[1] / 6, ((windowSize[0] / 8) * 5, windowSize[1] / 3)
)

create_obstacle(
    windowSize[0] / 2, windowSize[1] / 6, (windowSize[0] / 4, (windowSize[1] / 6) * 4)
)

create_obstacle(windowSize[0] / 16, windowSize[1], (0, 0))

create_obstacle(windowSize[0] / 16, windowSize[1], (windowSize[0] / 16) * 15, 0)

create_obstacle(windowSize[0], windowSize[1] / 12, (0, 0))

create_obstacle(windowSize[0], windowSize[1] / 12, (0, (windowSize[1] / 12) * 11))

mainWindow = pygame.display.set_mode(windowSize)

mainWindow.fill(backgroundColor)

time1 = pygame.time.Clock()

running = True

while running:
    parseKeys(pygame.event.get())
    pygame.display.flip()
    for i in range(len(objects)):
        moveObject(i)
        draw_object(objects[i])


pygame.display.quit()
pygame.quit()
