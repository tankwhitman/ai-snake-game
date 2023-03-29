# Snake heuristic calc

import random
import typing
import time
import sys

random_seed = None

def get_next(current_head, next_move):
    """
    return the coordinate of the head if our snake goes that way
    """
    MOVE_LOOKUP = {"left":-1, "right": 1, "up": 1, "down":-1}
    # Copy first
    future_head = current_head.copy()

    if next_move in ["left", "right"]:
        # X-axis
        future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
    elif next_move in ["up", "down"]:
        future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]

    return future_head

def avoid_walls(next_head):
    # Function to check if the coordinates of the next head will hit a wall or not
    result = True

    x = int(next_head["x"])
    y = int(next_head["y"])

    if x<0 or y<0 or x>10 or y>10:
        result = False
    return result

def avoid_snakes(next_head, snakes):
    result = True
    for snake in snakes:
        if next_head in snake["body"][:-1]:
            result = False
    return result

def get_safe_moves(possible_moves, body, board):
    safe_moves = []
    for guess in possible_moves:
        guess_coord = get_next(body[0], guess)
        if avoid_walls(guess_coord, board["width"], board["height"]) and avoid_snakes(guess_coord, board["snakes"]): 
            safe_moves.append(guess)
        elif len(body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
           # The tail is also a safe place to go... unless there is a non-tail segment there too
           safe_moves.append(guess)
    return safe_moves

def distance_from_food(food, head):
    dist = 0
    xdist = abs(head["x"]-food["x"])
    ydist = abs(head["y"]-food["y"])
    dist = xdist+ydist
    return dist
    
def heuristic_calc(food_dist_me, food_dist_opp):
    point = 0
    if food_dist_me < food_dist_opp:
        point = food_dist_me
    else:
        point = -1
    return point


