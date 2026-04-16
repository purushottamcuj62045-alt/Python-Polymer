'''Case 2: House Price Analysis 
Context: 
A real estate company wants to analyze house prices and detect extreme values that may 
indicate incorrect listings or luxury properties. CSV dataset is provided. Read and perform the 
following tasks: 
Tasks: 
1. Robust Method: 
o Normalize the “Price” column  
2. IQR Method: 
o Compute Q1, Q3, and IQR for the "Price" column. 
o Identify outliers and replace them with the median value. 
3. Z-Score Method (user defined method): 
o Compute Z-scores for the "Price" column. 
o Detect outliers using a Z-score threshold (±3). 
4. Analysis: 
o Which method performs better for detecting anomalies in house prices? 
o How would handling outliers affect machine learning models predicting house 
prices?'''

import numpy as np
import pandas as pd

data = pd.read_csv("C:/Users/Luffy/Downloads/house_prices_200.csv")
print("<=========Data===========>")
print(data)

data = data.sort_values(by="Price ($)").reset_index(drop=True)
n = data["Price ($)"].count()

def find_median(sorted_col, start, end):
    length = end - start
    mid = start + length // 2
    if length % 2 == 0:
        return (sorted_col.iloc[mid - 1] + sorted_col.iloc[mid]) / 2
    else:
        return sorted_col.iloc[mid]

q1 = find_median(data["Price ($)"], 0, n // 2)

if n % 2 == 0:
    q3 = find_median(data["Price ($)"], n // 2, n)
else:
    q3 = find_median(data["Price ($)"], n // 2 + 1, n)

iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("<==========IQR Method=========>")
print(f"Q1           : {q1}")
print(f"Q3           : {q3}")
print(f"IQR          : {iqr}")
print(f"Lower Bound  : {lower_bound}")
print(f"Upper Bound  : {upper_bound}")

