#Problem Statement: Age Check (Voting Eligibility)-Input age and check eligibility. If eligible print the message
# “You are eligible to vote”, otherwise print “Not Eligible”.
age = int(input("Enter your age: "))
if age >= 18:
    print("You are eligible to vote.")
else:
    print("Not Eligible.")
