import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Dataset
data = pd.read_csv('product_sales_clean.csv')

# Create Filter By "Week"
with st.sidebar:
     st.sidebar.header("Week:")
     min_week = data['week'].min()
     max_week = data['week'].max()
     min_value, max_value = st.slider("Select Week :",
                                 min_value=min_week,
                                 max_value=max_week,
                                 value=[min_week, max_week]
                                )
     data = data[(data['week'] >= min_value) & (data['week'] <= max_value)]

# Location (State) Filter
with st.sidebar:
     region = data['state'].unique()
     st.sidebar.header("State:")
     state = st.multiselect(label="Choose State", options=region, default=region)

# Sales Method Filter
with st.sidebar:
     sales = data['sales_method'].unique()
     st.sidebar.header("Sales Method:")
     method = st.multiselect(label="Choose Sales Method", options=sales, default=sales)

# Link Both Filter to Main Data
data = data[(data["state"].isin(state)) & (data["sales_method"].isin(method))]

## ---- Dashboard Page --- ##

## KPI Metrics
col1, col2, col3 = st.columns(3)

### Total Sales Revenue
total_revenue = data['revenue'].sum().round(2)
col1.metric(label="Total Sales Revenue", value=total_revenue)

### Total Products Sales
total_prod = data['nb_sold'].sum()
col2.metric(label="Total Product Sold", value=total_prod)

### Total Customers
total_cust = data['customer_id'].count()
col3.metric(label="Total Customer", value=total_cust)

# Number of Customers per Methods
num_cust_by_sales_method = data['sales_method'].value_counts()

# Revenue Over Time By Sales Method
revenue_over_time = data.groupby(['week', 'sales_method'])['revenue'].sum()

# Business Metrics
# Average Revenue per Customer by Sales Method Over Time
avg_revenue_cust_time = data.groupby(['week', 'sales_method']).agg({'revenue':'sum', 
                                                                                'customer_id' :'count'}).reset_index()
avg_revenue_cust_time['avg_revenue_by_customer'] = avg_revenue_cust_time['revenue']/avg_revenue_cust_time['customer_id']
pivot = avg_revenue_cust_time.pivot_table(index='week', columns='sales_method', values='avg_revenue_by_customer')

# Dashboard Plot

st.set_page_config(page_title="Pens & Printers New Product Sales Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")
## Main Page
st.title("New Product Sales Dashboard")

col1, col2 = st.columns(2)

## Number of Customers per Sales Method
with col1:
     st.subheader("Number of Customers per Sales Method")
     fig, ax = plt.subplots()
     ax = sns.barplot(x=num_cust_by_sales_method.index, y=num_cust_by_sales_method.values)
     plt.title('Number of Customers by Sales Methods')
     plt.xlabel('Sales Method')
     plt.ylabel('Number of Customers')

## Add value label for each bar plot
     for i, v in enumerate(num_cust_by_sales_method.values):
          ax.text(i, v + 0.5, str(v), ha='center')

     st.pyplot(fig)

## Revenue Over Time By Sales Method
with col2:
     st.subheader("Revenue Over Time By Sales Method")
     fig, ax = plt.subplots()
     revenue_over_time.unstack().plot(kind='line', ax=ax)

     plt.title('Revenue Over Time by Sales Method')
     plt.xlabel('Week')
     plt.ylabel('Revenue ($)')

     st.pyplot(fig)

## Business Metrics
## Average Revenue per Customer by Sales Method Over Time
st.subheader("Average Revenue per Customers by Sales Method Over Time")

fig, ax = plt.subplots(figsize=(16, 8))
pivot.plot(kind='line', marker='.', ax=ax)

plt.xlabel('Week')
plt.ylabel('Average Revenue per Customer')
plt.title('Average Revenue per Customer by Sales Method over Time')
plt.legend(title='Sales Method')
plt.grid()
plt.ylim(0, 250)

st.pyplot(fig)
