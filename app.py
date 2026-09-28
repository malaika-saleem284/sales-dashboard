import streamlit as st
import pandas as pd

st.title("Sales Dashboard")
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    df["Month"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")

    # Sidebar filters
    cities = ["All"] + list(df["City"].unique())
    selected_city = st.sidebar.selectbox("Filter by city", cities)

    categories = ["All"] + list(df["Category"].unique())
    selected_category = st.sidebar.selectbox("Filter by category", categories)

    # Apply filters
    filtered_df = df

    if selected_city != "All":
        filtered_df = filtered_df[filtered_df["City"] == selected_city]

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    st.dataframe(filtered_df)
    st.write(f"Total rows: {len(filtered_df)}")

    # KPI calculations
    total_sales = filtered_df["Sales"].sum()
    total_orders = len(filtered_df)
    avg_order = filtered_df["Sales"].mean()

    # KPI cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Sales", f"Rs {total_sales:,.0f}")

    with col2:
        st.metric("Total Orders", total_orders)

    with col3:
        st.metric("Average Order Value", f"Rs {avg_order:,.0f}")

    # Charts
    st.subheader("Sales by Category")
    category_sales = filtered_df.groupby("Category")["Sales"].sum()
    st.bar_chart(category_sales)

    st.subheader("Monthly Sales Trend")
    monthly_sales = filtered_df.groupby("Month")["Sales"].sum()
    st.line_chart(monthly_sales)