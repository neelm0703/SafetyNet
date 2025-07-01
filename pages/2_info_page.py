import streamlit as st
import requests
import pandas as pd
import numpy as np
import pydeck as pdk
import json
from streamlit_geolocation import streamlit_geolocation

# Button styling for every button on the page. Has to be done on every page
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #b4d7db;
        color: black;
        font-size: 25px;
        padding: 10px 24px;
        border-radius: 10px;
        border: none;
        margin: 8px 0;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #92abad;
    }
    </style>
""", unsafe_allow_html=True)


# Variables for the API
endpoint = "https://maps.googleapis.com/maps/api/place/textsearch/json"
key = st.secrets["api_keys"]["maps_key"]

st.set_page_config(layout="wide")
st.logo("assets/logo.png", size="large")



# Back button
if st.button("", icon = "🔙"):
    st.switch_page("pages/1_symptoms_page.py")



# Function to retrieve nearby doctors from the API
def doctors_nearby(query, location):
    params = {
        "query" : query,
        "location" : f"{location['latitude']},{location['longitude']}",
        "key" : key
    }


    try:
        res = requests.get(endpoint, params=params)
        res.raise_for_status()
        data = res.json()

        if data["status"] == "OK":
            places = []
            for place in data.get("results", []):
                places.append({
                    "Name": place.get("name"),
                    "Address": place.get("formatted_address"),
                    "Rating": place.get("rating"),
                    "Latitude": place.get("geometry", {}).get("location", {}).get("lat"),
                    "Longitude": place.get("geometry", {}).get("location", {}).get("lng"),
                    "Place ID": place.get("place_id")
                })
            return pd.DataFrame(places)
        elif data["status"] == "ZERO_RESULTS":
            col2.warning("No results found!")
            return None
        else:
            st.error("Error with API")
            return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None





# Function to calculate the. distance (in KM) between two sets of coordinates
def distance_between_coords(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return (R * c)







# Function to create a mapwith your location and the location of the doctors returned by the API
def create_map(column):
    st.info("Press the button below to give us location access so we can provide you with doctors near your location ")
    location = streamlit_geolocation()

    # Getting their location from session state if they previously gave it
    if (not(location['latitude'] and location['longitude'])):
        if ('location' in st.session_state):
            location = st.session_state['location']


    # Getting information from API and creating map if they gave information
    if (location['latitude'] and location['longitude']):
        st.session_state['location'] = location
        col2.write("Specialists Nearby:")
        df = doctors_nearby("doctor for " + st.session_state["selected_disease"], location)

        if (df == None):
            column.write("Sorry! We were unable to find specialists near your location.")
            return None
            
        df = df.dropna(subset = ['Latitude', 'Longitude'])
        # Adding a distance column relative to current location
        df["Distance (KM)"] = distance_between_coords(location['latitude'], location['longitude'], df["Latitude"], df["Longitude"])
        # Removing doctors which are further than 10km away
        df = df[df["Distance (KM)"] <= 20]

        if (not df.empty):
            # Dropping the columns the user has no use for 
            df2 = df.drop(["Latitude", "Longitude", "Place ID"],axis = 1)
            column.dataframe(df2, use_container_width = True)

            # Creating the different layers shown on top of the map
            doctor_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[Longitude, Latitude]',
                get_radius=100,
                # [R, G, B, Opacity]
                get_fill_color='[182, 244, 252, 200]', 
                pickable=True
            )

            user_layer = pdk.Layer(
                "ScatterplotLayer",
                data=pd.DataFrame([{"Latitude": location['latitude'], "Longitude": location['longitude'], "Name": "You"}]),
                get_position='[Longitude, Latitude]',
                get_radius=200,
                get_fill_color='[200, 204, 204, 300]',
                pickable=True
            )

            line_data = pd.DataFrame([{
                "from_lon": location['longitude'],
                "from_lat": location['latitude'],
                "to_lon": row["Longitude"],
                "to_lat": row["Latitude"],
                # Because the tooltip shows the name
                "Name": str(round(row["Distance (KM)"], 2)) + " KM"
            } for _, row in df.iterrows()])

            line_layer = pdk.Layer(
                "LineLayer",
                data = line_data,
                get_source_position = '[from_lon, from_lat]',
                get_target_position = '[to_lon, to_lat]',
                get_width = 5,
                get_color='[59, 192, 209, 200]',
                pickable = True
            )

            tooltip = {"text": "{Name}"}

            view_state = pdk.ViewState(
                latitude=(df["Latitude"].mean() + location['latitude']) / 2,
                longitude=(df["Longitude"].mean() + location['longitude']) / 2,
                zoom=12,
            )

            # Showing the map with the created layers
            col2.pydeck_chart(pdk.Deck(
                layers=[line_layer, doctor_layer, user_layer],
                initial_view_state=view_state,
                tooltip=tooltip
            ))

            column.image("assets/google_on_white.png", width=70, caption="Powered by Google")

        else:
            column.write("Sorry! We were unable to find specialists near your location.")
    else:
        column.write("Location not available. Please click the black location toggle in the bottom left of your screen to enable your location")




if "selected_disease" in st.session_state:
    selected_disease = st.session_state["selected_disease"]
    st.title(selected_disease.title())

    col1, col2 = st.columns([1, 4], gap = "large", border=True)

    # COL1
    # Description of each disease
    df = pd.read_csv("data/disease_details.csv", sep='|')
    matches = df[df['Disease'] == selected_disease]
    if not matches.empty:
        description = matches.iloc[0, 1]
        col1.subheader("Description:")
        col1.markdown(

            f'<span style="font-size:20px;">*{description}*</span>',
            unsafe_allow_html=True
        )
    else:
        col1.subheader("Disease description not found.")

    # COL 2
    #Specialists near them
    create_map(col2)
else:
    st.error("Please input your symtoms and select a disease to see it's details")
