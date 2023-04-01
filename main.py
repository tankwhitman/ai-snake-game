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
    
    snakeArr = snake["you"]["body"]
    prev = snakeArr[0]
    spot=1
    while spot < snake["you"]["length"]:
        # print("comparing ", prev, " to ", snakeArr[spot])
        if prev == snakeArr[spot]:
            
            # print("same coord")
            prev = snakeArr[spot] 
        else:
            hold = snakeArr[spot]
            # print("HOLD = ", hold)
            snakeArr[spot] = prev
            prev = hold
        spot = spot+1
    
         

def moveSnake(snake, move):
    if(move == 'up'):
        prevHead = snake["you"]["head"]

        snake["you"]["head"]["y"] = snake["you"]["head"]["y"]+1
        

        follow(snake, prevHead)
        snake["you"]["body"][0] = snake["you"]["head"]

    elif(move== 'down'):
        prevHead = snake["you"]["head"]

        snake["you"]["head"]["y"] = snake["you"]["head"]["y"]-1
        

        follow(snake, prevHead)
        snake["you"]["body"][0] = snake["you"]["head"]

    elif(move=='left'):
        prevHead = snake["you"]["head"]

        snake["you"]["head"]["x"] = snake["you"]["head"]["x"]-1
        

        follow(snake, prevHead)
        snake["you"]["body"][0] = snake["you"]["head"]

    elif(move =='right'):
        prevHead = snake["you"]["head"]

        snake["you"]["head"]["x"] = snake["you"]["head"]["x"]+1
        

        follow(snake, prevHead)
        snake["you"]["body"][0] = snake["you"]["head"]
    return snake

            

    



def minimax(gameState, depth, maximizingPlayer,value, move ):
    #if there are no optimal moves, choose a random safe move :)


    # print(gameState["board"]["snakes"])
    if depth == 0 or len(gameState['board']['snakes']) == 1: #gamestate = terminal
        # print("HERES YOUR PROBLEM")
        return  value, move#the heuristic value of current state
    if (maximizingPlayer==True):
        move_option =  heuristic.get_safe_moves( gameState["you"]["body"], gameState["board"] )#
        item = ['down','up', 'left', 'right']
        #make a not safe move option!
        # if(len(move_option) < 4):
        notsafe = set(item) - set(move_option)
        #     for item in notsafe:
        #         return (-1000000, item)
        if(len(move_option) ==0):
            return (-5000000000, '')

        value = -1000000
        bestMove = None
        # print("STARTING POINT", gameState["you"]['body'])
        
        moveResults = {'up': -1, 'down': -1, 'left': -1, 'right': -1}
        for x in move_option:
            newState = copy.deepcopy(gameState)
            newState = moveSnake(newState, x)
            # print("MOVING: ", x, " " ,newState["you"]["head"])
            #heuristic_calc(food_dist_me, food_dist_opp, opp_dist):
            foodValueList = []
            for food in gameState["board"]["food"]:
                foodValueList.append(heuristic.heuristic_calc(heuristic.distance_from_food(food, newState["you"]["head"]), 
                                                      heuristic.distance_from_food(food, newState["board"]["snakes"][1]["head"]),
                                                      heuristic.distance_from_opp(newState["you"]["head"], newState["board"]["snakes"][1]["body"]),
                                                      heuristic.distance_from_food(newState['you']['head'], newState["board"]["snakes"][1]["head"])))
            
            value = max(foodValueList)
            moveResults[x] = max(foodValueList)
            bestMove = max(moveResults, key=moveResults.get)
            minimaxResult = minimax(newState, depth-1, False,value, bestMove)
            if(minimaxResult[0]>0):
                value = max(value, minimaxResult[0])
                if(value == minimaxResult[0]):
                    bestMove = minimaxResult[1]
            


        
        bestMove = max(moveResults, key=moveResults.get)

        # try:
        #     if(moveResults[bestMove] == -1):
        #         bestMove = random.choice(move_option)
        # except:

            # print(x, "  - ",newState["you"]["body"])
        
        return (value, bestMove) # value, bestmove
    else: # minimizing player
        
        move_option =  heuristic.get_safe_moves( gameState["board"]["snakes"][1]["body"], gameState["board"] )#['down','up', 'left', 'right']
        
        value = 10000000000
        bestMove = None
        # print("STARTING POINT", gameState["you"]['body'])
        
        moveResults = {'up': -1, 'down': -1, 'left': -1, 'right': -1}
        for x in move_option:
            newState = copy.deepcopy(gameState)
            newState = moveSnake(newState, x)
            
            foodValueList = []
            for food in gameState["board"]["food"]:
                foodValueList.append(heuristic.heuristic_calc(heuristic.distance_from_food(food, newState["board"]["snakes"][1]["head"]), 
                                                      heuristic.distance_from_food(food, newState["you"]["head"]),
                                                      heuristic.distance_from_opp(newState["board"]["snakes"][1]["head"], newState["you"]["body"] ),
                                                      heuristic.distance_from_food(newState["you"]["head"], newState["board"]["snakes"][1]["head"] )))
            
            value = min(foodValueList)

            moveResults[x] = min(foodValueList)
            # print(newState)
            bestMove = min(moveResults, key=moveResults.get)
            minimaxResult = minimax(newState, depth-1, True,value,bestMove)
            value = min(value, minimaxResult[0])

        
        bestMove = max(moveResults, key=moveResults.get)
        
        # print(moveResults)
        # print(bestMove)
        # if(moveResults[bestMove] == -1):
        #     bestMove = random.choice(move_option)

        return (value, bestMove)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    print(game_state['turn'])
    move = minimax(game_state, 6, True,0, 'up')

    print(f"MOVE {game_state['turn']}: {move[1]}")
    return {"move": move[1]}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
