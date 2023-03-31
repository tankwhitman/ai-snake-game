# Snake heuristic calc

import random
import typing
import time
import sys
import numpy as np

random_seed = None
### code used from given simple.py file
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

def avoid_walls(next_head, board_width, board_height):
    # Function to check if the coordinates of the next head will hit a wall or not
    result = True

    x = int(next_head["x"])
    y = int(next_head["y"])

    if x<0 or y<0 or x>=board_width or y>=board_height:
        result = False
    return result

def avoid_snakes(next_head, snakes):
    result = True
    for snake in snakes:
        if next_head in snake["body"][:-1]:
            result = False
    return result

def get_safe_moves(body, board):
    possible_moves = ["up", "down", "left", "right"]
    safe_moves = []
    for guess in possible_moves:
        guess_coord = get_next(body[0], guess)
        if avoid_walls(guess_coord, board["width"], board["height"]) and avoid_snakes(guess_coord, board["snakes"]) and avoid_self(guess_coord, body): 
            safe_moves.append(guess)
        elif len(body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
           # The tail is also a safe place to go... unless there is a non-tail segment there too
           safe_moves.append(guess)
    return safe_moves
### End of code used from simple.py file


def distance_from_food(food, head):
    dist = 0
    # print(head["x"])
    xdist = abs(head["x"]-food["x"])
    ydist = abs(head["y"]-food["y"])
    dist = xdist+ydist
    return dist

def distance_from_opp(head, snake):
    dist_list = []
    for part in snake:
         xdist = abs(head["x"]-part["x"])
         ydist = abs(head["y"]-part["y"])
         dist_list.append(xdist+ydist)
    return max(dist_list)
    # Calculate distance from our head to the nearest part of the other snake

def avoid_self(guess_coord, body):
  x_Cord = []
  y_Cord = []
  for segment in body:
    x_Cord.append(segment["x"])
    y_Cord.append(segment["y"])

  np_x = np.array(x_Cord)
  np_y = np.array(y_Cord)

  if len(body) > 15:
    if guess_coord["x"] > (np.bincount(np_x).argmax()) or guess_coord["x"] < (np.bincount(np_x).argmax()) or guess_coord["y"] > (np.bincount(np_y).argmax()) or guess_coord["y"] < (np.bincount(np_y).argmax()):
      return True
    return False
  else:
    return True
  print(guess_coord)
  print(x_Cord)
  print(np.bincount(np_x).argmax())
  
    
def heuristic_calc(food_dist_me, food_dist_opp, opp_dist):
    # Highest number will be the best heuristic
    point = 0
    if food_dist_me < food_dist_opp:
        point = abs(food_dist_me - 100)
    else:
        point = -1
    if opp_dist <= 3:
        point = -1
    return point


    # create a linked list tree to store all connected moves
    # Loop checking heuristic of moves as they are created and assign them to each move
    # for checking heuristic, will also need to calc heuristic of every piece of food and assign the best from those
    # return list of move(s) with path to highest heuristic after looking 5 turns in the future
    # main code chooses move from here randomly, or if there arent any, from safe_moves randomly