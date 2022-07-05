from config import dictionaryloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import finalprize

import time
import random
import csv
from string import ascii_lowercase

def welcomeMessage():
    print("Welcome to Wheel of Fortune!")
    time.sleep(2)
    print("This game is to be played by 3 people, and will last 2 rounds - unless you have the most money, in which case you get to play the final bonus round!")
    time.sleep(5)

def readDictionaryFile():
    with open(dictionaryloc, "r") as file:

        puzzles_categories = []
        csv_reader = csv.reader(file)
        for row in csv_reader:
            round = row[3]

            if round.find("B") == -1:
                round = "normal"

            else:
                round = "final"

            puzzles_categories.append({"puzzle":row[0], "category":row[1], "round":round})

        return puzzles_categories

def readWheelTxtFile():
    wheel_values = []

    file = open(wheeltextloc, "r")
    for row in file:
        wheel_values.append(row.strip())
    
    return wheel_values

def getPlayerInfo():
    players = []
    for i in range(3):

        invalid_name = True
        while invalid_name:
            name = input("Please enter player " + str(i + 1) + "'s name: ")

            valid = input("Are you sure player " + str(i + 1) + "'s name is " + name + "? [y/n]: ")
            if valid == "y":
                invalid_name = False
        
        players.append({"name":name, "round money":0, "total money":0})
    
    return players

def getWord(puzzles_categories, round):
    round_puzzles_categories = list(filter(lambda item: item["round"] == round, puzzles_categories))
    puzzle = round_puzzles_categories[random.randint(0, len(round_puzzles_categories) - 1)]

    for i in range(len(puzzles_categories)):
        if puzzles_categories[i]["puzzle"] == puzzle["puzzle"]:
            del puzzles_categories[i]
            break

    del puzzle["round"]
    return puzzle

def getHiddenWord(puzzle):
    hidden_puzzle = ""

    for c in puzzle:
        if c != " ":
            hidden_puzzle += "_"
        
        else:
            hidden_puzzle += " "

    return hidden_puzzle

def getUnchosenLetters():
    unchosen_letters = []
    for c in ascii_lowercase:
        unchosen_letters.append(c)

    return unchosen_letters

def getRandomPlayerTurn():
    return random.randint(0, 2)

def wofRoundMenu(hidden_puzzle, category, word_bank, players):
    print("")
    print(hidden_puzzle)
    print("")
    print(category)
    print("")
    print(word_bank)
    print("")
    print("Round Scores")
    print(players[0]["name"] + " " + str(players[0]["round money"]) + " | " + players[1]["name"] + " " + str(players[1]["round money"]) + " | " + players[2]["name"] + " " + str(players[2]["round money"]))
    print("")
    print("1. Spin the Wheel")
    print("2. Buy a Vowel")
    print("3. Solve the Puzzle")
    print("")

def nextPlayer(players, player_turn):
    print("Sorry " + players[player_turn]["name"] + ", you lost your turn.")

    if player_turn == 2:
        player_turn = 0
    else: player_turn += 1

    print(players[player_turn]["name"] + " you're up.")

    return player_turn

def spinWheel(wheel_values):
    return wheel_values[random.randint(0, len(wheel_values) - 1)]

def revealHiddenWord(hidden_puzzle, puzzle, letter):
    hidden_puzzle_list = [char for char in hidden_puzzle]

    i = 0
    for c in puzzle:
        if c == letter.upper() or c == "-":
            hidden_puzzle_list[i] = c
        
        i += 1

    return "".join(hidden_puzzle_list)

def setPlayersRoundOver(players, player_turn):
    players[player_turn]["total money"] += players[player_turn]["round money"]

    for i in range(3):
        players[i]["round money"] = 0

    return players

def chooseFinalRoundPlayer(players):
    highest_money_player_turn = 0
    
    for i in range(1, 3):
        print(i)
        if players[i]["total money"] > players[highest_money_player_turn]["total money"]:
            highest_money_player_turn = i

    return highest_money_player_turn

def revealRSTLNE(unchosen_letters, hidden_puzzle, puzzle):
    for c in ['r', 's', 't', 'l', 'n', 'e']:
        unchosen_letters.remove(c)

        count = [char for char in puzzle].count(c.upper())

        if count != 0:
            hidden_puzzle = revealHiddenWord(hidden_puzzle, puzzle, c)

    return hidden_puzzle

