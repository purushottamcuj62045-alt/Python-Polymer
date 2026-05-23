'''. Write a program that checks if a character entered by the user is a vowel or 
a consonant. If the input is neither a vowel nor a 
consonant (e.g., a number or special character),
 print "Invalid input."'''
 
word=input("Enter a letter :")

if word in "AEIOUaeiou":
    print("Entered Letter is Vowel")
elif word in "BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz":
    print("Entered letter is Constant")
else:
    print("Invalid input")
