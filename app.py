import streamlit as st
from datetime import datetime
import warnings
from config import Config
from ui import UIComponents
from modelHandler import ModelHandler
from userIO import UserInputHandler, ResultsDisplayHandler
warnings.filterwarnings('ignore')

class SocialMediaApp:
    """Main application class with clean, modern design"""
    
    def __init__(self):
        st.set_page_config(
            page_title="Social Media Addiction Predictor",
            page_icon="📱",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        UIComponents.load_custom_css()
        UIComponents.render_header()
        
        self.model_package = ModelHandler.load_model()
        if self.model_package is None:
            st.stop()
        
        col_status1, col_status2 = st.columns(2)
        with col_status1:
            st.success(f"✅ Model: **{self.model_package['model_name']}**")
        with col_status2:
            ai_status = '✅ Active' if Config.GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY_HERE' else '⚠️ Configure API Key'
            st.info(f"🤖 AI Assistant: {ai_status}")
    
    def run(self):
        """Run the main application with clean layout"""
        user_input, predict_button = UserInputHandler.collect_user_input()

        if predict_button:
            with st.spinner("🔄 Analyzing your social media habits..."):
                prediction = ModelHandler.make_prediction(self.model_package, user_input)

            if prediction is not None:
                st.session_state['prediction'] = prediction
                st.session_state['user_input'] = user_input

                st.markdown("---")
                
                col_results1, col_results2 = st.columns([2, 1])
                
                with col_results1:
                    ResultsDisplayHandler.display_prediction_results(prediction, user_input)
                
                with col_results2:
                    ResultsDisplayHandler.display_user_profile(user_input)

                if Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                    ResultsDisplayHandler.display_ai_analysis(user_input, prediction)
                else:
                    st.markdown("---")
                    UIComponents.display_section_header("🤖 AI Analysis")
                    st.info("Please configure your Gemini API key to enable AI insights!")

                ResultsDisplayHandler.display_basic_analysis(prediction)
                
                ResultsDisplayHandler.display_insights_recommendations(user_input, prediction)

        elif 'user_input' in st.session_state and 'prediction' in st.session_state:
            st.markdown("---")
            
            col_prev1, col_prev2 = st.columns([2, 1])
            
            with col_prev1:
                ResultsDisplayHandler.display_prediction_results(
                    st.session_state['prediction'], 
                    st.session_state['user_input']
                )
            
            with col_prev2:
                ResultsDisplayHandler.display_user_profile(st.session_state['user_input'])

            if Config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                ResultsDisplayHandler.display_ai_analysis(
                    st.session_state['user_input'],
                    st.session_state['prediction']
                )

            ResultsDisplayHandler.display_basic_analysis(st.session_state['prediction'])
            ResultsDisplayHandler.display_insights_recommendations(
                st.session_state['user_input'],
                st.session_state['prediction']
            )

        self.render_footer()

    def render_footer(self):
        """Render clean application footer"""
        st.markdown("---")
        st.markdown(
            f"<div style='text-align: center; color: #6b7280; padding: 1rem;'>"
            f"Model: {self.model_package['model_name']} | "
            f"Time: {datetime.now().strftime('%H:%M:%S')} | "
            f"AI: {'Active' if Config.GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY_HERE' else 'Inactive'}"
            f"</div>", 
            unsafe_allow_html=True
        )

def main():
    """Main function to run the application"""
    app = SocialMediaApp()
    app.run()

if __name__ == "__main__":
    main()