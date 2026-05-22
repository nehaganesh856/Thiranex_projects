
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


folders = [
    "raw_data",
    "cleaned_data",
    "reports",
    "charts"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# =========================================================
# CREATE SAMPLE DATASET (IF FILE DOES NOT EXIST)
# =========================================================

file_path = "raw_data/sales_data.csv"

if not os.path.exists(file_path):

    sample_data = {
        "Order ID": [101, 102, 103, 104, 104, 105, 106, 107],
        "Product": ["Laptop", "Mouse", "Keyboard", None,
                    "Monitor", "mouse", "Laptop ", "Keyboard"],
        "Quantity": [2, 5, np.nan, 3, 3, 4, 1, 2],
        "Price": [50000, 500, 1500, 12000, 12000, np.nan, 52000, 1500],
        "Date": [
            "2025-01-10",
            "2025-01-11",
            "2025-01-12",
            "2025-01-13",
            "2025-01-13",
            "2025-01-14",
            "2025-01-15",
            "2025-01-16"
        ]
    }

    sample_df = pd.DataFrame(sample_data)

    sample_df.to_csv(file_path, index=False)

    print("Sample dataset created successfully!\n")

# =========================================================
# LOAD DATASET
# =========================================================

print("Loading Dataset...\n")

df = pd.read_csv(file_path)

print("Original Dataset:")
print(df)

# =========================================================
# DATA CLEANING
# =========================================================

print("\n================ DATA CLEANING STARTED ================\n")

# ---------------------------------------------------------
# REMOVE EMPTY ROWS
# ---------------------------------------------------------

df.dropna(how='all', inplace=True)

# ---------------------------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------------------------

df.drop_duplicates(inplace=True)

# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

df.columns = df.columns.str.strip()

# ---------------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------------

# Fill missing Product names
df['Product'] = df['Product'].fillna("Unknown")

# Fill missing Quantity with mean
df['Quantity'] = df['Quantity'].fillna(df['Quantity'].mean())

# Fill missing Price with mean
df['Price'] = df['Price'].fillna(df['Price'].mean())

# ---------------------------------------------------------
# FIX INCONSISTENT TEXT
# ---------------------------------------------------------

df['Product'] = df['Product'].str.strip()
df['Product'] = df['Product'].str.title()

# ---------------------------------------------------------
# CONVERT DATE FORMAT
# ---------------------------------------------------------

df['Date'] = pd.to_datetime(df['Date'])

# ---------------------------------------------------------
# CREATE NEW COLUMN
# ---------------------------------------------------------

df['Total'] = df['Quantity'] * df['Price']

# =========================================================
# DISPLAY CLEANED DATA
# =========================================================

print("Cleaned Dataset:\n")

print(df)

# =========================================================
# SAVE CLEANED DATA
# =========================================================

cleaned_file = "cleaned_data/cleaned_sales_data.csv"

df.to_csv(cleaned_file, index=False)

print("\nCleaned data saved successfully!")

# =========================================================
# DATA ANALYSIS & REPORTING
# =========================================================

print("\n================ REPORT GENERATION ================\n")

# ---------------------------------------------------------
# BASIC STATISTICS
# ---------------------------------------------------------

total_revenue = df['Total'].sum()
average_sales = df['Total'].mean()
highest_sale = df['Total'].max()
lowest_sale = df['Total'].min()

print(f"Total Revenue : {total_revenue}")
print(f"Average Sales : {average_sales}")
print(f"Highest Sale  : {highest_sale}")
print(f"Lowest Sale   : {lowest_sale}")

# ---------------------------------------------------------
# PRODUCT WISE SALES
# ---------------------------------------------------------

product_sales = df.groupby('Product')['Total'].sum()

print("\nProduct Wise Sales:\n")

print(product_sales)

# =========================================================
# CREATE CHART
# =========================================================

print("\nGenerating Chart...\n")

plt.figure(figsize=(8, 5))

product_sales.plot(kind='bar')

plt.title("Product Wise Revenue")

plt.xlabel("Products")

plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

chart_path = "charts/product_sales_chart.png"

plt.savefig(chart_path)

plt.show()

print("Chart saved successfully!")

# =========================================================
# EXPORT EXCEL REPORT
# =========================================================

report_file = "reports/summary_report.xlsx"

with pd.ExcelWriter(report_file, engine='openpyxl') as writer:

    # Save cleaned data
    df.to_excel(writer,
                sheet_name='Cleaned Data',
                index=False)

    # Save summary report
    summary_df = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Average Sales",
            "Highest Sale",
            "Lowest Sale"
        ],
        "Value": [
            total_revenue,
            average_sales,
            highest_sale,
            lowest_sale
        ]
    })

    summary_df.to_excel(writer,
                        sheet_name='Summary',
                        index=False)

    # Save product sales
    product_sales.to_excel(writer,
                           sheet_name='Product Sales')

print("\nExcel report generated successfully!")

# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n================ PROJECT COMPLETED ================\n")

print("Generated Files:")

print(f"1. Cleaned CSV  : {cleaned_file}")
print(f"2. Excel Report : {report_file}")
print(f"3. Sales Chart  : {chart_path}")

print("\nAutomation Completed Successfully!")


"""
import streamlit as st
import pandas as pd

df = pd.read_csv("cleaned_data/cleaned_sales_data.csv")

st.title("Data Cleaning Dashboard")

st.subheader("Cleaned Dataset")

st.dataframe(df)

st.metric("Total Revenue", round(df['Total'].sum(), 2))

st.metric("Average Sales", round(df['Total'].mean(), 2))

st.subheader("Product Wise Revenue")

product_sales = df.groupby('Product')['Total'].sum()

st.bar_chart(product_sales)

st.success("Dashboard Loaded Successfully!")
"""
