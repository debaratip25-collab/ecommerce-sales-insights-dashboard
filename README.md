# 📊 E-Commerce Sales Insights Dashboard

> A complete, industry-oriented data analytics project analyzing e-commerce sales performance, product profitability, regional trends, and customer behavior — built with Python, pandas, and matplotlib.

---

## 🎯 Objective

To design and execute a comprehensive sales analytics project that provides actionable insights into:
- Product performance and category profitability
- Regional revenue and margin trends
- Customer behavior and segmentation
- Payment and delivery operational metrics
- Impact of discounts on profitability

This project mirrors how e-commerce companies like **Amazon, Flipkart, and Meesho** use data analytics to drive business decisions.

---

## 📁 Project Structure

```
ecommerce-sales-insights-dashboard/
│
├── data/
│   ├── ecommerce_sales_data.csv       # Primary dataset (310 orders)
│
├── charts/
│   ├── 01_kpi_cards.png               # KPI Summary Cards
│   ├── 02_monthly_trend.png           # Monthly Sales & Profit Trend
│   ├── 03_category_revenue.png        # Category-wise Revenue & Profit
│   ├── 04_region_analysis.png         # Region-wise Sales Analysis
│   ├── 05_top_products.png            # Top 10 Products by Revenue
│   ├── 06_profit_margin_category.png  # Profit Margin % by Category
│   ├── 07_customer_segment.png        # Customer Segment Analysis
│   ├── 08_payment_method.png          # Payment Method Analysis
│   ├── 09_delivery_status.png         # Delivery Status Distribution
│   ├── 10_top_customers.png           # Top 10 High-Value Customers
│   ├── 11_discount_profit_scatter.png # Discount vs Profit Impact
│   └── 12_shipping_mode.png           # Shipping Mode Analysis
│
├── python/
    ├── generate_dataset.py                # Dataset generation script
    ├── generate_charts.py                 # All 12 visualization scripts
    ├── eda_analysis.py                    # Full EDA with business insights
│
├── dashboard/
    ├── master_dashboard.png           # Main dashboard
│     
└── README.md                          # Project documentation (this file)
```

---

## 📋 Dataset Description

A **synthetic but realistic** e-commerce dataset covering **310 orders** across January–December 2024.

| Column | Description |
|--------|-------------|
| `Order_ID` | Unique order identifier (ORD-XXXX) |
| `Customer_ID` | Unique customer identifier (CXXXX) |
| `Customer_Name` | Customer full name |
| `Order_Date` | Date of order placement |
| `Region` | Geographic region (North / South / East / West) |
| `State` | Indian state |
| `City` | City of delivery |
| `Product_Category` | Product category (6 categories) |
| `Product_Name` | Product name (59 unique products) |
| `Quantity_Sold` | Units ordered |
| `Unit_Price` | Price per unit (₹) |
| `Discount_Pct` | Discount applied (%) |
| `Sales_Amount` | Net revenue after discount |
| `Cost_Amount` | Cost of goods sold |
| `Profit_Amount` | Net profit |
| `Profit_Margin_Pct` | Profit as % of sales |
| `Payment_Method` | UPI / Credit Card / Debit Card / EMI / Net Banking / COD |
| `Shipping_Mode` | Standard / Express / Same Day / Economy |
| `Delivery_Status` | Delivered / In Transit / Returned / Cancelled |
| `Customer_Segment` | Consumer / Corporate / Small Business / Home Office |

### Dataset Snapshot

```
Total Orders      : 310
Unique Customers  : 78
Unique Products   : 59
Categories        : 6
Regions           : 4
Date Range        : Jan 2024 – Dec 2024
Total Revenue     : ₹98.14 Lakhs
Total Profit      : ₹35.33 Lakhs
Avg Profit Margin : 43.4%
Avg Order Value   : ₹31,659
```

---

## 🛠️ Methodology

### Step 1 — Data Collection & Structuring
- Designed schema covering all transactional, geographic, product, and customer dimensions
- Generated 310 realistic orders using Python (random + numpy seeded for reproducibility)
- Covered 4 regions, 16 states, and 48 cities across India

### Step 2 — Data Cleaning & Transformation
- Validated zero missing values and zero duplicate Order_IDs
- Ensured date parsing consistency via `pd.to_datetime()`
- Derived computed columns: Sales_Amount, Profit_Margin_Pct, Cost_Amount
- Added Month, Quarter, and Discount_Band grouping columns for trend analysis

