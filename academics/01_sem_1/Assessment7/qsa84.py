'''. Create a Python module that includes the following functions: 
•	A function to calculate the area of a circle (given the radius). 
•	A function to calculate the area of a rectangle (given length and width). 
•	A function to calculate the area of a triangle (given base and height). 

Use these functions in a script where you import the module and call each 
function with different values.
'''
import math
def area_of_circle(radius):
    """Calculate the area of a circle given the radius."""
    return math.pi * (radius ** 2)
def area_of_rectangle(length, width):
    """Calculate the area of a rectangle given length and width."""
    return length * width
def area_of_triangle(base, height):
    """Calculate the area of a triangle given base and height."""
    return 0.5 * base * height
# Example usage
if __name__ == "__main__":
    radius = 5
    length = 10
    width = 4
    base = 6
    height = 3
    
    circle_area = area_of_circle(radius)
    rectangle_area = area_of_rectangle(length, width)
    triangle_area = area_of_triangle(base, height)
    
    print(f"Area of circle with radius {radius}: {circle_area:.2f}")
    print(f"Area of rectangle with length {length} and width {width}: {rectangle_area:.2f}")
    print(f"Area of triangle with base {base} and height {height}: {triangle_area:.2f}")
#<-- IGNORE --->
