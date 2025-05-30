import streamlit as st
from Gemini_integration import GeminiAI
import os
import pycountry
from ui import UIComponents
from AnalyzeAddiction import ChartGenerator, AddictionAnalyzer 

class UserInputHandler:
    
    @staticmethod
    def collect_user_input():
        
        def get_country_list():
            return sorted([country.name for country in pycountry.countries])
        
        UIComponents.display_section_header("Personal Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=15, max_value=30, value=20, 
                                help="Your current age")
            gender = st.selectbox("Gender", ["Male", "Female"], 
                                help="Select your gender")
            academic_level = st.selectbox("Academic Level", 
                                        ["High School", "Undergraduate", "Graduate"],
                                        help="Your current academic level")
        
        with col2:
            country = st.selectbox("Country", get_country_list(),
                                 help="Your country of residence")
            daily_usage = st.number_input("Daily Usage (Hours)", 
                                        min_value=0.5, max_value=12.0, value=4.0, step=0.5,
                                        help="Hours spent on social media daily")
            platform = st.selectbox("Most Used Platform",
                                   ["Instagram", "TikTok", "Facebook", "YouTube", 
                                    "Twitter", "Snapchat", "LinkedIn", "WhatsApp"],
                                   help="Which platform do you use most?")
        
        with col3:
            affects_academic = st.selectbox("Affects Academic Performance?",
                                          ["Yes", "No"],
                                          help="Does social media affect your academic performance?")
            sleep_hours = st.number_input("Sleep Hours Per Night",
                                        min_value=4.0, max_value=10.0, value=7.0, step=0.5,
                                        help="How many hours do you sleep per night?")
            mental_health = st.slider("Mental Health Score",
                                    min_value=1, max_value=10, value=6,
                                    help="Rate your mental health (1=Poor, 10=Excellent)")
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            conflicts = st.slider("Conflicts Over Social Media",
                                min_value=0, max_value=5, value=1,
                                help="How often do you have conflicts due to social media use?")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            predict_button = st.button("Predict Addiction Score", 
                                     type="primary", 
                                     use_container_width=True)
        
        user_input = {
            'Age': age,
            'Gender': gender,
            'Academic_Level': academic_level,
            'Country': country,
            'Avg_Daily_Usage_Hours': daily_usage,
            'Most_Used_Platform': platform,
            'Affects_Academic_Performance': affects_academic,
            'Sleep_Hours_Per_Night': sleep_hours,
            'Mental_Health_Score': mental_health,
            'Conflicts_Over_Social_Media': conflicts
        }
        
        return user_input, predict_button

