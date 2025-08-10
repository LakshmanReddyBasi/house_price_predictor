import streamlit as st
import pandas as pd
import pickle
import os
from streamlit_lottie import st_lottie
import requests
import time


st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    body {
        color: #E5E7EB;
        background-color: #0F172A;
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0F172A;
        color: #E5E7EB;
        padding: 2rem 3rem;
    }

    /* Headings */
    h1 {
        color: #FFFFFF;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: -0.02em;
    }
    h3 {
        color: #E5E7EB;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Subheader */
    .subheader {
        color: #9CA3AF;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Form Styling */
    .stForm {
        background-color: #1E293B;
        padding: 2.2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        border: 1px solid #334155;
        transition: box-shadow 0.3s ease;
    }
    .stForm:hover {
        box-shadow: 0 12px 32px rgba(79, 70, 229, 0.15);
    }

    /* Buttons */
    .stButton button {
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        border: none;
        transition: all 0.25s ease;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
    }
    .stButton button:hover {
        background-color: #4338CA;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
    }

    /* Input Labels */
    .field-label {
        font-size: 0.95rem;
        font-weight: 500;
        color: #CBD5E1;
        margin-bottom: 0.5rem;
        display: block;
    }

    /* Inputs */
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] > div {
        background-color: #334155 !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        transition: border 0.2s ease;
    }
    div[data-baseweb="input"] input:focus,
    div[data-baseweb="select"]:focus-within {
        border-color: #818CF8 !important;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2);
    }

    /* Select Dropdown */
    div[role="listbox"] {
        background-color: #1E293B !important;
        border-radius: 8px;
        border: 1px solid #475569;
    }

    /* Slider */
    div[data-testid="stSlider"] > div > div > div {
        background-color: #818CF8 !important;
    }

    /* Prediction Result */
    .prediction-result {
        font-size: 1.6rem;
        font-weight: 700;
        padding: 1.6rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #1E40AF, #1E3A8A);
        color: #FFFFFF;
        text-align: center;
        margin: 1.5rem 0;
        border: 1px solid #3730A3;
        box-shadow: 0 4px 14px rgba(30, 64, 175, 0.3);
        animation: fadeIn 0.5s ease;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Responsive padding */
    @media (max-width: 768px) {
        .main { padding: 1rem; }
        h1 { font-size: 2.2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# Cache Lottie Animation
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"Failed to load animation: {e}")
        return None
# Load Animations 
SPLASH_URL = "https://lottie.host/ce4eeaf6-e2bc-421f-98b7-2f8af195f0b7/obnXRuFFLl.json"
MAIN_URL = "https://lottie.host/a2425c91-7630-4c68-aa51-7b88388fbb7c/NvaArmIdzH.json"

splash_animation = load_lottie_url(SPLASH_URL)
main_animation = load_lottie_url(MAIN_URL)

# Session State Initialization
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "splash"

def switch_to_main():
    st.session_state.app_mode = "main"
    # No delay — instant transition

# Model Loading (Cached)
@st.cache_resource
def load_model(model_path):
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        return None

# Get model path
script_dir = os.path.dirname(__file__)
model_path = os.path.join(script_dir, 'house_price_model.pkl')
model = load_model(model_path)
model_loaded = model is not None

if st.session_state.app_mode == "splash":
    st.markdown("<div style='text-align: center; padding: 6rem 1rem;'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if splash_animation:
            st_lottie(splash_animation, height=300, key="splash_anim", speed=1.2)
        st.markdown("<h1 style='color: white;'>🏡 House Price Predictor</h1>", unsafe_allow_html=True)
        st.markdown("""
            <p style='font-size: 1.3rem; color: #9CA3AF; margin: 1rem 0 2rem;'>
                Get smart, accurate predictions in seconds.
            </p>
        """, unsafe_allow_html=True)
        st.button("🚀 Get Started", on_click=switch_to_main, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Main App 
else:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # Header with animation
        header_col1, header_col2 = st.columns([2, 1])
        with header_col1:
            st.markdown("<h1>Smart House Price Prediction</h1>", unsafe_allow_html=True)
            st.markdown("<p class='subheader'>Fill in the property details for an instant estimate.</p>", unsafe_allow_html=True)
        with header_col2:
            if main_animation:
                st_lottie(main_animation, height=160, key="main_anim", loop=True, speed=1)

        # Prediction Form
        with st.form("prediction_form"):
            st.markdown("<h3>PropertyParams</h3>", unsafe_allow_html=True)

            # First Row: MSSubClass, LotArea, BldgType
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("<p class='field-label'>🏷️ MS SubClass</p>", unsafe_allow_html=True)
                MSSubClass = st.number_input("", min_value=20, max_value=190, value=60, step=1, key="mssubclass", label_visibility="collapsed")

                st.markdown("<p class='field-label'>🏙️ MS Zoning</p>", unsafe_allow_html=True)
                MSZoning = st.selectbox("", ['RL', 'RM', 'FV', 'RH', 'C (all)'], key="mszoning", label_visibility="collapsed")

                st.markdown("<p class='field-label'>🏗️ Year Built</p>", unsafe_allow_html=True)
                YearBuilt = st.number_input("", min_value=1800, max_value=2025, value=2000, step=1, key="yearbuilt", label_visibility="collapsed")

            with c2:
                st.markdown("<p class='field-label'>📏 Lot Area (sq.ft)</p>", unsafe_allow_html=True)
                LotArea = st.number_input("", min_value=1000, value=8000, step=100, key="lotarea", label_visibility="collapsed")

                st.markdown("<p class='field-label'>📐 Lot Configuration</p>", unsafe_allow_html=True)
                LotConfig = st.selectbox("", ['Inside', 'FR2', 'Corner', 'CulDSac', 'FR3'], key="lotconfig", label_visibility="collapsed")

                st.markdown("<p class='field-label'>🔨 Remodeled Year</p>", unsafe_allow_html=True)
                YearRemodAdd = st.number_input("", min_value=1800, max_value=2025, value=2000, step=1, key="yearremod", label_visibility="collapsed")

            with c3:
                st.markdown("<p class='field-label'>🏘️ Building Type</p>", unsafe_allow_html=True)
                BldgType = st.selectbox("", ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'], key="bldgtype", label_visibility="collapsed")

                st.markdown("<p class='field-label'>🔧 Overall Condition</p>", unsafe_allow_html=True)
                OverallCond = st.slider("", 1, 10, 5, key="condition", label_visibility="collapsed")

                st.markdown("<p class='field-label'>🎨 Exterior Material</p>", unsafe_allow_html=True)
                Exterior1st = st.selectbox("", ['VinylSd', 'MetalSd', 'Wd Sdng', 'HdBoard', 'BrkFace', 'WdShing', 'Plywood', 'CemntBd', 'ImStucc', 'Stone', 'Stucco'], key="exterior", label_visibility="collapsed")

            # Basement
            st.markdown("<h3>Basement Details</h3>", unsafe_allow_html=True)
            cb1, cb2 = st.columns(2)
            with cb1:
                st.markdown("<p class='field-label'>🏚️ Finished SF2</p>", unsafe_allow_html=True)
                BsmtFinSF2 = st.number_input("", min_value=0.0, value=0.0, step=10.0, key="bsmtfin", label_visibility="collapsed")
            with cb2:
                st.markdown("<p class='field-label'>🏠 Total Basement SF</p>", unsafe_allow_html=True)
                TotalBsmtSF = st.number_input("", min_value=0.0, value=800.0, step=10.0, key="totalbsmt", label_visibility="collapsed")

            # Submit Button
            submitted = st.form_submit_button("💡 Predict Price", use_container_width=True)

        # Handle Prediction
        if submitted:
            if not model_loaded:
                st.error("❌ Model not loaded. Please check the file path.")
            else:
                # Minimal progress bar 
                with st.spinner("Predicting..."):
                    time.sleep(0.3)  # Simulate brief processing 

                try:
                    # Feature construction
                    features = {
                        'MSSubClass': MSSubClass,
                        'LotArea': LotArea,
                        'OverallCond': OverallCond,
                        'YearBuilt': YearBuilt,
                        'YearRemodAdd': YearRemodAdd,
                        'BsmtFinSF2': BsmtFinSF2,
                        'TotalBsmtSF': TotalBsmtSF
                    }

                    # One-hot encoding mapping
                    cat_map = {
                        'MSZoning': ['C (all)', 'FV', 'RH', 'RL', 'RM'],
                        'LotConfig': ['Corner', 'CulDSac', 'FR2', 'FR3', 'Inside'],
                        'BldgType': ['1Fam', '2fmCon', 'Duplex', 'Twnhs', 'TwnhsE'],
                        'Exterior1st': ['AsbShng', 'AsphShn', 'BrkComm', 'BrkFace', 'CBlock', 'CemntBd', 'HdBoard', 'ImStucc', 'MetalSd', 'Plywood', 'Stone', 'Stucco', 'VinylSd', 'Wd Sdng', 'WdShing']
                    }

                    for col, opts in cat_map.items():
                        val = globals()[col]
                        for opt in opts:
                            features[f"{col}_{opt}"] = 1.0 if val == opt else 0.0

                    input_df = pd.DataFrame([features])
                    prediction = model.predict(input_df)[0]

                    # Display result with animation
                    st.markdown(f"""
                        <div class='prediction-result'>
                            💰 Estimated Price: <strong>${prediction:,.2f}</strong>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error("⚠️ Prediction failed. Please verify inputs.")
                    st.code(str(e))
