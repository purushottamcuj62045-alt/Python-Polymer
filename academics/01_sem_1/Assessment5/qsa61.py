#<------- Write a Python program to check whether a string is palindrome or not.------->
puru=input("Enter a string")
n=len(puru)
urup=puru[n: :-1]
if puru==urup:
    print("Palindrone")
else:
    print("not a palindrone")