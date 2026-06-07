import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("/home/claude/ecommerce-dashboard/dataset/ecommerce_sales_data.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M")
df["Month_Label"] = df["Order_Date"].dt.strftime("%b %Y")

# ── Palette ────────────────────────────────────────────────────────────────────
DARK_BG   = "#1a1f2e"
CARD_BG   = "#242b3d"
ACCENT1   = "#4f8ef7"   # blue
ACCENT2   = "#f7c948"   # gold
ACCENT3   = "#3ecf8e"   # green
ACCENT4   = "#f75b5b"   # red
ACCENT5   = "#a78bfa"   # purple
TEXT_MAIN = "#e8eaf0"
TEXT_SUB  = "#8892a4"
GRID_CLR  = "#2e3650"

CAT_COLORS = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, "#f97316"]
REG_COLORS = {"North": ACCENT1, "South": ACCENT3, "East": ACCENT2, "West": ACCENT4}

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    DARK_BG,
    "axes.edgecolor":    GRID_CLR,
    "axes.labelcolor":   TEXT_MAIN,
    "xtick.color":       TEXT_SUB,
    "ytick.color":       TEXT_SUB,
    "text.color":        TEXT_MAIN,
    "grid.color":        GRID_CLR,
    "grid.linewidth":    0.5,
    "font.family":       "DejaVu Sans",
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
})

def savefig(name):
    path = f"/home/claude/ecommerce-dashboard/charts/{name}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"  ✓ {name}.png")

def fmt_inr(x, _=None):
    if x >= 1_000_000: return f"₹{x/1_000_000:.1f}M"
    if x >= 1_000:     return f"₹{x/1_000:.0f}K"
    return f"₹{x:.0f}"

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 – KPI Summary Cards
# ══════════════════════════════════════════════════════════════════════════════
print("Generating charts …")

total_sales   = df["Sales_Amount"].sum()
total_profit  = df["Profit_Amount"].sum()
total_orders  = len(df)
aov           = total_sales / total_orders
avg_margin    = df["Profit_Margin_Pct"].mean()
unique_cust   = df["Customer_ID"].nunique()

kpis = [
    ("Total Sales",     f"₹{total_sales/1e6:.2f}M",   ACCENT1),
    ("Total Profit",    f"₹{total_profit/1e6:.2f}M",  ACCENT3),
    ("Total Orders",    f"{total_orders:,}",            ACCENT2),
    ("Avg Order Value", f"₹{aov:,.0f}",                ACCENT5),
    ("Profit Margin",   f"{avg_margin:.1f}%",           ACCENT4),
    ("Unique Customers",f"{unique_cust}",               "#f97316"),
]

fig, axes = plt.subplots(1, 6, figsize=(18, 3))
fig.patch.set_facecolor(DARK_BG)

