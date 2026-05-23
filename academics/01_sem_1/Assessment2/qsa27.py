#ATM Withdrawal Challenge
#Rules for a bank transaction:
#Withdrawals must be in multiples of 5.
#Bank charges ₹0.50 per successful transaction.
#If balance is insufficient, transaction fails.
balance = float(input("Enter initial account balance: "))
withdrawal_amount = float(input("Enter withdrawal amount (multiple of 5): "))
if withdrawal_amount % 5 == 0:
    total_deduction = withdrawal_amount + 0.50
    if balance >= total_deduction:
        balance -= total_deduction
        print(f"Transaction successful! New balance: ₹{balance:.2f}")
    else:
        print("Insufficient balance for this transaction.")
