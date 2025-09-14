import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date, time
from utils.data_manager import DataManager
from utils.ai_simulator import AISimulator
from utils.styling import add_app_styling

# Initialize components
@st.cache_resource
def init_components():
    return DataManager(), AISimulator()

data_manager, ai_simulator = init_components()

st.set_page_config(
    page_title="Mental Health Support - HEALTHTECH",
    page_icon="🧠",
    layout="wide"
)

def main():
    add_app_styling()
    st.title("🧠 Mental Health & Wellness Support")
    st.markdown("### Your Mental Health Matters - Find Support and Resources")
    
    # Mental health disclaimer
    st.warning("⚠️ If you're experiencing a mental health crisis, please contact emergency services (102) or a crisis helpline immediately. This platform provides support resources but is not a substitute for professional mental health care.")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.info("🔒 Some features require login. You can still access mental health resources and emergency contacts.")
    
    # Tabs for different mental health features
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

def show_mental_health_check():
    """Mental health screening and self-assessment"""
    st.header("🧠 Mental Health Self-Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Quick Mental Health Screening")
        
        st.info("💡 This screening tool can help identify if you might benefit from talking to a mental health professional. It's not a diagnosis.")
        
        # PHQ-2 Depression Screening
        st.markdown("**🔍 Depression Screening (PHQ-2)**")
        
        with st.form("depression_screening"):
            st.write("Over the past 2 weeks, how often have you been bothered by:")
            
            phq2_q1 = st.radio(
                "1. Little interest or pleasure in doing things",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="phq2_1"
            )
            
            phq2_q2 = st.radio(
                "2. Feeling down, depressed, or hopeless",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="phq2_2"
            )
            
            if st.form_submit_button("📊 Check Depression Risk"):
                score_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
                total_score = score_map[phq2_q1] + score_map[phq2_q2]
                
                if total_score >= 3:
                    st.warning("⚠️ **Positive Screen**: Your responses suggest you may be experiencing symptoms of depression. Consider speaking with a healthcare provider.")
                    st.info("📞 **Resources**: National Mental Health Helpline: 1800-599-0019")
                else:
                    st.success("✅ **Negative Screen**: Your responses suggest low likelihood of depression. Continue monitoring your mental health.")
                
                # Save screening result
                if 'user_id' in st.session_state and st.session_state.user_id:
                    screening_log = f"Depression Screening (PHQ-2): Score {total_score}/6 - {'Positive' if total_score >= 3 else 'Negative'} screen"
                    data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=screening_log
                    )
        
        st.markdown("---")
        
        # GAD-2 Anxiety Screening
        st.markdown("**😰 Anxiety Screening (GAD-2)**")
        
        with st.form("anxiety_screening"):
            st.write("Over the past 2 weeks, how often have you been bothered by:")
            
            gad2_q1 = st.radio(
                "1. Feeling nervous, anxious, or on edge",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="gad2_1"
            )
            
            gad2_q2 = st.radio(
                "2. Not being able to stop or control worrying",
                ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                key="gad2_2"
            )
            
            if st.form_submit_button("📊 Check Anxiety Risk"):
                score_map = {"Not at all": 0, "Several days": 1, "More than half the days": 2, "Nearly every day": 3}
                total_score = score_map[gad2_q1] + score_map[gad2_q2]
                
                if total_score >= 3:
                    st.warning("⚠️ **Positive Screen**: Your responses suggest you may be experiencing symptoms of anxiety. Consider speaking with a healthcare provider.")
                    st.info("📞 **Resources**: National Mental Health Helpline: 1800-599-0019")
                else:
                    st.success("✅ **Negative Screen**: Your responses suggest low likelihood of anxiety disorder. Continue monitoring your mental health.")
                
                # Save screening result
                if 'user_id' in st.session_state and st.session_state.user_id:
                    screening_log = f"Anxiety Screening (GAD-2): Score {total_score}/6 - {'Positive' if total_score >= 3 else 'Negative'} screen"
                    data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=screening_log
                    )
        
        st.markdown("---")
        
        # Stress Level Assessment
        st.markdown("**😤 Stress Level Assessment**")
        
        with st.form("stress_assessment"):
            stress_level = st.select_slider(
                "How would you rate your current stress level?",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                value=5,
                format_func=lambda x: f"{x} - {'Very Low' if x <= 2 else 'Low' if x <= 4 else 'Moderate' if x <= 6 else 'High' if x <= 8 else 'Very High'}"
            )
            
            stress_sources = st.multiselect(
                "What are your main sources of stress? (Select all that apply)",
                ["Work/Career", "Relationships", "Financial", "Health", "Family", "Education", "Social", "Other"]
            )
            
            coping_methods = st.multiselect(
                "How do you currently cope with stress? (Select all that apply)",
                ["Exercise", "Meditation", "Talking to friends/family", "Hobbies", "Music", "Reading", "Sleep", "Unhealthy habits", "None"]
            )
            
            if st.form_submit_button("📊 Assess Stress Level"):
                if stress_level <= 4:
                    st.success("✅ **Low Stress**: You're managing stress well. Keep up the good work!")
                elif stress_level <= 7:
                    st.warning("⚠️ **Moderate Stress**: Consider implementing more stress management techniques.")
                else:
                    st.error("🚨 **High Stress**: Your stress level is concerning. Consider speaking with a mental health professional.")
                
                st.write("**🎯 Personalized Recommendations:**")
                
                if "Exercise" not in coping_methods:
                    st.info("💪 Try adding physical activity - even 10 minutes of walking can reduce stress")
                
                if "Meditation" not in coping_methods:
                    st.info("🧘‍♀️ Consider mindfulness or meditation practices")
                
                if "Unhealthy habits" in coping_methods:
                    st.warning("⚠️ Try to replace unhealthy coping methods with healthier alternatives")
                
                if stress_sources:
                    st.write(f"**Main stress sources:** {', '.join(stress_sources)}")
                    if "Work/Career" in stress_sources:
                        st.info("💼 Consider work-life balance strategies and time management")
                    if "Financial" in stress_sources:
                        st.info("💰 Consider financial counseling or budgeting resources")
    
    with col2:
        st.subheader("🆘 Crisis Resources")
        
        crisis_resources = [
            {"name": "National Mental Health Helpline", "number": "1800-599-0019", "availability": "24/7"},
            {"name": "Suicide Prevention Helpline", "number": "1800-273-8255", "availability": "24/7"},
            {"name": "Crisis Text Line", "number": "Text HOME to 741741", "availability": "24/7"},
            {"name": "Women's Helpline", "number": "1091", "availability": "24/7"},
            {"name": "Child Helpline", "number": "1098", "availability": "24/7"}
        ]
        
        for resource in crisis_resources:
            st.error(f"**{resource['name']}**\n📞 {resource['number']}\n🕐 {resource['availability']}")
        
        st.subheader("💡 Mental Health Tips")
        
        daily_tips = [
            "🌅 Start your day with positive affirmations",
            "🧘‍♀️ Practice 5 minutes of deep breathing",
            "📱 Limit social media time",
            "🌿 Spend time in nature",
            "📞 Connect with a friend or family member",
            "📝 Write down 3 things you're grateful for",
            "🎵 Listen to calming music",
            "💤 Maintain a regular sleep schedule"
        ]
        
        for tip in daily_tips:
            st.info(tip)
        
        st.subheader("📚 Mental Health Resources")
        
        resources = [
            "📖 Mental health education articles",
            "🎥 Guided meditation videos",
            "📱 Mental health apps recommendations",
            "👥 Support group information",
            "🏥 Local mental health services",
            "📞 Therapist finder tools"
        ]
        
        for resource in resources:
            st.success(resource)