for ax, (title, val, clr) in zip(axes, kpis):
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(clr); spine.set_linewidth(2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(0.5, 0.62, val,  transform=ax.transAxes, ha="center", va="center",
            fontsize=18, fontweight="bold", color=clr)
    ax.text(0.5, 0.25, title, transform=ax.transAxes, ha="center", va="center",
            fontsize=9, color=TEXT_SUB)

fig.suptitle("E-Commerce Sales Insights Dashboard — KPI Summary (2024)",
             fontsize=14, fontweight="bold", color=TEXT_MAIN, y=1.06)
plt.tight_layout(pad=0.6)
savefig("01_kpi_cards")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 2 – Monthly Sales & Profit Trend
# ══════════════════════════════════════════════════════════════════════════════
monthly = df.groupby("Month").agg(Sales=("Sales_Amount","sum"),
                                   Profit=("Profit_Amount","sum")).reset_index()
monthly["MonthStr"] = monthly["Month"].dt.strftime("%b")

fig, ax = plt.subplots(figsize=(13, 5))
x = range(len(monthly))

ax.fill_between(x, monthly["Sales"], alpha=0.12, color=ACCENT1)
ax.plot(x, monthly["Sales"],  marker="o", color=ACCENT1, linewidth=2.5,
        markersize=7, label="Monthly Sales")
ax.fill_between(x, monthly["Profit"], alpha=0.12, color=ACCENT3)
ax.plot(x, monthly["Profit"], marker="s", color=ACCENT3, linewidth=2.5,
        markersize=7, linestyle="--", label="Monthly Profit")

for i, row in monthly.iterrows():
    ax.annotate(f"₹{row['Sales']/1000:.0f}K", (i, row["Sales"]),
                textcoords="offset points", xytext=(0,10),
                ha="center", fontsize=7.5, color=ACCENT1)

ax.set_xticks(list(x)); ax.set_xticklabels(monthly["MonthStr"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Monthly Sales & Profit Trend — 2024", pad=12)
ax.set_xlabel("Month"); ax.set_ylabel("Amount (₹)")
ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN)
ax.grid(axis="y", linestyle="--")
plt.tight_layout()
savefig("02_monthly_trend")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 – Category-wise Revenue & Profit
# ══════════════════════════════════════════════════════════════════════════════
cat = df.groupby("Product_Category").agg(Sales=("Sales_Amount","sum"),
                                          Profit=("Profit_Amount","sum")).sort_values("Sales", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
y = range(len(cat))
bar_h = 0.38
bars1 = ax.barh([i+bar_h/2 for i in y], cat["Sales"],  height=bar_h, color=ACCENT1, label="Sales")
bars2 = ax.barh([i-bar_h/2 for i in y], cat["Profit"], height=bar_h, color=ACCENT3, label="Profit")

for bar in bars1:
    ax.text(bar.get_width()+20000, bar.get_y()+bar.get_height()/2,
            f"₹{bar.get_width()/1e6:.2f}M", va="center", fontsize=8, color=ACCENT1)
for bar in bars2:
    ax.text(bar.get_width()+20000, bar.get_y()+bar.get_height()/2,
            f"₹{bar.get_width()/1e6:.2f}M", va="center", fontsize=8, color=ACCENT3)

ax.set_yticks(list(y)); ax.set_yticklabels(cat.index, fontsize=10)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Category-wise Revenue & Profit", pad=12)
ax.set_xlabel("Amount (₹)")
ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN)
ax.grid(axis="x", linestyle="--")
plt.tight_layout()
savefig("03_category_revenue")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 – Region-wise Sales (Donut)
# ══════════════════════════════════════════════════════════════════════════════
reg = df.groupby("Region")["Sales_Amount"].sum().sort_values(ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
colors = [REG_COLORS[r] for r in reg.index]
wedges, texts, autotexts = ax1.pie(
    reg.values, labels=reg.index, colors=colors,
    autopct="%1.1f%%", startangle=90,
    wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2),
    textprops=dict(color=TEXT_MAIN, fontsize=11)
)
for at in autotexts:
    at.set_fontsize(10); at.set_color(DARK_BG); at.set_fontweight("bold")
ax1.set_title("Region-wise Sales Distribution", pad=12)

reg_profit = df.groupby("Region").agg(Sales=("Sales_Amount","sum"),
                                       Profit=("Profit_Amount","sum"),
                                       Margin=("Profit_Margin_Pct","mean")).sort_values("Sales", ascending=False)
bars = ax2.bar(reg_profit.index, reg_profit["Sales"], color=[REG_COLORS[r] for r in reg_profit.index],
               width=0.5, edgecolor=DARK_BG, linewidth=0.8)
for bar, (_, row) in zip(bars, reg_profit.iterrows()):
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+15000,
             f"₹{bar.get_height()/1e6:.2f}M\n{row['Margin']:.1f}% margin",
             ha="center", fontsize=9, color=TEXT_MAIN)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax2.set_title("Region-wise Sales & Margin", pad=12)
ax2.set_ylabel("Sales Amount (₹)")
ax2.grid(axis="y", linestyle="--")

plt.tight_layout()
savefig("04_region_analysis")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 5 – Top 10 Products by Revenue
# ══════════════════════════════════════════════════════════════════════════════
prod = df.groupby("Product_Name").agg(Sales=("Sales_Amount","sum"),
                                       Profit=("Profit_Amount","sum")).nlargest(10,"Sales").sort_values("Sales")

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(prod.index, prod["Sales"], color=ACCENT1, alpha=0.85, edgecolor=DARK_BG)
ax.barh(prod.index, prod["Profit"], color=ACCENT3, alpha=0.85, edgecolor=DARK_BG)
for bar in bars:
    ax.text(bar.get_width()+5000, bar.get_y()+bar.get_height()/2,
            f"₹{bar.get_width()/1000:.0f}K", va="center", fontsize=8.5, color=ACCENT1)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Top 10 Products by Revenue", pad=12)
ax.set_xlabel("Amount (₹)")
patch1 = mpatches.Patch(color=ACCENT1, label="Sales")
patch2 = mpatches.Patch(color=ACCENT3, label="Profit")
ax.legend(handles=[patch1, patch2], facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN)
ax.grid(axis="x", linestyle="--")
plt.tight_layout()
savefig("05_top_products")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 6 – Profitability by Category (Profit Margin %)
# ══════════════════════════════════════════════════════════════════════════════
cat_margin = df.groupby("Product_Category")["Profit_Margin_Pct"].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(cat_margin.index, cat_margin.values, color=CAT_COLORS,
              edgecolor=DARK_BG, linewidth=0.8, width=0.6)
for bar, val in zip(bars, cat_margin.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold", color=TEXT_MAIN)
ax.set_title("Average Profit Margin % by Category", pad=12)
ax.set_ylabel("Profit Margin (%)")
ax.set_xticklabels(cat_margin.index, rotation=20, ha="right")
ax.axhline(cat_margin.mean(), color=ACCENT2, linestyle="--", linewidth=1.5, label=f"Avg: {cat_margin.mean():.1f}%")
ax.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN)
ax.grid(axis="y", linestyle="--")
plt.tight_layout()
savefig("06_profit_margin_category")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 7 – Customer Segment Analysis
# ══════════════════════════════════════════════════════════════════════════════
seg = df.groupby("Customer_Segment").agg(Sales=("Sales_Amount","sum"),
                                          Orders=("Order_ID","count"),
                                          Profit=("Profit_Amount","sum")).sort_values("Sales", ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
seg_colors = [ACCENT1, ACCENT2, ACCENT3, ACCENT5]

bars = axes[0].bar(seg.index, seg["Sales"], color=seg_colors, edgecolor=DARK_BG, width=0.55)
for bar in bars:
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+5000,
                 f"₹{bar.get_height()/1e6:.2f}M", ha="center", fontsize=9, color=TEXT_MAIN)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[0].set_title("Sales by Customer Segment", pad=12)
axes[0].set_ylabel("Sales Amount (₹)")
axes[0].grid(axis="y", linestyle="--")

wedges, texts, ats = axes[1].pie(seg["Orders"], labels=seg.index, colors=seg_colors,
    autopct="%1.1f%%", startangle=140,
    wedgeprops=dict(edgecolor=DARK_BG, linewidth=1.5),
    textprops=dict(color=TEXT_MAIN, fontsize=11))
for at in ats: at.set_fontsize(10); at.set_color(DARK_BG); at.set_fontweight("bold")
axes[1].set_title("Order Share by Customer Segment", pad=12)

plt.tight_layout()
savefig("07_customer_segment")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 8 – Payment Method Analysis
# ══════════════════════════════════════════════════════════════════════════════
pay = df.groupby("Payment_Method").agg(Orders=("Order_ID","count"),
                                        Sales=("Sales_Amount","sum")).sort_values("Sales", ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
pay_colors = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, "#f97316"]
bars = ax.bar(pay.index, pay["Sales"], color=pay_colors, edgecolor=DARK_BG, width=0.6)
ax2 = ax.twinx()
ax2.plot(pay.index, pay["Orders"], marker="D", color=TEXT_MAIN, linewidth=2, markersize=8, label="# Orders")
ax2.set_ylabel("Number of Orders", color=TEXT_MAIN)
ax2.tick_params(axis="y", labelcolor=TEXT_SUB)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8000,
            f"₹{bar.get_height()/1e6:.2f}M", ha="center", fontsize=8.5, color=TEXT_MAIN)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Payment Method — Sales & Order Volume", pad=12)
