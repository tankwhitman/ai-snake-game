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
        "head": "alligator",  # TODO: Choose head
        "tail": "fat-rattle",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")

# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def follow(snake, head):
    # print("supposidly previous ", head)

    x = 0
    prev = head.copy()
    while x < len(snake):
        tmp = snake["you"]["body"][x].copy()
        snake[x] = prev
        prev = tmp
        x = x +1

    return snake
         

def moveSnake(snake, move):
    MOVE_LOOKUP = {"left":-1, "right": 1, "up": 1, "down":-1}
    # Copy first
    # print("before snake head move", snake['you']['body'])
    future_head = snake[0].copy()
    if move in ["left", "right"]:
        # X-axis
        future_head["x"] = snake[0]["x"] + MOVE_LOOKUP[move]
    elif move in ["up", "down"]:
        future_head["y"] = snake[0]["y"] + MOVE_LOOKUP[move]
    # print('before follow', snake['you']['body'])
    snake = follow(snake, future_head)

    print("after snake head move",move, snake['you']['body'])

    return snake

            

    





def minimax(gameState, depth, maximizingPlayer, bestMove):
    # print()
    # print(f"before being called", gameState["you"]["body"], "LEVEL: ", depth, " and the value/move", bestMove)
    # try:
    if len(gameState['board']['snakes']) ==1:
        return (100, "up")

    if depth == 1:
        foodValueList = [] 
        for food in gameState["board"]["food"]:
            foodValueList.append(heuristic.distance_from_food(food, gameState["you"]['body'][0]))
        food = min(foodValueList)
        print(f"With {food} moves from food. my head is at ",gameState['you']['body'][0])
        value = heuristic.heuristic_calc(food,
                                heuristic.distance_from_opp(gameState["board"]["snakes"][1]["head"], gameState["you"]["body"]),
                                heuristic.distance_from_opp(gameState["board"]["snakes"][1]["head"], gameState["board"]["snakes"][1]["body"][2:]),
                                heuristic.distance_from_wall(gameState["board"]["snakes"][1]["head"], gameState["board"]),
                                gameState["board"]["snakes"][1]["length"],
                                gameState["you"]["length"],
                                bestMove,
                                gameState["you"]["body"])
        print(value, bestMove)
        return (value, bestMove)
    # except:
    #     print("game must be over")
    moveResults = {'up': -10000, 'down': -10000, 'left': -10000, 'right': -10000}
    if maximizingPlayer:
        move_option =  heuristic.get_safe_moves( gameState["you"]["body"], gameState["board"] )#
        value = -999999
        print(f"{move_option} are the safe moves at level {depth} for good snake")

        for move in move_option:
            
            # print(f"before {gameState['you']['body']} with a move of {move}")
            newState = copy.copy(gameState)
            newState= moveSnake(newState['snakes'][0]['body'],move)
            newState['you']['body'] = newState['snakes'][0]['body']
            print("TESTING MOVE", move ,"at level", depth)
            minimaxResult = minimax(newState, depth-1,False,move)
            print(minimaxResult)
            value = max(value, minimaxResult[0])
            if(depth == highestDepth):
                moveResults[minimaxResult[1]] = minimaxResult[0]

        if(depth == highestDepth):
            bestMove = max(moveResults, key=moveResults.get)
            print(moveResults)
            value = max(moveResults.values())
        return (value, bestMove)
    else:
        value = 999999
        move_option =  heuristic.get_safe_moves( gameState["board"]["snakes"][1]["body"], gameState["board"] )#['down','up', 'left', 'right']
        for move in move_option:
            newState = copy.copy(gameState)
            newState = moveSnake(newState['snakes'][1], move)
            
            # if (value == minimaxResult[0]):
                # bestMove = minimaxResult[1]
        move
        minimaxResult =minimax(newState, depth-1, True,move)
        value = min(value, minimaxResult[0])
        print(value, bestMove)    
        return (value, bestMove)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    move = minimax(game_state, highestDepth, True,'')

    print(f"MOVE {game_state['turn']}: {move[1]} with value of {move[0]} ***************************")
    return {"move": move[1]}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
