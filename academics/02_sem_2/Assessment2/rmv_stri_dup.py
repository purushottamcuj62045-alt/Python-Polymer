'''Write a Python program that: 
• Takes a list of strings as input (some strings may repeat). 
• Creates a set from the list to remove duplicates. 
• Then, for each unique string, counts its occurrences in the
 original list and displays the count.'''

pist = input("Enter the string value of list seprated with ',' :")
puru = pist.split(',')
pushu_set = set(puru)
count={}
for w in puru:
    if w not in count:
        coop=0
        for x in puru:
            if x == w:
                coop+=1

    count[w] = coop
print(count) 



