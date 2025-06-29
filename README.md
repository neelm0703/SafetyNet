# SafeSide
## Description
Safety Net is a web application developed in light of the growing need for healthcare, but lack of affordable access to it or simply reluctance to go to a doctor. 

Safety Net provides you with the most likely conditions based on the symptoms you provide us with, along with a list of specialists in your area to treat those conditions

## How to Run
1. View our official website at the following link:
2. Run locally
   - Install Python and git. Get a free API key for the Google Places API

   - In your terminal, navigate to where you would like to create the project folder and clone the respository using the following command
        ```bash
        git clone https://github.com/neelm0703/Safety-Net.git 
        ```

   - Navigate into the repository
        ```bash
        cd Safety-Net
        ```

   - (Optional but recommended) Create a virtual environment and activate it by running the command
        ```bash
        python3 -m venv .venv
        ```
     followed by
     (for mac OS and Linux)
        ```bash
        source .venv/bin/activate
        ```
     (for Windows)
        ```bash
        .venv\Scripts\activate
        ```

   - Install all dependencies
        ```bash
        pip install -r requirements.txt
        ```
   - Create a .streamlit/secrets.toml file with your API key. It should be structured as follows
        ```toml
        [api_keys]
        maps_key = "YOUR_API_KEY"
        ```
    - Run the program with the command
        ```bash
        streamlit run Home.py
        ```



## Features
* Select your symptoms from over 350+ possible options.

* Get the 5 most likely conditions, along with their corresponding probabilities, using our ML model.

* Get a description for any of the predicted diseases, along with specialists in your area, by pressing on them.

* Visualise these specialists by seeing them on a map relative to your location.

## Project Structure
```
SafeSide/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
|
├── .venv/
|
├── assets/
│   ├── emblem.png
│   ├── google_on_white.png
│   └── logo.png
|
├── data/
│   ├── cost_unmet.csv
│   ├── disease_details.csv
│   └── Disease-Prediction-Data.csv
|   └── test_decline.csv
|
├── model/
│   ├── label_encoder.pkl
│   ├── model_weights.pth
│   └── model.py
|
├── pages/
│   ├── 1_symptoms_page.py
│   └── 2_info_page.py
|
├── Home.py
├── README.md
└── requirements.txt
```

## File Descriptions