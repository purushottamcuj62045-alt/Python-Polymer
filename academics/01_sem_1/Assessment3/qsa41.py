#Write a program to find sum of series:
#   2+22+222+2222+……..+n
n=int(input("Enter a the number till you a want series"))
term=0
sum_term=0
for i in range(n):
    term=term*10+2
    sum_term+= term
print("Sum of series",sum_term)
