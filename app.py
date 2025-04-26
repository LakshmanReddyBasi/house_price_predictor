import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open('model/house_price_model.pkl', 'rb'))

st.title("🏠 House Price Prediction App")

# Input fields matching training columns
MSSubClass = st.number_input("MSSubClass", min_value=20, max_value=190)
MSZoning = st.selectbox("MSZoning", ['RL', 'RM', 'FV', 'RH', 'C (all)'])
LotArea = st.number_input("LotArea", min_value=1000)
LotConfig = st.selectbox("LotConfig", ['Inside', 'FR2', 'Corner', 'CulDSac', 'FR3'])
BldgType = st.selectbox("BldgType", ['1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'Twnhs'])
OverallCond = st.slider("OverallCond", 1, 10, 5)
YearBuilt = st.number_input("Year Built", min_value=1800, max_value=2025)
YearRemodAdd = st.number_input("Year Remodeled", min_value=1800, max_value=2025)
Exterior1st = st.selectbox("Exterior1st", ['VinylSd', 'MetalSd', 'Wd Sdng', 'HdBoard', 'BrkFace', 'WdShing'])
BsmtFinSF2 = st.number_input("BsmtFinSF2", min_value=0)
TotalBsmtSF = st.number_input("TotalBsmtSF", min_value=0)

# Create a DataFrame with the same columns as model expects
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

# Predict button
if st.button("Predict House Price"):
    prediction = model.predict(input_data)[0]
    st.success(f"🏷️ Estimated House Price: ₹ {prediction:,.2f}")

# Footer
st.markdown("---")
st.write("© 2023 House Price Prediction App. All rights reserved.") 