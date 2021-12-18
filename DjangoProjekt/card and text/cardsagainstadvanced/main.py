# Program to read a random question or phrase from a file and print the game card with the user's response
import random
import time
 
# Open the Cards Against text file
file1 = open('cards.txt','r')

# Open the Words text file
file2 = open('words.txt','r')
 
# Read the both files and store each line in a a seperate list
cardText = file1.readlines()
options = file2.readlines()

# Choose a random question card
cardText = file1.readlines()
card = random.choice(cardText)
 
# Pick your answer cards
option1 = random.choice(options)
option2 = random.choice(options)
option3 = random.choice(options)
 
#Display the random question card
print(card)
time.sleep(1)
  
#Display the options
print("A. " + option1) 
print("B. " + option2) 
print("C. " + option3) 
choice = input(">>> ")
if choice.upper() == "A":
  card = card.replace("blank", option1)
elif choice.upper() == "B":
  card = card.replace("blank", option2)
else:
  card = card.replace("blank", option3)
  
#Print question card with your players answer
print(card)