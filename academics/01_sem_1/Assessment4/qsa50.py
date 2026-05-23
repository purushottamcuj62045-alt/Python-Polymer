#Quadratic equation is calculated as follows: ax² + bx + c = 0. 
# Write a function which calculates solution set of a quadratic equation, solve_quadratic_eqn
import cmath
def solve_quadratic_eqn(a, b, c):
    discriminant = b**2 - 4*a*c
    root1 = (-b + cmath.sqrt(discriminant)) / (2*a)
    root2 = (-b - cmath.sqrt(discriminant)) / (2*a)
    return (root1, root2)
print("roots",solve_quadratic_eqn(1, 4, 4))