def show_stress_management():
    """Stress management tools and techniques"""
    st.header("😌 Stress Management & Relaxation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🧘‍♀️ Breathing Exercises", "🎵 Relaxation Techniques", "📝 Stress Journal", "🎯 Stress Management Plan"])
    
    with tab1:
        st.subheader("🫁 Guided Breathing Exercises")
        
        col_breath1, col_breath2 = st.columns(2)
        
        with col_breath1:
            st.markdown("**🔢 4-7-8 Breathing Technique**")
            st.write("This technique helps reduce anxiety and promote relaxation:")
            st.write("1. Inhale through nose for 4 counts")
            st.write("2. Hold breath for 7 counts") 
            st.write("3. Exhale through mouth for 8 counts")
            st.write("4. Repeat 4 times")
            
            if st.button("▶️ Start 4-7-8 Breathing", use_container_width=True):
                run_breathing_exercise("4-7-8")
        
        with col_breath2:
            st.markdown("**📦 Box Breathing Technique**")
            st.write("Used by military and first responders:")
            st.write("1. Inhale for 4 counts")
            st.write("2. Hold for 4 counts")
            st.write("3. Exhale for 4 counts")
            st.write("4. Hold for 4 counts")
            st.write("5. Repeat 4-6 times")
            
            if st.button("▶️ Start Box Breathing", use_container_width=True):
                run_breathing_exercise("Box")
        
        st.markdown("---")
        
        st.markdown("**🌊 Progressive Muscle Relaxation**")
        st.write("Systematically tense and relax different muscle groups:")
        
        muscle_groups = [
            "🦶 Feet and toes - Curl toes, then relax",
            "🦵 Calves - Tighten, then release",
            "🦵 Thighs - Squeeze, then relax",
            "✋ Hands - Make fists, then open",
            "💪 Arms - Flex biceps, then relax",
            "🤷‍♀️ Shoulders - Raise to ears, then drop",
            "😤 Face - Scrunch up, then release"
        ]
        
        if st.button("🎵 Start Progressive Muscle Relaxation"):
            st.success("🎵 Starting guided progressive muscle relaxation session...")
            for i, muscle in enumerate(muscle_groups, 1):
                st.write(f"**Step {i}:** {muscle}")
            st.info("Hold tension for 5 seconds, then relax for 10 seconds before moving to the next group.")
    
    with tab2:
        st.subheader("🎵 Relaxation & Mindfulness Techniques")
        
        relaxation_techniques = [
            {
                "name": "🧘‍♀️ 5-Minute Mindfulness Meditation",
                "description": "Simple mindfulness practice for beginners",
                "duration": "5 minutes",
                "steps": [
                    "Find a comfortable seated position",
                    "Close your eyes or soften your gaze",
                    "Focus on your breath",
                    "Notice when mind wanders, gently return to breath",
                    "End with gratitude"
                ]
            },
            {
                "name": "🌈 Visualization Exercise",
                "description": "Mental imagery for relaxation",
                "duration": "10 minutes",
                "steps": [
                    "Close your eyes and take deep breaths",
                    "Imagine a peaceful place",
                    "Engage all your senses in the visualization",
                    "Stay in this peaceful place",
                    "Slowly return to the present moment"
                ]
            },
            {
                "name": "🔢 5-4-3-2-1 Grounding Technique",
                "description": "Grounding exercise for anxiety",
                "duration": "3-5 minutes",
                "steps": [
                    "Name 5 things you can see",
                    "Name 4 things you can touch",
                    "Name 3 things you can hear", 
                    "Name 2 things you can smell",
                    "Name 1 thing you can taste"
                ]
            }
        ]
        
        for technique in relaxation_techniques:
            with st.expander(f"{technique['name']} - {technique['duration']}"):
                st.write(technique['description'])
                st.write("**Steps:**")
                for i, step in enumerate(technique['steps'], 1):
                    st.write(f"{i}. {step}")
                
                if st.button(f"▶️ Start {technique['name']}", key=f"start_{technique['name']}"):
                    st.success(f"Starting {technique['name']} - Follow the steps above")
    
    with tab3:
        st.subheader("📝 Stress Journal")
        
        if 'user_id' not in st.session_state or st.session_state.user_id is None:
            st.error("🔒 Please login to access stress journaling")
        else:
            # Stress journal entry
            with st.form("stress_journal_entry"):
                st.write("**📝 Record Your Stress Experience**")
                
                col_journal1, col_journal2 = st.columns(2)
                
                with col_journal1:
                    stress_date = st.date_input("📅 Date", value=date.today())
                    stress_level = st.slider("😤 Stress Level (1-10)", 1, 10, 5)
                    stress_triggers = st.text_area("🎯 What triggered your stress?")
                
                with col_journal2:
                    physical_symptoms = st.multiselect("💔 Physical symptoms", [
                        "Headache", "Muscle tension", "Fatigue", "Sleep problems", 
                        "Stomach issues", "Heart racing", "Sweating", "Other"
                    ])
                    
                    emotional_symptoms = st.multiselect("😔 Emotional symptoms", [
                        "Anxiety", "Irritability", "Sadness", "Overwhelmed",
                        "Angry", "Restless", "Worried", "Other"
                    ])
                
                coping_used = st.text_area("🛠️ How did you cope with the stress?")
                
                effectiveness = st.selectbox("📊 How effective was your coping strategy?", [
                    "Very effective", "Somewhat effective", "Not very effective", "Not effective at all"
                ])
                
                notes = st.text_area("📔 Additional notes or reflections")
                
                if st.form_submit_button("💾 Save Journal Entry"):
                    # Save stress journal entry
                    journal_entry = f"Stress Journal: Date {stress_date}, Level {stress_level}/10. Triggers: {stress_triggers}. Physical: {', '.join(physical_symptoms)}. Emotional: {', '.join(emotional_symptoms)}. Coping: {coping_used}. Effectiveness: {effectiveness}. Notes: {notes}"
                    
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=journal_entry
                    )
                    
                    if record_id:
                        st.success("✅ Stress journal entry saved!")
                    else:
                        st.error("❌ Error saving journal entry")
            
            st.markdown("---")
            
            # Stress patterns analysis
            st.subheader("📈 Stress Patterns Analysis")
            
            # Mock stress data for analysis
            stress_data = pd.DataFrame({
                'Date': pd.date_range('2024-08-01', periods=30, freq='D'),
                'Stress_Level': [5, 7, 4, 6, 8, 3, 4, 9, 6, 5, 7, 4, 8, 5, 6, 3, 7, 8, 4, 5, 6, 7, 5, 4, 8, 6, 5, 7, 4, 6]
            })
            
            # Stress level chart
            fig = px.line(stress_data, x='Date', y='Stress_Level', 
                         title="Stress Level Trends (Past 30 Days)",
                         labels={'Stress_Level': 'Stress Level (1-10)', 'Date': 'Date'})
            fig.update_traces(line_color='red')
            fig.add_hline(y=5, line_dash="dash", line_color="orange", 
                         annotation_text="Moderate Stress Level")
            st.plotly_chart(fig, use_container_width=True)
            
            # Stress insights
            avg_stress = stress_data['Stress_Level'].mean()
            high_stress_days = len(stress_data[stress_data['Stress_Level'] >= 7])
            
            col_insight1, col_insight2, col_insight3 = st.columns(3)
            
            with col_insight1:
                st.metric("📊 Average Stress Level", f"{avg_stress:.1f}/10")
            
            with col_insight2:
                st.metric("🔴 High Stress Days", f"{high_stress_days}/30")
            
            with col_insight3:
                trend = "📈 Increasing" if stress_data['Stress_Level'].iloc[-5:].mean() > stress_data['Stress_Level'].iloc[:5].mean() else "📉 Decreasing"
                st.metric("📈 Trend", trend)
    
    with tab4:
        st.subheader("🎯 Personal Stress Management Plan")
        
        if 'user_id' not in st.session_state or st.session_state.user_id is None:
            st.error("🔒 Please login to create your stress management plan")
        else:
            with st.form("stress_management_plan"):
                st.write("**🎯 Create Your Personalized Stress Management Plan**")
                
                # Stress triggers identification
                common_triggers = st.multiselect("🎯 Your main stress triggers", [
                    "Work deadlines", "Financial concerns", "Relationship issues", "Health problems",
                    "Traffic/commuting", "Technology", "Social situations", "Family responsibilities",
                    "Academic pressure", "Major life changes", "Other"
                ])
                
                # Preferred coping strategies
                coping_strategies = st.multiselect("🛠️ Your preferred coping strategies", [
                    "Deep breathing", "Exercise/walking", "Meditation", "Talking to others",
                    "Listening to music", "Reading", "Journaling", "Time in nature",
                    "Hobbies", "Professional help", "Other"
                ])
                
                # Daily stress management routine
                morning_routine = st.text_area("🌅 Morning stress prevention routine")
                evening_routine = st.text_area("🌙 Evening stress relief routine")
                
                # Emergency stress response
                emergency_response = st.text_area("🚨 Emergency stress response plan (what to do when stress is overwhelming)")
                
                # Support system
                support_people = st.text_area("👥 Support people you can contact")
                
                # Goals
                stress_goals = st.text_area("🎯 Your stress management goals")
                
                if st.form_submit_button("💾 Save Stress Management Plan"):
                    plan = f"Stress Management Plan: Triggers: {', '.join(common_triggers)}. Coping: {', '.join(coping_strategies)}. Morning: {morning_routine}. Evening: {evening_routine}. Emergency: {emergency_response}. Support: {support_people}. Goals: {stress_goals}"
                    
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=plan
                    )
                    
                    if record_id:
                        st.success("✅ Stress management plan saved!")
                        st.balloons()
                    else:
                        st.error("❌ Error saving plan")

