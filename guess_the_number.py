import random

print("\nHello Player\nLet's play a game. Guess a number between 0 to 10.\nYou have 3 chances to gues the correct number.")
number = random.randint(0,10)
counter = 0

while(counter<3):
    guess = int(input("\nEnter your guess: "))
    if guess == number:
        print("\nYou Won!, you have correctly guessed the number {} in {} attempts\n".format(number, counter+1))
        break
    elif guess>=11 or guess<0:
        print("You can only guess numbers from 0 to 10")
    elif guess > number:
        print("Guess a lower number")
    elif guess < number:
        print("Guess a higher number")
    counter+=1
if counter == 3:
    print("\n\n\nOops! you lost, the correct number was {}\n\n\n".format(number))