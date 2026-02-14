#<------- Write a Python program to check whether a string is palindrome or not.
stri=input("Enter a string")
n=len(stri)
revs=stri[n: :-1]
if stri==revs:
    print("Palindrone!")
else:
    print("Not a palidrone")