salary = float(input("Enter your salary: "))
credit_score = int(input("Enter your credit score: "))
if credit_score < 600:
    print("Loan denied due to low credit score.")
else:
    if salary > 50000:
        max_loan = 1000000
    elif 30000 < salary <= 50000:
        max_loan = 500000
    else:
        max_loan = 0

    if credit_score > 750:
        max_loan += 200000

    if max_loan > 0:
        print(f"Eligible for loan. Maximum loan amount: ₹{max_loan}")
    else:
        print("Not eligible for a loan based on salary.")