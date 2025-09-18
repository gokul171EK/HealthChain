import streamlit as st
from utils.styling import add_app_styling
from utils.gemini_client import get_gemini_response
from datetime import date, time, datetime

# --- Mock DataManager ---
# In a real app, this would be your actual DataManager import
class DataManager:
    def add_health_record(self, user_id, notes):
        # This simulates saving the assessment result
        print(f"Record for user {user_id}: {notes}")
        return True
data_manager = DataManager()
# ------------------------

def show_mental_health_check():
    """Mental health screening and self-assessment tools."""
    st.header("🧠 Mental Health Self-Assessment")
    
    st.info("💡 These screening tools can help identify if you might benefit from talking to a mental health professional. They are not a diagnosis.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # PHQ-2 Depression Screening
        st.subheader("Depression Screening (PHQ-2)")
        with st.form("depression_screening"):
            st.write("Over the **last 2 weeks**, how often have you been bothered by the following problems?")
            
            phq2_q1 = st.radio(
                "1. Little interest or pleasure in doing things.",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="phq2_1", horizontal=True
            )
            
            phq2_q2 = st.radio(
                "2. Feeling down, depressed, or hopeless.",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="phq2_2", horizontal=True
            )
            
            if st.form_submit_button("Assess Depression Risk", use_container_width=True):
                score_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
                total_score = score_map[phq2_q1] + score_map[phq2_q2]
                
                if total_score >= 3:
                    st.warning("⚠️ **Further Evaluation Recommended**: Your responses suggest you may be experiencing symptoms of depression. Please consider speaking with a healthcare provider.")
                else:
                    st.success("✅ **Low Risk Indicated**: Your responses suggest a low likelihood of depression at this time. Continue to monitor your well-being.")
                
                # Log the result
                if 'user_id' in st.session_state and st.session_state.user_id:
                    log_note = f"Completed PHQ-2 Depression Screening. Score: {total_score}/6."
                    data_manager.add_health_record(st.session_state.user_id, notes=log_note)

    with col2:
        # GAD-2 Anxiety Screening
        st.subheader("Anxiety Screening (GAD-2)")
        with st.form("anxiety_screening"):
            st.write("Over the **last 2 weeks**, how often have you been bothered by the following problems?")
            
            gad2_q1 = st.radio(
                "1. Feeling nervous, anxious, or on edge.",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="gad2_1", horizontal=True
            )
            
            gad2_q2 = st.radio(
                "2. Not being able to stop or control worrying.",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="gad2_2", horizontal=True
            )
            
            if st.form_submit_button("Assess Anxiety Risk", use_container_width=True):
                score_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
                total_score = score_map[gad2_q1] + score_map[gad2_q2]
                
                if total_score >= 3:
                    st.warning("⚠️ **Further Evaluation Recommended**: Your responses suggest you may be experiencing symptoms of anxiety. It could be helpful to talk to a mental health professional.")
                else:
                    st.success("✅ **Low Risk Indicated**: Your responses suggest a low likelihood of an anxiety disorder. Continue to practice self-care.")

                # Log the result
                if 'user_id' in st.session_state and st.session_state.user_id:
                    log_note = f"Completed GAD-2 Anxiety Screening. Score: {total_score}/6."
                    data_manager.add_health_record(st.session_state.user_id, notes=log_note)

def show_stress_management():
    """Stress management tools and AI Mindfulness Coach"""
    st.header("😌 Stress Management & Relaxation")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧘‍♀️ Breathing Exercises", 
        "🎵 Relaxation Techniques", 
        "📝 Stress Journal", 
        "🤖 AI Mindfulness Coach"
    ])
    
    with tab1:
        st.subheader("🫁 Guided Breathing Exercises")
        st.info("Practice simple breathing exercises to calm your mind and body.")
        
        st.markdown("**Box Breathing Technique**")
        st.write("A simple technique to calm your nervous system. Inhale for 4s, hold for 4s, exhale for 4s, hold for 4s.")
        if st.button("Start Box Breathing Exercise"):
            st.success("Follow the guide: Inhale... Hold... Exhale... Hold...")

        st.markdown("**4-7-8 Breathing Technique**")
        st.write("A relaxing breath technique to help with sleep and anxiety. Inhale for 4s, hold for 7s, exhale for 8s.")
        if st.button("Start 4-7-8 Breathing Exercise"):
            st.success("Follow the guide: Inhale... Hold... Exhale...")

    with tab2:
        st.subheader("🎵 Relaxation & Mindfulness Techniques")
        st.info("Explore guided techniques to reduce stress and increase mindfulness.")

        with st.expander("5-Minute Mindfulness Meditation"):
            st.markdown("""
            1.  **Find a comfortable position:** Sit or lie down.
            2.  **Focus on your breath:** Notice the sensation of the air entering and leaving your body.
            3.  **Acknowledge thoughts:** When your mind wanders, gently guide your focus back to your breath without judgment.
            4.  **Body scan:** Briefly bring your attention to different parts of your body, noticing any sensations.
            """)
        
        with st.expander("Progressive Muscle Relaxation"):
            st.markdown("""
            1.  Start with your feet. Tense the muscles for 5 seconds, then release for 10 seconds.
            2.  Move up to your legs, tensing and releasing.
            3.  Continue with your torso, arms, and finally your face.
            4.  Notice the feeling of relaxation after releasing the tension.
            """)

    with tab3:
        st.subheader("📝 Stress Journal")
        st.info("Track your stress triggers and coping mechanisms to identify patterns.")

        with st.form("stress_journal_form"):
            st.write("Log your stress levels and triggers for today.")
            stress_level = st.slider("Rate your stress level (1=Low, 10=High):", 1, 10, 5)
            stress_triggers = st.text_area("What were the main triggers for your stress today?")
            coping_methods = st.text_area("What methods did you use to cope with the stress?")

            if st.form_submit_button("Log Stress Entry", use_container_width=True):
                if 'user_id' in st.session_state and st.session_state.user_id:
                    log_note = f"Stress Log: Level {stress_level}/10. Triggers: {stress_triggers}. Coping: {coping_methods}."
                    data_manager.add_health_record(st.session_state.user_id, notes=log_note)
                    st.success("Your stress log for today has been saved.")
                else:
                    st.warning("Please log in to save your journal entries.")


    with tab4:
        st.subheader("🤖 AI Mindfulness Coach")
        st.info("Feeling overwhelmed, stressed, or just need a moment to reset? Describe how you're feeling, and our AI coach will provide a supportive message and a short mindfulness exercise.")

        feeling_input = st.text_area("How are you feeling right now?", key="feeling_input", height=100)

        if st.button("Get Support", use_container_width=True):
            if feeling_input:
                with st.spinner("Your coach is preparing a response..."):
                    system_prompt = "You are a caring and supportive AI mindfulness coach. A user is telling you how they feel. Your task is to respond with two things: First, a short (1-2 sentences), empathetic, and validating message. Second, a simple, guided 1-minute mindfulness or breathing exercise they can do right now to help them process their feeling. Your tone should be gentle and encouraging. Always include a disclaimer that you are an AI and not a therapist."
                    full_prompt = f"{system_prompt}\n\nUser's feeling: '{feeling_input}'"
                    ai_response = get_gemini_response(full_prompt)
                    st.markdown(ai_response)
            else:
                st.warning("Please describe how you're feeling.")