### Step 3 — KPI Definition
DAX-equivalent formulas (Python implementation):
```
Total Revenue     = SUM(Sales_Amount)
Total Profit      = SUM(Profit_Amount)
Profit Margin %   = (Profit_Amount / Sales_Amount) × 100
AOV               = Total Revenue / Total Orders
Sales Growth MoM  = (Current Month Sales − Previous Month Sales) / Previous Month Sales × 100
```

### Step 4 — Exploratory Data Analysis
- Monthly and quarterly trend analysis
- Category-wise and region-wise revenue & margin breakdown
- Top 10 product and customer ranking
- Payment method and delivery operational analysis
- Discount vs profit margin correlation analysis

### Step 5 — Visualization & Dashboard
- 12 professional charts using matplotlib with dark corporate theme
- Covers KPIs, trends, category, region, customer, payment, and delivery dimensions

---

## 📈 Analysis Performed

| Analysis Type | Key Question Answered |
|---------------|-----------------------|
| Sales Trend | Which months/quarters peak? |
| Category Analysis | Which category earns most revenue and best margin? |
| Regional Analysis | Which region leads in sales and profitability? |
| Product Analysis | Which are the top 10 revenue-generating products? |
| Customer Analysis | Who are the top 10 high-value customers? |
| Segment Analysis | Which customer segment has highest AOV? |
| Payment Analysis | Which payment mode is most preferred? |
| Delivery Analysis | What % of orders are returned or cancelled? |
| Discount Impact | How do discounts affect profit margin? |

---

## 🖥️ Dashboard Features

- **KPI Cards** — Total Sales, Total Profit, Orders, AOV, Profit Margin, Unique Customers
- **Monthly Trend Chart** — Line chart with MoM sales and profit trend
- **Category Revenue Chart** — Horizontal bar chart showing revenue and profit by category
- **Region Analysis** — Donut chart and bar chart for regional distribution
- **Top 10 Products** — Horizontal bar chart sorted by revenue
- **Profit Margin by Category** — Comparison vs average benchmark
- **Customer Segment** — Bar + donut for segment-wise performance
- **Payment Method** — Bar + line dual-axis chart
- **Delivery Status** — Donut and horizontal bar
- **Top 10 Customers** — Ranked by lifetime value
- **Discount vs Margin Scatter** — Correlation visualization with trend line
- **Shipping Mode** — Side-by-side order volume and revenue comparison

---

## 💡 Key Business Insights

1. **Electronics dominates** — 51.4% of total revenue (₹50.5 Lakhs). Cross-selling accessories here offers strong upside.

2. **Beauty & Personal Care has the highest margin (51.9%)** — though small in volume, this category should be prioritized for upselling and premium positioning.

3. **East Region leads in sales (30.2%)** but has the lowest margin — logistics cost review recommended.

4. **North Region has the highest margin (45.1%)** — good candidate for premium product launches.

5. **Bluetooth Speakers and Smartwatches** are the top 2 revenue-generating products — keep adequately stocked.

6. **Q3 (Jul–Sep) is the strongest quarter** at ₹29.75 Lakhs — ideal window for big campaign investments.

7. **UPI is the #1 payment method** — cashback offers via UPI can significantly boost conversion rates.

8. **31% of orders are returned or cancelled** — a critical operational issue requiring logistics and quality review.

9. **Corporate segment contributes 33.5% of revenue** — dedicated B2B account management can improve retention.

10. **Higher discounts correlate with lower revenue per order**, suggesting a value-destruction risk from blanket discount campaigns.

---

## ✅ Conclusion

This project demonstrates end-to-end data analytics workflow — from data generation and cleaning through EDA, visualization, and business insight extraction. The dashboard provides a 360° view of e-commerce business health and equips analysts and business leaders with the information needed to:

- Optimize product mix and inventory planning
- Improve regional marketing spend efficiency
- Reduce churn through better delivery and returns management
- Design targeted promotions for high-value customer segments

---

## 🧑‍💻 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core programming language |
| pandas | Data manipulation & EDA |
| matplotlib | Chart generation |
| numpy | Numerical computation |
| openpyxl | 

---

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ecommerce-sales-insights-dashboard.git
cd ecommerce-sales-insights-dashboard

# 2. Install dependencies
pip install pandas matplotlib numpy openpyxl

# 3. Generate the dataset
python generate_dataset.py

# 4. Run EDA analysis (prints full report)
python eda_analysis.py

# 5. Generate all 12 charts
python generate_charts.py
# Charts saved to /charts/ folder
```
---

*Project by: Debarati Pal*
