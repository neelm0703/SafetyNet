import streamlit as st
import pandas as pd
import numpy as np
import torch
from model.model import DiseasePredictor
import joblib
from sklearn.preprocessing import LabelEncoder

#Button Styling
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #b4d7db;
        color: black;
        font-size: 40px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        margin: 8px 0;
        transition: 0.3s;
        font-weight: bold;
        text-transform: capitalize;
    }
    div.stButton > button:hover {
        background-color: #3a6063;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Multiselect dropdown styling
st.markdown("""
    <style>
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #3a6063; 
        color: #d3e4e6;          
        border: 1px solid #4a7c6f; 
        text-transform: capitalize;
    }

    .stMultiSelect [data-baseweb="tag"] > span[role="button"] {
        color: white; 
    }

    </style>
""", unsafe_allow_html=True)



# Function that is used to create a button for the predicted diseases so that when pressed it navigates to the
# information page of that disease
def create_dynamic_page_button(button_label: str):
    if col2.button(button_label):
        st.session_state["selected_disease"] = button_label.split(":")[0]
        st.switch_page("pages/2_info_page.py")





st.set_page_config(layout="wide")
st.logo("assets/logo.png", size="large")


# Reading in first 10 lines of data used to train the model to get the symptom list from the columns
df = pd.read_csv("data/Disease-Prediction-Data.csv", nrows = 10)
symptoms = df.columns.tolist()[1:]
symptom_to_index = {symptom: index for index, symptom in enumerate(symptoms)}

# Creating columns
col1, col2 = st.columns([1, 2], gap="large", border=True)

#COLUMN 1: SEARCH
col1.title("Symptom Search")
selected_symptoms = col1.multiselect(
    "Choose Symptoms",
    options = symptoms,
    help="Type and select whichever symptoms you are experiencing",
    default = st.session_state['symptoms'] if 'symptoms' in st.session_state else []
)
button = col1.button("Find Potential Condition")

# Disclaimer
col1.warning("Disclaimer", icon="⚠️")
col1.warning("The results provided are based on statistical data and are NOT a formal diagnosis. Before beginning any medications, consult a medical professional")


#COLUMN 2: RESULTS
if (button):
    if not selected_symptoms:
        col2.warning("Select atleast one symptom")
    
    else:
        model = DiseasePredictor()
        model.load_state_dict(torch.load('model/model_weights.pth', map_location=torch.device('cpu')))
        le = joblib.load('model/label_encoder.pkl')

        input_vector = np.zeros(len(symptoms))
        for symptom in selected_symptoms:
            index = symptom_to_index[symptom]
            input_vector[index] = 1
                
        input_tensor = torch.tensor(input_vector, dtype=torch.float).unsqueeze(0)
        model.eval()
        with torch.inference_mode():
            output_tensor = model(input_tensor)[0]

        output_probabilities = torch.softmax(output_tensor, dim=0)
        best_probabilities, best_indices = torch.topk(output_probabilities, k=5)
        best_probabilities = best_probabilities.tolist()
        best_probabilities.append(1 - sum(best_probabilities))
        best_indices = best_indices.tolist()

        best_disease_preds = le.inverse_transform(best_indices).tolist()
        best_disease_preds.append("Other")

        st.session_state['diseases'] = best_disease_preds
        st.session_state['probabilities'] = best_probabilities
        st.session_state['symptoms'] = selected_symptoms



if 'diseases' in st.session_state:
    col2.title("Predicted Conditions")
    col2.text("Click the respective button to find out more about a condition and/or find specialists near you")
    for i in range(5):
        create_dynamic_page_button(f"{st.session_state['diseases'][i]}: {st.session_state['probabilities'][i] * 100: .2f}%")

    graph_df = pd.DataFrame({
        'Condition': st.session_state['diseases'],
        'Probability': st.session_state['probabilities']
    })
    
    colour = ['#91d7e3']
    st.bar_chart(graph_df, x="Condition", x_label='Condition', y="Probability", y_label='Probability', color=colour)


else:
    col2.title("No results")
    col2.subheader("Enter symptoms to get predicted condition")
