'''////Write a Python program to remove duplicate characters from a string.
Input: 'programming'
Output: 'progamin'/////'''
stri="programming"
puru=''
for char in stri:
    if char not in puru:
        puru+=char
print("New string",puru)
    