import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv(r"orders(1).csv" , encoding="latin-1")

data['purchase_date'] = pd.to_datetime(data['purchase_date'])
data['Month'] = data['purchase_date'].dt.month
data['Sales'] = data['quantity'] * data['item_price']
data['Year'] = data['purchase_date'].dt.year
data['ship_country'] = data['ship_country'].astype(str)
data['ship_city'] = data['ship_city'].astype(str)
data['sku'] = data['sku'].astype(str)

# Sidebar for user input
# Sidebar for user input
st.sidebar.title("Trend Analysis Dashboard")

# Filter data by year
selected_year = st.sidebar.selectbox("Select Year", sorted(data['Year'].unique()))
year_data = data[data['Year'] == selected_year]

# Filter data by country
selected_country = st.sidebar.selectbox("Select Country", sorted(data['ship_country'].unique()))
country_data = year_data[year_data['ship_country'] == selected_country]

# Filter data by city
selected_city = st.sidebar.selectbox("Select City", sorted(data['ship_city'].unique()))
city_data = year_data[year_data['ship_city'] == selected_city]

# Main content
st.title("Sales Trend Analysis")

# Monthly Sales Bar Chart
st.subheader("Monthly Sales Trend")
monthly_sales = year_data.groupby('Month')['Sales'].sum()
plt.bar(monthly_sales.index, monthly_sales)
plt.xlabel("Month")
plt.ylabel("Sales")
st.pyplot()

test=px.bar(monthly_sales,monthly_sales.index,'Sales',title="Plot")
st.plotly_chart(test)

# Yearly Sales Bar Chart
st.subheader("Yearly Sales Trend")
yearly_sales = data.groupby('Year')['Sales'].sum()
plt.bar(yearly_sales.index, yearly_sales)
plt.xlabel("Year")
plt.ylabel("Sales")
st.pyplot()

test=px.bar(yearly_sales,yearly_sales.index,'Sales',title="Plot")
st.plotly_chart(test)

# Country-wise Sales Bar Chart
st.subheader("Country-wise Sales Distribution")
country_sales = country_data.groupby('ship_country')['Sales'].sum()
plt.bar(country_sales.index, country_sales)
plt.xlabel("Country")
plt.ylabel("Sales")
plt.xticks(rotation='vertical')
st.pyplot()

test=px.bar(country_sales,country_sales.index,'Sales',title="Plot")
st.plotly_chart(test)

# City-wise Sales Scatter Plot
st.subheader("City-wise Sales Distribution")
plt.scatter(city_data['ship_city'], city_data['Sales'])
plt.xlabel("City")
plt.ylabel("Sales")
plt.xticks(rotation='vertical')
st.pyplot()



st.subheader("City-wise Sales Distribution")
city_sales = city_data.groupby('ship_city')['Sales'].sum()
plt.plot(city_sales.index, city_sales, marker='o')
plt.xlabel("City")
plt.ylabel("Sales")
plt.xticks(rotation='vertical')
st.pyplot()

test=px.bar(city_sales,city_sales.index,'Sales',title="Plot")
st.plotly_chart(test)

st.subheader("SKU Analysis")

# Grouping by SKU and calculating quantity ordered
product_group = data.groupby('sku')
quantity_ordered = product_group.sum()['quantity']

keys = [pair for pair, df in product_group]

# Displaying the SKU bar chart
st.bar_chart(quantity_ordered, use_container_width=True)

# Display top 20 SKU value counts
st.write("Top 20 SKUs:")
sku_value_counts = data['sku'].value_counts()
top_20_sku = sku_value_counts.head(20)
st.write(top_20_sku)