import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


df = pd.read_csv("sales.csv", encoding='latin1')

st.write(df.columns)
df.columns = df.columns.str.strip()
df.rename(columns={
    'Order Date': 'Date',
    'Product Name': 'Product',
    'Sales': 'Revenue'
}, inplace=True)


if 'Revenue' not in df.columns:

    if 'Sales' in df.columns:
        df['Revenue'] = df['Sales']

    elif 'Price' in df.columns and 'Quantity' in df.columns:
        df['Revenue'] = df['Price'] * df['Quantity']


if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])


st.sidebar.header("Filter Dashboard")


if 'Region' in df.columns:

    region = st.sidebar.multiselect(
        "Select Region",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    df = df[df['Region'].isin(region)]


if 'Category' in df.columns:

    category = st.sidebar.multiselect(
        "Select Category",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    df = df[df['Category'].isin(category)]


total_revenue = df['Revenue'].sum()

total_orders = len(df)

average_sales = df['Revenue'].mean()

top_product = "N/A"

if 'Product' in df.columns:
    top_product = (
        df.groupby('Product')['Revenue']
        .sum()
        .idxmax()
    )


st.title("📊 Sales & Revenue Dashboard")

st.markdown("Interactive business dashboard using Python and Streamlit")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")

col2.metric("Total Orders", total_orders)

col3.metric("Average Sales", f"₹{average_sales:,.0f}")

col4.metric("Top Product", top_product)


if 'Date' in df.columns:

    monthly_sales = (
        df.groupby(df['Date'].dt.to_period('M'))['Revenue']
        .sum()
        .reset_index()
    )

    monthly_sales['Date'] = monthly_sales['Date'].astype(str)

    fig1 = px.line(
        monthly_sales,
        x='Date',
        y='Revenue',
        title="Monthly Revenue Trend",
        markers=True
    )

    st.plotly_chart(fig1, use_container_width=True)


if 'Product' in df.columns:

    top_products = (
        df.groupby('Product')['Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top_products,
        x='Product',
        y='Revenue',
        title="Top 10 Products"
    )

    st.plotly_chart(fig2, use_container_width=True)

if 'Region' in df.columns:

    region_sales = (
        df.groupby('Region')['Revenue']
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        region_sales,
        names='Region',
        values='Revenue',
        title="Region-wise Revenue"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Sales Data")

st.dataframe(df)

csv = df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_sales.csv',
    mime='text/csv'
)