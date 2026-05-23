# Product Price Management System (PPMS)

store_product = {
    'apple': 80,
    'banana': 75,
    'grapes': 76,
    'pineapple': 55,
    'kiwi': 65,
    'avocado': 85,
    'blueberry': 63,
    'sapota': 95,
    'dragonfruit': 105,
    'raspberry': 180,
    'guava': 80,
    'walnuts': 189,
    'almonds': 400,
    'watermelon': 30,
    'plum': 40,
    'mango': 10,
    'custard apple': 456,
    'cherry': 35,
    'peach': 45,
    'lime': 10
}

# ------------------ FUNCTIONS ------------------

# Add new product
def add_product(name, price):
    if name in store_product:
        print("Product already exists ")
    else:
        store_product[name] = price
        print("Product added successfully ")

# Update product price
def update_price(name, price):
    if name in store_product:
        store_product[name] = price
        print("Price updated successfully ")
    else:
        print("Product not found ")

# Delete a product
def delete_product(name):
    if name in store_product:
        del store_product[name]
        print("Product deleted successfully ")
    else:
        print("Product not found ")

# Calculate total price of all products
def total_price():
    total = sum(store_product.values())
    print("Total price of all products:", total)

# Apply discount on all products
def apply_discount(discount_percent):
    for product in store_product:
        store_product[product] -= store_product[product] * (discount_percent / 100)
    print(f"{discount_percent}% discount applied to all products ")

# ------------------ USER INPUT (UPDATE PRICE) ------------------

pn = input("Enter the product name for price update: ").strip().lower()
pp = int(input("Enter updated price: "))

update_price(pn, pp)

print("\nUpdated Product List:")
print(store_product)

pu= input("Enter the new product name to add: ").lower()
pt = int(input("Enter  price: "))

add_product(pu,pt)