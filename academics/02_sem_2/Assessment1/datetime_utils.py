'''Q5. Create a Python module called datetime_utils.py that includes the following functions: 
• get_current_time(): Returns the current time in "HH:MM:SS" format. 
• get_current_date(): Returns the current date in "YYYY-MM-DD" format. 
• days_between_dates(date1, date2): Takes two dates in the format "YYYY-MM-DD" and 
returns the number of days between the two dates. 
Then, write a script that imports this module and uses these functions to display the current date, 
time, and the difference in days between two dates provided by the user. '''
from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def days_between_dates(date1, date2):
    d1 = datetime.strptime(date1, "%Y-%m-%d")
    d2 = datetime.strptime(date2, "%Y-%m-%d")
    return abs((d2 - d1).days)

# Example usage:
if __name__ == "__main__":
    print("Current Time:", get_current_time())
    print("Current Date:", get_current_date())
    date1 = input("Enter the first date (YYYY-MM-DD): ")
    date2 = input("Enter the second date (YYYY-MM-DD): ")
    print("Days between dates:", days_between_dates(date1, date2))