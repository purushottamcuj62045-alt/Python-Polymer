'''Write a Python program that prints all numbers from 1 to 100, but for multiples of 3 print 
"Fizz" instead of the number, for multiples of 5 print "Buzz", and for numbers which are multiples 
of both 3 and 5 print "FizzBuzz". '''

for i in range(1,101):
    if i%3==0 and i%5==0:
        print("FizzBuzz")
    elif i%3==0:
        print("Fizz")
    elif i%5==0:
        print("Buzz")
    else:
        print(i)
