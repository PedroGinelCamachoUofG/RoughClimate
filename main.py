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
import time

def main_loop() -> None:
    # instantiate cities
    game = Game()
    # instantiate other variables
    # run loop
    is_win = True
    while game.round_num < 30:
        # start of day
        # - city start of day action triggered
        time.sleep(1)
        game.communicate_cities()
        game.trigger_first()
        game.consume_food()
        # disaster
        # - generate a disaster on x cities
        # - update all cities with info of where the disaster happened
        time.sleep(1)
        game.communicate_cities()
        game.trigger_climate()
        # response actions
        # - city response action triggered
        time.sleep(1)
        game.communicate_cities()
        game.trigger_response()
        # final actions
        # - city final action triggered
        time.sleep(1)
        game.communicate_cities()
        game.trigger_last()
        # damages counted
        # - total damages for the day counted and displayed (score)
        round_report = game.count_damages()
        print(f"Damage this round has been:", round_report["damage"])
        time.sleep(1)
        #if total damages exceed a certain amount OR if all of the days have passed
        #finish game and display score
        if game.is_game_over():
            print("Game Over")
            is_win = False
            break

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