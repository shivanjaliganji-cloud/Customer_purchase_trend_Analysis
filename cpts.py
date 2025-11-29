
import pandas as pd

pd.set_option('display.max_rows', None)       # show all rows
pd.set_option('display.max_columns', None)    # show all columns
pd.set_option('display.width', None)          # no wrapping
pd.set_option('display.max_colwidth', None)   # show full column text

df = pd.read_csv("customer_purchase__trends.csv")

print(df)

#to check Structure
df.info()

# Summary statistics using .describe()
print(df.describe(include='all'))

# Checking if missing data or null values are present in the dataset
print(df.isnull().sum())

# Imputing missing values in Review Rating column with the median rating of the product category

df['Ratings'] = df.groupby('Category')['Ratings'].transform(
    lambda x: x.fillna(x.median())
)

print(df['Ratings'])

print(df.isnull().sum())

# Renaming columns according to snake casing for better readability and documentation

df.columns = df.columns.str.lower()              # convert all column names to lowercase
df.columns = df.columns.str.replace(' ', '_')    # replace spaces with underscores
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})  # rename specific column

print(df.columns)  # 🔍 This will show your updated column names

# Check null values in age column
print(df['age'].isnull().sum())

# Fill missing age values (optional)
df['age'] = df['age'].fillna(df['age'].median())

# Create age group column
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

print(df[['age', 'age_group']].head(30))

# create new column purchase_frequency_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(30))

print(df[['discount_applied', 'promo_code_used']].head(30))

print((df['discount_applied'] == df['promo_code_used']).all())

# Dropping promo_code_used column
df = df.drop('promo_code_used', axis=1)

print(df.columns)   # to verify it is removed


# Install libraries if not already installed (run in terminal in PyCharm)
# pip install pymysql sqlalchemy pandas

import pandas as pd
from sqlalchemy import create_engine

# CSV file
csv_file = "customer_purchase__trends.csv"  # Replace with your actual CSV path
df = pd.read_csv(csv_file)

# MySQL connection (connect to server without specifying database first)
username = "root"
password = "Myactuallpassword"
host = "localhost"
port = "3306"
database = "customer_purchase"

# Connect to MySQL server
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/")

# Connect to the newly created database
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5;", engine)
print(sample)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")













