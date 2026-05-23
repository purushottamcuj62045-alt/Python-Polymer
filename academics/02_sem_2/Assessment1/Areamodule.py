'''. Create a Python module that includes the following functions: 
• A function to calculate the area of a circle (given the radius). 
• A function to calculate the area of a rectangle (given length and width). 
• A function to calculate the area of a triangle (given base and height). 
Use these functions in a script where you import the module and call each function with different 
values.'''

from math import pi

def area_of_circle(radius):
    return pi * radius * radius

def area_of_rectangle(length, width):
    return length * width

def area_of_triangle(base, height):
    return 0.5 * base * height
# Example usage:
if __name__ == "__main__":
    print("Area of Circle with radius 5:", area_of_circle(5))
    print("Area of Rectangle with length 4 and width 6:", area_of_rectangle(4, 6))
    print("Area of Triangle with base 3 and height 7:", area_of_triangle(3, 7)) 