def run_breathing_exercise(technique):
    """Run guided breathing exercise"""
    if technique == "4-7-8":
        st.success("🫁 Starting 4-7-8 Breathing Exercise")
        st.write("**Instructions:**")
        st.write("1. 🫁 Inhale through nose for 4 counts")
        st.write("2. ⏸️ Hold breath for 7 counts")
        st.write("3. 💨 Exhale through mouth for 8 counts")
        st.write("4. 🔄 Repeat 4 times")
        
    elif technique == "Box":
        st.success("📦 Starting Box Breathing Exercise")
        st.write("**Instructions:**")
        st.write("1. 🫁 Inhale for 4 counts")
        st.write("2. ⏸️ Hold for 4 counts")
        st.write("3. 💨 Exhale for 4 counts")
        st.write("4. ⏸️ Hold for 4 counts")
        st.write("5. 🔄 Repeat 4-6 times")
    
    st.info("🎵 Find a comfortable position and follow along. Focus only on your breathing.")

def show_sleep_wellness():
    """Sleep health and hygiene tools"""
    st.header("💤 Sleep Wellness")
    
    tab1, tab2, tab3 = st.tabs(["😴 Sleep Assessment", "🛏️ Sleep Hygiene", "📊 Sleep Tracking"])
    
    with tab1:
        st.subheader("😴 Sleep Quality Assessment")
        
        with st.form("sleep_assessment"):
            st.write("**💤 Answer these questions about your sleep patterns:**")
            
            col_sleep1, col_sleep2 = st.columns(2)
            
            with col_sleep1:
                sleep_hours = st.number_input("🕐 Average hours of sleep per night", min_value=1, max_value=12, value=7)
                
                bedtime = st.time_input("🛏️ Usual bedtime", value=time(22, 30))
                wake_time = st.time_input("⏰ Usual wake time", value=time(7, 0))
                
                sleep_quality = st.selectbox("😴 How would you rate your sleep quality?", [
                    "Very poor", "Poor", "Fair", "Good", "Excellent"
                ])
                
                fall_asleep_time = st.selectbox("⏱️ How long does it take you to fall asleep?", [
                    "Less than 15 minutes", "15-30 minutes", "30-60 minutes", "More than 60 minutes"
                ])
            
            with col_sleep2:
                night_awakenings = st.selectbox("🌙 How often do you wake up during the night?", [
                    "Never", "1-2 times", "3-4 times", "5+ times"
                ])
                
                morning_feeling = st.selectbox("🌅 How do you feel when you wake up?", [
                    "Very refreshed", "Somewhat refreshed", "Neutral", "Tired", "Very tired"
                ])
                
                sleep_problems = st.multiselect("😓 Sleep problems you experience", [
                    "Difficulty falling asleep", "Frequent awakenings", "Early morning awakening",
                    "Snoring", "Sleep apnea", "Restless legs", "Nightmares", "None"
                ])
                
                caffeine_timing = st.selectbox("☕ When do you last have caffeine?", [
                    "Before noon", "1-3 PM", "4-6 PM", "After 6 PM", "I don't consume caffeine"
                ])
            
            screen_time = st.selectbox("📱 Screen time before bed", [
                "No screens 2+ hours before bed", "No screens 1 hour before bed", 
                "Some screen time before bed", "Heavy screen time before bed"
            ])
            
            if st.form_submit_button("📊 Assess Sleep Quality"):
                # Calculate sleep score
                score = 0
                
                if sleep_hours >= 7 and sleep_hours <= 9:
                    score += 2
                elif sleep_hours >= 6 or sleep_hours <= 10:
                    score += 1
                
                quality_scores = {"Excellent": 2, "Good": 1, "Fair": 0, "Poor": -1, "Very poor": -2}
                score += quality_scores.get(sleep_quality, 0)
                
                if fall_asleep_time == "Less than 15 minutes":
                    score += 2
                elif fall_asleep_time == "15-30 minutes":
                    score += 1
                elif fall_asleep_time == "30-60 minutes":
                    score -= 1
                else:
                    score -= 2
                
                if night_awakenings == "Never":
                    score += 2
                elif night_awakenings == "1-2 times":
                    score += 1
                else:
                    score -= 1
                
                feeling_scores = {"Very refreshed": 2, "Somewhat refreshed": 1, "Neutral": 0, "Tired": -1, "Very tired": -2}
                score += feeling_scores.get(morning_feeling, 0)
                
                # Sleep quality interpretation
                if score >= 6:
                    st.success("✅ **Excellent Sleep Quality** - You have healthy sleep patterns!")
                elif score >= 3:
                    st.info("😊 **Good Sleep Quality** - Your sleep is generally healthy with room for improvement")
                elif score >= 0:
                    st.warning("⚠️ **Fair Sleep Quality** - Consider implementing sleep hygiene practices")
                else:
                    st.error("🚨 **Poor Sleep Quality** - Significant sleep issues detected. Consider consulting a healthcare provider")
                
                # Personalized recommendations
                st.subheader("🎯 Personalized Sleep Recommendations")
                
                if sleep_hours < 7:
                    st.info("⏰ Try to get 7-9 hours of sleep per night")
                
                if fall_asleep_time in ["30-60 minutes", "More than 60 minutes"]:
                    st.info("🧘‍♀️ Try relaxation techniques before bed")
                
                if "Heavy screen time before bed" in screen_time:
                    st.info("📱 Avoid screens 1-2 hours before bedtime")
                
                if caffeine_timing == "After 6 PM":
                    st.info("☕ Avoid caffeine after 2 PM")
                
                if sleep_problems and "None" not in sleep_problems:
                    st.warning("⚠️ Consider discussing your sleep problems with a healthcare provider")
                
                # Save assessment
                if 'user_id' in st.session_state and st.session_state.user_id:
                    assessment_log = f"Sleep Assessment: Score {score}, Quality: {sleep_quality}, Hours: {sleep_hours}, Problems: {', '.join(sleep_problems) if sleep_problems else 'None'}"
                    data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=assessment_log
                    )
    
    with tab2:
        st.subheader("🛏️ Sleep Hygiene Guidelines")
        
        # Sleep hygiene categories
        hygiene_categories = {
            "🛏️ Sleep Environment": [
                "Keep bedroom cool (60-67°F/15-19°C)",
                "Make room as dark as possible",
                "Minimize noise or use white noise",
                "Invest in comfortable mattress and pillows",
                "Reserve bed for sleep and intimacy only"
            ],
            "⏰ Sleep Schedule": [
                "Go to bed and wake up at same time daily",
                "Avoid sleeping in on weekends", 
                "Limit naps to 20-30 minutes before 3 PM",
                "Get natural sunlight exposure in morning",
                "Establish consistent bedtime routine"
            ],
            "🍽️ Food & Drink": [
                "Avoid large meals 2-3 hours before bed",
                "Limit caffeine after 2 PM",
                "Avoid alcohol 3 hours before bedtime",
                "Don't go to bed hungry or overly full",
                "Consider herbal tea (chamomile, valerian)"
            ],
            "💪 Lifestyle Habits": [
                "Exercise regularly, but not close to bedtime",
                "Avoid screens 1-2 hours before bed",
                "Try relaxation techniques",
                "Manage stress and worries before bed",
                "If can't sleep, get up and do quiet activity"
            ]
        }
        
        for category, tips in hygiene_categories.items():
            with st.expander(category, expanded=True):
                for tip in tips:
                    st.write(f"✅ {tip}")
        
        # Sleep hygiene checklist
        st.subheader("📋 Personal Sleep Hygiene Checklist")
        
        if 'user_id' in st.session_state and st.session_state.user_id:
            st.write("Check off the sleep hygiene practices you currently follow:")
            
            all_tips = []
            for tips in hygiene_categories.values():
                all_tips.extend(tips)
            
            checked_tips = []
            for i, tip in enumerate(all_tips):
                if st.checkbox(tip, key=f"hygiene_{i}"):
                    checked_tips.append(tip)
            
            if st.button("💾 Save My Sleep Hygiene Progress"):
                hygiene_log = f"Sleep Hygiene Checklist: Following {len(checked_tips)}/{len(all_tips)} practices: {', '.join(checked_tips)}"
                data_manager.add_health_record(
                    st.session_state.user_id,
                    notes=hygiene_log
                )
                st.success(f"✅ Progress saved: {len(checked_tips)}/{len(all_tips)} practices followed")
        else:
            st.info("🔒 Login to track your sleep hygiene progress")
    
    with tab3:
        st.subheader("📊 Sleep Tracking")
        
        if 'user_id' not in st.session_state or st.session_state.user_id is None:
            st.error("🔒 Please login to access sleep tracking")
        else:
            # Sleep log entry
            with st.form("sleep_log"):
                st.write("**📝 Log Last Night's Sleep**")
                
                col_log1, col_log2 = st.columns(2)
                
                with col_log1:
                    sleep_date = st.date_input("📅 Sleep Date", value=date.today() - timedelta(days=1))
                    bedtime_log = st.time_input("🛏️ Bedtime", value=time(22, 30))
                    wake_time_log = st.time_input("⏰ Wake Time", value=time(7, 0))
                
                with col_log2:
                    sleep_quality_log = st.selectbox("😴 Sleep Quality", [
                        "Excellent", "Good", "Fair", "Poor", "Very Poor"
                    ])
                    
                    sleep_interruptions = st.number_input("🌙 Number of times you woke up", min_value=0, max_value=20, value=0)
                    
                    sleep_notes = st.text_area("📝 Sleep Notes", placeholder="Any factors that affected your sleep...")
                
                if st.form_submit_button("💾 Log Sleep"):
                    # Calculate sleep duration
                    bedtime_dt = datetime.combine(sleep_date, bedtime_log)
                    wake_dt = datetime.combine(sleep_date + timedelta(days=1), wake_time_log)
                    if wake_time_log < bedtime_log:
                        wake_dt = datetime.combine(sleep_date + timedelta(days=1), wake_time_log)
                    else:
                        wake_dt = datetime.combine(sleep_date, wake_time_log)
                    
                    sleep_duration = (wake_dt - bedtime_dt).total_seconds() / 3600
                    
                    sleep_log_entry = f"Sleep Log: Date {sleep_date}, Bedtime {bedtime_log}, Wake {wake_time_log}, Duration {sleep_duration:.1f}h, Quality {sleep_quality_log}, Interruptions {sleep_interruptions}. Notes: {sleep_notes}"
                    
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=sleep_log_entry
                    )
                    
                    if record_id:
                        st.success(f"✅ Sleep logged: {sleep_duration:.1f} hours of {sleep_quality_log.lower()} sleep")
                    else:
                        st.error("❌ Error logging sleep")
            
            st.markdown("---")
            
            # Sleep analytics
            st.subheader("📈 Sleep Analytics")
            
            # Mock sleep data for visualization
            sleep_data = pd.DataFrame({
                'Date': pd.date_range('2024-08-01', periods=30, freq='D'),
                'Duration': [7.2, 6.8, 7.5, 8.1, 6.5, 7.8, 8.2, 6.9, 7.1, 7.6, 6.7, 7.9, 8.0, 7.3, 6.8, 7.4, 7.7, 6.6, 7.2, 8.1, 7.0, 7.5, 6.9, 7.8, 7.1, 6.8, 7.6, 7.4, 7.2, 7.7],
                'Quality': [4, 3, 4, 5, 2, 4, 5, 3, 4, 4, 3, 5, 4, 4, 3, 4, 4, 3, 4, 5, 4, 4, 3, 4, 4, 3, 4, 4, 4, 4]  # 1-5 scale
            })
            
            # Sleep duration chart
            fig_duration = px.line(sleep_data, x='Date', y='Duration', 
                                 title="Sleep Duration Trends (Past 30 Days)",
                                 labels={'Duration': 'Hours of Sleep', 'Date': 'Date'})
            fig_duration.add_hline(y=7, line_dash="dash", line_color="green", 
                                 annotation_text="Recommended 7+ hours")
            fig_duration.add_hline(y=9, line_dash="dash", line_color="green", 
                                 annotation_text="Upper limit 9 hours")
            st.plotly_chart(fig_duration, use_container_width=True)
            
            # Sleep quality chart
            fig_quality = px.line(sleep_data, x='Date', y='Quality',
                                title="Sleep Quality Trends (Past 30 Days)", 
                                labels={'Quality': 'Quality Rating (1-5)', 'Date': 'Date'})
            fig_quality.update_traces(line_color='purple')
            st.plotly_chart(fig_quality, use_container_width=True)
            
            # Sleep insights
            avg_duration = sleep_data['Duration'].mean()
            avg_quality = sleep_data['Quality'].mean()
            good_sleep_nights = len(sleep_data[sleep_data['Duration'] >= 7])
            
            col_sleep_insight1, col_sleep_insight2, col_sleep_insight3 = st.columns(3)
            
            with col_sleep_insight1:
                st.metric("😴 Average Sleep", f"{avg_duration:.1f} hours")
            
            with col_sleep_insight2:
                st.metric("⭐ Average Quality", f"{avg_quality:.1f}/5")
            
            with col_sleep_insight3:
                st.metric("✅ Good Sleep Nights", f"{good_sleep_nights}/30")