def wofRound(puzzles_categories, wheel_values, players):
    puzzle = getWord(puzzles_categories, "normal")
    hidden_puzzle = getHiddenWord(puzzle["puzzle"])
    unchosen_letters = getUnchosenLetters()

    player_turn = getRandomPlayerTurn()

    print(players[player_turn]["name"] + " is up first!")
    print("Here is the puzzle, category, and your letter bank.")

    round_over = False
    while not round_over:
        wofRoundMenu(hidden_puzzle, puzzle["category"], " ".join(unchosen_letters), players)
        menu_choice = input(players[player_turn]["name"] + " what would you like to do? [1-3]: ")
        if menu_choice == "1":
            print("")
            print("You spin the wheel.")

            time.sleep(2)
            wheel_value = spinWheel(wheel_values)

            print("")
            print(wheel_value)
            print("")

            if wheel_value == "Lose a Turn":
                player_turn = nextPlayer(players, player_turn)

            elif wheel_value == "Bankrupt":
                print("Unfortunately you lost all your round money.")
                players[player_turn]["round money"] = 0
                player_turn = nextPlayer(players, player_turn)
            
            else:
                print("")
                valid_consonant = False

                while not valid_consonant:
                    consonant = (input("Choose a consonant: ")).lower()
                    if not consonant.isalpha() or len(consonant) != 1:
                        print("Please choose a valid consonant.")

                    elif consonant not in unchosen_letters:
                        print("That letter has already been chosen.")

                    elif consonant in ['a', 'e', 'i', 'o', 'u']:
                        print("Please choose a consonant.")

                    else: valid_consonant = True

                unchosen_letters.remove(consonant)

                count = [char for char in puzzle["puzzle"]].count(consonant.upper())

                if count == 0:
                    print("There are no " + consonant + "'s.")
                    player_turn = nextPlayer(players, player_turn)

                else:
                    print("There are " + str(count) + " " + consonant + "'s.")
                    hidden_puzzle = revealHiddenWord(hidden_puzzle, puzzle["puzzle"], consonant)
                    players[player_turn]["round money"] += int(wheel_value) * count

        elif menu_choice == "2":
            if players[player_turn]["round money"] >= vowelcost:
                valid_vowel = False

                while not valid_vowel:
                    vowel = (input("Choose a vowel: ")).lower()
                    if not vowel.isalpha() or len(vowel) != 1:
                        print("Please choose a valid vowel.")

                    elif vowel not in unchosen_letters:
                        print("That letter has already been chosen.")

                    elif vowel not in ['a', 'e', 'i', 'o', 'u']:
                        print("Please choose a vowel.")

                    else: valid_vowel = True

                unchosen_letters.remove(vowel)

                count = [char for char in puzzle["puzzle"]].count(vowel.upper())

                if count == 0:
                    print("There are no " + vowel + "'s.")
                    player_turn = nextPlayer(players, player_turn)

                else:
                    print("There are " + str(count) + " " + vowel + "'s.")
                    hidden_puzzle = revealHiddenWord(hidden_puzzle, puzzle["puzzle"], vowel)
                    players[player_turn]["round money"] -= vowelcost

            else:
                print("Sorry " + players[player_turn]["name"] + " you don't have enough money to buy a vowel. You need $250 for each vowel.")

        elif menu_choice == "3":
            valid_solve = False

            while not valid_solve:
                solve = (input("What are you thinking?: ")).lower()

                if len(solve) != len(puzzle["puzzle"]):
                    print("Please try to solve the puzzle where the words match the hidden puzzle.")

                else:
                    valid_solve = True

            if solve.upper() == puzzle["puzzle"].upper():
                print("You got it!")
                print("")
                time.sleep(2)

                print(players[player_turn]["name"] + ", you just added $" + str(players[player_turn]["round money"]) + " to your total winnings.")
                players = setPlayersRoundOver(players, player_turn)
                
                time.sleep(2)
                print("")
                print("Total Scores")
                print(players[0]["name"] + " " + str(players[0]["total money"]) + " | " + players[1]["name"] + " " + str(players[1]["total money"]) + " | " + players[2]["name"] + " " + str(players[2]["total money"]))
                print("")
                time.sleep(5)

                round_over = True

            else:
                print("I'm sorry, but that's incorrect.")
                player_turn = nextPlayer(players, player_turn)    

        else:
            print("Invalid selection, try again.")

