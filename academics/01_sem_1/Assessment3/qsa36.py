#Write a program to print numbers from 1-20 but write “EVEN” for even numbers and “ODD” for odd numbers
for i in range(1, 21):
    if i % 2 == 0:
        print("EVEN")
    else:
        print("ODD")