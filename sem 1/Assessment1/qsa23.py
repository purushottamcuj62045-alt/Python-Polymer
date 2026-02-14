#Problem Statement: Given three sides of a triangle, determine its type:
#a. If all three sides are equal, print "Equilateral"
#b. If two sides are equal, print "Isosceles"
#c. If all three sides are different, print "Scalene"
#d. If it does not form a valid triangle, print "Not a Triangle"
#Input: 5 5 8
#Output: Isosceles
a = float(input("Enter side a: "))
b = float(input("Enter side b: "))
c = float(input("Enter side c: "))
if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("Equilateral")
    elif a == b or b == c or a == c:
        print("Isosceles")
    else:
        print("Scalene")