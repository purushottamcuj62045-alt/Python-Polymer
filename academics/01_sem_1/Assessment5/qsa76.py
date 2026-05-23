'''Write a Python program to replace vowels in a string with '*'.
Input: 'Education'
Output: '*d*c*t**n'''
stri="Education"
vowels="aeiouAEIOU"
new_stri=""
for char in stri:
    if char in vowels:
        new_stri += "*"
    else:
        new_stri += char
print(new_stri)
#<-----Ignore------->