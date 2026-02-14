'''Q6. Write a function is_anagram(str1, str2) that checks whether two strings are anagrams of each 
other. The function should ignore spaces and be case-insensitive. 
Example: 
• is_anagram("listen", "silent") should return True. 
• is_anagram("hello", "world") should return False'''

#Taking input 

stri=input("Enter a word")
stri2=input("Enter 2nd word")
 
 #creating anagram function:

def is_anagram(str1, str2):
    # Remove spaces and convert to lowercase
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    # Sort the characters of both strings and compare
    if sorted(str1) == sorted(str2):
        print("Both word are anagrams:")
    else:
        print("Not an anagram")
# calling a function
is_anagram(stri,stri2)
