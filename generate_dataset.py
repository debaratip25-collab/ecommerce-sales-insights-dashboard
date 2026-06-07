import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# --- Reference data ---
regions = {
    "North": {
        "states": ["Delhi", "Uttar Pradesh", "Haryana", "Punjab"],
        "cities": {
            "Delhi": ["New Delhi", "Dwarka", "Rohini"],
            "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra"],
            "Haryana": ["Gurugram", "Faridabad", "Hisar"],
            "Punjab": ["Amritsar", "Ludhiana", "Chandigarh"],
        },
    },
    "South": {
        "states": ["Karnataka", "Tamil Nadu", "Telangana", "Kerala"],
        "cities": {
            "Karnataka": ["Bengaluru", "Mysuru", "Hubli"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
            "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
            "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
        },
    },
    "East": {
        "states": ["West Bengal", "Odisha", "Bihar", "Jharkhand"],
        "cities": {
            "West Bengal": ["Kolkata", "Howrah", "Durgapur"],
            "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
            "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
            "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
        },
    },
    "West": {
        "states": ["Maharashtra", "Gujarat", "Rajasthan", "Goa"],
        "cities": {
            "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
            "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
            "Goa": ["Panaji", "Margao", "Vasco da Gama"],
        },
    },
}

categories = {
    "Electronics": {
        "products": ["Laptop", "Smartphone", "Tablet", "Smartwatch", "Bluetooth Speaker",
                     "Wireless Earbuds", "DSLR Camera", "LED Monitor", "Gaming Mouse", "Keyboard"],
        "price_range": (800, 80000),
        "cost_pct": (0.60, 0.80),
        "discount_range": (0, 20),
    },
    "Fashion": {
        "products": ["Formal Shirt", "Casual T-Shirt", "Jeans", "Ethnic Kurta", "Sports Shoes",
                     "Sneakers", "Saree", "Jacket", "Handbag", "Sunglasses"],
        "price_range": (300, 5000),
        "cost_pct": (0.40, 0.65),
        "discount_range": (5, 35),
    },
    "Home & Kitchen": {
        "products": ["Air Fryer", "Mixer Grinder", "Pressure Cooker", "Non-Stick Cookware Set",
                     "Vacuum Cleaner", "Water Purifier", "Ceiling Fan", "LED Bulbs Pack",
                     "Bed Sheet Set", "Pillow Set"],
        "price_range": (200, 25000),
        "cost_pct": (0.50, 0.72),
        "discount_range": (5, 25),
    },
    "Beauty & Personal Care": {
        "products": ["Face Serum", "Moisturiser SPF", "Hair Dryer", "Electric Shaver",
                     "Perfume Set", "Nail Polish Kit", "Sunscreen SPF50", "Face Wash",
                     "Shampoo Combo", "Lipstick Pack"],
        "price_range": (150, 4000),
        "cost_pct": (0.35, 0.60),
        "discount_range": (10, 40),
    },
    "Sports & Fitness": {
        "products": ["Yoga Mat", "Resistance Bands Set", "Dumbbell Pair", "Treadmill",
                     "Cycling Gloves", "Protein Shaker", "Cricket Bat", "Football",
                     "Badminton Racket", "Skipping Rope"],
        "price_range": (200, 35000),
        "cost_pct": (0.50, 0.68),
        "discount_range": (5, 30),
    },
    "Books & Stationery": {
        "products": ["Business Strategy Book", "Data Science Handbook", "Fiction Novel",
                     "Self-Help Book", "Notebook Set", "Fountain Pen", "Planner",
                     "Sticky Notes Pack", "Art Supplies Kit", "Coloring Book"],
        "price_range": (100, 1500),
        "cost_pct": (0.40, 0.60),
        "discount_range": (5, 20),
    },
}

payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "EMI"]
shipping_modes = ["Standard", "Express", "Same Day", "Economy"]
delivery_statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "In Transit", "Returned", "Cancelled"]
customer_segments = ["Consumer", "Corporate", "Home Office", "Small Business"]

