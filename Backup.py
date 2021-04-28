import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
from PIL import Image
st.set_page_config(layout="wide")

#Read the Datafile in
def load_data():
    df=pd.read_csv("volcanoes.csv",encoding="cp1252").dropna()
    return df

#In this section I am creating a user interface where they chose a city and they are given a list of
#facts about the nearest volcano to them.  I tried to use an index but kept getting an syntax error


def load_inputs():
    dict = {
        "cities" : ["Boston", "New York", "Los Angeles", "Chicago", "Naples", "Rome", "Tokyo"],
        "lat" : [42.36, 40.71, 34.05, 41.88, 40.85, 41.91, 35.68],
        "long" : [-71.06, -74, -118.24, -87.63, 14.27, 12.49, 139.65]
    }
    city_data = pd.DataFrame(dict)

    st.title("Should you be scared of dying from lava, smoke, or rocks?")
    st.write("")
    st.write("")
    st.write("Wohoo Volcanoes")

    location = st.selectbox(
        "Location Option",
        city_data["cities"])


    if location == "Boston":
        dotsero = Image.open("Dotsero.jpeg")
        st.write(f"Your Latitude is {city_data['lat'][0]}")
        st.write(f"Your Longitude is {city_data['long'][0]}")
        st.write(f"The closest volcano to you is the Dotsero Volcano in Colorado")
        st.write("This Volcano is 2110 miles away, putting you at very low risk")
        st.image(dotsero, width=400)
    if location == "New York":
        dotsero = Image.open("Dotsero.jpeg")
        st.write(f"Your Latitude is {city_data['lat'][1]}")
        st.write(f"Your Longitude is {city_data['long'][1]}")
        st.write(f"The closest volcano to you is the Dotsero Volcano in Colorado")
        st.write("This Volcano is 1939 miles away, putting you at very low risk")
        st.image(dotsero, width=400)
    if location == "Los Angeles":
        coso = Image.open("coso.jpg")
        st.write(f"Your Latitude is {city_data['lat'][2]}")
        st.write(f"Your Longitude is {city_data['long'][2]}")
        st.write(f"The closest volcano to you is the Coso Volcanic Field in California")
        st.write("This Volcano is 170 miles away, putting you at low risk")
        st.image(coso, width=400)
    if location == "Chicago":
        yellowstone = Image.open("yellowstone.jpg")
        st.write(f"Your Latitude is {city_data['lat'][3]}")
        st.write(f"Your Longitude is {city_data['long'][3]}")
        st.write(f"The closest volcano to you is the Yellow Stone Volcano in Wyoming")
        st.write("This Volcano is 1341 miles away, putting you at very low risk")
        st.image(yellowstone, width=400)
    if location == "Naples":
        pompeii = Image.open("pompeii.jpg")
        st.write(f"Your Latitude is {city_data['lat'][4]}")
        st.write(f"Your Longitude is {city_data['long'][4]}")
        st.write(f"The closest volcano to you is Pompeii")
        st.write("This Volcano is 12 miles away, putting you at very high risk")
        st.image(pompeii, width=400)
    if location == "Rome":
        sabatini = Image.open("sabatini.jpg")
        st.write(f"Your Latitude is {city_data['lat'][5]}")
        st.write(f"Your Longitude is {city_data['long'][5]}")
        st.write(f"The closest volcano to you is Mount Sabatini")
        st.write("This Volcano is 26 miles away, putting you at high risk")
        st.image(sabatini, width=400)
    if location == "Tokyo":
        fuji = Image.open("fuji.jpg")
        st.write(f"Your Latitude is {city_data['lat'][6]}")
        st.write(f"Your Longitude is {city_data['long'][6]}")
        st.write(f"The closest volcano to you is Mount Fuji")
        st.write("This Volcano is 62 miles away, putting you at medium high risk")
        st.image(fuji, width=400)
#One chart, and one table, the chart shows where volcanoes have the highest density latitudionally
#The table just gives the basic elevation statistics using .describe
def chart_page(index):
    c2,c3,c4=st.beta_columns(3)
    color=c4.selectbox("Select Color for Charts",["red","blue","green","yellow"],key=index)
    style = 0
    thickness = 0
    return style,thickness,color


def load_charts():
    st.header("Volcanoes Chart!")
    index=0
    style,thickness,color=chart_page(index)
    df=load_data()
    column1,column2=st.beta_columns(2)

    plt.hist(df["Latitude"], bins=30,color=color)

    plt.ylabel("Number of Volcanos")
    plt.xlabel("Latitude of Volcanos")
    plt.title(f"Latitude of Volcanoes in the Dataset")

    column1.pyplot(plt)
    column2.header("Volcano Elevation Statistics")
    column2.write(df["Elevation (m)"].describe())
    plt.clf()

#This is the last section, and it creates a map that shows where the volcanic eruptions are across the globe
#I tried to create an interface where you could hover over the volcano and see details but it caused streamlit
#to freeze


def load_maps():
    df=load_data()
    map_options=[]
    for data in df:
        map_options.append(data)

    under=df[df["Elevation (m)"]<0]
    under["height"]=-under["Elevation (m)"]
    over=df[df["Elevation (m)"]>0]
    over["height"]=over["Elevation (m)"]
    viewpoint=pdk.ViewState(latitude=over["Latitude"].mean(),longitude=over["Longitude"].mean(),pitch=20,zoom=0)

    ov = pdk.Layer("ColumnLayer",data=over,get_position=["Longitude", "Latitude"],get_elevation="height",elevation_scale=100,radius=12000,get_fill_color=[350,75,330,250])
    und= pdk.Layer("ColumnLayer",data=under,get_position=["Longitude", "Latitude"],get_elevation="height",elevation_scale=100,radius=12000,get_fill_color=[30,40,350,100])

    map=pdk.Deck(map_provider='carto',layers=[ov,und],initial_view_state=viewpoint)
    st.pydeck_chart(map)
    st.dataframe(df)

def main():
    st.title("Volcanoes Final Project")
    st.sidebar.title("Menu:")
    menu=st.sidebar.selectbox("Select Volcano Feature",["View Graph","View Map","Safety Check"])
    if menu =="Safety Check":
        load_inputs()
    if menu =="View Graph":
        load_charts()
    if menu =="View Map":
        load_maps()

main()

