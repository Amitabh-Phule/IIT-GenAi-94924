import pandas as pd
import pandasql as ps

filepath = r"D:\GenAI Assignments\day4\1\emp_hdr.csv"
df = pd.read_csv(filepath)

print("Dataframe Column Types:")
print(df.dtypes)

print("\nEmp Data:")
print(df)

query = input("\nEnter SQL query (use table name 'data'): ")

result = ps.sqldf(query, {"data": df})

print("\nQuery Result:")
print(result)
