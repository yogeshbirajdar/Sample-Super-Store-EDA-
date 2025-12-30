import pandas as pd
import streamlit as st
import plotly
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')

#Page Layout And Heading Section

st.set_page_config(page_title="Super Store....!", page_icon=":bar_chart", layout="wide")

st.title(" :bar_chart: Sample Super Store EDA")

# st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

st.markdown("""
<style>
.sidebar .sidebar-content {
    background: #1e1e2f;
    color: white;
}
div.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# File Upload Section

fl = st.file_uploader(":file_folder: Upload File", type=(["csv", "xlsx", "txt", "xls"]))

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
    # os.chdir(r"C:\Users\nages\OneDrive\Desktop\Python Basic")
    df = pd.read_excel("Sample_Superstore.xls")


col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the MIN znd MAX Date

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


# for filters

st.sidebar.header("Choose Your Filter: ")

st.divider()

# Create For Region

region = st.sidebar.multiselect("Pick Your Region", df["Region"].unique())

if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]


# Create for State

state = st.sidebar.multiselect("Pick Your State", df2["State"].unique())

if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# Create for City

city = st.sidebar.multiselect("Pick Your City", df3["City"].unique())

if not city:
    df4 = df3.copy()
else:
    df4 = df3[df3["City"].isin(city)]

# Filter the Data Based on Filter Choosen like (Region, State, City)

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]


# KPIs (Total_Sales, Total_Profit, Total_Quantity

total_sales = filtered_df["Sales"].sum()
total_Profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    kpi1.metric("Total Sales", f"${total_sales:,.2f}")

with kpi2:
    kpi2.metric("Total_Profit", f"${total_Profit:,.2f}")

with kpi3:
    kpi3.metric("Total_Quantity", f"${total_quantity:,}")


category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()


column1, column2 = st.columns((2))


# BAR Chart

with column1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:.2f}'.format(x) for x in category_df["Sales"]],
                  template="seaborn")
    # st.plotly_chart(fig,use_container_width=True, config={"displayModebar": False, "scrollzoom": True, "responsive": True}, height = 200)
    st.plotly_chart(fig)



# PIE Chart

with column2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values= "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    # st.plotly_chart(fig,use_container_width=True, config={"displayModebar": False, "scrollzoom": True, "responsive": True})
    st.plotly_chart(fig)


# For DOWNLOAD the Data

cl1, cl2 = st.columns((2))

with cl1:
    with st.expander("Category_View_Data"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index= False).encode('utf-8')
        st.download_button("Download Data", data= csv, file_name = "Category.csv", mime = "text/csv",
                           help = "Click Here to Download The Data as a CSV File")
        
with cl2:
    with st.expander("Region_View_Data"):
        region = filtered_df.groupby(by= "Region", as_index= False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index= False).encode('utf-8')
        st.download_button("Download Data", data= csv, file_name= "Region.csv", mime= "text/csv",
                           help = "Click Here to Download The Data as a CSV File")
        

# LINE Chart

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y = "Sales", labels= {"Sales: Amount"}, height = 500, width = 1000, template= "gridon", markers=True)
st.plotly_chart(fig2)


# For Download Data of Line Chatr

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index= False).encode("utf-8")
    st.download_button("Download Data", data= csv, file_name= "TimeSeries.csv", mime= "text/csv", 
                       help = "Click Here to Download The Data as a CSV File")
    

# TREE MAP  based on (Region, Category, Sales)

st.subheader("Hierarchical View of Sales using Tree Map")
fig3 = px.treemap(filtered_df, path= ["Region", "Category", "Sub-Category"], values= "Sales", hover_data= ["Sales"],
                  color="Sub-Category")
# fig3.update_layout(width= 800, height = 650)

fig3.update_layout(
    margin=dict(t=50, l=25, r=25, b=25),
    treemapcolorway=["#003f5c","#58508d","#bc5090","#ff6361","#ffa600"]
)
st.plotly_chart(fig3)

with st.expander("View TreeMap Data"):
    st.write(filtered_df.style.background_gradient(cmap="Oranges"))
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data= csv, file_name= "TreeMap.csv", mime= "text/csv",
                       help="Click Here to Download The Data as a CSV File")
    

chart1, chart2 = st.columns((2))

# PIE Chart 1

with chart1:
    st.subheader("Segment Wise Sales")
    fig4 = px.pie(filtered_df, values="Sales", names="Segment", template= "plotly_dark")
    fig4.update_traces(text= filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig4)
    

#PIE Chart 2

with chart2:
    st.subheader("Category Wise Sales")
    fig5= px.pie(filtered_df, values="Sales", names="Category", template="gridon")
    fig5.update_traces(text= filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig5)



with chart1:
    with st.expander("View Segment Wise Sales Data"):
        segment = filtered_df.groupby("Segment", as_index=False)["Sales"].sum()
        st.write(segment.style.background_gradient(cmap="Blues"))
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Data", data= csv, file_name="Segment_Wise_Sales.csv", mime="text/csv",
                       help="Click Here to Download Data")
with chart2:
    with st.expander("Category Wise Sales"):
        category = filtered_df.groupby("Category", as_index= False)["Sales"].sum()
        st.write(category.style.background_gradient(cmap="Greens"))
        csv = filtered_df.to_csv(index= False).encode("utf-8")
        st.download_button("Download Data", data= csv, file_name="Category_wise_Sales.csv", mime="text/csv",
                       help="Click Here to Download Data")


# Adding TABLE on Dashboard

import plotly.figure_factory as ff

st.subheader(":point_right: Month Wise Sub-Category Sales Summery")
with st.expander("Summery Table"):
    df_sample = df[0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    fig6 = ff.create_table(df_sample, colorscale= "Cividis")
    st.plotly_chart(fig6)

    st.markdown("Moth Wise Sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"], columns="month")
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))


# SCATTER PLOT
st.subheader("Relationship Between Sales and Profit using Scatter Plot")
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size= "Quantity")
data1.update_layout(
    # title={"text": "Relationship Between Sales and Profit using Scatter Plot",
    #        "font": {"size": 25, "color": "white"},
    #         }
)
st.plotly_chart(data1)

# Download original DataSet

csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name= "Data.csv", mime= "text/csv")


