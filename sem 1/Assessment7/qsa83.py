'''Write a Python function that accepts two list with integer elements. 
Now design function code to perform union between these two lists and store 
the result in third list and print.

'''
def union_of_lists(list1, list2):
    # Create a set to store unique elements from both lists
    unique_elements = set(list1) | set(list2)
    
    # Convert the set back to a list
    result_list = list(unique_elements)
    
    return result_list
# Example usage
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
result = union_of_lists(list1, list2)
print("Union of the two lists:", result)
#<-- IGNORE --->
