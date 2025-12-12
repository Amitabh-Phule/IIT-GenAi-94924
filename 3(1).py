import pandas as pd

#1.read csv file
path=r"D:\GenAI Assignments\product.csv"
data=pd.read_csv(path)

print("-------------------------------------------")

#2.print each row
for index, row in data.iterrows():
    print(f"Row {index+1}: {row.to_dict()}")


print("-------------------------------------------")

#3.total number of rows
total_rows=len(data)    
print(f"Total number of rows: {total_rows}")

print("-------------------------------------------")


#4.total number product prices above 500
price_above_500=data[data['price']>500]
count_above_500=len(price_above_500)
print(f"Total number of products with price above 500: {count_above_500}")

print("-------------------------------------------")


#5.average price of all products
average_price=data['price'].mean()
print(f"Average price of all products: {average_price}")

print("-------------------------------------------")

#6.all product belonging to user input category
user_category=input("Enter a category to filter products: ")
filtered_products=data[data['category'].str.lower()==user_category.strip().lower()]
if not filtered_products.empty:
    print(f"Products in category '{user_category}':")
    for index, row in filtered_products.iterrows():
        print(f"- {row['product_name']} (price: {row['price']})")
else:
    print(f"No products found in category '{user_category}'.")


print("-------------------------------------------")


#7.TOTAL QUANTITY OF PRODUCTS IN STOCK
total_quantity=data['quantity'].sum()
print(f"Total quantity of products in stock: {total_quantity}")