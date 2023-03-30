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

            

    



def minimax(gameState, depth, maximizingPlayer ):
    #if there are no optimal moves, choose a random safe move :)

    move_option =  heuristic.get_safe_moves( gameState["you"]["body"], gameState["board"] )#['down','up', 'left', 'right']

    if depth == 0: #gamestate = terminal
        return #the heuristic value of current state
    if (maximizingPlayer==True):
        value = 00000000000
        bestMove = None
        # print("STARTING POINT", gameState["you"]['body'])
        
        moveResults = {'up': -1, 'down': -1, 'left': -1, 'right': -1}
        for x in move_option:
            newState = copy.deepcopy(gameState)
            newState = moveSnake(newState, x)
            # print("MOVING: ", x, " " ,newState["you"]["head"])
            #heuristic_calc(food_dist_me, food_dist_opp, opp_dist):
            value = []
            for food in gameState["board"]["food"]:
                value.append(heuristic.heuristic_calc(heuristic.distance_from_food(food, newState["you"]["head"]), 
                                                      heuristic.distance_from_food(food, newState["board"]["snakes"][1]["head"]),
                                                      heuristic.distance_from_opp(newState["you"]["head"], newState["board"]["snakes"][1]["body"])))
            
            moveResults[x] = max(value)
        bestMove = max(moveResults, key=moveResults.get)
        print(moveResults)
        print(bestMove)
        
            # print(x, "  - ",newState["you"]["body"])
            # value, bestMove = max(value, minimax(newState, depth-1, False))
        return (bestMove) # value, bestmove
    # else # minimizing player
    #     value = -122222
    #     bestMove = None
    #     for each child of node do
    #         newState = gameState.apply(move_option)
    #         value, bestMove := min(value, minimax(newState, depth-1, True))
    #     return (value, best_move)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    # is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # # We've included code to prevent your Battlesnake from moving backwards
    # my_head = game_state["you"]["body"][0]  # Coordinates of your head
    # my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    # if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    #     is_move_safe["left"] = False

    # elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    #     is_move_safe["right"] = False

    # elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    #     is_move_safe["down"] = False

    # elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    #     is_move_safe["up"] = False
    # # print(game_state)
    # # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']
    # length = game_state['you']['length']



    # # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # # Are there any safe moves left?
    # safe_moves = []
    # for move, isSafe in is_move_safe.items():
    #     if isSafe:
    #         safe_moves.append(move)

    # if len(safe_moves) == 0:
    #     print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    #     return {"move": "down"}

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    # game_state.apply('up')
    # move = 'down'
    move = minimax(game_state, 2, True)

    print(f"MOVE {game_state['turn']}: {move}")
    return {"move": move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
