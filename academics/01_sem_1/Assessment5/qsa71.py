'''////Write a Python program to check if two strings are anagrams.
Input: 'listen', 'silent'
Output: True////'''
stri1="listen"
stri2="silent"
if sorted(stri1)==sorted(stri2):
    print("Both strings are anagrams")
else:
    print("NOt an Anagrams")
#<-----Ignore------->