## This is the code for the Reversi game
## One player can play this against the computer
## For more information about Reversi, 
## see https://en.wikipedia.org/wiki/Reversi


import random
import datetime
import re

## Function to store the player's name
def ask_name():
    print(40*"-", "\nWelcome to Reversi!\n", 40*"-",sep="")
    name = input("Please type your name: ")
    print("Hello ", name, "! Let's play a game!\n", sep="")
    return name


## Class for bricks
class Brick():
    def __init__(self, row, col, state):
        self.row = row
        self.col = col
        self.state = state # either "x", "o" or " "

    def change_state(self, new_state):
        while True:
            try:
                self.state = new_state
                if new_state not in ["x", "o", " "]:
                    raise ValueError
            except (ValueError):
                print("The new state is not valid.")
            else:
                return self.state        


## Defining the size of the board
def choose_size():
    print("How big is the board supposed to be?\n\
Please choose an even number between 4 and 14: ")

    # check if the number is valid
    while True:
        try:
            size = int(input())
            if size < 4 or size > 14 or size%2 != 0:
                raise ValueError
        except (ValueError):
            print("That's not a valid number. Please choose an even number between 6 and 40: ")
        else:
            return size


## Creating a list with all bricks according to the board size
def create_list(size):
    # storing all bricks in a list
    bricks = []
    for i in range(1, size+1):
        for j in range(1,size+1):
            # assign bricks to Brick class
            brick = Brick(i, j, " ")
            bricks.append(brick)   
    return bricks
        

## Let the player choose his colour
def choose_colour():
    print("Do you want to be x or o?")
    while True:
        try:
            players_colour = input()
            if players_colour == "x":
                #set the colour of the opponent
                PC_colour = "o" 
            else:
                PC_colour = "x"
            if players_colour not in ["x","o"]:
                raise ValueError
        except (ValueError):
            print("That's not a valid option. Please type either 'x' or 'o'.")
        else:
            return players_colour, PC_colour 
            

## Print gameboard
def print_board(bricks, size):
    print("\n    ", end="")
    
    # ______1___2___3___4...
    for i in range(1, size+1):
        print("{:^4}".format(i), end="")

    # ____+---+---+---+---+...
    print("\n   ","+---"*size, "+\n", sep="", end="")
    
    for i in range (size): #i = row
        print("{:<3}".format(i+1), "|", sep="", end="") # 1 |
        for brick in bricks:
            if brick.row == i+1:
                print("{:^3}".format(brick.state), "|", sep="", end="")
        print("\n   ", "+---"*size, "+", sep="")


## Starting position of the first four bricks in the middle of the board
def start_position(bricks, size):
    # setting the state of the initial bricks
    for brick in bricks:
        if (brick.row == size/2 and brick.col == size/2)\
        or (brick.row == size/2+1 and brick.col == size/2+1):
            brick.change_state("x")
        if (brick.row == size/2 and brick.col == size/2+1)\
        or (brick.row == size/2+1 and brick.col == size/2):
            brick.change_state("o")            

## Players turn
def players_turn(bricks, players_colour, PC_colour, size, name):
    print("Please enter the number of row and column you want to play, seperated by a comma.\n\
If you need some help, type 'hint'. ")
    available_bricks = []
    for brick in bricks:
        if brick.state == " ":
            available_bricks.append(brick)
                        
    while True:
        try:
            choice = input()
            
            # check if choice have to be in the format <digit><,><digit>
            pattern = r"\d,\d"
            
            # give the player a hint, if he asks for it
            if choice == "hint":
                give_hint(bricks, players_colour, PC_colour, size)

            # continue if the input is according to the pattern
            elif re.match(pattern, choice):
                pass
            else:
                print("You have to provide the information in the format <row>,<column>")
                raise ValueError
            
            row = int(choice.split(",")[0])
            col = int(choice.split(",")[1])

            for brick in bricks:
                # brick can't already belong to one colour / can't already have a state
                if brick.row == row and brick.col == col:
                    if brick not in available_bricks:
                        print("This brick is not available anymore.")
                        raise ValueError

            # 2. rule: brick has to touch another one of the oppponents colour:
            if first_rule(bricks, row, col, PC_colour) == False:
                print("This brick doesn't touch another one of your opponent's colour.")
                raise ValueError
            
            # 2. rule: there has to be another brick of the players colour in the same line
            elif second_rule(bricks, row, col, players_colour, PC_colour, size) == False:
                print("The brick has to be in direct line with one of your bricks.")
                raise ValueError
            
        except ValueError:
            if choice == "hint":
                print("Then let's go!")
            else:
                print("Try again!")

        else:
            #change state of the bricks according to the played move
            bricks_to_flip = second_rule(bricks, row, col, players_colour, PC_colour, size)
            for brick in bricks_to_flip:
                brick.change_state(players_colour)
                
            #change colour of the played brick
            for brick in bricks:
                if brick.col == col and brick.row == row:
                    brick.change_state(players_colour)
            break
                                       
    print_board(bricks, size)
    if check_game_finished(bricks, PC_colour, players_colour, players_colour, PC_colour, size, name) == "Skip":
        print("There is no possible move for the computer. It's your turn again.\n")
        players_turn(bricks, players_colour, PC_colour, size, name)
    else:
        input("Press Enter to let the computer play")
        computers_turn(bricks, PC_colour, players_colour, size, name)
            



