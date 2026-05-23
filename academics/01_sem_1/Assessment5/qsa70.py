'''////Write a Python program to find the longest word in a sentence.
Input: 'Deep learning improves computer vision'
Output: 'learning////'''
stri='Deep learning improves computer vision'

words=stri.split()
longest=max(words ,key=len)
print(longest)
#<-----Ignore------->