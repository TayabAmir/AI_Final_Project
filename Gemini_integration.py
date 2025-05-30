from AnalyzeAddiction import AddictionAnalyzer
from config import Config
from google import genai

from fpdf import FPDF
import os
from datetime import datetime

class PDFGenerator:
    @staticmethod
    def generate_report(user_input, prediction_score, addiction_level, ai_response):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        font_path = "fonts/DejaVuSans.ttf" 
        pdf.add_font("DejaVu", "", font_path, uni=True)
        pdf.set_font("DejaVu", "", 14)

        pdf.set_font("DejaVu", "", 16)
        pdf.cell(0, 10, "Social Media Addiction Analysis Report", ln=True, align='C')
        
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(10)

        pdf.set_font("DejaVu", "", 14)
        pdf.cell(0, 10, "User Profile", ln=True)
        pdf.set_font("DejaVu", "", 12)
        for key, value in user_input.items():
            pdf.cell(0, 8, f"{key.replace('_', ' ')}: {value}", ln=True)
        pdf.ln(5)

        pdf.set_font("DejaVu", "", 14)
        pdf.cell(0, 10, "Prediction Results", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(0, 8, f"Addiction Score: {prediction_score:.1f}/10", ln=True)
        pdf.cell(0, 8, f"Addiction Level: {addiction_level}", ln=True)
        pdf.ln(5)

        pdf.set_font("DejaVu", "", 14)
        pdf.cell(0, 10, "AI Personalized Analysis", ln=True)
        pdf.set_font("DejaVu", "", 12)
        for line in ai_response.split("\n"):
            pdf.multi_cell(0, 8, line)

        os.makedirs("reports", exist_ok=True)
        file_path = os.path.join("reports", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        pdf.output(file_path)
        return file_path



class GeminiAI:
    """Class to handle Gemini AI integration using the official genai.Client"""

    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    @staticmethod
    def query_gemini_api(user_input, prediction_score):
        """Query Gemini AI API with prediction results for personalized advice"""
        try:
            addiction_level, _, _ = AddictionAnalyzer.get_addiction_level(prediction_score)

            prompt = f"""
            I am a social media addiction prediction system. Here are the results for a user:

            User Profile:
            - Age: {user_input['Age']} years old
            - Gender: {user_input['Gender']}
            - Academic Level: {user_input['Academic_Level']}
            - Country: {user_input['Country']}
            - Daily Social Media Usage: {user_input['Avg_Daily_Usage_Hours']} hours
            - Most Used Platform: {user_input['Most_Used_Platform']}
            - Affects Academic Performance: {user_input['Affects_Academic_Performance']}
            - Sleep Hours: {user_input['Sleep_Hours_Per_Night']} hours per night
            - Mental Health Score: {user_input['Mental_Health_Score']}/10
            - Social Media Conflicts: {user_input['Conflicts_Over_Social_Media']} incidents

            Prediction Results:
            - Addiction Score: {prediction_score:.1f}/10
            - Addiction Level: {addiction_level}

            Please provide:
            1. A personalized analysis of this user's social media habits
            2. Specific, actionable recommendations for improvement
            3. Potential risks or concerns based on their profile
            4. Positive aspects of their current habits (if any)
            5. Long-term strategies for maintaining healthy social media use

            Keep the response as brief as possible but easy to understand, and make it encouraging and supportive.
            """

            response = GeminiAI.client.models.generate_content(
                model="gemini-1.5-flash",  
                contents=prompt
            )
            PDFGenerator.generate_report(user_input, prediction_score, addiction_level, response.text)
            return response.text, True

        except Exception as e:
            return f"Error: {str(e)}", False

    @staticmethod
    def create_follow_up_query(user_input, prediction_score, custom_question):
        """Handle follow-up questions from the user using Gemini client"""
        try:
            addiction_level, _, _ = AddictionAnalyzer.get_addiction_level(prediction_score)

            prompt_text = f"""
            You are an AI assistant helping with social media addiction analysis. 

            User's Profile Summary:
            - Age: {user_input['Age']}, Gender: {user_input['Gender']}
            - Daily Usage: {user_input['Avg_Daily_Usage_Hours']} hours
            - Addiction Score: {prediction_score:.1f}/10 ({addiction_level} level)
            - Most Used Platform: {user_input['Most_Used_Platform']}
            - Academic Impact: {user_input['Affects_Academic_Performance']}
            - Sleep: {user_input['Sleep_Hours_Per_Night']} hours
            - Mental Health: {user_input['Mental_Health_Score']}/10

            User's Question: {custom_question}

            Please provide a helpful, personalized response based on their social media usage profile.
            """
            response = GeminiAI.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[{"role": "user", "parts": [{"text": prompt_text}]}]
            )

            return response.text, True

        except Exception as e:
            return f"Error: {str(e)}", False

