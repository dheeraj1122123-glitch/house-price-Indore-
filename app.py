import streamlit as st
import pandas as pd
import joblib
st.markdown(
    """
    <head>
        <meta name="google-site-verification" content="w86RdQgR9US_r7V4OengDvxUfTtiJ3MMYt6_fcJZWdM" />
    </head>
    """, 
    unsafe_allow_html=True
)

st.title("My Streamlit App")
# Load saved items
model = joblib.load('house_model.pkl')
model_columns = joblib.load('model_columns.pkl')
rare_locations = joblib.load('rare_locations.pkl')

st.set_page_config(page_title="Indore House Predictor")
st.title("🏠 Indore House Price Predictor")

# Input UI
col1, col2 = st.columns(2)
with col1:
    area = st.number_input("Area (sqft)", value=1000)
    bhk = st.number_input("BHK", value=2)
    location = st.text_input("Location (e.g., Vijay Nagar)", "Vijay Nagar")
with col2:
    bathrooms = st.number_input("Bathrooms", value=2)
    age = st.number_input("Property Age (Years)", value=5)
    facing = st.selectbox("Facing", ["East", "West", "North", "South"])

if st.button("Predict Price"):
    # Preprocess user input
    loc_to_use = "other" if location in rare_locations else location
    
    # Create empty dataframe with same columns as training
    input_df = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # Fill numeric values (make sure names match train.py columns)
    input_df['area_sqft'] = area
    input_df['bhk'] = bhk
    input_df['bathrooms'] = bathrooms
    input_df['age_of_property'] = age
    
    # Fill categorical values
    for col in [f"location_{loc_to_use}", f"facing_{facing}"]:
        if col in model_columns:
            input_df[col] = 1
            
    # Predict
    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Market Price: ₹ {round(prediction, 2)}")

