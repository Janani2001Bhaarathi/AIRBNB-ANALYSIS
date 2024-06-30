import pandas as pd 
import numpy as np
from streamlit_option_menu import option_menu
import streamlit as st
from PIL import Image
import warnings
import plotly.express as px

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis", layout="centered")
st.image(Image.open(r"C:\Users\JANANI BHAARATHI\OneDrive\Desktop\Airbnb\Project4 Airbnb.png"))
#with st.title:
 
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Contact"],
    icons=["house", "bar-chart", "at"],
    default_index=2,
    orientation="horizontal")

#--------------------------------------------------------------------Home---------------------------------------------------------------------#

if SELECT == "Home":

    st.header('Airbnb Analysis')
    st.write("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
    st.subheader('Skills take away From This Project:')
    st.write('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDb, PowerBI or Tableau')
    st.subheader('Domain:')
    st.write('Travel Industry, Property management and Tourism')
#---------------------------------------------------------------Explore Data--------------------------------------------------------------#
if SELECT == "Explore Data":
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename)
        st.sidebar.header("Choose your filter: ")
        # Create for room_type
        room_type = st.sidebar.multiselect("Pick your room_type", df["room_type"].unique())
        if not room_type:
            df2 = df.copy()
        else:
            df2 = df[df["room_type"].isin(room_type)]

        # Create for property_type
        property_type = st.sidebar.multiselect("Pick the property_type", df2["property_type"].unique())
        if not property_type:
            df3 = df2.copy()
        else:
            df3 = df2[df2["property_type"].isin(property_type)]

        # Filter the data based on room_type, property_type

        if not room_type and not property_type:
            filtered_df = df
        elif not property_type:
            filtered_df = df[df["room_type"].isin(room_type)]
        elif not room_type:
            filtered_df = df[df["property_type"].isin(property_type)]
        elif property_type:
            filtered_df = df3[df["property_type"].isin(property_type)]
        elif room_type:
            filtered_df = df3[df["room_type"].isin(room_type)]
        elif room_type and property_type:
            filtered_df = df3[df["room_type"].isin(room_type) & df3["property_type"].isin(property_type)]
        else:
            filtered_df = df3[df3["room_type"].isin(room_type) & df3["property_type"].isin(property_type)]  

        col1, col2 = st.columns(2)
        with col1: 
            st.subheader("room_type_ViewData")
            fig = px.pie(filtered_df, values="price", names="room_type", hole=0.5)
            fig.update_traces(text=filtered_df["room_type"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)      
        with col2:
            room_type_counts = filtered_df['room_type'].value_counts()
            # Convert the Series to a DataFrame
            room_type_counts_df = room_type_counts.reset_index()

            # Rename the columns for better readability
            room_type_counts_df.columns = ['room_type', 'count']

            # Calculate the sum of price for each unique room_type
            room_type_price_sum = df.groupby('room_type')['price'].sum().reset_index()

            # Merge the room_type_counts_df with the room_type_price_sum
            room_type_summary_df = pd.merge(room_type_counts_df, room_type_price_sum, on='room_type')

            # Rename the columns for better readability
            room_type_summary_df.columns = ['room_type', 'count', 'total_price']
            st.dataframe(room_type_summary_df)
            

        col1, col2 = st.columns(2)
        with col1: 
            st.subheader("property_type_ViewData")
            fig = px.pie(filtered_df, values="price", names="property_type", hole=0.5)
            fig.update_traces(text=filtered_df["property_type"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)      
        with col2:
            property_type_counts = filtered_df['property_type'].value_counts()
            # Convert the Series to a DataFrame
            property_type_counts_df = property_type_counts.reset_index()

            # Rename the columns for better readability
            property_type_counts_df.columns = ['property_type', 'count']

            # Calculate the sum of price for each unique room_type
            property_type_price_sum = df.groupby('property_type')['price'].sum().reset_index()

            # Merge the room_type_counts_df with the room_type_price_sum
            property_type_summary_df = pd.merge(property_type_counts_df, property_type_price_sum, on='property_type')

            # Rename the columns for better readability
            property_type_summary_df.columns = ['property_type', 'count', 'total_price']
            st.dataframe(property_type_summary_df)

        bed_counts = filtered_df['beds'].value_counts()
        # Convert the Series to a DataFrame
        bed_counts_df = bed_counts.reset_index()
        # Rename the columns for better readability
        bed_counts_df.columns = ['No.of.beds', 'count']
        st.subheader("Number of Beds Counts")
        fig = px.bar(bed_counts_df, x="No.of.beds", y="count", text="count",
                    template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

        bed_type_counts = filtered_df['bed_type'].value_counts()
        # Convert the Series to a DataFrame
        bed_type_df = bed_type_counts.reset_index()
        # Rename the columns for better readability
        bed_type_df.columns = ['bed_type', 'count']
        st.subheader("Number of bed_type Counts")
        fig = px.line(bed_type_df, x="bed_type", y="count", text="count")
        st.plotly_chart(fig, use_container_width=True, height=200)

        bedrooms_counts = filtered_df['bedrooms'].value_counts()
        # Convert the Series to a DataFrame
        bedrooms_df = bedrooms_counts.reset_index()
        # Rename the columns for better readability
        bedrooms_df.columns = ['No.of.bedrooms', 'count']
        st.subheader("Number of bedrooms Counts")
        fig = px.bar(bedrooms_df, x="No.of.bedrooms", y="count", text="count",
                    template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)  

        bathrooms_counts = filtered_df['bathrooms'].value_counts()
        # Convert the Series to a DataFrame
        bathrooms_df = bathrooms_counts.reset_index()
        # Rename the columns for better readability
        bathrooms_df.columns = ['bathrooms', 'count']
        st.subheader("Number of bathrooms Counts")
        fig = px.line(bathrooms_df, x="bathrooms", y="count", text="count")
        st.plotly_chart(fig, use_container_width=True, height=200)  

        st.subheader("Airbnb Analysis in Map view")
        dfmap = filtered_df.rename(columns={"latitude": "lat", "longitude": "lon"})

        st.map(dfmap)        
    else:    
        st.markdown("<h1 style='text-align: center; font-weight: bold;'>Upload the data</h1>", unsafe_allow_html=True)



#--------------------------------------------------------------------Contact---------------------------------------------------------------------#
if SELECT == "Contact":
    col1, col2 = st.columns(2) 
    with col1:
        st.markdown("## Done by : JANANI BHAARATHI K M") 
        st.markdown(" An Aspiring DATA-SCIENTIST..!")
        st.markdown("Gmail: jananibharathi2001@gmail.com")
        st.markdown("[Githublink](https://github.com/Janani2001Bhaarathi/)")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/janani-bhaarathi-k-m-25988a22a/)") 
    st.write("---")  
    col2.image(Image.open(r"C:\Users\JANANI BHAARATHI\OneDrive\Desktop\Airbnb\JANANI BHAARATHI K M.jpeg"))