# Generate customer pool
num_customers = 80
customer_ids = [f"C{str(i).zfill(4)}" for i in range(1001, 1001 + num_customers)]
first_names = ["Aarav","Vivaan","Aditya","Sai","Arjun","Rohan","Priya","Ananya","Sneha","Pooja",
               "Rahul","Amit","Neha","Kavita","Suresh","Rajesh","Meena","Divya","Karan","Nikhil",
               "Akash","Deepa","Shreya","Riya","Suman","Vijay","Sunita","Mohan","Geeta","Pankaj",
               "Seema","Tarun","Bhavna","Harish","Lata","Sachin","Rekha","Girish","Swati","Manish",
               "Usha","Nilesh","Vidya","Prakash","Smita","Ajay","Lalita","Yash","Rasika","Tushar"]
last_names = ["Sharma","Patel","Singh","Gupta","Kumar","Verma","Joshi","Shah","Mehta","Rao",
              "Nair","Iyer","Reddy","Pillai","Mishra","Pandey","Chopra","Kapoor","Bose","Das",
              "Malhotra","Agarwal","Tiwari","Yadav","Sinha","Chauhan","Dubey","Jain","Saxena","Kulkarni"]

random.shuffle(first_names)
customer_names = {cid: f"{random.choice(first_names)} {random.choice(last_names)}" for cid in customer_ids}
customer_segments_map = {cid: random.choice(customer_segments) for cid in customer_ids}

# Date range: Jan 2024 – Dec 2024
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

def random_date():
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

rows = []
order_counter = 1001

for _ in range(310):
    region = random.choice(list(regions.keys()))
    state = random.choice(regions[region]["states"])
    city = random.choice(regions[region]["cities"][state])

    category = random.choice(list(categories.keys()))
    cat_info = categories[category]
    product = random.choice(cat_info["products"])

    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(*cat_info["price_range"]), 2)
    discount_pct = round(random.uniform(*cat_info["discount_range"]), 1)

    sales_amount = round(quantity * unit_price * (1 - discount_pct / 100), 2)
    cost_pct = random.uniform(*cat_info["cost_pct"])
    cost_amount = round(sales_amount * cost_pct, 2)
    profit_amount = round(sales_amount - cost_amount, 2)
    profit_margin = round((profit_amount / sales_amount) * 100, 2) if sales_amount > 0 else 0

    customer_id = random.choice(customer_ids)
    order_date = random_date()
    payment = random.choice(payment_methods)
    shipping = random.choice(shipping_modes)
    delivery = random.choice(delivery_statuses)

    rows.append({
        "Order_ID": f"ORD-{order_counter}",
        "Customer_ID": customer_id,
        "Customer_Name": customer_names[customer_id],
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Region": region,
        "State": state,
        "City": city,
        "Product_Category": category,
        "Product_Name": product,
        "Quantity_Sold": quantity,
        "Unit_Price": unit_price,
        "Discount_Pct": discount_pct,
        "Sales_Amount": sales_amount,
        "Cost_Amount": cost_amount,
        "Profit_Amount": profit_amount,
        "Profit_Margin_Pct": profit_margin,
        "Payment_Method": payment,
        "Shipping_Mode": shipping,
        "Delivery_Status": delivery,
        "Customer_Segment": customer_segments_map[customer_id],
    })
    order_counter += 1

df = pd.DataFrame(rows)
df = df.sort_values("Order_Date").reset_index(drop=True)

# Save CSV
df.to_csv("/home/claude/ecommerce-dashboard/dataset/ecommerce_sales_data.csv", index=False)

# Save Excel
df.to_excel("/home/claude/ecommerce-dashboard/dataset/ecommerce_sales_data.xlsx", index=False)

print(f"Dataset generated: {len(df)} rows")
print(df.head(3).to_string())
print("\nColumn summary:")
print(df.dtypes)
print("\nKey stats:")
print(f"Total Sales: ₹{df['Sales_Amount'].sum():,.0f}")
print(f"Total Profit: ₹{df['Profit_Amount'].sum():,.0f}")
print(f"Avg Profit Margin: {df['Profit_Margin_Pct'].mean():.1f}%")
print(f"Total Orders: {len(df)}")
print(f"Unique Customers: {df['Customer_ID'].nunique()}")
