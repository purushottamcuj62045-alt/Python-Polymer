'''. Write a function is_anagram(str1, str2) that checks whether two 
strings are anagrams of each other. The function should ignore spaces
 and be case-insensitive. 
Example: 
•	is_anagram("listen", "silent") should return True. 
•	is_anagram("hello", "world") should return False. 

'''
def is_anagram(str1, str2):
    # Remove spaces and convert to lowercase
    str1 = str1.replace(" ", "").lower()
    str2 = str2.replace(" ", "").lower()
    
    # Sort the characters and compare
    return sorted(str1) == sorted(str2)
# Example usage
str1 = input("Enter the first string: ")
str2 = input("Enter the second string: ")
print("Are the two strings anagrams?", is_anagram(str1, str2))
#<-- IGNORE --->
