'''Case 1: Detecting Fraudulent Transactions in Banking 
Context: 
A bank is analyzing transaction records to detect possible fraudulent activities. Suspicious 
transactions are often extreme values in terms of amount. Read CSV file and perform the 
following tasks:  
Tasks: 
1. Min-Max Method (user defined method): 
o Normalize the “Amount” column  
2. IQR Method: 
o Compute Q1, Q3, and IQR for the "Amount" column. 
o Identify outliers and replace them with the mean value. 
3. Z-Score Method (user defined method): 
o Compute Z-scores for the "Amount" column. 
o Detect outliers using a Z-score threshold (±3). 
4. Comparison: 
o Compare the number of outliers detected using both methods. 
o Discuss which method is better for fraud detection and why. '''
import numpy as np
import pandas as pd

data = pd.read_csv("C:/Users/Luffy/Downloads/fraud_transactions_200.csv")
print("<-----------Data--------------->")
print(data)

# ------------------Min-Max Normalization-------------------
def find_min(column):
    min_val = column.iloc[0]
    for value in column:
        if value < min_val:
            min_val = value
    return min_val


def find_max(column):
    max_val = column.iloc[0]
    for value in column:
        if value > max_val:
            max_val = value
    return max_val


def min_max_normalize(column):
    min_val = find_min(column)
    max_val = find_max(column)
    normalized = []
    for value in column:
        norm_val = (value - min_val) / (max_val - min_val)
        normalized.append(round(norm_val, 4))
    return normalized


print("<-----------Minimum Value-------------->")
print(find_min(data['Amount ($)']))
print("<-----------Maximum Value-------------->")
print(find_max(data['Amount ($)']))

data['Normalized_Amount'] = min_max_normalize(data['Amount ($)'])
print("<-----------Min-Max Normalized Amount-------------->")
print(data[['Amount ($)', 'Normalized_Amount']])


# -----------------IQR Method--------------------
data_s = data.sort_values(by="Amount ($)").reset_index(drop=True)
n = data_s["Amount ($)"].count()

def find_median(sorted_col, start, end):
    length = end - start
    mid = start + length // 2
    if length % 2 == 0:
        return (sorted_col.iloc[mid - 1] + sorted_col.iloc[mid]) / 2
    else:
        return sorted_col.iloc[mid]

# Q1 = median of lower half, Q3 = median of upper half
q1 = find_median(data_s["Amount ($)"], 0, n // 2)

if n % 2 == 0:
    q3 = find_median(data_s["Amount ($)"], n // 2, n)
else:
    q3 = find_median(data_s["Amount ($)"], n // 2 + 1, n)

iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("<-----------IQR Method-------------->")
print(f"Q1           : {q1}")
print(f"Q3           : {q3}")
print(f"IQR          : {iqr}")
print(f"Lower Bound  : {lower_bound}")
print(f"Upper Bound  : {upper_bound}")

# Compute mean manually
total = 0
for value in data['Amount ($)']:
    total += value
mean_val = total / n

# Identify outliers and replace with mean
iqr_outlier_count = 0
data['IQR_Cleaned_Amount'] = data['Amount ($)'].copy()
for i in range(len(data)):
    val = data.loc[i, 'Amount ($)']
    if val < lower_bound or val > upper_bound:
        data.loc[i, 'IQR_Cleaned_Amount'] = round(mean_val, 2)
        iqr_outlier_count += 1

print(f"Mean Value   : {round(mean_val, 2)}")
print(f"Outliers Found (IQR): {iqr_outlier_count}")
print("<-----------After Replacing IQR Outliers with Mean-------------->")
print(data[['Amount ($)', 'IQR_Cleaned_Amount']])


#===============Z-Score Method==================
def find_mean(column):
    total = 0
    for value in column:
        total += value
    return total / len(column)


def find_std(column):
    mean = find_mean(column)
    variance = 0
    for value in column:
        variance += (value - mean) ** 2
    variance = variance / len(column)
    return variance ** 0.5


def compute_zscore(column):
    mean = find_mean(column)
    std  = find_std(column)
    zscores = []
    for value in column:
        z = (value - mean) / std
        zscores.append(round(z, 4))
    return zscores


data['Z_Score'] = compute_zscore(data['Amount ($)'])

print("<-----------Z-Score Method-------------->")
print(f"Mean : {round(find_mean(data['Amount ($)']), 2)}")
print(f"Std  : {round(find_std(data['Amount ($)']), 2)}")

threshold = 3
zscore_outliers = []
zscore_outlier_count = 0
for i in range(len(data)):
    z = data.loc[i, 'Z_Score']
    if z > threshold or z < -threshold:
        zscore_outliers.append(i)
        zscore_outlier_count += 1

print(f"Outliers Found (Z-Score ±{threshold}): {zscore_outlier_count}")
print("<-----------Z-Score Outlier Transactions-------------->")
print(data.loc[zscore_outliers, ['Amount ($)', 'Z_Score']])


# ===============Comparison==================
print("\n<-----------Comparison: IQR vs Z-Score-------------->")
print(f"Number of outliers detected by IQR Method    : {iqr_outlier_count}")
print(f"Number of outliers detected by Z-Score Method: {zscore_outlier_count}")
