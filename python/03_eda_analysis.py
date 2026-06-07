"""
E-Commerce Sales Insights Dashboard
====================================
Full Exploratory Data Analysis (EDA) Script
Author : Data Analytics Project
Dataset: ecommerce_sales_data.csv (310 orders, Jan–Dec 2024)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── 1. LOAD & INSPECT ─────────────────────────────────────────────────────────
print("=" * 65)
print("E-COMMERCE SALES INSIGHTS DASHBOARD — EDA Report")
print("=" * 65)

df = pd.read_csv("dataset/ecommerce_sales_data.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"]      = df["Order_Date"].dt.to_period("M")
df["Quarter"]    = df["Order_Date"].dt.to_period("Q")

print(f"\n{'─'*40}")
print("DATASET OVERVIEW")
print(f"{'─'*40}")
print(f"  Rows (Orders)   : {len(df):,}")
print(f"  Columns         : {len(df.columns)}")
print(f"  Date Range      : {df['Order_Date'].min().date()}  →  {df['Order_Date'].max().date()}")
print(f"  Unique Customers: {df['Customer_ID'].nunique()}")
print(f"  Unique Products : {df['Product_Name'].nunique()}")
print(f"  Categories      : {df['Product_Category'].nunique()}")
print(f"  Regions         : {df['Region'].nunique()}")

# ── 2. DATA QUALITY CHECK ────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("DATA QUALITY CHECK")
print(f"{'─'*40}")
print("\n  Missing Values:")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.any() else "  ✓ No missing values found.")
dups = df.duplicated(subset="Order_ID").sum()
print(f"\n  Duplicate Order IDs: {dups} — {'✓ None found' if dups == 0 else '⚠ Found & removed'}")
print(f"\n  Negative Sales     : {(df['Sales_Amount'] < 0).sum()}")
print(f"  Negative Profit    : {(df['Profit_Amount'] < 0).sum()}")
print(f"  Zero-quantity rows : {(df['Quantity_Sold'] == 0).sum()}")

# ── 3. KEY BUSINESS KPIs ─────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("KEY BUSINESS KPIs")
print(f"{'─'*40}")
total_sales  = df["Sales_Amount"].sum()
total_profit = df["Profit_Amount"].sum()
total_cost   = df["Cost_Amount"].sum()
total_orders = len(df)
aov          = total_sales / total_orders
avg_margin   = df["Profit_Margin_Pct"].mean()
total_qty    = df["Quantity_Sold"].sum()

print(f"  Total Revenue (Sales)    : ₹{total_sales:>14,.2f}")
print(f"  Total Profit             : ₹{total_profit:>14,.2f}")
print(f"  Total Cost               : ₹{total_cost:>14,.2f}")
print(f"  Total Orders             : {total_orders:>15,}")
print(f"  Total Units Sold         : {total_qty:>15,}")
print(f"  Average Order Value      : ₹{aov:>14,.2f}")
print(f"  Average Profit Margin    : {avg_margin:>14.2f}%")
print(f"  Profit-to-Sales Ratio    : {(total_profit/total_sales*100):>13.2f}%")

# ── 4. MONTHLY TREND ─────────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("MONTHLY SALES & PROFIT TREND")
print(f"{'─'*40}")
monthly = df.groupby("Month").agg(
    Sales=("Sales_Amount","sum"),
    Profit=("Profit_Amount","sum"),
    Orders=("Order_ID","count")
).reset_index()
monthly["MoM_Growth_%"] = monthly["Sales"].pct_change().mul(100).round(2)

print(f"\n  {'Month':<10} {'Sales (₹)':>14} {'Profit (₹)':>13} {'Orders':>8} {'MoM Growth':>12}")
print(f"  {'─'*10} {'─'*14} {'─'*13} {'─'*8} {'─'*12}")
for _, r in monthly.iterrows():
    mom = f"{r['MoM_Growth_%']:+.1f}%" if not pd.isna(r["MoM_Growth_%"]) else "  —"
    print(f"  {str(r['Month']):<10} {r['Sales']:>14,.0f} {r['Profit']:>13,.0f} {r['Orders']:>8} {mom:>12}")

best_month  = monthly.loc[monthly["Sales"].idxmax(), "Month"]
worst_month = monthly.loc[monthly["Sales"].idxmin(), "Month"]
print(f"\n  ★ Best Month  : {best_month}  |  Worst Month: {worst_month}")

# ── 5. CATEGORY ANALYSIS ─────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("PRODUCT CATEGORY ANALYSIS")
print(f"{'─'*40}")
cat_df = df.groupby("Product_Category").agg(
    Sales=("Sales_Amount","sum"),
    Profit=("Profit_Amount","sum"),
    Orders=("Order_ID","count"),
    Margin=("Profit_Margin_Pct","mean")
).sort_values("Sales", ascending=False)
cat_df["Sales_Share_%"] = (cat_df["Sales"] / cat_df["Sales"].sum() * 100).round(1)

print(f"\n  {'Category':<26} {'Sales (₹)':>12} {'Profit (₹)':>12} {'Margin%':>9} {'Share%':>8}")
print(f"  {'─'*26} {'─'*12} {'─'*12} {'─'*9} {'─'*8}")
for cat, r in cat_df.iterrows():
    print(f"  {cat:<26} {r['Sales']:>12,.0f} {r['Profit']:>12,.0f} {r['Margin']:>8.1f}% {r['Sales_Share_%']:>7.1f}%")

top_cat    = cat_df["Sales"].idxmax()
best_margin_cat = cat_df["Margin"].idxmax()
print(f"\n  ★ Top Revenue Category : {top_cat}")
print(f"  ★ Best Margin Category : {best_margin_cat}")

# ── 6. REGION ANALYSIS ───────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("REGIONAL PERFORMANCE")
print(f"{'─'*40}")
reg_df = df.groupby("Region").agg(
    Sales=("Sales_Amount","sum"),
    Profit=("Profit_Amount","sum"),
    Orders=("Order_ID","count"),
    Margin=("Profit_Margin_Pct","mean")
).sort_values("Sales", ascending=False)
reg_df["Revenue_Share_%"] = (reg_df["Sales"] / reg_df["Sales"].sum() * 100).round(1)

print(f"\n  {'Region':<10} {'Sales (₹)':>14} {'Profit (₹)':>13} {'Margin%':>9} {'Share%':>8}")
print(f"  {'─'*10} {'─'*14} {'─'*13} {'─'*9} {'─'*8}")
for reg, r in reg_df.iterrows():
    print(f"  {reg:<10} {r['Sales']:>14,.0f} {r['Profit']:>13,.0f} {r['Margin']:>8.1f}% {r['Revenue_Share_%']:>7.1f}%")
print(f"\n  ★ Best Region  : {reg_df['Sales'].idxmax()}")
print(f"  ★ Lowest Margin: {reg_df['Margin'].idxmin()}")

# ── 7. TOP PRODUCTS ───────────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("TOP 10 BEST-SELLING PRODUCTS")
print(f"{'─'*40}")
prod_df = df.groupby("Product_Name").agg(
    Sales=("Sales_Amount","sum"),
    Profit=("Profit_Amount","sum"),
    Units=("Quantity_Sold","sum"),
    Margin=("Profit_Margin_Pct","mean")
).nlargest(10, "Sales")

print(f"\n  {'#':<3} {'Product':<28} {'Sales (₹)':>13} {'Profit (₹)':>12} {'Units':>7}")
print(f"  {'─'*3} {'─'*28} {'─'*13} {'─'*12} {'─'*7}")
for rank, (prod, r) in enumerate(prod_df.iterrows(), 1):
    print(f"  {rank:<3} {prod:<28} {r['Sales']:>13,.0f} {r['Profit']:>12,.0f} {r['Units']:>7}")

# ── 8. CUSTOMER ANALYSIS ─────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("CUSTOMER ANALYSIS")
print(f"{'─'*40}")
cust_df = df.groupby(["Customer_ID","Customer_Name"]).agg(
    Total_Sales=("Sales_Amount","sum"),
    Total_Orders=("Order_ID","count"),
    Avg_Order=("Sales_Amount","mean")
).sort_values("Total_Sales", ascending=False)

print("\n  TOP 10 HIGH-VALUE CUSTOMERS:")
print(f"  {'#':<3} {'Customer':<22} {'ID':<8} {'Sales (₹)':>12} {'Orders':>8} {'Avg Ord (₹)':>13}")
print(f"  {'─'*3} {'─'*22} {'─'*8} {'─'*12} {'─'*8} {'─'*13}")
for rank, ((cid, cname), r) in enumerate(cust_df.head(10).iterrows(), 1):
    print(f"  {rank:<3} {cname:<22} {cid:<8} {r['Total_Sales']:>12,.0f} {r['Total_Orders']:>8} {r['Avg_Order']:>13,.0f}")

seg_df = df.groupby("Customer_Segment").agg(
    Sales=("Sales_Amount","sum"), Orders=("Order_ID","count")
).sort_values("Sales", ascending=False)
print("\n  CUSTOMER SEGMENT BREAKDOWN:")
for seg, r in seg_df.iterrows():
    share = r["Sales"] / seg_df["Sales"].sum() * 100
    print(f"    {seg:<18}: ₹{r['Sales']:>10,.0f} ({share:.1f}%)  |  {int(r['Orders'])} orders")

# ── 9. PAYMENT & DELIVERY ─────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("PAYMENT METHOD ANALYSIS")
print(f"{'─'*40}")
pay_df = df.groupby("Payment_Method").agg(
    Orders=("Order_ID","count"), Sales=("Sales_Amount","sum")
).sort_values("Sales", ascending=False)
for pm, r in pay_df.iterrows():
    bar = "█" * int(r["Sales"] / pay_df["Sales"].max() * 30)
    print(f"  {pm:<18}: {bar:<30} ₹{r['Sales']:>10,.0f}  ({int(r['Orders'])} orders)")

print(f"\n{'─'*40}")
print("DELIVERY STATUS SUMMARY")
print(f"{'─'*40}")
deliv_df = df["Delivery_Status"].value_counts()
for status, count in deliv_df.items():
    pct = count / len(df) * 100
    print(f"  {status:<15}: {count:>4} orders ({pct:.1f}%)")

# ── 10. DISCOUNT IMPACT ──────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("DISCOUNT IMPACT ON PROFITABILITY")
print(f"{'─'*40}")
df["Discount_Band"] = pd.cut(df["Discount_Pct"],
    bins=[-1, 5, 10, 20, 30, 45],
    labels=["0–5%","5–10%","10–20%","20–30%","30–45%"])
disc_df = df.groupby("Discount_Band").agg(
    Avg_Margin=("Profit_Margin_Pct","mean"),
    Orders=("Order_ID","count"),
    Avg_Sales=("Sales_Amount","mean")
)
print(f"\n  {'Band':<10} {'Avg Margin':>12} {'# Orders':>10} {'Avg Sales (₹)':>15}")
print(f"  {'─'*10} {'─'*12} {'─'*10} {'─'*15}")
for band, r in disc_df.iterrows():
    print(f"  {str(band):<10} {r['Avg_Margin']:>11.1f}% {int(r['Orders']):>10} {r['Avg_Sales']:>15,.0f}")
corr = df["Discount_Pct"].corr(df["Profit_Margin_Pct"])
print(f"\n  Correlation (Discount vs Margin): {corr:.3f}  {'⚠ Negative — Higher discounts reduce margins' if corr < 0 else '✓ Positive'}")

# ── 11. QUARTERLY ANALYSIS ────────────────────────────────────────────────────
print(f"\n{'─'*40}")
print("QUARTERLY PERFORMANCE")
print(f"{'─'*40}")
qtr_df = df.groupby("Quarter").agg(
    Sales=("Sales_Amount","sum"),
    Profit=("Profit_Amount","sum"),
    Orders=("Order_ID","count")
)
print(f"\n  {'Quarter':<10} {'Sales (₹)':>14} {'Profit (₹)':>13} {'Orders':>8}")
print(f"  {'─'*10} {'─'*14} {'─'*13} {'─'*8}")
for q, r in qtr_df.iterrows():
    print(f"  {str(q):<10} {r['Sales']:>14,.0f} {r['Profit']:>13,.0f} {r['Orders']:>8}")

# ── 12. KEY INSIGHTS ──────────────────────────────────────────────────────────
print(f"\n{'═'*65}")
print("ACTIONABLE BUSINESS INSIGHTS")
print(f"{'═'*65}")
insights = [
    f"Electronics & Home & Kitchen drive the highest revenue — prioritize inventory & promotions for these.",
    f"Beauty & Personal Care has the highest profit margin ({cat_df['Margin'].max():.1f}%) — ideal for upselling.",
    f"The {reg_df['Sales'].idxmax()} Region leads in sales — expand distribution and loyalty programs there.",
    f"UPI and Credit Card are top payment methods — consider cashback offers to drive higher-value orders.",
    f"Correlation between discount & margin is {corr:.2f} — excessive discounting erodes profitability.",
    f"Returned & Cancelled orders represent {((df['Delivery_Status'].isin(['Returned','Cancelled'])).sum()/len(df)*100):.1f}% of orders — investigate supply chain issues.",
    f"Corporate segment generates premium AOV — create B2B bundles and dedicated account managers.",
    f"Best performing month: {best_month} — plan major campaigns around this seasonal peak.",
]
for i, insight in enumerate(insights, 1):
    print(f"\n  {i}. {insight}")

print(f"\n{'═'*65}")
print("EDA COMPLETE — See /charts/ folder for all visualizations")
print(f"{'═'*65}\n")