def computers_turn(bricks, PC_colour, players_colour, size, name):
    print("\nNow your big opponent, the COMPUTER plays!\n")
    #create list with all available bricks    
    available_bricks = []
    for brick in bricks:
        if brick.state == " ":
            available_bricks.append(brick)
            
    while True:
        try:
            if len(available_bricks)==0:
                print("There are no moves left")
                check_game_finished(bricks, players_colour, PC_colour, players_colour, PC_colour, size, name)
                break

            # else let the computer play one of the possible moves
            # find out which move is possible by testing each of the available bricks
            choosen_brick = random.choice(available_bricks) 
            available_bricks.remove(choosen_brick)

            #for each move the first and the second rule has to be fulfilled, otherwise raise ValueError
            if first_rule(bricks, choosen_brick.row, choosen_brick.col, players_colour) == False:
                raise ValueError
            elif second_rule(bricks, choosen_brick.row, choosen_brick.col, PC_colour, players_colour, size) == False:
                raise ValueError
                        
        except ValueError:
            pass
        
        else:
            bricks_to_flip = second_rule(bricks, choosen_brick.row, choosen_brick.col, PC_colour, players_colour, size)
            for brick in bricks_to_flip:
                brick.change_state(PC_colour)
            for brick in bricks:
                if brick.col == choosen_brick.col and brick.row==choosen_brick.row:
                    brick.change_state(PC_colour)
                    print("The computer played the brick", choosen_brick.row, "|", choosen_brick.col)
            break
                    
    print_board(bricks, size)
    if check_game_finished(bricks, players_colour, PC_colour, players_colour, PC_colour, size, name) == "Skip":
        print("There is no possible move for you. It's the computer's turn again.")
        input("Press Enter to let the computer play")
        computers_turn(bricks, PC_colour, players_colour, size, name)
    else:
        players_turn(bricks, players_colour, PC_colour, size, name)


## First rule: Check if the brick touches another brick of the opponent's colour
def first_rule(bricks, row, col, opp_colour):
    
    # create a list directions with the directions of the touched bricks (not of the new brick!)
    # diagional/vertical left/right up/down
    directions = []
    for brick in bricks:
        if brick.state == opp_colour:
            if brick.row == row-1:
                if brick.col == col-1:
                    directions.append("diagonal left up")
                if brick.col == col:
                    directions.append("vertical up")
                if brick.col == col+1:
                    directions.append("diagonal right up")
            if brick.row == row:
                if brick.col == col-1:
                    directions.append("horizontal left")
                if brick.col == col+1:
                    directions.append("horizontal right")
            if brick.row == row+1:
                if brick.col == col-1:
                    directions.append("diagonal left down")
                if brick.col == col:
                    directions.append("vertical down")
                if brick.col == col+1:
                    directions.append("diagonal right down")
    if len(directions) == 0:
        return False #brick doesn't touch a brick of the opponent's colour
    else:
        return directions

## List with temporary bricks to flip (needed for the second rule)
def create_temp(direction, directions, brick, temp_bricks, colour):
    done = False
    temp_bricks.append(brick)

    # count the own bricks of the player's colour
    own_bricks = 0
    for brick in temp_bricks:
        if brick.state == colour:
           own_bricks += 1

    # check if there is an empty brick before the next brick of the player's colour
    if brick.state == " " and own_bricks == 0: #invalid move
        directions.remove(direction)
        done = True
    return done, temp_bricks
  