ax.set_ylabel("Sales Amount (₹)")
ax.set_xticklabels(pay.index, rotation=15, ha="right")
ax.grid(axis="y", linestyle="--")
ax2.legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN, loc="upper right")
plt.tight_layout()
savefig("08_payment_method")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 9 – Delivery Status Analysis
# ══════════════════════════════════════════════════════════════════════════════
deliv = df["Delivery_Status"].value_counts()
deliv_colors = {"Delivered": ACCENT3, "In Transit": ACCENT2, "Returned": ACCENT4, "Cancelled": "#f97316"}
colors_d = [deliv_colors.get(s, ACCENT5) for s in deliv.index]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
wedges, texts, ats = ax1.pie(deliv.values, labels=deliv.index, colors=colors_d,
    autopct="%1.1f%%", startangle=90,
    wedgeprops=dict(edgecolor=DARK_BG, linewidth=1.5),
    textprops=dict(color=TEXT_MAIN, fontsize=11))
for at in ats: at.set_fontsize(10); at.set_color(DARK_BG); at.set_fontweight("bold")
ax1.set_title("Delivery Status Distribution", pad=12)

deliv_sales = df.groupby("Delivery_Status")["Sales_Amount"].sum().loc[deliv.index]
bars = ax2.barh(deliv_sales.index, deliv_sales.values, color=colors_d, edgecolor=DARK_BG, height=0.5)
for bar in bars:
    ax2.text(bar.get_width()+10000, bar.get_y()+bar.get_height()/2,
             f"₹{bar.get_width()/1e6:.2f}M", va="center", fontsize=9, color=TEXT_MAIN)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax2.set_title("Sales Amount by Delivery Status", pad=12)
