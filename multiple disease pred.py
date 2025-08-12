# -*- coding: utf-8 -*-
"""
Modernized Multiple Disease Prediction System UI
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Personal Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️",
    initial_sidebar_state="expanded"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .prediction-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
    }
    .success-card {
        background-color: #d4edda;
        color: #155724;
    }
    .danger-card {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- LOAD MODELS ----------------------
diabetes_model = pickle.load(open('C:/Users/deysw/OneDrive/Desktop/Multiple Disease Prediction System/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('C:/Users/deysw/OneDrive/Desktop/Multiple Disease Prediction System/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('C:/Users/deysw/OneDrive/Desktop/Multiple Disease Prediction System/parkinsons_model.sav', 'rb'))

# ---------------------- SIDEBAR MENU ----------------------
with st.sidebar:
    selected = option_menu(
        '🩺 Multiple Disease Prediction App',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
        menu_icon='hospital-fill',
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

# ---------------------- FUNCTION FOR CARD ----------------------
def show_prediction(result, positive_msg, negative_msg):
    if result == 1:
        st.markdown(f"<div class='prediction-card danger-card'>{positive_msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='prediction-card success-card'>{negative_msg}</div>", unsafe_allow_html=True)

# ---------------------- DIABETES PAGE ----------------------
if selected == 'Diabetes Prediction':
    st.title('🩸 Diabetes Prediction')
    st.write("Fill in the details below to check the likelihood of diabetes.")

    col1, col2, col3 = st.columns(3)
    Pregnancies = col1.number_input('Number of Pregnancies', min_value=0)
    Glucose = col2.number_input('Glucose Level', min_value=0.0)
    BloodPressure = col3.number_input('Blood Pressure value', min_value=0.0)
    SkinThickness = col1.number_input('Skin Thickness value', min_value=0.0)
    Insulin = col2.number_input('Insulin Level', min_value=0.0)
    BMI = col3.number_input('BMI value', min_value=0.0)
    DiabetesPedigreeFunction = col1.number_input('Diabetes Pedigree Function value', min_value=0.0)
    Age = col2.number_input('Age of the Person', min_value=0)

    if st.button('🔍 Check Diabetes Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        diab_prediction = diabetes_model.predict([user_input])
        show_prediction(diab_prediction[0], '⚠ The person is diabetic', '✅ The person is not diabetic')

# ---------------------- HEART DISEASE PAGE ----------------------
if selected == 'Heart Disease Prediction':
    st.title('❤️ Heart Disease Prediction')
    st.write("Fill in the details below to check the likelihood of heart disease.")

    col1, col2, col3 = st.columns(3)
    age = col1.number_input('Age', min_value=0)
    sex = col2.selectbox('Sex', [0, 1], format_func=lambda x: 'Male' if x == 1 else 'Female')
    cp = col3.number_input('Chest Pain types', min_value=0)
    trestbps = col1.number_input('Resting Blood Pressure', min_value=0.0)
    chol = col2.number_input('Serum Cholestoral in mg/dl', min_value=0.0)
    fbs = col3.selectbox('Fasting Blood Sugar > 120 mg/dl', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
    restecg = col1.number_input('Resting Electrocardiographic results', min_value=0)
    thalach = col2.number_input('Maximum Heart Rate achieved', min_value=0.0)
    exang = col3.selectbox('Exercise Induced Angina', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
    oldpeak = col1.number_input('ST depression induced by exercise', min_value=0.0)
    slope = col2.number_input('Slope of the peak exercise ST segment', min_value=0)
    ca = col3.number_input('Major vessels colored by flourosopy', min_value=0)
    thal = col1.number_input('Thal (0=normal, 1=fixed defect, 2=reversable defect)', min_value=0)

    if st.button('🔍 Check Heart Disease Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                      exang, oldpeak, slope, ca, thal]
        heart_prediction = heart_disease_model.predict([user_input])
        show_prediction(heart_prediction[0], '⚠ The person has heart disease', '✅ The person does not have heart disease')

# ---------------------- PARKINSONS PAGE ----------------------
if selected == 'Parkinsons Prediction':
    st.title("🧠 Parkinson's Disease Prediction")
    st.write("Fill in the details below to check the likelihood of Parkinson's disease.")

    fields = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", 
              "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)",
              "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR",
              "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"]
    
    values = []
    cols = st.columns(5)
    for i, field in enumerate(fields):
        col = cols[i % 5]
        values.append(col.number_input(field, min_value=0.0))

    if st.button("🔍 Check Parkinson's Result"):
        parkinsons_prediction = parkinsons_model.predict([values])
        show_prediction(parkinsons_prediction[0], "⚠ The person has Parkinson's disease", "✅ The person does not have Parkinson's disease")
