#<------Write a Python program to count the number of vowels in a string------>
stri="Luffy is main protaganist of one piece."
vowels="aeiouAEIOU"
count = 0
for char in stri:
    if char in vowels:
        count += 1
print("Number of vowels in the string:", count)