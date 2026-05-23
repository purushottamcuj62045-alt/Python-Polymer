'''Write a Python program that takes two lists as input and: 
• Converts them into sets. 
• Computes and displays the union, intersection, and difference of these sets. 
• Checks if one set is a subset or superset of the other. 
• Finds the symmetric difference of the two sets. 
• Output the results in a sorted manner.'''
 
#Taking input seprated with commasfor creating a list

pist =input("Enter the value of list seprated with ',' :")
list1 = pist.split(',')
qist =input("Enter the value of list seprated with ',' :")
list2 = qist.split(',')

#converting into sets

set1 = set(list1)
set2 = set(list2)
print("Set 1:", set1)
print("Set 2:", set2)

# Taking union , intersection , difference

uni = sorted(set1.union(set2))
intersec = sorted(set1.intersection(set2))
difff = sorted(set1.difference(set2))

print("Union of set1 and set2 is:",uni)
print("intersection of set1 and set2 is:",intersec)
print("Difference of set1 and set2 is :",difff)

#Checks if one set is a subset or superset of the other. 

if set2.issubset(set2) == 1:
    print("Set2 is subset of Set1:😒")
elif set1.issuperset(set2) == 1:
    print("Set1 is superset of set2😑")

#Finds the symmetric difference of the two sets. 

syst = sorted(set1.symmetric_difference(set2)) 
print("Symmetric difference of Set1 and set2 is:",syst)