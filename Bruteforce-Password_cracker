import random
import string
import time

# Step 1: Take password from user
password = input("Enter password: ")

# Step 2: Define all possible characters
keys = string.digits + string.ascii_lowercase + string.ascii_uppercase + "!@#$%^&*"

# Step 3: Initialize variables
attempts = 0
start_time = time.time()

# Step 4: Keep guessing until match
while True:
    attempts += 1

    # Generate random password of same length
    guess = ''.join(random.choice(keys) for _ in range(len(password)))

    if guess == password:
        break

# Step 5: Calculate time
end_time = time.time()

# Step 6: Show result
print("\nPassword cracked!")
print(f"Password : {guess}")
print(f"Attempts : {attempts}")
print(f"Time taken : {end_time - start_time:.2f} seconds")
