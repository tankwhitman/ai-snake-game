# Snake heuristic calc

import random
import typing
import time
import sys
from collections import Counter

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

    print()
    x = int(next_head["x"])
    y = int(next_head["y"])

    if x>=0 and y>=0 and x<board_width and y<board_height:
        return True
    return False

def avoid_snakes(next_head, snakes):
    result = True
    for snake in snakes:
        if next_head in snake["body"][:-1]:
            result = False
            # print("going to runinto an opponent")
    return result

def get_safe_moves(body, board):

    possible_moves = ["up", "down", "left", "right"]
    safe_moves = []
    for guess in possible_moves:
        guess_coord = get_next(body[0], guess)
        # print("guess_coord:", guess_coord)
        if avoid_walls(guess_coord, board["width"], board["height"]) and avoid_snakes(guess_coord, board["snakes"]): 
            safe_moves.append(guess)
        elif len(body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
        # The tail is also a safe place to go... unless there is a non-tail segment there too
            safe_moves.append(guess)

    return safe_moves
### End of code used from simple.py file


def distance_from_food(food, head):
    dist = 0
    xdist = abs(head["x"]-food["x"])
    ydist = abs(head["y"]-food["y"])
    dist = xdist+ydist
    return dist


    # Calculate distance from our head to the nearest part of the other snake

def distance_from_opp(head, snake):
    dist_list = []
    for part in snake:
      xdist = abs(head["x"]-part["x"])
      ydist = abs(head["y"]-part["y"])
      dist_list.append(xdist+ydist)
    # print("dist list", dist_list)
    return max(dist_list)
    # Calculate distance from our head to the nearest part of the other snake

def distance_from_wall(head, board):
    height = board['height']
    width = board['width']

    if head["x"] >= (width/2):
       x_wall = width - head["x"]
    else:
        x_wall = head["x"]

    if head['y'] >= height/2:
        y_wall =  height - head['y']
    else:
        y_wall = head['y']    
    
    if x_wall > y_wall:
        return x_wall
    else:
        return y_wall

def avoid_self(guess_coord, body):
    
  x_Cord = []
  y_Cord = []
  for segment in body:
    x_Cord.append(segment["x"])
    y_Cord.append(segment["y"])

  # Use Counter to count the occurrences of each number
  count_x = Counter(x_Cord)
  count_y = Counter(y_Cord)

  x_avoid, count_of_most_common = count_x.most_common(1)[0]
  y_avoid, count_of_most_common = count_y.most_common(1)[0]

  if len(body) > 5:
    if guess_coord["x"] > x_avoid or guess_coord["x"] < x_avoid or guess_coord["y"] > y_avoid or guess_coord["y"] < y_avoid:
      return True
    return False
  else:
    return True
  

def floodFill(x, y, gameState, iters, depth):
    a = {'x': x, 'y': y}
    # print(gameState['board']['snakes'][0]['body'])
    inMe = any(x ==a for a in gameState['board']['snakes'][0]['body'])
    inOpp = any(x ==a for a in (gameState['board']['snakes'][1]['body']) )
    print('called ', iters, 'times')
    if(depth ==0):
        return iters

    if( inMe or inOpp or x>gameState['board']['width'] or x < 0 or y> gameState['board']['height'] or y < 0 ):
        return iters
    

    iters = floodFill(x+1, y, gameState, iters+1, depth -1)
    iters = iters + floodFill(x-1, y, gameState, iters+1, depth -1)
    iters = iters + floodFill(x, y+1, gameState,iters+1, depth -1)
    iters = iters + floodFill(x, y-1, gameState, iters+1, depth-1)

    return iters


def heuristic_calc(food_dist_me, opp_dist, self_dist, wall_dist, you_len, opp_len, mybody,oppBody): 
    # Highest number will be the best heuristic 
    # print(f"{get_next(body[0],guess_move)} is the next head in {body}")
    # if get_next(body[0],guess_move) in body:
    #     # print('i will run intomyself')
    #     return 9999999
    
    # if food_dist_me ==1:
    #     return 999999
    


    out = any(check in mybody for check in oppBody)
    if out:
        print(oppBody, mybody)
        return 100000
    point = 0 # Assign a weight to each factor 
    w1 = 0.9 # Weight for food distance of me 
    w2 = 0.1 # Weight for food distance of opponent 
    w3 = 0.2 # Weight for enemy distance 
    w4 = 0.1 # Weight for distance from self
    w5 = 0.2 # Weight for distance from wall
    # Calculate the inverse probabilities 
    foodProbability_me = 1 / (1+food_dist_me) 
    # foodProbability_opp = 1 / (1+food_dist_opp) 
    enemyProbability = 1 / (1+opp_dist) 
    selfProbability = 1 / (1+self_dist)
    wallProbability = 1 / (1+wall_dist)
    # Add the weighted probabilities to get the point value w2 * foodProbability_opp
    point = w1 * foodProbability_me  - w3 * enemyProbability - w4 * selfProbability - w5 * wallProbability
    # Penalize states or actions that are too close to the enemy 
    # if opp_dist <= 3: 
    #     point = -1 
    # if(opp_dist <=1):
    #     point = -10000
    # if you_len > opp_len:
    #     point = 10000
    # print('h calc',point)
    return point

# add logic that sets point value to really big if any part of your snake is in the opposing snake


    # create a linked list tree to store all connected moves
    # Loop checking heuristic of moves as they are created and assign them to each move
    # for checking heuristic, will also need to calc heuristic of every piece of food and assign the best from those
    # return list of move(s) with path to highest heuristic after looking 5 turns in the future
    # main code chooses move from here randomly, or if there arent any, from safe_moves randomly
