import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Dataset
data = pd.read_csv('product_sales_clean.csv')

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

# Dashboard

st.set_page_config(page_title="Pens & Printers New Product Sales Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

## Time Filter Component
min_week = data['week'].min()
max_week = data['week'].max()



