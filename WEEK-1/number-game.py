#  Number guessing game

import random

correct_number = random.randrange(0,11)

i = 4
while i > -1:
    value = int(input("Enter Your Guess: "))
    if value == correct_number:
        print("You Guessed Right!")
        break
    else:
        print(f"Wrong Guess, Try again. {i} more guesses")
    i -= 1

print(f"The correct number is {correct_number}")