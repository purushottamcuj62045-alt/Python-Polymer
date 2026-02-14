#Problem Statement: Given a character, check if it is a vowel or consonant.
#Example:
#Input: e
#Output: Vowel
char = input("Enter a character: ").lower()
if char in 'aeiou':
    print("Vowel")
else:
    print("Consonant")
    