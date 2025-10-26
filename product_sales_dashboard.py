import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Dataset
data = pd.read_csv('product_sales_clean.csv')

# Create Filter By "Week"
min_week = data['week'].min()
max_week = data['week'].max()
min_value, max_value = st.slider("Select Week :",
                                 min_value=min_week,
                                 max_value=max_week,
                                 value=[min_week, max_week]
                                )


main_data = data[(data['week'] >= min_value) & (data['week'] <= max_value)]

# Number of Customers per Methods
num_cust_by_sales_method = main_data['sales_method'].value_counts()

# Revenue Over Time By Sales Method
revenue_over_time = main_data.groupby(['week', 'sales_method'])['revenue'].sum()

# Business Metrics
# Average Revenue per Customer by Sales Method Over Time
avg_revenue_cust_time = main_data.groupby(['week', 'sales_method']).agg({'revenue':'sum', 
                                                                                'customer_id' :'count'}).reset_index()
avg_revenue_cust_time['avg_revenue_by_customer'] = avg_revenue_cust_time['revenue']/avg_revenue_cust_time['customer_id']
pivot = avg_revenue_cust_time.pivot_table(index='week', columns='sales_method', values='avg_revenue_by_customer')

# Dashboard

st.set_page_config(page_title="Pens & Printers New Product Sales Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

## Main Page
st.title("New Product Sales Dashboard")

## Number of Customers per Sales Method
st.subheader("Number of Customers per Sales Method")

fig, ax = plt.subplots(figsize=(12, 8))
ax = sns.barplot(x=num_cust_by_sales_method.index, y=num_cust_by_sales_method.values)

plt.title('Number of Customers by Sales Methods')
plt.xlabel('Sales Method')
plt.ylabel('Number of Customers')

## Add value label for each bar plot
for i, v in enumerate(num_cust_by_sales_method.values):
    ax.text(i, v + 0.5, str(v), ha='center')

st.pyplot(fig)

## Revenue Over Time By Sales Method
st.subheader("Revenue Over Time By Sales Method")

fig, ax = plt.subplots(figsize=(12, 8))
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
