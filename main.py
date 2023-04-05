# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys
import copy
import heuristic
import random

highestDepth = 3

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "MegaTron Snakinator",  # TODO: Your Battlesnake Username
        "color": "#e1e96b",  # TODO: Choose color
        "head": "gamer",  # TODO: Choose head
        "tail": "fat-rattle",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def follow(snake, head):


    x = 0
    prev = head.copy()
    while x < snake['length']:
        tmp = snake["body"][x].copy()

        snake['body'][x] = prev
        prev = tmp
        x = x +1

    return snake
         

def moveSnake(snake, move):
    MOVE_LOOKUP = {"left":-1, "right": 1, "up": 1, "down":-1}
    # Copy first


    future_head = snake['body'][0].copy()
    if move in ["left", "right"]:
        # X-axis
        future_head["x"] = snake['body'][0]["x"] + MOVE_LOOKUP[move]
    elif move in ["up", "down"]:
        future_head["y"] = snake['body'][0]["y"] + MOVE_LOOKUP[move]

    snake = follow(snake, future_head)



    return snake
  
def minimax(gameState, depth, maximizingPlayer):


    if len(gameState['board']['snakes']) ==1:
        return (100, "up")

    if depth == 1:
        
        foodValueList = [] 
        for food in gameState["board"]["food"]:
            foodValueList.append(heuristic.distance_from_food(food, gameState["board"]["snakes"][0]['body'][0]))
        food = min(foodValueList)
        value = heuristic.heuristic_calc(food,
                                heuristic.distance_from_opp(gameState["board"]["snakes"][0]["body"][0], gameState["board"]["snakes"][1]["body"]),
                                heuristic.distance_from_opp(gameState["board"]["snakes"][0]["body"][0], gameState["board"]["snakes"][0]["body"][2:]),
                                heuristic.distance_from_wall(gameState["board"]["snakes"][0]["body"][0], gameState["board"]),
                                len(gameState["board"]["snakes"][0]["body"]),
                                len(gameState["board"]["snakes"][1]["body"]),
                                gameState["board"]["snakes"][0]["body"],
                                gameState['board']['snakes'][1]['body'])

        return value


    moveResults = {'up': -10000, 'down': -10000, 'left': -10000, 'right': -10000}
    move_option =  heuristic.get_safe_moves( gameState["board"]["snakes"][0]["body"], gameState["board"] )

    possibleChildren = []
    for move in move_option:
        newState = copy.deepcopy(gameState)

        newState['board']['snakes'][0] = moveSnake(newState['board']['snakes'][0], move)
        possibleChildren.append(copy.deepcopy(newState))
    
    # if depth == highestDepth and len(move_option)>1:

    #     x=0
    #     while x < len(move_option):

    #         safe = heuristic.floodFill(gameState["board"]["snakes"][0]["body"][0]['x'], gameState["board"]["snakes"][0]["body"][0]['y'], possibleChildren[x], 0, 4)
    #         if(safe  < len(gameState["board"]["snakes"][0]["body"])):
    #             del possibleChildren[x]
    #             del move_option[x]
    #         x = x + 1

    x=0
    if maximizingPlayer:
        
        maxEval = -999999

        while x < len(possibleChildren):
            eval = minimax(possibleChildren[x], depth-1,False)
          
            maxEval = max(maxEval, eval)
            if(depth == highestDepth):
                moveResults[move_option[x]] = eval
            x=x+1
          
        if(depth == highestDepth):
          
          bestMove = max(moveResults, key=moveResults.get) 

          maxEval = max(moveResults.values())

          if(bestMove in move_option):
            return (maxEval, bestMove)
          return (random.choice(move_option), maxEval)
        return (maxEval, bestMove)
    else:
        minEval = 999999
        #['down','up', 'left', 'right']
        while x < len(possibleChildren):
            eval =minimax(possibleChildren[x], depth-1, True)
            # print("minimizing IS COMPARING," ,minEval, eval[0])
            minEval = min(minEval, eval)
            x =x+1
        return minEval

        






# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    move = minimax(game_state, highestDepth, True)

    print(f"MOVE {game_state['turn']}: {move[1]} with value of {move[0]}")
    return {"move": move[1]}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
