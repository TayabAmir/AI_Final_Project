import streamlit as st
from Gemini_integration import GeminiAI
import os
import pycountry
from AnalyzeAddiction import ChartGenerator, AddictionAnalyzer 

class UserInputHandler:
    """Class to handle user input collection"""
    
    @staticmethod
    def collect_user_input():
        """Collect user input from sidebar"""
        st.sidebar.header("📋 User Information")
        st.sidebar.markdown("Please fill in your details below:")
        
        def get_country_list():
            return sorted([country.name for country in pycountry.countries])
        
        with st.sidebar:
            age = st.slider("Age", min_value=15, max_value=30, value=20, help="Your current age")
            
            gender = st.selectbox("Gender", ["Male", "Female"], help="Select your gender")
            
            academic_level = st.selectbox(
                "Academic Level", 
                ["High School", "Undergraduate", "Graduate"],
                help="Your current academic level"
            )
            
            country = st.selectbox(
                "Country",
                get_country_list(),
                help="Your country of residence"
            )
            
            daily_usage = st.slider(
                "Average Daily Usage (Hours)", 
                min_value=0.5, max_value=12.0, value=4.0, step=0.5,
                help="How many hours do you spend on social media daily?"
            )
            
            platform = st.selectbox(
                "Most Used Platform",
                ["Instagram", "TikTok", "Facebook", "YouTube", "Twitter", "Snapchat", "LinkedIn", "WhatsApp"],
                help="Which platform do you use most?"
            )
            
            affects_academic = st.selectbox(
                "Affects Academic Performance?",
                ["Yes", "No"],
                help="Do you feel social media affects your academic performance?"
            )
            
            sleep_hours = st.slider(
                "Sleep Hours Per Night",
                min_value=4.0, max_value=10.0, value=7.0, step=0.5,
                help="How many hours do you sleep per night?"
            )
            
            mental_health = st.slider(
                "Mental Health Score",
                min_value=1, max_value=10, value=6,
                help="Rate your mental health (1=Poor, 10=Excellent)"
            )
            
            conflicts = st.slider(
                "Conflicts Over Social Media",
                min_value=0, max_value=5, value=1,
                help="How often do you have conflicts due to social media use?"
            )
        
        # Predict button
        predict_button = st.sidebar.button("🔮 Predict Addiction Score", type="primary")
        
        # Return user input dictionary
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
    """Class to handle results display"""
    
    @staticmethod
    def display_prediction_results(prediction, user_input):
        """Display prediction results with charts and analysis"""
        # Get addiction level
        level, emoji, color = AddictionAnalyzer.get_addiction_level(prediction)
        
        # Display prediction
        st.markdown(f"""
        <div class="prediction-box">
            <h2>🎯 Prediction Results</h2>
            <div class="prediction-score">{emoji} {prediction:.1f}/10</div>
            <h3>Addiction Level: {level}</h3>
            <p>Based on your social media usage patterns and personal characteristics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge chart
        st.plotly_chart(ChartGenerator.create_gauge_chart(prediction), use_container_width=True)
    
    @staticmethod
    @staticmethod
    def display_ai_analysis(user_input, prediction):
        """Display AI-powered analysis"""
        st.markdown("---")
        st.markdown("""
        <div class="chatbot-header">
            🤖 AI-Powered Personalized Analysis
        </div>
        """, unsafe_allow_html=True)

        # Save to session_state for later use
        st.session_state["user_input"] = user_input
        st.session_state["prediction"] = prediction

        # Get AI analysis
        with st.spinner("🧠 AI is analyzing your profile and generating personalized insights..."):
            ai_response, success = GeminiAI.query_gemini_api(user_input, prediction)

        if success:
            st.markdown(f"""
            <div class="gemini-response">
                <h4>🎯 Personalized AI Analysis:</h4>
                {ai_response.replace('\n', '<br>')}
            </div>
            """, unsafe_allow_html=True)
            
            # Add this after displaying the response
            report_files = os.listdir("reports")
            latest_report = sorted(report_files)[-1]
            report_path = os.path.join("reports", latest_report)

            with open(report_path, "rb") as f:
                st.download_button(
                    label="📄 Download Full Report (PDF)",
                    data=f,
                    file_name=latest_report,
                    mime="application/pdf"
                )

            # Use session values instead of direct args
            ResultsDisplayHandler.display_follow_up_questions(
                st.session_state["user_input"],
                st.session_state["prediction"]
            )
        else:
            st.error(f"❌ AI Analysis failed: {ai_response}")

    
    @staticmethod
    def display_follow_up_questions(user_input, prediction):
        user_input = st.session_state.get("user_input")
        prediction = st.session_state.get("prediction")

        if not user_input or prediction is None:
            st.error("Missing data. Please restart analysis.")
            st.stop()

        """Display follow-up questions section"""
        st.markdown("### 💬 Ask Follow-up Questions")
        
        # Predefined quick questions
        col_q1, col_q2, col_q3 = st.columns(3)
        
        with col_q1:
            if st.button("📚 Academic Impact Help"):
                with st.spinner("🤔 Thinking..."):
                    follow_up = "How can I minimize social media's impact on my academic performance?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="user-query"><strong>Q:</strong> {follow_up}</div>
                    <div class="gemini-response"><strong>AI:</strong> {response}</div>
                    """, unsafe_allow_html=True)
        
        with col_q2:
            if st.button("😴 Sleep & Usage Tips"):
                with st.spinner("🤔 Thinking..."):
                    follow_up = "How can I improve my sleep while managing social media use?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="user-query"><strong>Q:</strong> {follow_up}</div>
                    <div class="gemini-response"><strong>AI:</strong> {response}</div>
                    """, unsafe_allow_html=True)
        
        with col_q3:
            if st.button("🧠 Mental Health Support"):
                with st.spinner("🤔 Thinking..."):
                    follow_up = "What strategies can help improve my mental health related to social media use?"
                    response, _ = GeminiAI.create_follow_up_query(user_input, prediction, follow_up)
                    st.markdown(f"""
                    <div class="user-query"><strong>Q:</strong> {follow_up}</div>
                    <div class="gemini-response"><strong>AI:</strong> {response}</div>
                    """, unsafe_allow_html=True)
        
        # Custom question input
        st.markdown("#### 💭 Ask Your Own Question")
        custom_question = st.text_input(
            "Type your question about social media addiction, habits, or wellness:",
            placeholder="e.g., How can I reduce my TikTok usage?",
            key="custom_q"
        )
        
        if st.button("🚀 Ask AI") and custom_question:
            with st.spinner("🤖 Getting personalized answer..."):
                custom_response, success = GeminiAI.create_follow_up_query(
                    user_input, prediction, custom_question
                )
                if success:
                    st.markdown(f"""
                    <div class="user-query"><strong>Your Question:</strong> {custom_question}</div>
                    <div class="gemini-response"><strong>AI Response:</strong> {custom_response}</div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ Failed to get AI response. Please try again.")
    
    @staticmethod
    def display_basic_analysis(prediction):
        """Display basic analysis without AI"""
        st.markdown("---")
        st.markdown("### 📊 Basic Analysis")
        if prediction <= 3:
            st.markdown("""
            <div class="success-box">
                <h4>✅ Great News!</h4>
                <p>Your social media usage appears to be well-controlled. You maintain a healthy balance between online and offline activities.</p>
            </div>
            """, unsafe_allow_html=True)
        elif prediction <= 6:
            st.markdown("""
            <div class="warning-box">
                <h4>⚠️ Moderate Usage</h4>
                <p>Your social media usage is moderate. Consider monitoring your habits to prevent them from becoming problematic.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                <h4>🚨 High Usage Detected</h4>
                <p>Your social media usage patterns suggest potential addiction. Consider seeking support or implementing digital wellness strategies.</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def display_user_profile(user_input):
        """Display user profile summary"""
        st.markdown("### 📊 Your Profile")
        
        profile_data = [
            ["Age", f"{user_input['Age']} years"],
            ["Daily Usage", f"{user_input['Avg_Daily_Usage_Hours']} hours"],
            ["Sleep", f"{user_input['Sleep_Hours_Per_Night']} hours"],
            ["Mental Health", f"{user_input['Mental_Health_Score']}/10"],
            ["Platform", user_input['Most_Used_Platform']],
            ["Academic Impact", user_input['Affects_Academic_Performance']]
        ]
        
        for label, value in profile_data:
            st.markdown(f"**{label}:** {value}")
        
        # Comparison radar chart
        st.markdown("### 📈 Profile Comparison")
        user_radar = [
            user_input['Avg_Daily_Usage_Hours'], 
            user_input['Sleep_Hours_Per_Night'], 
            user_input['Mental_Health_Score'], 
            user_input['Conflicts_Over_Social_Media']
        ]
        avg_radar = [4.5, 6.5, 6.5, 2.0]  # Sample averages
        
        fig_radar = ChartGenerator.create_comparison_chart(user_radar, avg_radar)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    @staticmethod
    def display_insights_recommendations(user_input, prediction):
        """Display insights and recommendations"""
        st.markdown("---")
        st.markdown("### 💡 Insights & Recommendations")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if user_input['Avg_Daily_Usage_Hours'] > 6:
                st.warning("📱 **High Usage Alert**\nConsider setting daily time limits")
            else:
                st.success("📱 **Usage Normal**\nGood control over screen time")
        
        with col4:
            if user_input['Sleep_Hours_Per_Night'] < 6:
                st.warning("😴 **Sleep Concern**\nTry to get 7-8 hours of sleep")
            else:
                st.success("😴 **Sleep Healthy**\nGood sleep patterns maintained")
        
        with col5:
            if user_input['Mental_Health_Score'] < 5:
                st.warning("🧠 **Mental Health**\nConsider professional support")
            else:
                st.success("🧠 **Mental Health**\nPositive mental wellbeing")
        
        # Recommendations based on prediction
        st.markdown("### 🎯 Personalized Recommendations")
        if prediction > 7:
            st.markdown("""
            - 🕒 Set specific times for social media use
            - 📵 Use app timers and notifications
            - 🏃‍♂️ Engage in offline physical activities
            - 👥 Spend more time with friends and family in person
            - 📚 Focus on academic/professional goals
            """)
        elif prediction > 4:
            st.markdown("""
            - ⏰ Monitor your daily usage patterns
            - 🔕 Turn off non-essential notifications
            - 🌱 Develop new hobbies outside of social media
            - 💤 Avoid social media before bedtime
            """)
        else:
            st.markdown("""
            - ✅ Continue your healthy usage patterns
            - 🎯 Share your strategies with others
            - 📈 Consider helping friends with social media balance
            """)