## Second rule: Find another brick of the player's colour in the same direction as of the touched brick
## function returns a list with the bricks that have to be flipped
def second_rule(bricks, row, col, colour, opp_colour, size):
    directions = first_rule(bricks, row, col, opp_colour)
    bricks_to_flip = []
    temp_bricks = []

    #check for every directions if there are bricks to flip and if so add them to bricks_to_flip list
    if "diagonal left up" in directions:
        done = False
        for brick in reversed(bricks):
            
            # add all the bricks in the according direction to the list bricks_to_flip
            # and break if an empty brick is found
            for i in range(row-1,1,-1):
                for j in range(col-1,1,-1):
                    if brick.row == i and brick.col == j\
                       and row - brick.row == col - brick.col:

                        # add brick to the list of temporary bricks to flip
                        done, temp_bricks = create_temp("diagonal left up", directions, brick, temp_bricks, colour)
                    if done == True:
                        break
                    
            # check if a brick of the player's colour is found in the same direction and if so break the loop
            if brick.row < row and brick.col < col \
               and row - brick.row == col - brick.col \
               and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            
            # check if end of board is reached and still there is no other brick of the player's colour
            elif ((brick.row == 1 and brick.col == col - row + 1)\
                  or (brick.col == 1 and brick.row == row - col + 1))\
                  and brick.state !=colour: #invalid move
                directions.remove("diagonal left up")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list

    if "vertical up" in directions:
        done = False
        for brick in reversed(bricks):
            for i in range(row-1,1,-1):
                if brick.row ==i and brick.col == col:
                    done, temp_bricks = create_temp("vertical up", directions, brick, temp_bricks, colour)
                if done == True:
                    break
            if brick.row < row and brick.col == col and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif brick.row == 1 and brick.col == col and brick.state !=colour: #invalid move
                directions.remove("vertical up")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list

    if "diagonal right up" in directions:
        done = False
        for brick in reversed(bricks):
            for i in range(row-1,1,-1):
                for j in range(col+1,size):
                    if brick.row == i and brick.col == j\
                       and row - brick.row == brick.col - col:
                        done, temp_bricks = create_temp("diagonal right up", directions, brick, temp_bricks, colour)
                    if done == True:
                        break
            if brick.row < row and brick.col > col\
               and row - brick.row == brick.col - col \
               and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif ((brick.row == 1 and brick.col == row + col - 1)\
                  or (brick.col == size and brick.row == row + col - size))\
                  and brick.state !=colour: #invalid move
                directions.remove("diagonal right up")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list
                        
    if "horizontal left" in directions:
        done = False
        for brick in reversed(bricks):
            for i in range(col-1,1,-1):
                if brick.row ==row and brick.col == i:
                    done, temp_bricks = create_temp("horizontal left", directions, brick, temp_bricks, colour)
                if done == True:
                    break
            if brick.row == row and brick.col < col and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif brick.row == row and brick. col == 1 and brick.state != colour: #invalid move
                directions.remove("horizontal left")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list

    if "horizontal right" in directions:
        done = False
        for brick in bricks:
            for i in range(col+1,size):
                if brick.row ==row and brick.col == i:
                    done, temp_bricks = create_temp("horizontal right", directions, brick, temp_bricks, colour)
                if done == True:
                    break
 
            if brick.row == row and brick.col > col and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif brick.row == row and brick.col == size and brick.state != colour: #invalid move
                directions.remove("horizontal right")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list

    if "diagonal left down" in directions:
        done = False
        for brick in bricks:
            for i in range(row+1,size):
                for j in range(col-1,1,-1):
                    if brick.row == i and brick.col == j\
                       and brick.row - row == col - brick.col:
                        done, temp_bricks = create_temp("diagonal left down", directions, brick, temp_bricks, colour)
                    if done == True:
                        break
                if done == True:
                    break
            if brick.row > row and brick.col < col\
               and brick.row - row == col - brick.col\
                and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif ((brick.row == size and brick.col == row + col - size)\
                 or (brick.col == 1 and brick.row == row + col - 1))\
                 and brick.state !=colour: #invalid move
                directions.remove("diagonal left down")
                done = True
                break

            if done == True:
                break
        temp_bricks = [] #empty temporary list

    if "vertical down" in directions:
        done = False
        for brick in bricks:
            for i in range(row+1,size):
                if brick.row ==i and brick.col == col:
                    done, temp_bricks = create_temp("vertical down", directions, brick, temp_bricks, colour)
                if done == True:
                    break
            if brick.state == colour and brick.col == col and brick.row > row: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif (brick.row == size and brick.col == col) and brick.state !=colour: #invalid move
                directions.remove("vertical down")
                done = True
                break
            if done == True:    
                break
        temp_bricks = [] #empty temporary list
            
    if "diagonal right down" in directions:
        done = False
        for brick in bricks:
            for i in range(row+1,size):
                for j in range(col+1,size):
                    if brick.row == i and brick.col == j\
                       and brick.row - row == brick.col - col:
                        done, temp_bricks = create_temp("diagonal right down", directions, brick, temp_bricks, colour)
                    if done == True:
                        break
                if done == True:
                    break
            if brick.row > row and brick.col > col\
               and brick.row - row == brick.col - col\
                and brick.state == colour: #valid move
                bricks_to_flip.extend(temp_bricks)
                done = True
                break
            elif ((brick.row == size and brick.col == col - row + size)\
                    or (brick.col == size and brick.row == row - col + size))\
                  and brick.state !=colour: #invalid move
                directions.remove("diagonal right down")
                done = True
                break
            if done == True:
                break
        temp_bricks = [] #empty temporary list
                        
    if len(directions)==0:
        return False
    else:
        return bricks_to_flip
        
        
