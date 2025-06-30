import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
from streamlit.components.v1 import html

# Setting the page layout to wide to utilise all the space on the page
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Adding the logo and emblem
st.logo("assets/logo.png", size="large")
co1, co2, co3, co4, co5 = st.columns(5)
co3.image("assets/emblem.png")
st.markdown(
    f'''
    <div style="text-align:center;">
        <span style="font-size:20px;">
            <em>
                Safety Net is an AI driven symptom diagnosis platform where you enter symptoms and we will give you a list of possible conditions and specialists near you.
            </em>
        </span>
    </div>
    ''',
    unsafe_allow_html=True
)

# Creating the columns for the graphs
left, middle,right = st.columns(3, vertical_alignment="center", border=True, gap="medium")

#1: LEFT COLUMN
#1.a: graph 1
cost_unmet = pd.read_csv("data/cost_unmet.csv")
left.subheader("Unmet Need for Health Care Due to Cost")
left.text("Source: NHIS")
left.line_chart(cost_unmet, x="Year", x_label="Year", y="Percentage of Population", y_label="Percentage of Population", color="#a9e1eb", width=50)

#2: MIDDLE COLUMN
#2.a: graph 2
middle.subheader("Clinically Undiagnosed Findings Identified in UHZ, Switzerland")
middle.text("Source: Arch Pathol Lab Med")
cd = pd.DataFrame({
        'Category': ['Diagnosed', 'Undiagnosed'],
        'Value': [15, 633],
        'Percent':[0.02, 0.98],
        'Colour': ['#91d7e3', '#435d75'] 
    })
base = alt.Chart(cd).encode(
        theta=alt.Theta("Value", stack=True) 
    )
pie = base.mark_arc(outerRadius=100, innerRadius=50).encode(
        color=alt.Color("Category", scale=alt.Scale(range=cd['Colour'].tolist())),
        order=alt.Order("Value", sort="descending"),
    )
text = base.mark_text(radius=120).encode(
        text=alt.Text("Percent", format=".2%"), 
        order=alt.Order("Percent", sort="descending"), 
        color=alt.value("black")
    )
chart = pie + text
middle.altair_chart(chart)

#3: RIGHT COLUMN
#3.a : graph 3
test_decline = pd.read_csv("data/test_decline.csv")
right.subheader("Percentage Decline in Lab Tests by Category")
right.text("Source: American Clinical Laboratory Association")
colour = ['#91d7e3']
right.bar_chart(test_decline, x="Category", x_label='Category', y="Percentage Decline", y_label='Percentage Decline (%)', color=colour)


#Bottom Text
st.markdown("<h2 style='text-align: center;'>Want to stay on the safe side?</h2>", unsafe_allow_html=True)


st.markdown("""
<style>{ /
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# Making columns to center the button
c1, c2, c3, c4, c5 = st.columns(5)
if c3.button("Search Your Symptoms", use_container_width=True):
    st.switch_page("pages/1_symptoms_page.py")
