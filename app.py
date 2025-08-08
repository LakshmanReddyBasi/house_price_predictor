import streamlit as st
import pandas as pd
import joblib
from streamlit_lottie import st_lottie
import requests
from sklearn.preprocessing import LabelEncoder
import time

# Set page configuration first with wider layout
st.set_page_config(
    page_title="House Price Predictor", 
    page_icon="🏡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

#CSS 
st.markdown("""
<style>
    body {
        color: #ffffff;
        background-color: #111827;
    }
    .main {
        background-color: #111827;
        color: #ffffff;
        padding: 2rem 3rem;
    }
    .stButton button {
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    h1 {
        color: #ffffff;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    h3 {
        color: #ffffff !important;
        margin-top: 1rem !important;
    }
    .subheader {
        color: #9CA3AF;
        font-size: 1.3rem !important;
        margin-bottom: 2rem !important;
    }
    .stForm {
        background-color: #1F2937;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 1px solid #374151;
    }
    div[data-testid="stForm"] {
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px;
        background-color: #1F2937;
    }
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
    }
    .prediction-result {
        font-size: 1.4rem;
        font-weight: bold;
        padding: 1.5rem;
        border-radius: 8px;
        background-color: #153E75;
        color: white;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #2563EB;
    }
    label {
        font-weight: 500;
        color: #E5E7EB !important;
    }
    /* Make input fields more visible */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #374151 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #374151 !important;
        color: white !important;
        border-color: #4B5563 !important;
    }
    input, .st-bq, .st-aj, .st-c0 {
        color: white !important;
    }
    /* Make number input more visible */
    input[type="number"] {
        background-color: #374151 !important;
        color: white !important;
        border-color: #4B5563 !important;
    }
    /* Style the select dropdowns */
    div[data-baseweb="select"] {
        background-color: #374151 !important;
    }
    div[role="listbox"] {
        background-color: #1F2937 !important;
    }
    /* Style the slider */
    div[data-testid="stSlider"] > div {
        background-color: #4F46E5 !important;
    }
    /* Remove hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Icon colors */
    .emoji-span {
        font-size: 1.2rem;
        margin-right: 8px;
        color: #4F46E5;
    }
    /* Specific field label styling */
    .field-label {
        color: #D1D5DB !important;
        font-weight: 500;
        margin-bottom: 5px;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Lottie animations
@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    try:
        return r.json()
    except ValueError:
        return None

# Different animations for splash and main page
splash_animation = load_lottie_url("https://lottie.host/ce4eeaf6-e2bc-421f-98b7-2f8af195f0b7/obnXRuFFLl.json")
main_animation = load_lottie_url("https://lottie.host/a2425c91-7630-4c68-aa51-7b88388fbb7c/NvaArmIdzH.json")

# Initialize session state
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "splash"

# Button callback to switch from splash to main app
def switch_to_main():
    st.session_state.app_mode = "main"

# Show either splash screen or main app based on app_mode
if st.session_state.app_mode == "splash":
    # Splash screen with centered content
    st.markdown("<div style='text-align: center; padding: 3rem 0;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(splash_animation, height=350, key="splash")
        st.markdown("<h1 style='text-align: center; font-size: 3rem !important; color: white;'>🏠 House Price Predictor</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.5rem; margin-bottom: 2rem; color: #9CA3AF;'>Welcome to the Smart House Price Prediction App!</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9CA3AF; margin-bottom: 2rem;'>Get accurate house price predictions using advanced machine learning algorithms.</p>", unsafe_allow_html=True)
        st.button("Enter App →", on_click=switch_to_main, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Main app - only load model when in main mode
    try:
        model_pipeline = joblib.load('model/house_price_model.pkl')
        model_loaded = True
    except Exception as e:
        model_loaded = False
        model_error = str(e)

    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Header section with animation side by side
        header_col1, header_col2 = st.columns([2, 1])
        
        with header_col1:
            st.markdown("<h1>Smart House Price Prediction App</h1>", unsafe_allow_html=True)
            st.markdown("<p class='subheader'>Fill the details below to get an accurate prediction</p>", unsafe_allow_html=True)
        
        with header_col2:
            st_lottie(main_animation, height=150, key="main")
        
        # Form with improved styling and visibility
        with st.form("prediction_form"):
            st.markdown("<h3>Property Details</h3>", unsafe_allow_html=True)
            
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            
            with row1_col1:
                st.markdown("<p class='field-label'>🏷️ MS SubClass</p>", unsafe_allow_html=True)
                MSSubClass = st.number_input("", min_value=20, max_value=190, value=60, key="mssubclass", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>🏙️ MS Zoning</p>", unsafe_allow_html=True)
                MSZoning = st.selectbox("", ['RL', 'RM', 'FV', 'RH', 'C (all)'], key="mszoning", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>🏗️ Year Built</p>", unsafe_allow_html=True)
                YearBuilt = st.number_input("", min_value=1800, max_value=2025, value=2000, key="yearbuilt", label_visibility="collapsed")
                
            with row1_col2:
                st.markdown("<p class='field-label'>📏 Lot Area (sq.ft)</p>", unsafe_allow_html=True)
                LotArea = st.number_input("", min_value=1000, value=8000, key="lotarea", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>📐 Lot Config</p>", unsafe_allow_html=True)
                LotConfig = st.selectbox("", ['Inside', 'FR2', 'Corner', 'CulDSac', 'FR3'], key="lotconfig", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>🔨 Year Remodeled</p>", unsafe_allow_html=True)
                YearRemodAdd = st.number_input("", min_value=1800, max_value=2025, value=2000, key="yearremod", label_visibility="collapsed")
                
            with row1_col3:
                st.markdown("<p class='field-label'>🏘️ Building Type</p>", unsafe_allow_html=True)
                BldgType = st.selectbox("", ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'], key="bldgtype", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>🔧 Overall Condition</p>", unsafe_allow_html=True)
                OverallCond = st.slider("", 1, 10, 5, key="condition", label_visibility="collapsed")
                
                st.markdown("<p class='field-label'>🎨 Exterior Material</p>", unsafe_allow_html=True)
                Exterior1st = st.selectbox("", ['VinylSd', 'MetalSd', 'Wd Sdng', 'HdBoard', 'BrkFace', 'WdShing'], key="exterior", label_visibility="collapsed")
            
            st.markdown("<h3>Basement Details</h3>", unsafe_allow_html=True)
            
            row2_col1, row2_col2 = st.columns(2)
            
            with row2_col1:
                st.markdown("<p class='field-label'>🏚️ Basement Finished SF2</p>", unsafe_allow_html=True)
                BsmtFinSF2 = st.number_input("", min_value=0, value=0, key="bsmtfin", label_visibility="collapsed")
                
            with row2_col2:
                st.markdown("<p class='field-label'>🏠 Total Basement SF</p>", unsafe_allow_html=True)
                TotalBsmtSF = st.number_input("", min_value=0, value=800, key="totalbsmt", label_visibility="collapsed")
            
            st.markdown("")
            submitted = st.form_submit_button("💡 Predict House Price")

        # Prediction Section with improved styling
        if submitted:
            progress_bar = st.progress(0)
            
            for i in range(101):
                time.sleep(0.01)
                progress_bar.progress(i)
            
            if not model_loaded:
                st.error(f" Model file not found: {model_error}")
            else:
                try:
                    # Convert input data into a DataFrame
                    input_data = pd.DataFrame({
                        'MSSubClass': [MSSubClass],
                        'MSZoning': [MSZoning],
                        'LotArea': [LotArea],
                        'LotConfig': [LotConfig],
                        'BldgType': [BldgType],
                        'OverallCond': [OverallCond],
                        'YearBuilt': [YearBuilt],
                        'YearRemodAdd': [YearRemodAdd],
                        'Exterior1st': [Exterior1st],
                        'BsmtFinSF2': [BsmtFinSF2],
                        'TotalBsmtSF': [TotalBsmtSF]
                    })

                    # Label Encoding for categorical columns
                    label_encoder = LabelEncoder()
                    input_data['MSZoning'] = label_encoder.fit_transform(input_data['MSZoning'])
                    input_data['LotConfig'] = label_encoder.fit_transform(input_data['LotConfig'])
                    input_data['BldgType'] = label_encoder.fit_transform(input_data['BldgType'])
                    input_data['Exterior1st'] = label_encoder.fit_transform(input_data['Exterior1st'])

                    # Make the prediction
                    prediction = model_pipeline.predict(input_data)
                    
                    # Display result with better styling
                    st.markdown(f"""
                    <div class='prediction-result'>
                        🏷️ Estimated House Price: ₹ {prediction[0]:,.2f}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("⚠️ Prediction failed. Please make sure your model and input format are correct.")
                    st.exception(e)