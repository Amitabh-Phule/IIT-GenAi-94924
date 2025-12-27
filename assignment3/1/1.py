
import pandas as pd
import pandasql as ps

filepath = r"D:\GenAI Assignments\day3\assignment3\1\books_hdr.csv"
df = pd.read_csv(filepath)

print("Dataframe Column Types:")
print(df.dtypes)

print("\nData:")
print(df)

query = """
SELECT author, COUNT(*) AS total_books
FROM data
GROUP BY author
"""

result = ps.sqldf(query, {"data": df})

print("\nQuery Result:")
print(result)