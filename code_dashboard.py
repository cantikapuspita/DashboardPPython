# IMPORT LIBRARIES
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime


# 1. Setel konfigurasi halaman (judul browser/tab)
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Tampilkan judul dashboard di layar
st.title(":bar_chart:  Supermarket Sales Dashboard")
# Membuat button klik yang menampilkan sumber data
klik = st.button("Click Here for Credit")
if klik:
    st.image("logo_kaggle.png", width=70) 
    st.write("Data Source: [Supermarket Sales Dataset](https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales?utm_source)")
    st.write("Created by Kelompok 6")
st.markdown("##")

page_bg_css = '''
<style>
.stApp {
  position: relative;
  background-image: url("https://images.unsplash.com/photo-1604719312566-8912e9227c6a?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  z-index: 0;
}

/* Overlay layer */
.stApp::before {
  content: "";
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(14, 18, 63, 0.7); 
  z-index: -1;
}
</style>
'''

st.markdown(page_bg_css, unsafe_allow_html=True)

# IMPORT DATA SALES
data = pd.read_csv(r"SuperMarket Analysis.csv")

#Sidebar Filters
st.sidebar.header('Filter Here:')
try:
    city_sb = st.sidebar.multiselect(
        "City",
        options=data['City'].unique(),
        default=data['City'].unique()
    )
except:
    st.sidebar.write('⚠️ City - Create column to get the filter')

try:
    customer_sb = st.sidebar.multiselect(
        "Customer type",
        options=data['Customer type'].unique(),
        default=data['Customer type'].unique(),
    )
except:
    st.sidebar.write('⚠️ Customer - Create column to get the filter')

try:
    gender_sb = st.sidebar.multiselect(
        "Gender",
        options=data['Gender'].unique(),
        default=data['Gender'].unique()
    )
except:
    st.sidebar.write('⚠️ Gender - Create column to get the filter')
try:
    productline_sb = st.sidebar.multiselect(
        "Product line",
        options=data['Product line'].unique(),
        default=data['Product line'].unique()
    )
except:
    st.sidebar.write('⚠️ Product line - Create column to get the filter')
try:
    payment_sb = st.sidebar.multiselect(
        "Payment",
        options=data['Payment'].unique(),
        default=data['Payment'].unique()
    )
except:
    st.sidebar.write('⚠️ Payment - Create column to get the filter')
try:
    data["Date"] = pd.to_datetime(data["Date"])

    # Ambil rentang tanggal dari data
    startDate = data["Date"].min()
    endDate = data["Date"].max()

    # Input date filter
    col1, col2 = st.columns((2))
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    # Filter data dengan semua kondisi termasuk tanggal
    data_selection = data[
        (data['City'].isin(city_sb)) &
        (data['Customer type'].isin(customer_sb)) &
        (data['Gender'].isin(gender_sb)) &
        (data['Product line'].isin(productline_sb)) &
        (data['Payment'].isin(payment_sb)) &
        (data['Date'] >= date1) &
        (data['Date'] <= date2)
    ]

except Exception as e:
    st.write('⚠️ Create Date Transaction column to get a data filter')
    st.write(f"Error: {e}")

st.markdown("---")

# MEMBUAT KEY PERFORMANCE INDICATORS (KPI)
total_sales = int(data_selection["Sales"].sum())
average_sales = round(data_selection["Sales"].mean(), 2)

# MEMBUAT KARTU KPI
left_column,  right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US$ {total_sales:,}")
with right_column:
    st.subheader("Average Sales:")
    st.subheader(f"US$ {average_sales:,}")


st.markdown("---")


# Membuat grid untuk menampilkan beberapa chart dalam satu tampilan yang lebih kecil
col1, col2, col3 = st.columns(3)

# Income per Product Line
with col1:
    income_per_product = data_selection.groupby("Product line").sum(numeric_only=True)[["gross income"]].sort_values(by="gross income", ascending=False).reset_index()
    fig = px.bar(
        income_per_product,
        x="Product line",
        y="gross income",
        title="<b>Gross Income per Product Line</b>",
        color_discrete_sequence=["#8d62ee"] * len(income_per_product),
        template="plotly_dark"
    )
    fig.update_layout(
        xaxis_title="<b>Product Line</b>",
        yaxis_title="<b>Gross Income</b>",
        legend_title="<b>Legend</b>",
        height=250,
        plot_bgcolor="rgba(0,0,0,0)",    
        paper_bgcolor="rgba(0,0,0,0)" 
    )
    st.plotly_chart(fig, use_container_width=True)