ax2.set_xlabel("Sales Amount (₹)")
ax2.grid(axis="x", linestyle="--")
plt.tight_layout()
savefig("09_delivery_status")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 10 – Top 10 Customers by Revenue
# ══════════════════════════════════════════════════════════════════════════════
cust = df.groupby(["Customer_ID","Customer_Name"]).agg(
    Sales=("Sales_Amount","sum"), Orders=("Order_ID","count")).reset_index()
cust["Label"] = cust["Customer_Name"] + "\n(" + cust["Customer_ID"] + ")"
top_cust = cust.nlargest(10, "Sales").sort_values("Sales")

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(top_cust["Label"], top_cust["Sales"], color=ACCENT5, edgecolor=DARK_BG, height=0.6)
for bar, orders in zip(bars, top_cust["Orders"]):
    ax.text(bar.get_width()+3000, bar.get_y()+bar.get_height()/2,
            f"₹{bar.get_width()/1000:.0f}K  |  {orders} orders", va="center", fontsize=8.5, color=TEXT_MAIN)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Top 10 High-Value Customers", pad=12)
ax.set_xlabel("Total Sales Amount (₹)")
ax.grid(axis="x", linestyle="--")
plt.tight_layout()
savefig("10_top_customers")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 11 – Discount vs Profit Margin Scatter
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 6))
scatter_colors = [CAT_COLORS[list(df["Product_Category"].unique()).index(c) % len(CAT_COLORS)]
                  for c in df["Product_Category"]]
sc = ax.scatter(df["Discount_Pct"], df["Profit_Margin_Pct"],
                c=[CAT_COLORS[i % len(CAT_COLORS)] for i in df["Product_Category"].astype("category").cat.codes],
                alpha=0.55, s=40, edgecolors="none")
z = np.polyfit(df["Discount_Pct"], df["Profit_Margin_Pct"], 1)
p = np.poly1d(z)
xs = np.linspace(df["Discount_Pct"].min(), df["Discount_Pct"].max(), 100)
ax.plot(xs, p(xs), color=ACCENT2, linewidth=2, linestyle="--", label="Trend Line")
ax.set_title("Discount % vs Profit Margin % — Impact Analysis", pad=12)
ax.set_xlabel("Discount %"); ax.set_ylabel("Profit Margin %")
patches = [mpatches.Patch(color=CAT_COLORS[i], label=c)
           for i, c in enumerate(df["Product_Category"].unique())]
patches.append(mpatches.Patch(color=ACCENT2, label="Trend"))
ax.legend(handles=patches, facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN,
          fontsize=8, ncol=2, loc="upper right")
ax.grid(linestyle="--")
plt.tight_layout()
savefig("11_discount_profit_scatter")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 12 – Shipping Mode Analysis
# ══════════════════════════════════════════════════════════════════════════════
ship = df.groupby("Shipping_Mode").agg(Orders=("Order_ID","count"),
                                        Sales=("Sales_Amount","sum"),
                                        Profit=("Profit_Amount","sum")).sort_values("Sales", ascending=False)
ship_colors = [ACCENT1, ACCENT2, ACCENT3, ACCENT4]
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].bar(ship.index, ship["Orders"], color=ship_colors, edgecolor=DARK_BG, width=0.55)
for i, (idx, row) in enumerate(ship.iterrows()):
    axes[0].text(i, row["Orders"]+1, str(int(row["Orders"])), ha="center", fontsize=11, color=TEXT_MAIN)
axes[0].set_title("Orders by Shipping Mode", pad=12)
axes[0].set_ylabel("Number of Orders")
axes[0].grid(axis="y", linestyle="--")

width = 0.38
x = np.arange(len(ship))
b1 = axes[1].bar(x - width/2, ship["Sales"]/1e6, width, color=ship_colors, edgecolor=DARK_BG, label="Sales (₹M)")
b2 = axes[1].bar(x + width/2, ship["Profit"]/1e6, width, color=[c+"aa" for c in ship_colors],
                  edgecolor=DARK_BG, label="Profit (₹M)", hatch="//")
axes[1].set_xticks(x); axes[1].set_xticklabels(ship.index)
axes[1].set_title("Sales & Profit by Shipping Mode", pad=12)
axes[1].set_ylabel("Amount (₹ Million)")
axes[1].legend(facecolor=CARD_BG, edgecolor=GRID_CLR, labelcolor=TEXT_MAIN)
axes[1].grid(axis="y", linestyle="--")
plt.tight_layout()
savefig("12_shipping_mode")

print("\nAll 12 charts generated successfully!")
