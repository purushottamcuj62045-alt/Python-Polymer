'''Case 3: Employee Salary Analysis 
Scenario: You are working as an HR analyst and need to analyze salaries based on various 
attributes. 
Employee_ID     Experience (Years)     Department      Salary ($)         Education Level
E001            2                      IT               55,000            Bachelor's
E002            10                     Finance          85,000            Master's
E003            6                      HR               65,000            Bachelor's
E004            15                     IT               120,000           PhD
1. Robust Normalization: Apply robust scaling on "Experience (Years)". 
2. Z-score Standardization: Standardize the "Salary" column. 
3. Ordinal Encoding: Encode "Education Level" (Bachelor's < Master's < PhD). 
4. One-Hot Encoding: Encode "Department". 
5. Label Encoding: Apply label encoding on "Education Level". '''

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler, OrdinalEncoder, LabelEncoder, OneHotEncoder

data = {
    'Employee_ID':  ['E001', 'E002', 'E003', 'E004'],
    'Experience':   [2, 10, 6, 15],
    'Department':   ['IT', 'Finance', 'HR', 'IT'],
    'Salary':       [55000, 85000, 65000, 120000],
    'Education':    ["Bachelor's", "Master's", "Bachelor's", "PhD"]
}

df = pd.DataFrame(data)
print(df)

# Robust Scaling on Experience
scaler = RobustScaler()
robust_scaled = scaler.fit_transform(df[['Experience']])
print("========== Robust Scaled Data =============")
print(robust_scaled)

# Z-Score Standardization on Salary  
scaler = StandardScaler()
standardized_data = scaler.fit_transform(df[['Salary']])
print("============ Z-Score Normalization =========")
print(standardized_data)

# Ordinal Encoding
education_order = {"Bachelor's": 0, "Master's": 1, "PhD": 2}
df["Education_ordinal"] = df["Education"].map(education_order)

# One-Hot Encoding  
ohe = OneHotEncoder(sparse_output=False)
dept_encoded = ohe.fit_transform(df[["Department"]])
dept_df = pd.DataFrame(dept_encoded, columns=ohe.get_feature_names_out(["Department"]))

# Merge back
df = pd.concat([df, dept_df], axis=1)

# Label Encoding 
le = LabelEncoder()
df["Education_label"] = le.fit_transform(df["Education"])

print(df)