def show_sleep_wellness():
    """Sleep health and hygiene tools."""
    st.header("💤 Sleep Wellness")
    st.info("Improve your sleep quality with our assessment and sleep hygiene guidelines.")
    
    with st.form("sleep_assessment"):
        st.subheader("Sleep Quality Assessment")
        st.write("Answer these questions about your typical sleep patterns.")
        
        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.slider("On average, how many hours do you sleep per night?", 1, 12, 7)
            sleep_quality = st.select_slider("How would you rate your overall sleep quality?", ["Very Poor", "Poor", "Fair", "Good", "Excellent"], "Fair")
        with col2:
            fall_asleep_time = st.selectbox("How long does it usually take you to fall asleep?", ["< 15 min", "15-30 min", "30-60 min", "> 60 min"])
            morning_feeling = st.selectbox("How do you typically feel upon waking?", ["Refreshed", "Somewhat Tired", "Very Tired"])

        if st.form_submit_button("Assess My Sleep", use_container_width=True):
            st.success("Assessment Complete! Based on your responses, here are some recommendations to improve your sleep hygiene.")
            if sleep_hours < 7:
                st.warning("Recommendation: Aim for at least 7-8 hours of sleep per night for optimal health.")
            if fall_asleep_time not in ["< 15 min", "15-30 min"]:
                st.warning("Recommendation: Establish a relaxing bedtime routine to help you fall asleep faster.")
            if morning_feeling != "Refreshed":
                st.warning("Recommendation: To feel more refreshed, ensure your bedroom is dark, quiet, and cool.")

