#Problem Statement: Given a student's marks (out of 100), print the grade:
#90-100: "A+"
#80-89: "A"
#70-79: "B"
#60-69: "C"
#50-59: "D"
#Below 50: "Fail"
marks = float(input("Enter the student's marks (out of 100): "))
if 90 <= marks <= 100:
    print("Grade: A+")
elif 80 <= marks < 90:
    print("Grade: A")
elif 70 <= marks < 80:
    print("Grade: B")
elif 60 <= marks < 70:
    print("Grade: C")
elif 50 <= marks < 60:
    print("Grade: D")
else:
    print("Grade: Fail")