# Sales per Month
with col2:
    data_selection["Date"] = pd.to_datetime(data_selection["Date"])
    data_selection["Date"] = data_selection["Date"].dt.to_period("M").dt.to_timestamp()
    sales_per_month = data_selection.groupby("Date").sum(numeric_only=True)[["Sales"]].reset_index()
    fig = px.line(
        sales_per_month,
        x="Date",
        y="Sales",
        title="<b>Sales per Month</b>",
        color_discrete_sequence=["#8d62ee"] * len(sales_per_month),
        template="plotly_dark"
    )
    fig.update_layout(
        xaxis_title="<b>Order Date</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Legend</b>",
        height=250,
        plot_bgcolor="rgba(0,0,0,0)",    
        paper_bgcolor="rgba(0,0,0,0)" 
    )
    st.plotly_chart(fig, use_container_width=True)

# Sales per City
with col3:
    sales_per_branch = data_selection.groupby("City").sum(numeric_only=True)[["Sales"]].reset_index()
    fig = px.bar(
        sales_per_branch,
        x="City",
        y="Sales",
        title="<b>Sales per City</b>",
        color_discrete_sequence=["#8d62ee"] * len(sales_per_branch),
        template="plotly_dark"
    )
    fig.update_layout(
        xaxis_title="<b>City</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Legend</b>",
        height=250,
        plot_bgcolor="rgba(0,0,0,0)",    
        paper_bgcolor="rgba(0,0,0,0)" 
    )
    st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

# MEMBUAT KEY PERFORMANCE INDICATORS (KPI)
avg_rating = round(data_selection["Rating"].mean(), 1)
rating_by_product = data_selection.groupby("Product line")["Rating"].mean()
top_product = rating_by_product.idxmax()
top_rating = round(rating_by_product.max(), 1)

# MEMBUAT KARTU KPI
left_column, middle_column = st.columns(2)

with left_column:
    st.subheader("Average Rating:")
    st.subheader(f"⭐{avg_rating:,}")
with middle_column:
    st.metric("Top Rated Product Line", top_product, f"⭐ {top_rating}")

st.markdown("---")

sales_by_product = data_selection.groupby("Product line")["Sales"].sum().sort_values(ascending=True)
sales_df = sales_by_product.reset_index()

# Pipeline chart (bar horizontal)
fig = px.bar(
    sales_df,
    x="Sales",
    y="Product line",
    orientation="h",
    title="Best Selling Product Lines",
    color="Sales",
    color_continuous_scale="purpor",
    labels={"Sales": "Total Sales", "Product line": "Product Line"}
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  
    paper_bgcolor="rgba(0,0,0,0)", 
    title_font=dict(size=20, color="white"),
    xaxis=dict(title="<b>Total Sales</b>", color="white"),
    yaxis=dict(title="<b>Product Line</b>", color="white"),
    coloraxis_colorbar=dict(title="Sales")
)
# Tampilkan chart di Streamlit
st.plotly_chart(fig)

st.markdown("---")

# Membuat grid lebih lanjut
col4, col5, col6 = st.columns(3)

# Distribusi Gender
with col4:
    gender_dist = data_selection['Gender'].value_counts()
    fig = px.pie(
        gender_dist,
        values=gender_dist.values,
        names=gender_dist.index,
        hole=0.5,
        title="<b>Gender Distribution</b>",
        color_discrete_sequence=["#8d62ee", "#fc50cd"],
        template="plotly_dark"
    )
    fig.update_layout(height=250,
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)" )
    st.plotly_chart(fig, use_container_width=True)

# Member customer
with col5:
    payment_counts = data_selection["Customer type"].value_counts().reset_index()
    payment_counts.columns = ["Customer type", "Count"]

    # Buat doughnut chart
    fig = px.pie(
        payment_counts,
        names="Customer type",
        values="Count",
        hole=0.5,  
        color_discrete_sequence=["#8d62ee", "#fc50cd", "#a5b9c2", "#f39c12"],
    )

    fig.update_layout(
        title="<b>Customer type Distribution</b>",
        title_font=dict(size=18, color="white"),
        legend_title="<b>Payment</b>",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=250
    )

    st.plotly_chart(fig, use_container_width=True)

# Metode Pembayaran
with col6:
    payment_dist = data_selection['Payment'].value_counts()
    fig = px.pie(
        payment_dist,
        values=payment_dist.values,
        names=payment_dist.index,
        hole=0.5,
        title="<b>Payment Method Distribution</b>",
        color_discrete_sequence=["#8d62ee", "#fc50cd", "#a5b9c2", "#f39c12"],
        template="plotly_dark"
    )
    fig.update_layout(height=250,
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)" )
    st.plotly_chart(fig, use_container_width=True)


# Tabel di bawah
#st.markdown("## Data Selection")
#st.dataframe(data_selection, use_container_width=True)

# MENAMPILKAN DATA
#st.dataframe(data_selection)
