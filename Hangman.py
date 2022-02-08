hangmanWord = input("Enter your word: ")
print("\n"*35)

letterList = list(hangmanWord)
wordLength = len(letterList)
dashList = []
guessesLeft = 10

for letter in letterList:
    dashList.append("-")

while("".join(dashList)!=hangmanWord):
    while guessesLeft>0:
        print(dashList)
        if("".join(dashList)==hangmanWord):
            print("\nWELL DONE")
            break
        guess = input("\nEnter your guess: ")
        if guess=="-":
            print("N/A")
        elif guess in letterList:
            print("\nCorrect!")
            dashList[letterList.index(guess)] = guess
            letterList[letterList.index(guess)] = "-"
        else:
            print("\nIncorrect")
            print("%d guesses left" %guessesLeft)
            guessesLeft-=1  
    if("".join(dashList)!=hangmanWord):
        print("UNLUCKY!")
    break


