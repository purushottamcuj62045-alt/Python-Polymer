#<-----Write a Python program to count the frequency of each character in a string.------>
'''stri="hello world"
freq={}
for char in stri:
    if char in freq:
        freq[char] += 1
    else:
        freq[char] = 1
for char, count in freq.items():
    print(f"'{char}': {count}")'''
# --- IGNORE ---
st="hello world"
l=[]
count=0
for i in st:
    if i not in l:
        count+=1
    else:
        count=1
print(count)

