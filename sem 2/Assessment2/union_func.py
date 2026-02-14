'''Write a Python function that accepts two list with integer elements. 
Now design function code to perform union 
between these two lists and store the result in third list and print .'''


def union_of_lists(list1, list2):
    # Convert both lists to sets to remove duplicates
    set1 = set(list1)
    set2 = set(list2)
    
    # Perform union operation
    union_set = set1.union(set2)
    
    # Convert the union set back to a list
    union_list = list(union_set)
    
    return union_list   
# usage
pist =input("Enter the value of list seprated with ',' :")
list1 = pist.split(',')
qist =input("Enter the value of list seprated with ',' :")
list2 = qist.split(',')
result = union_of_lists(list1, list2)
print("Union of the two lists is:", result) 
