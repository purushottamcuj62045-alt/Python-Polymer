'''Problem Statement: Write a Python program that:
1. Takes a list of numbers as input.
2. Converts the list into a tuple.
3. Prints both the list and tuple.
Input Format: A list of integers separated by space.
Output Format:
 The list of numbers.
 The tuple of numbers.
Example Input:
5 10 15 20 25
Example Output:
[5, 10, 15, 20, 25]
(5, 10, 15, 20, 25)'''
numbers = input("Enter a list of numbers separated by space: ").split()
numbers = [int(num) for num in numbers]
# Convert the list into a tuple
numbers_tuple = tuple(numbers)
# Print the list and tuple
print("List of numbers:", numbers)
print("Tuple of numbers:", numbers_tuple)
#<-- IGNORE --->