def show_crisis_support():
    """Crisis support and emergency mental health resources"""
    st.header("📞 Crisis Support & Emergency Resources")
    
    # Emergency warning
    st.error("🚨 **If you are in immediate danger or having thoughts of harming yourself or others, please call emergency services (102) or go to your nearest emergency room immediately.**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📞 Crisis Helplines")
        
        crisis_numbers = [
            {
                "name": "National Suicide Prevention Lifeline",
                "number": "1800-273-8255", 
                "description": "24/7 crisis support for those in emotional distress or suicidal crisis",
                "availability": "24/7"
            },
            {
                "name": "Mental Health Helpline (KIRAN)",
                "number": "1800-599-0019",
                "description": "Free mental health support and counseling",
                "availability": "24/7"
            },
            {
                "name": "Crisis Text Line",
                "number": "Text HOME to 741741",
                "description": "Text-based crisis support",
                "availability": "24/7"
            },
            {
                "name": "Women's Helpline",
                "number": "181",
                "description": "Support for women in distress",
                "availability": "24/7"
            },
            {
                "name": "Child Helpline",
                "number": "1098",
                "description": "Support for children in crisis",
                "availability": "24/7"
            }
        ]
        
        for helpline in crisis_numbers:
            with st.container():
                col_help1, col_help2 = st.columns([3, 1])
                
                with col_help1:
                    st.markdown(f"### 📞 {helpline['name']}")
                    st.write(f"**Number:** {helpline['number']}")
                    st.write(f"**Description:** {helpline['description']}")
                    st.write(f"**Available:** {helpline['availability']}")
                
                with col_help2:
                    if st.button(f"📞 Call", key=f"call_{helpline['name']}", use_container_width=True):
                        st.success(f"Calling {helpline['number']}")
                
                st.markdown("---")
        
        st.subheader("🏥 Emergency Mental Health Services")
        
        emergency_services = [
            {
                "name": "Nearest Emergency Room",
                "description": "For immediate psychiatric emergencies",
                "action": "Go immediately or call 102"
            },
            {
                "name": "Mobile Crisis Team",
                "description": "Mental health professionals who come to you",
                "action": "Available in some areas - call local mental health center"
            },
            {
                "name": "Crisis Stabilization Units",
                "description": "Short-term residential crisis support",
                "action": "Contact through mental health services"
            }
        ]
        
        for service in emergency_services:
            st.info(f"**{service['name']}**: {service['description']} - {service['action']}")
        
        st.subheader("⚠️ Warning Signs of Mental Health Crisis")
        
        warning_signs = [
            "🚨 Thoughts of suicide or self-harm",
            "🗣️ Talking about wanting to die or hurt oneself",
            "🔍 Looking for ways to kill oneself",
            "💬 Talking about feeling hopeless or having no purpose",
            "😤 Talking about feeling trapped or in unbearable pain",
            "🍺 Increasing use of alcohol or drugs",
            "😴 Sleeping too little or too much",
            "😠 Extreme mood swings",
            "🚫 Withdrawing from family and friends",
            "📵 Giving away prized possessions"
        ]
        
        st.error("**If you or someone you know shows these signs:**")
        for sign in warning_signs:
            st.write(f"• {sign}")
        
        st.error("**Take immediate action:**")
        st.write("• Call a crisis helpline")
        st.write("• Don't leave the person alone")
        st.write("• Remove any potential means of self-harm")
        st.write("• Take the person to an emergency room")
        st.write("• Call emergency services (102)")
    
    with col2:
        st.subheader("🆘 Quick Crisis Actions")
        
        crisis_actions = [
            {"action": "🚨 Call Emergency", "number": "102"},
            {"action": "📞 Suicide Hotline", "number": "1800-273-8255"},
            {"action": "💬 Crisis Text", "number": "741741"},
            {"action": "🏥 Find ER", "number": "102"}
        ]
        
        for i, action in enumerate(crisis_actions):
            if st.button(action["action"], key=f"crisis_{i}", use_container_width=True):
                st.error(f"Calling {action['number']}")
        
        st.subheader("🤝 How to Help Someone in Crisis")
        
        help_steps = [
            "1. 👂 Listen without judgment",
            "2. ❤️ Show you care and want to help", 
            "3. 📞 Help them contact crisis resources",
            "4. 👥 Stay with them if possible",
            "5. 🚫 Remove potential means of harm",
            "6. 🏥 Help get professional help",
            "7. 📱 Follow up after the crisis"
        ]
        
        for step in help_steps:
            st.info(step)
        
        st.subheader("📱 Mental Health Apps")
        
        apps = [
            "🧘‍♀️ Headspace - Meditation & mindfulness",
            "😌 Calm - Sleep stories & relaxation",
            "📝 Daylio - Mood tracking",
            "🎯 MindShift - Anxiety management",
            "💪 Sanvello - Anxiety & mood tracking"
        ]
        
        for app in apps:
            st.success(app)
        
        st.subheader("🌐 Online Resources")
        
        resources = [
            "🧠 National Institute of Mental Health",
            "💚 Mental Health First Aid",
            "📚 Crisis Text Line resources",
            "👥 NAMI (National Alliance on Mental Illness)",
            "🏥 Local mental health centers"
        ]
        
        for resource in resources:
            st.info(resource)

