'''Write a Python program to count the number of vowels in a string.
Input: 'Education'''
pyt=input("Enter a string ")
a='aeiouAEIOU'
count=0
for char in pyt:
    if char in a:
        count+=1
print(count)