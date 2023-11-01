#main loop runs here
#triggers that need to happen
# 1- cities have start of day
# 2- disaster hits somewhere
#       - disasters may or may not hit but they get more frequent
# 3- response actions
# 4- final actions
# 5- damages counted
# Ideally all of this is displaeyd in the gui
from objects import *

# TO DO

# Interface
#   - show cities distinct by country and by features such as defences, population, infrastructure
#   - display cities on the map in random positions with borders
#   - display movement of resources
#   - display disasters
#   - start and end menu

# FUNCTIONALITY DONE
# - connect cities DONE
# - generate initial city resources and pops DONE
# - look at how everything can be accessed from logic DONE
# - resource consumption DONE
#   - food every day DONE
#   - infrastructure use every day DONE
#   - building once a day DONE
# This is the brainstorm corner:
#   - investing resources -> limited to 1 per day (Should I?????)
#       1 def from 10 iron DONE
#       1 infrastructure from 1 wood DONE
#   - sending resources DONE
#   - think about the rest
# Options for actions can be
# - invest resources DONE
# - send resources DONE
# - ask for resources?
# - respond to an ask for resources?
# - trading resources???

# TESTING AND QA
# - play the game yourself for testing (Andras and Louis Glantfield)
#   - test difficulty
#   - test functionality (stuff you should be able to do and you should not)
#   - test for values (for example is 500 cap for building infrastructure too little, initial values, luck sacling, etc.)
# - make the comments better, @params and such
# - refactor code, especially the send and receive functions





def main_loop() -> None:
    # instantiate cities
    game = Game()
    # instantiate other variables
    # run loop
    is_win = True
    while game.round_num < 30:
        # start of day
        # - city start of day action triggered
        game.communicate_cities()
        game.trigger_first()
        game.consume_food()
        # disaster
        # - generate a disaster on x cities
        # - update all cities with info of where the disaster happened
        game.communicate_cities()
        game.trigger_climate()
        # response actions
        # - city response action triggered
        game.communicate_cities()
        game.trigger_response()
        # final actions
        # - city final action triggered
        game.communicate_cities()
        game.trigger_last()
        # damages counted
        # - total damages for the day counted and displayed (score)
        round_report = game.count_damages()
        print(f"Damage this round has been:", round_report["damage"])
        #if total damages exceed a certain amount OR if all of the days have passed
        #finish game and display score
        if game.is_game_over():
            print("Game Over")
            is_win = False
            break
        game.round_num += 1

    # use is_win variable to display loss or victory menu
    # display score, give option to run again



if __name__ == "__main__" :
    main_loop()
    while True:
        user_input = str(input("Play again? (y/n): "))
        if user_input == "y":
            main_loop()
        elif user_input == "n":
            break
        else:
            print("Please answer with y or n")
    print("Program ended")