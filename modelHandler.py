import joblib
import streamlit as st
from config import Config
import pandas as pd

class ModelHandler:
    """Class to handle model operations"""
    
    @staticmethod
    @st.cache_resource
    def load_model():
        """Load the trained model package"""
        try:
            model_package = joblib.load(Config.MODEL_FILE)
            return model_package
        except FileNotFoundError:
            st.error(f"❌ Model file '{Config.MODEL_FILE}' not found. Please run the training script first.")
            return None
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None
    
    @staticmethod
    def make_prediction(model_package, user_input):
        """Make prediction using the loaded model"""
        try:
            # Create DataFrame with user input
            input_df = pd.DataFrame([user_input])
            
            # Apply label encoders
            encoders = model_package['encoders']
            
            # Encode categorical variables
            input_df['Gender'] = encoders['gender'].transform([user_input['Gender']])[0]
            input_df['Academic_Level'] = encoders['academic'].transform([user_input['Academic_Level']])[0]
            input_df['Country'] = encoders['country'].transform([user_input['Country']])[0]
            input_df['Most_Used_Platform'] = encoders['platform'].transform([user_input['Most_Used_Platform']])[0]
            input_df['Affects_Academic_Performance'] = encoders['affects'].transform([user_input['Affects_Academic_Performance']])[0]
            
            # Prepare features in correct order
            feature_order = model_package['feature_names']
            input_features = input_df[feature_order]
            
            # Apply scaling if needed
            if model_package['scaler'] is not None:
                input_features = model_package['scaler'].transform(input_features)
            
            # Make prediction
            prediction = model_package['model'].predict(input_features)[0]
            
            return max(0, min(10, prediction))  # Ensure prediction is between 0-10
            
        except Exception as e:
            st.error(f"❌ Prediction error: {str(e)}")
            return None