## function for checking the points of the computer and the player        
def check_points(bricks, players_colour, PC_colour):
    players_points = 0
    computers_points = 0
    for brick in bricks:
        if brick.state == players_colour:
            players_points +=1
        elif brick.state == PC_colour:
            computers_points +=1
    print("PC points:", computers_points, "   \
Your points:", players_points)
    return players_points, computers_points
            

## check if there are more possible moves
## if not the game is finished
## if only not for the current player, then he has to skip the turn
def check_game_finished(bricks, colour, opp_colour, players_colour, PC_colour, size, name):
    players_points, computers_points = check_points(bricks, players_colour, PC_colour)

    available_bricks = []
    for brick in bricks:
        if brick.state == " ":
            available_bricks.append(brick)

    # check if there are anymore moves possible for either of the player
    possible_moves = 0 #possible moves for the current player
    opp_possible_moves = 0 #possible moves for the other player
    for brick in available_bricks:
        if first_rule(bricks, brick.row, brick.col, opp_colour) != False:
            if second_rule(bricks, brick.row, brick.col, colour, opp_colour, size)!= False:
                possible_moves +=1 # possible moves for the current players
        if first_rule(bricks, brick.row, brick.col, colour) != False:
            if second_rule(bricks, brick.row, brick.col, opp_colour, colour, size)!= False:
                opp_possible_moves +=1 # possible moves for the other player

    if possible_moves == 0 and opp_possible_moves == 0:
        print("The game is finished")
        if players_points > computers_points:
            print("Congratulations, you won!")
            write_file(players_points, name)
        elif computers_points > players_points:
            print("Loser! The computer beat you!")
        elif players_points == computers_points:
            print("Draw!")        
        
        
        while True:
            try:
                choice = input("You wanna play again? Answer 'yes' or 'no'\n")
                if choice in ("yes", "Yes", "y", "Y"):
                    start_game(name)
                elif choice in ("no", "No", "n", "N"):
                    print("Goodbye and have a nice day")
                    quit()
                elif choice not in ("yes", "Yes", "y", "Y", "no", "No", "n", "N"):
                    raise ValueError
            except ValueError:
                print("What do you want?")
            else:
                break
            
    # if the current player can't play, but there are possible moves for the opponent        
    elif possible_moves == 0 and opp_possible_moves > 0:
        return "Skip" 

## Write new highscore to a textfile
def write_file(highscore, name):
    try:
        with open("Highscore.txt", "r") as text:
            content = text.readlines()
        old_highscore = 0
        for i, word in enumerate(content[-1].split()):
            if word == "scored":
                old_highscore= content[-1].split()[i+1]
    except IOError: 
        old_highscore = 0 
    if highscore > int(old_highscore):
        print("Even more awesome, you reached a new highscore!")
        timestamp = (datetime.datetime.now().strftime("%d %b %Y, %H:%M"))
        new_entry = [50*"*" + "\nReversi Highscore\n" + 50*"*" + \
                     str("\n" + name + " scored " + str(highscore) + " points " + timestamp)]
        with open("Highscore.txt","w") as text:
            text.writelines(new_entry)

## Give hint of possible moves for the player
def give_hint(bricks, colour, opp_colour, size):
    available_bricks = []
    for brick in bricks:
        if brick.state == " ":
            available_bricks.append(brick)
    possible_moves = []
    for brick in available_bricks:
        if first_rule(bricks, brick.row, brick.col, opp_colour) != False:
            if second_rule(bricks, brick.row, brick.col, colour, opp_colour, size)!= False:
                possible_moves.append(brick)
    no_possible_moves = len(possible_moves)
    #1. Hint
    print("There are", no_possible_moves, "possible bricks you could choose.")
    hint = random.choice(possible_moves)
    print("Try row" , hint.row)
    choice = input("If you need another hint, answer 'yes' or else type 'no'\n")
    if choice in ("yes", "Yes", "y", "Y"):
        print("Check out column:" , hint.col)


def start_game(name):        
    size = choose_size()
    bricks = create_list(size)
    players_colour, PC_colour = choose_colour()
    start_position(bricks, size)
    print_board(bricks, size)
    players_turn(bricks, players_colour, PC_colour, size, name)  

name = ask_name()    
start_game(name)