class ResultsDisplayHandler:
    
    @staticmethod
    def display_prediction_results(prediction, user_input):
        level, emoji, color = AddictionAnalyzer.get_addiction_level(prediction)
        UIComponents.display_score(prediction, level, emoji)
        st.plotly_chart(ChartGenerator.create_gauge_chart(prediction), 
                       use_container_width=True, config={'displayModeBar': False})
    
    @staticmethod
    def display_ai_analysis(user_input, prediction):
        st.markdown("---")
        UIComponents.display_section_header("AI-Powered Analysis")
        st.session_state["user_input"] = user_input
        st.session_state["prediction"] = prediction
        with st.spinner("AI is analyzing your profile..."):
            ai_response, success = GeminiAI.query_gemini_api(user_input, prediction)
        if success:
            st.markdown(f"""
            <div class="ai-section">
                <div class="ai-header">Personalized Analysis</div>
                <div class="ai-response">
                    {ai_response.replace('\n', '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            try:
                report_files = os.listdir("reports")
                if report_files:
                    latest_report = sorted(report_files)[-1]
                    report_path = os.path.join("reports", latest_report)
                    with open(report_path, "rb") as f:
                        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                        with col_dl2:
                            st.download_button(
                                label="Download Full Report (PDF)",
                                data=f,
                                file_name=latest_report,
                                mime="application/pdf",
                                use_container_width=True
                            )
            except:
                pass
            ResultsDisplayHandler.display_follow_up_questions(user_input, prediction)
        else:
            st.error(f"AI Analysis failed: {ai_response}")

    @staticmethod
    def display_follow_up_questions(user_input, prediction):
        UIComponents.display_section_header("Ask Follow-up Questions")
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            if st.button("Academic Impact", use_container_width=True):
                with st.spinner("Thinking..."):
                    follow_up = "How can I minimize social media's impact on my academic performance?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="ai-response" style="margin-top: 1rem;">
                        <strong>Q:</strong> {follow_up}<br><br>
                        <strong>AI:</strong> {response}
                    </div>
                    """, unsafe_allow_html=True)
        with col_q2:
            if st.button("Sleep & Usage", use_container_width=True):
                with st.spinner("Thinking..."):
                    follow_up = "How can I improve my sleep while managing social media use?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="ai-response" style="margin-top: 1rem;">
                        <strong>Q:</strong> {follow_up}<br><br>
                        <strong>AI:</strong> {response}
                    </div>
                    """, unsafe_allow_html=True)
        with col_q3:
            if st.button("Mental Health", use_container_width=True):
                with st.spinner("Thinking..."):
                    follow_up = "What strategies can help improve my mental health related to social media use?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="ai-response" style="margin-top: 1rem;">
                        <strong>Q:</strong> {follow_up}<br><br>
                        <strong>AI:</strong> {response}
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        custom_question = st.text_input(
            "Ask your own question:",
            placeholder="e.g., How can I reduce my TikTok usage?",
            key="custom_q"
        )
        col_ask1, col_ask2, col_ask3 = st.columns([1, 2, 1])
        with col_ask2:
            if st.button("Ask AI", use_container_width=True) and custom_question:
                with st.spinner("Getting personalized answer..."):
                    custom_response, success = GeminiAI.create_follow_up_query(
                        user_input, prediction, custom_question
                    )
                    if success:
                        st.markdown(f"""
                        <div class="ai-response" style="margin-top: 1rem;">
                            <strong>Your Question:</strong> {custom_question}<br><br>
                            <strong>AI Response:</strong> {custom_response}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Failed to get AI response. Please try again.")
    
    @staticmethod
    def display_basic_analysis(prediction):
        UIComponents.display_section_header("Analysis Summary")
        if prediction <= 3:
            UIComponents.display_recommendation(
                "Great News!",
                "Your social media usage appears to be well-controlled. You maintain a healthy balance between online and offline activities."
            )
        elif prediction <= 6:
            UIComponents.display_recommendation(
                "Moderate Usage",
                "Your social media usage is moderate. Consider monitoring your habits to prevent them from becoming problematic."
            )
        else:
            UIComponents.display_recommendation(
                "High Usage Detected",
                "Your social media usage patterns suggest potential addiction. Consider seeking support or implementing digital wellness strategies."
            )
    
    @staticmethod
    def display_user_profile(user_input):
        UIComponents.display_section_header("Your Profile Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            UIComponents.display_metric_card("Age", f"{user_input['Age']} years")
            UIComponents.display_metric_card("Daily Usage", f"{user_input['Avg_Daily_Usage_Hours']} hours")
        with col2:
            UIComponents.display_metric_card("Sleep Hours", f"{user_input['Sleep_Hours_Per_Night']} hours")
            UIComponents.display_metric_card("Mental Health", f"{user_input['Mental_Health_Score']}/10")
        with col3:
            UIComponents.display_metric_card("Platform", user_input['Most_Used_Platform'])
            UIComponents.display_metric_card("Academic Impact", user_input['Affects_Academic_Performance'])
    
    @staticmethod
    def display_insights_recommendations(user_input, prediction):
        UIComponents.display_section_header("Personalized Recommendations")
        col1, col2, col3 = st.columns(3)
        with col1:
            if user_input['Avg_Daily_Usage_Hours'] > 6:
                UIComponents.display_recommendation(
                    "Usage Alert",
                    "Consider setting daily time limits to reduce screen time."
                )
            else:
                UIComponents.display_recommendation(
                    "Usage Normal",
                    "Good control over your screen time. Keep it up!"
                )
        with col2:
            if user_input['Sleep_Hours_Per_Night'] < 6:
                UIComponents.display_recommendation(
                    "Sleep Concern",
                    "Try to get 7-8 hours of sleep for better health."
                )
            else:
                UIComponents.display_recommendation(
                    "Sleep Healthy",
                    "Good sleep patterns are being maintained."
                )
        with col3:
            if user_input['Mental_Health_Score'] < 5:
                UIComponents.display_recommendation(
                    "Mental Health",
                    "Consider professional support for mental wellness."
                )
            else:
                UIComponents.display_recommendation(
                    "Mental Health",
                    "Positive mental wellbeing detected."
                )
        st.markdown("<br>", unsafe_allow_html=True)
        if prediction > 7:
            UIComponents.display_recommendation(
                "High Priority Actions",
                "• Set specific times for social media use• Use app timers and notifications\n• Engage in offline physical activities\n• Spend more time with friends and family in person\n• Focus on academic/professional goals"
            )
        elif prediction > 4:
            UIComponents.display_recommendation(
                "Moderate Actions",
                "• Monitor your daily usage patterns\n• Turn off non-essential notifications\n• Develop new hobbies outside of social media\n• Avoid social media before bedtime"
            )
        else:
            UIComponents.display_recommendation(
                "Keep Going",
                "• Continue your healthy usage patterns\n• Share your strategies with others\n• Consider helping friends with social media balance"
            )