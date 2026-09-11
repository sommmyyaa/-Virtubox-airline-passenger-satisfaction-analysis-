"""
Airline Passenger Satisfaction - Data Analyst Assessment
Author: Somya Gupta

What this script does:
1. Loads the raw train.csv and test.csv files and combines them into one dataset
2. Cleans the data (missing values, duplicates, data types, text formatting)
3. Adds a few calculated columns to make analysis easier
4. Runs the exploratory analysis used to find the business insights in Q4 and Q5
5. Saves the cleaned dataset and a few charts

Dataset source: Kaggle - Airline Passenger Satisfaction
https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)


# ---------------------------------------------------------------
# STEP 1: Load and combine the raw data
# ---------------------------------------------------------------
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# both files have an extra "Unnamed: 0" index column from how they were exported - drop it
for d in (train, test):
    d.drop(columns=[c for c in d.columns if c.startswith('Unnamed')], inplace=True, errors='ignore')

df = pd.concat([train, test], ignore_index=True)
print("Combined raw data shape:", df.shape)


# ---------------------------------------------------------------
# STEP 2: Clean the data
# ---------------------------------------------------------------

# check + remove exact duplicate rows
dupes_found = df.duplicated().sum()
df = df.drop_duplicates()
print("Duplicate rows removed:", dupes_found)

# Arrival Delay in Minutes has some missing values - fill with median
# (median is safer than mean here since delay times are skewed by a few very long delays)
missing_before = df['Arrival Delay in Minutes'].isnull().sum()
median_delay = df['Arrival Delay in Minutes'].median()
df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].fillna(median_delay)
print(f"Filled {missing_before} missing Arrival Delay values with median ({median_delay})")

# fix data types
df['id'] = df['id'].astype(int)
df['Age'] = df['Age'].astype(int)

rating_cols = [
    'Inflight wifi service', 'Departure/Arrival time convenient', 'Ease of Online booking',
    'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort',
    'Inflight entertainment', 'On-board service', 'Leg room service',
    'Baggage handling', 'Checkin service', 'Inflight service', 'Cleanliness'
]
for c in rating_cols:
    df[c] = df[c].astype(int)

# standardize text columns (fix inconsistent capitalization etc.)
df['Gender'] = df['Gender'].str.strip().str.title()
df['Customer Type'] = df['Customer Type'].str.strip().replace({'disloyal Customer': 'Disloyal Customer'})
df['Type of Travel'] = df['Type of Travel'].str.strip()
df['Class'] = df['Class'].str.strip()
df['satisfaction'] = df['satisfaction'].str.strip()


# ---------------------------------------------------------------
# STEP 3: Create calculated fields for analysis
# ---------------------------------------------------------------

# 1/0 flag version of satisfaction - makes it easy to calculate % satisfied with .mean()
df['Satisfied_Flag'] = (df['satisfaction'] == 'satisfied').astype(int)

# total delay = departure delay + arrival delay
df['Total Delay in Minutes'] = df['Departure Delay in Minutes'] + df['Arrival Delay in Minutes']


def delay_bucket(minutes):
    if minutes == 0:
        return 'No Delay'
    elif minutes <= 15:
        return '1-15 min'
    elif minutes <= 60:
        return '16-60 min'
    elif minutes <= 180:
        return '61-180 min'
    else:
        return '180+ min'


df['Delay Bucket'] = df['Total Delay in Minutes'].apply(delay_bucket)


def age_group(age):
    if age < 18:
        return 'Under 18'
    elif age <= 30:
        return '18-30'
    elif age <= 45:
        return '31-45'
    elif age <= 60:
        return '46-60'
    else:
        return '60+'


df['Age Group'] = df['Age'].apply(age_group)

# average of all 14 service ratings, per passenger
df['Avg Service Rating'] = df[rating_cols].mean(axis=1).round(2)

# save the cleaned, analysis-ready dataset
df.to_csv('processed_data.csv', index=False)
print("\nFinal cleaned dataset shape:", df.shape)


# ---------------------------------------------------------------
# STEP 4: Exploratory analysis - the numbers behind the Q4/Q5 insights
# ---------------------------------------------------------------

print("\n--- Overall satisfaction ---")
print(df['satisfaction'].value_counts(normalize=True) * 100)

print("\n--- Satisfaction % by Class ---")
print(df.groupby('Class')['Satisfied_Flag'].mean() * 100)

print("\n--- Satisfaction % by Type of Travel ---")
print(df.groupby('Type of Travel')['Satisfied_Flag'].mean() * 100)

print("\n--- Satisfaction % by Customer Type ---")
print(df.groupby('Customer Type')['Satisfied_Flag'].mean() * 100)

print("\n--- Satisfaction % by Delay Bucket ---")
order = ['No Delay', '1-15 min', '16-60 min', '61-180 min', '180+ min']
print(df.groupby('Delay Bucket')['Satisfied_Flag'].mean().reindex(order) * 100)

print("\n--- Correlation of each service rating with satisfaction ---")
corrs = df[rating_cols + ['Satisfied_Flag']].corr()['Satisfied_Flag'].drop('Satisfied_Flag')
print(corrs.sort_values(ascending=False))

print("\n--- Satisfaction % by Age Group ---")
age_order = ['Under 18', '18-30', '31-45', '46-60', '60+']
print(df.groupby('Age Group')['Satisfied_Flag'].mean().reindex(age_order) * 100)

print("\n--- The surprising result: Class x Type of Travel ---")
print(df.groupby(['Class', 'Type of Travel'])['Satisfied_Flag'].mean() * 100)


# ---------------------------------------------------------------
# STEP 5: Charts used in the dashboard / presentation
# ---------------------------------------------------------------
plt.rcParams.update({'font.size': 11})

# Satisfaction by class
data = df.groupby('Class')['Satisfied_Flag'].mean().mul(100).sort_values()
fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(data.index, data.values, color=['#e15759', '#f1ce63', '#4e79a7'])
ax.set_xlabel('% Satisfied')
ax.set_title('Satisfaction Rate by Travel Class')
plt.tight_layout()
plt.savefig('chart1_class.png', dpi=150)
plt.close()

# Class x Type of Travel (the surprising insight)
pivot = df.groupby(['Class', 'Type of Travel'])['Satisfied_Flag'].mean().mul(100).unstack()
pivot = pivot.reindex(['Eco', 'Eco Plus', 'Business'])
fig, ax = plt.subplots(figsize=(6.5, 4))
pivot.plot(kind='bar', ax=ax, color=['#f28e2b', '#4e79a7'])
ax.set_ylabel('% Satisfied')
ax.set_title('Satisfaction: Class vs Purpose of Travel')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('chart2_class_travel.png', dpi=150)
plt.close()

# Correlation chart
corrs_sorted = corrs.sort_values()
fig, ax = plt.subplots(figsize=(6.5, 5))
ax.barh(corrs_sorted.index, corrs_sorted.values, color='#59a14f')
ax.set_xlabel('Correlation with Satisfaction')
ax.set_title('Which Service Ratings Matter Most')
plt.tight_layout()
plt.savefig('chart3_correlation.png', dpi=150)
plt.close()

print("\nAll charts saved. Analysis complete.")
