
# no of guesses 9
# print no of guesses left
# No of guesses he took to finish
# game over

n=18
number_of_guesses=1
print("Number of guesses is limited to only 5 times: ")
while (number_of_guesses<=5):
    guess_number = int(input("Guess the number :\n"))
    if guess_number<18:
        print("you enter less number please input greater number.\n")
    elif guess_number>18:
        print("you enter greater number please input smaller number.\n ")
    else:
        print("you won\n")
        print(number_of_guesses,"no.of guesses you took to finish.")
        break
    print(5-number_of_guesses,"no. of guesses left")
    number_of_guesses = number_of_guesses + 1

if(number_of_guesses>5):
    print("Game Over")


### Below is the another way tried 
'''
n =  45
x = 5 
a = int(input("Enter a guess between 1 to 50:"))
while True:
    x -= 1 
    if a>n and x!=0:
        print("Enter lesser number:")
        a = int(input())
    elif a<n and x!=0:
        print("Enter greater number:")
        a = int(input())
    elif a==n:
        print("Congrats!! Correct guess")
        print("Attempts left = ", x)
        print("Attempts used = ", 9-x)
        break
    else:
        print("Game over!! out of attempts. Correct number was ", n)
        break
    
    '''



  
