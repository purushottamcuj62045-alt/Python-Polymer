'''Write a Python program to count the number of digits and letters in a string.
Input: 'AI2025'
Output: Letters: 2, Digits: 4
19. Write a Python program to check if a string contains only digits.
Input: '12345'
Output: True'''
puru='25f5d6sc35f4hvv6g0'
letter=0
number=0
for char in puru:
    if char.isalpha():
        letter+=1
    elif char.isdigit():
        number+=1

print("Letter",letter)
print("Numbers",number)
 