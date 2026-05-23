'''Write a Python program to sort words in a string alphabetically.
Input: 'Python is powerful and easy'
Output: 'Python and easy is powerful'''
stri="Luffy is main protoganist of one piece"
puru=stri.split()
puru.sort()
new=" ".join(puru)
print(new)
#<-----Ignore------->