def show_mood_tracking():
    """Mood tracking and emotional wellness monitoring"""
    st.header("📊 Mood Tracking & Emotional Wellness")
    
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access mood tracking features")
        return
    
    tab1, tab2, tab3 = st.tabs(["😊 Daily Mood Log", "📈 Mood Analytics", "🎯 Emotional Goals"])
    
    with tab1:
        st.subheader("😊 Track Your Daily Mood")
        
        with st.form("mood_log"):
            col_mood1, col_mood2 = st.columns(2)
            
            with col_mood1:
                mood_date = st.date_input("📅 Date", value=date.today())
                
                overall_mood = st.select_slider(
                    "😊 Overall Mood",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    value=5,
                    format_func=lambda x: f"{x} - {'😢' if x <= 2 else '😟' if x <= 4 else '😐' if x <= 6 else '😊' if x <= 8 else '😄'}"
                )
                
                energy_level = st.select_slider(
                    "⚡ Energy Level", 
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    value=5
                )
                
                stress_level = st.select_slider(
                    "😤 Stress Level",
                    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    value=5
                )
            
            with col_mood2:
                emotions_felt = st.multiselect("💭 Emotions you felt today", [
                    "Happy", "Sad", "Angry", "Anxious", "Excited", "Calm", 
                    "Frustrated", "Grateful", "Lonely", "Confident", "Overwhelmed", "Content"
                ])
                
                mood_triggers = st.multiselect("🎯 What influenced your mood?", [
                    "Work", "Relationships", "Health", "Weather", "Sleep", "Exercise",
                    "Social media", "News", "Family", "Money", "Achievement", "Other"
                ])
                
                coping_activities = st.multiselect("🛠️ Coping activities you used", [
                    "Exercise", "Meditation", "Talking to friends", "Music", "Reading",
                    "Hobbies", "Nature", "Journaling", "Breathing exercises", "None"
                ])
            
            mood_notes = st.text_area("📝 Mood Notes", placeholder="Describe your day, thoughts, or anything that affected your mood...")
            
            gratitude = st.text_area("🙏 What are you grateful for today?", placeholder="List 1-3 things you're grateful for...")
            
            if st.form_submit_button("💾 Save Mood Entry"):
                mood_log_entry = f"Mood Log: Date {mood_date}, Mood {overall_mood}/10, Energy {energy_level}/10, Stress {stress_level}/10. Emotions: {', '.join(emotions_felt)}. Triggers: {', '.join(mood_triggers)}. Coping: {', '.join(coping_activities)}. Notes: {mood_notes}. Gratitude: {gratitude}"
                
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    notes=mood_log_entry
                )
                
                if record_id:
                    st.success("✅ Mood entry saved!")
                    
                    # Provide immediate feedback
                    if overall_mood <= 3:
                        st.warning("😔 It seems like you're having a tough day. Consider reaching out to someone or trying a coping activity.")
                        st.info("💙 Remember: This feeling is temporary and you're not alone.")
                    elif overall_mood >= 8:
                        st.success("😄 Great to see you're feeling good! What's working well for you today?")
                    
                    if stress_level >= 8:
                        st.warning("😤 High stress detected. Consider stress management techniques or speaking with someone.")
                else:
                    st.error("❌ Error saving mood entry")
    
    with tab2:
        st.subheader("📈 Mood Analytics & Insights")
        
        # Mock mood data for analytics
        mood_data = pd.DataFrame({
            'Date': pd.date_range('2024-08-01', periods=30, freq='D'),
            'Mood': [6, 4, 7, 8, 5, 6, 7, 3, 5, 7, 6, 8, 9, 6, 5, 7, 8, 4, 6, 7, 5, 8, 6, 7, 5, 6, 8, 7, 6, 7],
            'Energy': [6, 3, 7, 8, 4, 6, 7, 3, 5, 7, 5, 8, 9, 6, 4, 7, 8, 4, 6, 7, 5, 8, 6, 7, 5, 6, 8, 7, 6, 7],
            'Stress': [5, 8, 4, 3, 7, 5, 4, 8, 6, 4, 6, 3, 2, 5, 7, 4, 3, 8, 5, 4, 6, 3, 5, 4, 6, 5, 3, 4, 5, 4]
        })
        
        # Mood trends chart
        fig_mood = go.Figure()
        
        fig_mood.add_trace(go.Scatter(
            x=mood_data['Date'],
            y=mood_data['Mood'],
            mode='lines+markers',
            name='Mood',
            line=dict(color='blue')
        ))
        
        fig_mood.add_trace(go.Scatter(
            x=mood_data['Date'],
            y=mood_data['Energy'],
            mode='lines+markers',
            name='Energy',
            line=dict(color='green')
        ))
        
        fig_mood.add_trace(go.Scatter(
            x=mood_data['Date'],
            y=mood_data['Stress'],
            mode='lines+markers',
            name='Stress',
            line=dict(color='red')
        ))
        
        fig_mood.update_layout(
            title="Mood, Energy, and Stress Trends (Past 30 Days)",
            xaxis_title="Date",
            yaxis_title="Rating (1-10)",
            height=500
        )
        
        st.plotly_chart(fig_mood, use_container_width=True)
        
        # Mood statistics
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            avg_mood = mood_data['Mood'].mean()
            st.metric("😊 Average Mood", f"{avg_mood:.1f}/10")
        
        with col_stat2:
            avg_energy = mood_data['Energy'].mean()
            st.metric("⚡ Average Energy", f"{avg_energy:.1f}/10")
        
        with col_stat3:
            avg_stress = mood_data['Stress'].mean()
            st.metric("😤 Average Stress", f"{avg_stress:.1f}/10")
        
        with col_stat4:
            good_mood_days = len(mood_data[mood_data['Mood'] >= 7])
            st.metric("😄 Good Mood Days", f"{good_mood_days}/30")
        
        # Mood patterns analysis
        st.subheader("🔍 Mood Patterns Analysis")
        
        # Day of week analysis
        mood_data['DayOfWeek'] = mood_data['Date'].dt.day_name()
        day_mood = mood_data.groupby('DayOfWeek')['Mood'].mean().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        fig_day = px.bar(
            x=day_mood.index,
            y=day_mood.values,
            title="Average Mood by Day of Week",
            labels={'x': 'Day', 'y': 'Average Mood'},
            color=day_mood.values,
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_day, use_container_width=True)
        
        # Insights
        st.subheader("💡 Mood Insights")
        
        best_day = day_mood.idxmax()
        worst_day = day_mood.idxmin()
        
        insights = [
            f"📈 Your best mood day is typically {best_day}",
            f"📉 Your most challenging day is typically {worst_day}",
            f"🎯 Your mood has been {'stable' if mood_data['Mood'].std() < 2 else 'variable'} this month",
            f"⚡ Energy and mood correlation: {'Strong' if mood_data['Mood'].corr(mood_data['Energy']) > 0.7 else 'Moderate' if mood_data['Mood'].corr(mood_data['Energy']) > 0.5 else 'Weak'}"
        ]
        
        for insight in insights:
            st.info(insight)
    
    with tab3:
        st.subheader("🎯 Emotional Wellness Goals")
        
        with st.form("emotional_goals"):
            st.write("**🎯 Set Your Emotional Wellness Goals**")
            
            # Goal categories
            mood_goal = st.selectbox("😊 Mood Goal", [
                "Maintain current mood levels",
                "Increase overall happiness",
                "Reduce mood swings",
                "Better emotional regulation",
                "Increase positive emotions"
            ])
            
            stress_goal = st.selectbox("😤 Stress Management Goal", [
                "Reduce overall stress levels",
                "Better stress coping strategies",
                "Identify stress triggers",
                "Maintain current stress levels",
                "Prevent stress buildup"
            ])
            
            energy_goal = st.selectbox("⚡ Energy Goal", [
                "Increase daily energy levels",
                "More consistent energy throughout day",
                "Better energy management",
                "Reduce energy crashes",
                "Maintain current energy levels"
            ])
            
            # Specific targets
            target_mood = st.slider("🎯 Target average mood level", 1, 10, 7)
            target_stress = st.slider("🎯 Target maximum stress level", 1, 10, 5)
            
            # Action plans
            daily_practices = st.multiselect("🔄 Daily practices you'll commit to", [
                "Morning gratitude", "Evening reflection", "Mindfulness meditation",
                "Regular exercise", "Adequate sleep", "Social connection",
                "Stress management techniques", "Mood tracking"
            ])
            
            weekly_goals = st.multiselect("📅 Weekly emotional wellness activities", [
                "Talk to a friend/family member", "Engage in hobbies",
                "Spend time in nature", "Practice self-care",
                "Review mood patterns", "Try new coping strategies"
            ])
            
            goal_timeline = st.selectbox("⏰ Goal timeline", [
                "1 month", "3 months", "6 months", "1 year"
            ])
            
            success_measures = st.text_area("📊 How will you measure success?")
            
            if st.form_submit_button("🎯 Save Emotional Goals"):
                goals_log = f"Emotional Wellness Goals: Mood goal: {mood_goal}, Stress goal: {stress_goal}, Energy goal: {energy_goal}, Target mood: {target_mood}/10, Target stress: {target_stress}/10, Daily practices: {', '.join(daily_practices)}, Weekly goals: {', '.join(weekly_goals)}, Timeline: {goal_timeline}, Success measures: {success_measures}"
                
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    notes=goals_log
                )
                
                if record_id:
                    st.success("✅ Emotional wellness goals saved!")
                    st.balloons()
                    
                    # Show goal summary
                    st.subheader("📋 Your Emotional Wellness Plan")
                    st.write(f"**🎯 Primary Goals:** {mood_goal}, {stress_goal}, {energy_goal}")
                    st.write(f"**📊 Targets:** Mood {target_mood}/10, Max stress {target_stress}/10")
                    st.write(f"**🔄 Daily Practices:** {', '.join(daily_practices)}")
                    st.write(f"**📅 Weekly Activities:** {', '.join(weekly_goals)}")
                    st.write(f"**⏰ Timeline:** {goal_timeline}")
                else:
                    st.error("❌ Error saving goals")
        
        # Progress tracking
        st.subheader("📈 Goal Progress Tracking")
        
        # Mock progress data
        progress_data = [
            {"goal": "Increase overall happiness", "progress": 65, "target_date": "2024-11-01"},
            {"goal": "Reduce stress levels", "progress": 80, "target_date": "2024-10-15"},
            {"goal": "Better emotional regulation", "progress": 45, "target_date": "2024-12-01"}
        ]
        
        for goal in progress_data:
            col_goal1, col_goal2 = st.columns([3, 1])
            
            with col_goal1:
                st.write(f"**🎯 {goal['goal']}**")
                st.progress(goal['progress'] / 100)
                st.write(f"Progress: {goal['progress']}% (Target: {goal['target_date']})")
            
            with col_goal2:
                if st.button("📝 Update", key=f"update_{goal['goal']}", use_container_width=True):
                    st.info("Goal update form would open here")
            
            st.markdown("---")

if __name__ == "__main__":
    main()
