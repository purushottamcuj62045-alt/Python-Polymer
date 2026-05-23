#Write a program to print a multiplication table for any number given by the user
num = int(input("Enter a number to print its multiplication table: "))
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
