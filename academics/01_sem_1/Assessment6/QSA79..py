'''Problem Statement: Write a Python program that:
1. Takes a list of numbers as input.
2. Finds the largest and smallest numbers in the list.
3. Counts the occurrence of a user-given number in the list.
Input Format: A list of integers separated by space. A single integer to count occurrences.
Output Format:
 The largest and smallest numbers.
 The count of the given number.
Example Input:
10 20 30 40 50 20 10
20
Example Output:
Largest: 50, Smallest: 10
Count of 20: 2
'''
numbers = input("Enter a list of numbers separated by space: ").split()
numbers = [int(num) for num in numbers]
# Find the largest and smallest numbers
largest = max(numbers)
smallest = min(numbers)
# Count the occurrence of a user-given number
count_number = int(input("Enter a number to count its occurrences: "))
count = numbers.count(count_number)
print("Largest:", largest, ", Smallest:", smallest)
print("Count of", count_number, ":", count)
#<-- IGNORE --->
