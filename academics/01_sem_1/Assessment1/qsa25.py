#Problem Statement: A year is a leap year if:
#a. It is divisible by 400, or
#. It is divisible by 4 but not by 100.
 #Write a Python program to check if a given year is a leap year
year = int(input("Enter a year: "))
if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")
