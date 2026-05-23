#Write a program to display product of cubes of 1-5.
product_cubes = 1
for i in range(1, 6):
    product_cubes *= i ** 3
print("Product of cubes: ",product_cubes)