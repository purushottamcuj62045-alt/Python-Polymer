#Write a program to display a factorial of a number input from user.
num=int(input("Enter a number"))
factorial=1
for i in range(1,num+1):
    factorial*=i
print(factorial)
