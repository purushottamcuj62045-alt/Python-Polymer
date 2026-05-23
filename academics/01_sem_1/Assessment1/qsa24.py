#Problem Statement: Write a program that simulates a simple login system. The system
#should:
#a. Allow only three usernames ("admin", "user", "guest")
#b. If the username is "admin", print "Welcome Admin!"
#c. If "user", print "Welcome User!"
#d. If "guest", print "Welcome Guest!"
#e. If an unknown username is entered, print "Access Denied"
username = input("Enter your username: ").lower()
if username == "admin":
    print("Welcome Admin!")
elif username == "user":
    print("Welcome User!")
elif username == "guest":
    print("Welcome Guest!")
else:
    print("Access Denied")