def show_crisis_support():
    """Crisis support and emergency mental health resources."""
    st.header("📞 Crisis Support & Emergency Resources")
    st.error("🚨 **If you are in immediate danger or having thoughts of harming yourself or others, please call emergency services (102) or go to your nearest emergency room immediately.**")
    
    st.subheader("National Helplines (India)")
    crisis_resources = [
        {"name": "Mental Health Helpline (KIRAN)", "number": "1800-599-0019", "desc": "24/7 free mental health support."},
        {"name": "Suicide Prevention (AASRA)", "number": "91-9820466726", "desc": "24/7 emotional support for those in distress."},
        {"name": "Child Helpline", "number": "1098", "desc": "For children in need of care and protection."},
        {"name": "Women's Helpline", "number": "1091", "desc": "Support for women in distress."}
    ]
    for resource in crisis_resources:
        st.markdown(f"**{resource['name']}:** `{resource['number']}` - *{resource['desc']}*")

    with st.expander("⚠️ Warning Signs of a Mental Health Crisis"):
        st.markdown("""
        - Talking about wanting to die or to kill oneself.
        - Looking for a way to kill oneself.
        - Talking about feeling hopeless or having no reason to live.
        - Increasing the use of alcohol or drugs.
        - Withdrawing from activities, family, or friends.
        - Sleeping too much or too little.
        """)
        
def show_mood_tracking():
    """Mood tracking and emotional wellness monitoring."""
    st.header("📊 Mood Tracking & Emotional Wellness")
    st.info("Log your daily mood to understand your emotional patterns and triggers.")
    
    with st.form("mood_log"):
        st.subheader("How are you feeling today?")
        
        mood_rating = st.select_slider(
            "Rate your overall mood:",
            options=["😢", "😟", "😐", "😊", "😄"],
            value="😐"
        )
        
        emotions_felt = st.multiselect(
            "What emotions did you feel today?",
            ["Happy", "Sad", "Anxious", "Calm", "Angry", "Grateful", "Stressed", "Excited"]
        )
        
        mood_notes = st.text_area("Add a note about your day (optional):", placeholder="What influenced your mood today?")
        
        if st.form_submit_button("Log My Mood", use_container_width=True):
            if 'user_id' in st.session_state and st.session_state.user_id:
                log_note = f"Mood Log: Mood was {mood_rating}. Emotions felt: {', '.join(emotions_felt)}. Notes: {mood_notes}"
                data_manager.add_health_record(st.session_state.user_id, notes=log_note)
                st.success("✨ Your mood for today has been logged. Keep it up!")
            else:
                st.warning("Please log in to save your mood entries.")


def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    add_app_styling(theme=st.session_state.theme)

    st.title("🧠 Mental Health & Wellness Support")
    st.markdown("### Your Mental Health Matters - Find Support and Resources")
    
    st.warning("⚠️ If you're experiencing a mental health crisis, please contact emergency services (102) or a crisis helpline immediately. This platform provides support resources but is not a substitute for professional mental health care.")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 Mental Health Check", 
        "😌 Stress Management", 
        "💤 Sleep Wellness", 
        "📞 Crisis Support", 
        "📊 Mood Tracking"
    ])
    
    with tab1:
        show_mental_health_check()
    with tab2:
        show_stress_management()
    with tab3:
        show_sleep_wellness()
    with tab4:
        show_crisis_support()
    with tab5:
        show_mood_tracking()

if __name__ == "__main__":
    main()