def wofFinalRound(puzzles_categories, players):
    player_turn = chooseFinalRoundPlayer(players)

    print("Thank you to our contestants for playing today.")
    time.sleep(1)

    print("")
    print("Congratulations " + players[player_turn]["name"] + ", you will be playing in the final round!")

    puzzle = getWord(puzzles_categories, "final")
    hidden_puzzle = getHiddenWord(puzzle["puzzle"])
    unchosen_letters = getUnchosenLetters()

    print("Here is the puzzle, category, and your letter bank.")
    print("")
    print("We've given you the letters R, S, T, L, N, and E.")

    hidden_puzzle = revealRSTLNE(unchosen_letters, hidden_puzzle, puzzle["puzzle"])

    print("")
    print(hidden_puzzle)
    print("")
    print(puzzle["category"])
    print("")
    print(" ".join(unchosen_letters))
    print("")

    time.sleep(2)
    print("You will choose 3 consonants and a vowel, then make one attempt to solve the puzzle.")
    time.sleep(2)

    for i in range(3):
        valid_consonant = False
        while not valid_consonant:
            consonant = (input("Choose consonant #" + str(i + 1) + ": ")).lower()
            if not consonant.isalpha() or len(consonant) != 1:
                print("Please choose a valid consonant.")

            elif consonant not in unchosen_letters:
                print("That letter has already been chosen.")

            elif consonant in ['a', 'e', 'i', 'o', 'u']:
                print("Please choose a consonant.")

            else: valid_consonant = True

        unchosen_letters.remove(consonant)

        count = [char for char in puzzle["puzzle"]].count(consonant.upper())

        if count != 0:
            hidden_puzzle = revealHiddenWord(hidden_puzzle, puzzle["puzzle"], consonant)

    valid_vowel = False
    while not valid_vowel:
        vowel = (input("Choose a vowel: ")).lower()
        if not vowel.isalpha() or len(vowel) != 1:
            print("Please choose a valid vowel.")

        elif vowel not in unchosen_letters:
            print("That letter has already been chosen.")

        elif vowel not in ['a', 'e', 'i', 'o', 'u']:
            print("Please choose a vowel.")

        else: valid_vowel = True

    unchosen_letters.remove(vowel)

    count = [char for char in puzzle["puzzle"]].count(vowel.upper())

    if count != 0:
        hidden_puzzle = revealHiddenWord(hidden_puzzle, puzzle["puzzle"], vowel)

    print("")
    print("Here is your puzzle, good luck. You have one attempt.")

    print("")
    print(hidden_puzzle)
    print("")
    print(puzzle["category"])
    print("")

    valid_solve = False
    while not valid_solve:
        solve = (input("What are you thinking?: ")).lower()

        if len(solve) != len(puzzle["puzzle"]):
            print("Please try to solve the puzzle where the words match the hidden puzzle.")

        else:
            valid_solve = True

    if solve.upper() == puzzle["puzzle"].upper():
        print("You got it!")
        print("")
        time.sleep(2)

        players[player_turn]["round money"] = finalprize

        players = setPlayersRoundOver(players, player_turn)
        print(players[player_turn]["name"] + ", you just won the grand prize of $" + str(players[player_turn]["round money"]) + "!")
        time.sleep(2)
        print("")

    else:
        print("I'm sorry, but that's incorrect.")
        print("")
        print("The answer was " + puzzle["puzzle"] + ".")
        time.sleep(3)
        print("") 

    print("Congratulations " + players[player_turn]["name"] + ", you walk away with $" + str(players[player_turn]["total money"]) + ".")
    print("")
    time.sleep(5)
    print("Thanks for playing!")

    return

def main():
    # welcomeMessage()

    # puzzles_categories = readDictionaryFile()
    # wheel_values = readWheelTxtFile()
    # players =  getPlayerInfo()
    players = [{"name":"George", "round money":0, "total money":0}, {"name":"Peter", "round money":0, "total money":0}, {"name":"Amy", "round money":0, "total money":0}]   
    chooseFinalRoundPlayer(players)

    # for i in range(maxrounds):
    #     if i in [0,1]:
    #         wofRound(puzzles_categories, wheel_values, players)
    #     else:
    #         wofFinalRound(puzzles_categories, players)
     
if __name__ == "__main__":
    main()
