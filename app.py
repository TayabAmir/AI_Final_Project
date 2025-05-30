import streamlit as st
from datetime import datetime
import warnings
from config import Config
from ui import UIComponents
from modelHandler import ModelHandler
from userIO import UserInputHandler,ResultsDisplayHandler
warnings.filterwarnings('ignore')

class SocialMediaApp:
    """Main application class"""
    
    def __init__(self):
        # Configure page
        st.set_page_config(**Config.PAGE_CONFIG)
        
        # Load UI components
        UIComponents.load_custom_css()
        UIComponents.render_header()
        
        # Load model
        self.model_package = ModelHandler.load_model()
        if self.model_package is None:
            st.stop()
        
        # Display model info
        st.success(f"✅ Loaded Model: **{self.model_package['model_name']}**")
        st.success(f"🤖 AI Assistant: {'✅ Active' if Config.GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY_HERE' else '⚠️ API Key Required'}")
    
    def run(self):
        """Run the main application"""
        # Collect user input
        user_input, predict_button = UserInputHandler.collect_user_input()

        # Main content area
        col1, col2 = st.columns([2, 1])

        with col1:
            if predict_button:
                # Make prediction
                with st.spinner("🔄 Analyzing your social media habits..."):
                    prediction = ModelHandler.make_prediction(self.model_package, user_input)

                if prediction is not None:
                    # Save to session state
                    st.session_state['prediction'] = prediction
                    st.session_state['user_input'] = user_input

                    ResultsDisplayHandler.display_prediction_results(prediction, user_input)

                    if Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                        ResultsDisplayHandler.display_ai_analysis(user_input, prediction)
                    else:
                        st.info("🤖 **AI Analysis Disabled:** Please configure your Gemini API key in the Config class to enable AI insights!")

                    ResultsDisplayHandler.display_basic_analysis(prediction)

            # 👇 Add this fallback for follow-up rerun
            elif 'user_input' in st.session_state and 'prediction' in st.session_state:
                if Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                    ResultsDisplayHandler.display_ai_analysis(
                        st.session_state['user_input'],
                        st.session_state['prediction']
                    )

        with col2:
            if predict_button and 'prediction' in st.session_state:
                ResultsDisplayHandler.display_user_profile(user_input)

        # Display additional recommendations if we have session state
        if 'user_input' in st.session_state and 'prediction' in st.session_state:
            ResultsDisplayHandler.display_insights_recommendations(
                st.session_state['user_input'],
                st.session_state['prediction']
            )

        # Footer
        self.render_footer()

    def render_footer(self):
        """Render application footer"""
        st.markdown("---")
        col_footer1, col_footer2 = st.columns(2)
        
        with col_footer1:
            st.markdown(f"**Model:** {self.model_package['model_name']} | **Time:** {datetime.now().strftime('%H:%M:%S')}")
        
        with col_footer2:
            if Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                st.markdown("🤖 **AI Assistant:** ✅ Active")
            else:
                st.markdown("🤖 **AI Assistant:** ⚠️ API Key Required")

def main():
    """Main function to run the application"""
    app = SocialMediaApp()
    app.run()

if __name__ == "__main__":
    main()