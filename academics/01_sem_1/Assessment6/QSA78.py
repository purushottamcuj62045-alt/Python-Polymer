'''Problem Statement: Write a Python program that:
1. Takes a tuple of numbers as input.
2. Finds the minimum and maximum value in the tuple.
3. Converts the tuple into a list and adds a new element to it.
4. Converts the list back into a tuple and prints the final tuple.
Input Format: A tuple of integers separated by space.
Output Format:
 The minimum and maximum values.
 The modified tuple after adding an element.
Example Input:
(5, 12, 7, 18, 3)
Example Output:
Minimum: 3, Maximum: 18
(5, 12, 7, 18, 3, 25)
'''
try:
    tuple_input = input("Enter numbers separated by space (or commas): ")
    
    # Replace commas with spaces to handle "1, 2, 3" format, then split
    cleaned_input = tuple_input.replace(',', ' ').split()
    
    # Check if input is empty
    if not cleaned_input:
        print("Error: You didn't enter any numbers.")
    else:
        # Create the tuple
        tuple_numbers = tuple(int(num) for num in cleaned_input)

        # Find minimum and maximum values
        min_value = min(tuple_numbers)
        max_value = max(tuple_numbers)

        # Convert tuple to list and add a new element
        list_numbers = list(tuple_numbers)
        
        # Handle the new element input separately
        new_element_input = input("Enter a new integer to add: ")
        new_element = int(new_element_input)
        
        list_numbers.append(new_element)

        # Convert list back to tuple
        final_tuple = tuple(list_numbers)

        print("-" * 20)
        print(f"Minimum: {min_value}, Maximum: {max_value}")
        print(f"Modified tuple: {final_tuple}")

except ValueError:
    print("Error: Please make sure you enter only whole numbers (integers).")