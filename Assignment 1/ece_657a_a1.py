# -*- coding: utf-8 -*-
"""ECE_657A_A1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1be-1EYCP0HLS04qh5quqxxe9f695OkOT
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from scipy import stats

"""**Questions** **1. Data Cleaning and Preprocessing (for dataset A)**"""

#Load the dataset
DataA = pd.read_csv('DataA.csv',encoding='latin-1')
DataA.head()

print(DataA.columns)

DataA.shape

DataA.head()

# # Drop the 'Unnamed: 0' column
# DataA = DataA.drop('Unnamed: 0', axis=1, inplace=True)

# Drop the 'Unnamed: 0' column
DataA = DataA.drop('Unnamed: 0', axis=1)

# Reset the index
DataA = DataA.reset_index(drop=True)

DataA.head()

DataA.shape

print(DataA.columns)

DataA.info()

DataA.isnull().sum()

DataA.tail(775)

df_na = DataA.any(skipna=True, axis=1)
df_na[df_na==False].shape[0]

DataA.describe()

# Select the first 5 features
first_5_features = DataA.iloc[:, :5]

# Create box plots for the first 5 features
first_5_features.boxplot(figsize=(10, 6))
plt.title('Boxplot of First 5 Features')
plt.xticks(rotation=45)
plt.show()

"""**1. Detect any problems that need to be fixed in dataset A. Report such problems.**


Based on the analysis of dataset A, the following problems were identified:

i. Feature 34, 35, and 36 columns have only 1 non-null value.
**bold text**

*   This suggests that these columns may not contain sufficient information to be meaningful for analysis.
*   These columns could be candidates for removal from the dataset



**ii. The last 773 rows of the data set values are missing 18,227 to 18,999.**


*   It seems there is a significant chunk of missing data in the last portion of the dataset.

**iii. Missing values or Null values present in the data set.**


*    Identify the presence of missing or null values in the dataset




**iv. Outliers present in the data.**


*    Perform outlier detection to identify extreme values in the dataset using box plots that might adversely affect analysis or modeling.



"""



"""



**2. Fix the detected problems using some of the methods discussed in class.**

**i. Feature 34, 35, and 36 columns have only 1 non-null value.**

**Solution:**
Since these columns have only one non-null value, they are unlikely to contribute meaningful information to our analysis. Therefore, dropping them is a reasonable solution. This can be done using the drop method.

**ii. The last 773 rows of the data set values are missing 18,227 to 18,999**

**Solution:** As these last 773 rows contain incomplete data and may not contribute meaningfully to the analysis, consider dropping these rows.
By dropping these rows, we ensure that this dataset is more consistent and reliable for further analysis or modeling.

**iii. Missing values or Null values present in the data set.**

**Solution:**
Used DataA.fillna(DataA.median(), inplace=True) to replace missing values with the median of each column.


**iv. Outliers present in the data.**

**Solution:**
In the dataset, the Interquartile Range (IQR) method is being utilized to detect and smooth outliers using a custom function. Through iteration over each numerical column, extreme values beyond a specified IQR range are replaced with the nearest boundary."""

DataA.shape

# Remove columns 'fea.34', 'fea.35', and 'fea.36' from the DataFrame DataA
DataA=DataA.drop(columns=['fea.34','fea.35','fea.36'])
# Display information about the DataFrame to show the non-null values present in each column
DataA.info()

# Drop the last 773 rows
DataA = DataA.iloc[:-773]
DataA.shape

# Fill null values with median
DataA.fillna(DataA.median(), inplace=True)
DataA.info()

# Function to smooth outliers using IQR
def smooth_outliers_iqr(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    column[column < lower_bound] = lower_bound
    column[column > upper_bound] = upper_bound
    return column

# Apply the function to each numerical column in the DataFrame
numerical_columns = DataA.select_dtypes(include='number').columns
for column in numerical_columns:
    DataA[column] = smooth_outliers_iqr(DataA[column])

# Select the first 5 features
first_5_features = DataA.iloc[:, :5]

# Create box plots for the first 5 features
first_5_features.boxplot(figsize=(10, 6))
plt.title('Boxplot of First 5 Features')
plt.xticks(rotation=45)
plt.show()

"""**3. Normalize the data using min-max and z-score normalizaAon. Plot histograms of feature
9 and 24; compare and comment on the differences before and aHer normalizaAon.**



"""



from sklearn.preprocessing import MinMaxScaler, StandardScaler
import seaborn as sns

# Extract features 9 and 24
feature_9 = DataA['fea.9']
feature_24 = DataA['fea.24']

# Initialize MinMaxScaler and StandardScaler objects
min_max_scaler = MinMaxScaler()
standard_scaler = StandardScaler()

# Min-max normalization
feature_9_minmax = min_max_scaler.fit_transform(feature_9.values.reshape(-1, 1))
feature_24_minmax = min_max_scaler.fit_transform(feature_24.values.reshape(-1, 1))

# Z-score normalization
feature_9_zscore = standard_scaler.fit_transform(feature_9.values.reshape(-1, 1))
feature_24_zscore = standard_scaler.fit_transform(feature_24.values.reshape(-1, 1))

# Plot histograms before and after normalization
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
sns.histplot(feature_9, bins=30, color='blue')
plt.title('Feature 9 Before Normalization')

plt.subplot(2, 2, 2)
sns.histplot(feature_24, bins=30, color='blue')
plt.title('Feature 24 Before Normalization')

plt.subplot(2, 2, 3)
sns.histplot(feature_9_minmax, bins=30, color='green')
plt.title('Feature 9 After Min-Max Normalization')

plt.subplot(2, 2, 4)
sns.histplot(feature_24_minmax, bins=30, color='green')
plt.title('Feature 24 After Min-Max Normalization')

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
sns.histplot(feature_9_zscore, bins=30, color='red')
plt.title('Feature 9 After Z-Score Normalization')

plt.subplot(2, 2, 2)
sns.histplot(feature_24_zscore, bins=30, color='red')
plt.title('Feature 24 After Z-Score Normalization')

plt.tight_layout()
plt.show()

# Plot histograms before and after normalization
plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.hist(feature_9, bins=30, color='blue', alpha=0.5)
plt.title('Feature 9 Before Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(2, 2, 2)
plt.hist(feature_24, bins=30, color='blue', alpha=0.5)
plt.title('Feature 24 Before Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(2, 2, 3)
plt.hist(feature_9_minmax, bins=30, color='green', alpha=0.5)
plt.title('Feature 9 After Min-Max Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(2, 2, 4)
plt.hist(feature_24_minmax, bins=30, color='green', alpha=0.5)
plt.title('Feature 24 After Min-Max Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))

plt.subplot(2, 2, 1)
plt.hist(feature_9_zscore, bins=30, color='red', alpha=0.5)
plt.title('Feature 9 After Z-Score Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(2, 2, 2)
plt.hist(feature_24_zscore, bins=30, color='red', alpha=0.5)
plt.title('Feature 24 After Z-Score Normalization')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

"""Data normalization using min-max and z-score methods was conducted, followed by a comparison of histograms for features 9 and 24 before and after normalization."""