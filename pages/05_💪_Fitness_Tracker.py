import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import numpy as np
from utils.data_manager import DataManager
from utils.ai_simulator import AISimulator
from utils.styling import add_app_styling

# Initialize components
@st.cache_resource
def init_components():
    return DataManager(), AISimulator()

data_manager, ai_simulator = init_components()

st.set_page_config(
    page_title="Fitness Tracker - HEALTHTECH",
    page_icon="💪",
    layout="wide"
)

def main():
    add_app_styling()

    # Make sure this session state check is at the top of the function
    if 'theme' not in st.session_state:
      st.session_state.theme = "Light"

    add_app_styling(theme=st.session_state.theme)
    st.title("💪 Fitness & Wellness Tracker")
    st.markdown("### Monitor Your Physical Health and Achieve Fitness Goals")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access fitness tracking features")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different fitness features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Health Metrics", 
        "🏃‍♂️ Activity Tracker", 
        "🎯 Goals & Progress", 
        "📈 Analytics", 
        "🏆 Achievements"
    ])
    
    with tab1:
        show_health_metrics()
    
    with tab2:
        show_activity_tracker()
    
    with tab3:
        show_goals_progress()
    
    with tab4:
        show_analytics()
    
    with tab5:
        show_achievements()

def show_health_metrics():
    """Health metrics input and tracking"""
    st.header("📊 Track Your Health Metrics")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Record Today's Metrics")
        
        with st.form("health_metrics_form"):
            # Basic vitals
            st.markdown("**🫀 Vital Signs**")
            
            col_vitals1, col_vitals2 = st.columns(2)
            
            with col_vitals1:
                heart_rate = st.number_input("❤️ Heart Rate (BPM)", min_value=40, max_value=200, value=75)
                blood_pressure_systolic = st.number_input("🩺 Systolic BP", min_value=80, max_value=250, value=120)
                temperature = st.number_input("🌡️ Body Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6, step=0.1)
            
            with col_vitals2:
                resting_hr = st.number_input("😴 Resting Heart Rate", min_value=40, max_value=100, value=65)
                blood_pressure_diastolic = st.number_input("🩺 Diastolic BP", min_value=40, max_value=150, value=80)
                oxygen_saturation = st.number_input("🫁 Oxygen Saturation (%)", min_value=80, max_value=100, value=98)
            
            # Physical measurements
            st.markdown("**📏 Physical Measurements**")
            
            col_physical1, col_physical2 = st.columns(2)
            
            with col_physical1:
                weight = st.number_input("⚖️ Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
                height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
                bmi = round(weight / ((height/100) ** 2), 2) if height > 0 else 0
                st.metric("🧮 BMI", bmi)
            
            with col_physical2:
                waist = st.number_input("📐 Waist Circumference (cm)", min_value=50.0, max_value=200.0, value=80.0, step=0.1)
                body_fat = st.number_input("🏋️‍♂️ Body Fat Percentage", min_value=5.0, max_value=50.0, value=15.0, step=0.1)
                muscle_mass = st.number_input("💪 Muscle Mass (kg)", min_value=10.0, max_value=100.0, value=30.0, step=0.1)
            
            # Activity and wellness
            st.markdown("**🏃‍♂️ Daily Activity**")
            
            col_activity1, col_activity2 = st.columns(2)
            
            with col_activity1:
                steps = st.number_input("👣 Steps Today", min_value=0, max_value=50000, value=5000)
                calories_burned = st.number_input("🔥 Calories Burned", min_value=0, max_value=5000, value=200)
                exercise_minutes = st.number_input("⏱️ Exercise Minutes", min_value=0, max_value=300, value=30)
            
            with col_activity2:
                sleep_hours = st.number_input("😴 Sleep Hours", min_value=0.0, max_value=15.0, value=7.5, step=0.5)
                water_intake = st.number_input("💧 Water Intake (L)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
                stress_level = st.selectbox("😰 Stress Level", ["Low", "Moderate", "High", "Very High"])
            
            # Additional notes
            notes = st.text_area("📝 Additional Notes", 
                                placeholder="Any observations about your health, mood, or physical condition today...")
            
            submit_metrics = st.form_submit_button("💾 Save Metrics", use_container_width=True)
            
            if submit_metrics:
                # Calculate blood pressure reading
                blood_pressure = f"{blood_pressure_systolic}/{blood_pressure_diastolic}"
                
                # Save to health records
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    heart_rate=heart_rate,
                    blood_pressure=blood_pressure,
                    weight=weight,
                    height=height,
                    temperature=temperature,
                    notes=f"Steps: {steps}, Calories: {calories_burned}, Exercise: {exercise_minutes}min, Sleep: {sleep_hours}h, Water: {water_intake}L, Stress: {stress_level}. {notes}"
                )
                
                if record_id:
                    st.success("✅ Health metrics recorded successfully!")
                    
                    # Show health assessment
                    show_health_assessment(bmi, blood_pressure_systolic, blood_pressure_diastolic, heart_rate)
                else:
                    st.error("❌ Error saving metrics. Please try again.")
    
    with col2:
        st.subheader("📊 Today's Summary")
        
        # Get user's latest health record
        user_records = data_manager.get_user_health_records(st.session_state.user_id)
        
        if not user_records.empty:
            latest_record = user_records.iloc[-1]
            
            # Display current metrics
            st.metric("❤️ Heart Rate", f"{latest_record.get('heart_rate', 'N/A')} BPM")
            st.metric("🩺 Blood Pressure", latest_record.get('blood_pressure', 'N/A'))
            st.metric("⚖️ Weight", f"{latest_record.get('weight', 'N/A')} kg")
            st.metric("🌡️ Temperature", f"{latest_record.get('temperature', 'N/A')}°F")
        
        st.subheader("🎯 Health Status")
        
        # Health status indicators
        health_indicators = [
            {"name": "BMI Status", "value": get_bmi_status(bmi if 'bmi' in locals() else 22), "color": get_bmi_color(bmi if 'bmi' in locals() else 22)},
            {"name": "Activity Level", "value": "Moderate", "color": "green"},
            {"name": "Sleep Quality", "value": "Good", "color": "green"},
            {"name": "Hydration", "value": "Adequate", "color": "blue"}
        ]
        
        for indicator in health_indicators:
            st.markdown(f"**{indicator['name']}:** <span style='color:{indicator['color']}'>{indicator['value']}</span>", 
                       unsafe_allow_html=True)
        
        st.subheader("💡 Quick Tips")
        
        tips = [
            "💧 Drink water regularly throughout the day",
            "🚶‍♂️ Take breaks from sitting every hour",
            "😴 Maintain consistent sleep schedule",
            "🥗 Include variety in your meals",
            "📱 Track metrics consistently"
        ]
        
        for tip in tips:
            st.info(tip)

def show_health_assessment(bmi, systolic, diastolic, heart_rate):
    """Show AI-powered health assessment"""
    st.subheader("🤖 AI Health Assessment")
    
    assessments = []
    
    # BMI Assessment
    bmi_status = get_bmi_status(bmi)
    if bmi_status == "Normal":
        assessments.append("✅ Your BMI is in the healthy range")
    elif bmi_status == "Underweight":
        assessments.append("⚠️ Your BMI indicates underweight - consider nutritional consultation")
    elif bmi_status == "Overweight":
        assessments.append("⚠️ Your BMI indicates overweight - consider lifestyle modifications")
    else:
        assessments.append("🚨 Your BMI indicates obesity - recommend medical consultation")
    
    # Blood Pressure Assessment
    if systolic <= 120 and diastolic <= 80:
        assessments.append("✅ Your blood pressure is normal")
    elif systolic <= 139 or diastolic <= 89:
        assessments.append("⚠️ Your blood pressure is elevated - monitor regularly")
    else:
        assessments.append("🚨 Your blood pressure is high - consult healthcare provider")
    
    # Heart Rate Assessment
    if 60 <= heart_rate <= 100:
        assessments.append("✅ Your heart rate is normal")
    elif heart_rate < 60:
        assessments.append("ℹ️ Your heart rate is low - may be normal for athletes")
    else:
        assessments.append("⚠️ Your heart rate is elevated - consider medical evaluation")
    
    for assessment in assessments:
        if "✅" in assessment:
            st.success(assessment)
        elif "⚠️" in assessment:
            st.warning(assessment)
        elif "🚨" in assessment:
            st.error(assessment)
        else:
            st.info(assessment)

def get_bmi_status(bmi):
    """Get BMI status category"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_color(bmi):
    """Get color for BMI status"""
    status = get_bmi_status(bmi)
    colors = {"Normal": "green", "Underweight": "blue", "Overweight": "orange", "Obese": "red"}
    return colors.get(status, "gray")

def show_activity_tracker():
    """Activity and exercise tracking"""
    st.header("🏃‍♂️ Activity & Exercise Tracker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Log Your Activities")
        
        # Activity logging form
        with st.form("activity_form"):
            # Exercise type selection
            exercise_categories = {
                "🏃‍♂️ Cardio": ["Running", "Walking", "Cycling", "Swimming", "Dancing", "Aerobics"],
                "🏋️‍♂️ Strength": ["Weight Training", "Bodyweight", "Resistance Bands", "CrossFit"],
                "🧘‍♀️ Flexibility": ["Yoga", "Stretching", "Pilates", "Tai Chi"],
                "🏊‍♂️ Sports": ["Football", "Basketball", "Tennis", "Badminton", "Cricket"],
                "🚶‍♂️ Daily": ["Household Chores", "Gardening", "Stairs Climbing", "Walking"]
            }
            
            category = st.selectbox("🎯 Activity Category", list(exercise_categories.keys()))
            activity = st.selectbox("🏃‍♂️ Specific Activity", exercise_categories[category])
            
            col_details1, col_details2 = st.columns(2)
            
            with col_details1:
                duration = st.number_input("⏱️ Duration (minutes)", min_value=1, max_value=480, value=30)
                intensity = st.selectbox("🔥 Intensity", ["Low", "Moderate", "High", "Very High"])
            
            with col_details2:
                calories = st.number_input("🔥 Calories Burned (estimated)", min_value=10, max_value=2000, value=150)
                distance = st.number_input("📏 Distance (km, if applicable)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
            
            # Activity details
            st.markdown("**🎯 Activity Details**")
            
            col_metrics1, col_metrics2 = st.columns(2)
            
            with col_metrics1:
                heart_rate_avg = st.number_input("❤️ Average Heart Rate", min_value=60, max_value=220, value=120)
                perceived_effort = st.selectbox("💪 Perceived Effort (1-10)", list(range(1, 11)), index=4)
            
            with col_metrics2:
                weather = st.selectbox("🌤️ Weather Conditions", ["Indoor", "Sunny", "Cloudy", "Rainy", "Hot", "Cold"])
                mood_after = st.selectbox("😊 Mood After Exercise", ["Energized", "Tired", "Satisfied", "Frustrated", "Neutral"])
            
            # Exercise notes
            exercise_notes = st.text_area("📝 Exercise Notes", 
                                        placeholder="How did you feel? Any achievements or challenges?")
            
            log_activity = st.form_submit_button("📊 Log Activity", use_container_width=True)
            
            if log_activity:
                # Save activity log (would typically save to a separate activities table)
                activity_data = {
                    "user_id": st.session_state.user_id,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "category": category,
                    "activity": activity,
                    "duration": duration,
                    "intensity": intensity,
                    "calories": calories,
                    "distance": distance,
                    "heart_rate": heart_rate_avg,
                    "effort": perceived_effort,
                    "weather": weather,
                    "mood": mood_after,
                    "notes": exercise_notes
                }
                
                # For demo, save as health record with activity notes
                notes = f"Activity: {activity} ({duration}min, {intensity} intensity, {calories} cal)"
                if exercise_notes:
                    notes += f" - {exercise_notes}"
                
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    heart_rate=heart_rate_avg,
                    notes=notes
                )
                
                if record_id:
                    st.success("✅ Activity logged successfully!")
                    
                    # Show activity summary
                    show_activity_summary(activity_data)
                else:
                    st.error("❌ Error logging activity. Please try again.")
        
        st.markdown("---")
        
        # Quick activity buttons
        st.subheader("⚡ Quick Log Activities")
        
        quick_activities = [
            {"name": "🚶‍♂️ 10-min Walk", "duration": 10, "calories": 40},
            {"name": "🏃‍♂️ 20-min Run", "duration": 20, "calories": 200},
            {"name": "🧘‍♀️ 15-min Yoga", "duration": 15, "calories": 60},
            {"name": "🏋️‍♂️ 30-min Weights", "duration": 30, "calories": 180},
            {"name": "🚴‍♂️ 45-min Cycling", "duration": 45, "calories": 350},
            {"name": "🏊‍♂️ 30-min Swimming", "duration": 30, "calories": 300}
        ]
        
        cols = st.columns(3)
        for i, activity in enumerate(quick_activities):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(activity["name"], key=f"quick_{i}", use_container_width=True):
                    # Quick log activity
                    notes = f"Quick Log: {activity['name']} ({activity['duration']}min, {activity['calories']} cal)"
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=notes
                    )
                    if record_id:
                        st.success(f"✅ {activity['name']} logged!")
    
    with col2:
        st.subheader("📊 Today's Activity Summary")
        
        # Mock today's activity data
        today_stats = {
            "Total Steps": "8,456",
            "Active Minutes": "45",
            "Calories Burned": "320",
            "Distance": "6.2 km"
        }
        
        for stat, value in today_stats.items():
            st.metric(stat, value)
        
        st.subheader("🎯 Activity Goals")
        
        # Activity goals with progress
        goals = [
            {"name": "Daily Steps", "target": 10000, "current": 8456},
            {"name": "Exercise Minutes", "target": 60, "current": 45},
            {"name": "Calories Burned", "target": 500, "current": 320}
        ]
        
        for goal in goals:
            progress = min(goal["current"] / goal["target"] * 100, 100)
            st.progress(progress / 100)
            st.write(f"**{goal['name']}:** {goal['current']}/{goal['target']} ({progress:.0f}%)")
        
        st.subheader("🏆 Weekly Achievements")
        
        achievements = [
            "🎯 Met daily step goal 5/7 days",
            "💪 Completed 4 strength workouts",
            "🧘‍♀️ 30-day yoga streak!",
            "🏃‍♂️ New personal best: 5km run"
        ]
        
        for achievement in achievements:
            st.success(achievement)
        
        st.subheader("📈 Activity Trends")
        
        # Simple activity trend
        trend_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Minutes': [30, 45, 0, 60, 30, 90, 45]
        })
        
        fig = px.bar(trend_data, x='Day', y='Minutes', title="This Week's Exercise Minutes")
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)

def show_activity_summary(activity_data):
    """Show summary of logged activity"""
    st.subheader("📊 Activity Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⏱️ Duration", f"{activity_data['duration']} min")
    
    with col2:
        st.metric("🔥 Calories", f"{activity_data['calories']} cal")
    
    with col3:
        st.metric("💪 Effort Level", f"{activity_data['effort']}/10")
    
    # Calorie burn comparison
    st.info(f"💡 Great job! You burned approximately {activity_data['calories']} calories, equivalent to:")
    
    calorie_equivalents = [
        f"🍎 {activity_data['calories'] // 80} medium apples",
        f"🍫 {activity_data['calories'] // 150} chocolate bars",
        f"🥤 {activity_data['calories'] // 140} cans of soda"
    ]
    
    for equivalent in calorie_equivalents:
        st.write(f"• {equivalent}")

def show_goals_progress():
    """Fitness goals setting and progress tracking"""
    st.header("🎯 Fitness Goals & Progress")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Goal setting
        st.subheader("🎯 Set Your Fitness Goals")
        
        goal_types = st.multiselect(
            "Select goal types:",
            ["Weight Management", "Cardiovascular Fitness", "Strength Building", "Flexibility", "Endurance", "General Wellness"]
        )
        
        if goal_types:
            for goal_type in goal_types:
                with st.expander(f"🎯 {goal_type} Goals"):
                    create_goal_form(goal_type)
        
        st.markdown("---")
        
        # Current goals progress
        st.subheader("📊 Current Goals Progress")
        
        # Mock goals data
        current_goals = [
            {
                "name": "Lose 5kg in 3 months",
                "type": "Weight Management",
                "target": 5,
                "current": 2.5,
                "unit": "kg",
                "deadline": "2024-11-30",
                "status": "On Track"
            },
            {
                "name": "Run 5km under 25 minutes",
                "type": "Cardiovascular Fitness", 
                "target": 25,
                "current": 28,
                "unit": "minutes",
                "deadline": "2024-10-15",
                "status": "Needs Improvement"
            },
            {
                "name": "Do 50 push-ups continuously",
                "type": "Strength Building",
                "target": 50,
                "current": 30,
                "unit": "reps",
                "deadline": "2024-12-01",
                "status": "On Track"
            }
        ]
        
        for goal in current_goals:
            show_goal_progress(goal)
    
    with col2:
        st.subheader("🏆 Goal Achievements")
        
        # Completed goals
        completed_goals = [
            "✅ Lost 2kg in first month",
            "✅ Exercised 5 days/week for 4 weeks",
            "✅ Completed first 5km run",
            "✅ Maintained daily step goal for 30 days"
        ]
        
        for goal in completed_goals:
            st.success(goal)
        
        st.subheader("📅 Goal Timeline")
        
        # Timeline view
        timeline_goals = [
            {"goal": "5km run target", "date": "Oct 15", "status": "upcoming"},
            {"goal": "Weight loss milestone", "date": "Nov 30", "status": "in_progress"},
            {"goal": "Push-up challenge", "date": "Dec 01", "status": "in_progress"}
        ]
        
        for tgoal in timeline_goals:
            color = "orange" if tgoal["status"] == "upcoming" else "blue"
            st.markdown(f"**{tgoal['date']}:** <span style='color:{color}'>{tgoal['goal']}</span>", 
                       unsafe_allow_html=True)
        
        st.subheader("💡 Goal Tips")
        
        tips = [
            "🎯 Set SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)",
            "📊 Track progress regularly",
            "🔄 Adjust goals based on progress",
            "🎉 Celebrate small victories",
            "👥 Share goals with friends for accountability"
        ]
        
        for tip in tips:
            st.info(tip)

def create_goal_form(goal_type):
    """Create goal setting form for specific goal type"""
    with st.form(f"goal_form_{goal_type}"):
        goal_templates = {
            "Weight Management": {
                "options": ["Lose weight", "Gain weight", "Maintain weight"],
                "units": ["kg", "lbs"]
            },
            "Cardiovascular Fitness": {
                "options": ["Improve running time", "Increase distance", "Lower resting heart rate"],
                "units": ["minutes", "km", "BPM"]
            },
            "Strength Building": {
                "options": ["Increase reps", "Increase weight", "New exercises"],
                "units": ["reps", "kg", "exercises"]
            },
            "Flexibility": {
                "options": ["Touch toes", "Improve range of motion", "Hold poses longer"],
                "units": ["cm", "degrees", "seconds"]
            },
            "Endurance": {
                "options": ["Increase workout duration", "Reduce fatigue", "Improve stamina"],
                "units": ["minutes", "level", "rating"]
            },
            "General Wellness": {
                "options": ["Exercise frequency", "Sleep quality", "Stress reduction"],
                "units": ["days/week", "hours", "level"]
            }
        }
        
        template = goal_templates.get(goal_type, {"options": ["Custom goal"], "units": ["units"]})
        
        goal_description = st.selectbox("Goal Description", template["options"])
        target_value = st.number_input("Target Value", min_value=0.1, value=1.0)
        target_unit = st.selectbox("Unit", template["units"])
        deadline = st.date_input("Target Date", min_value=date.today(), value=date.today() + timedelta(days=90))
        
        if st.form_submit_button(f"Set {goal_type} Goal"):
            st.success(f"✅ Goal set: {goal_description} - {target_value} {target_unit} by {deadline}")

def show_goal_progress(goal):
    """Display individual goal progress"""
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**🎯 {goal['name']}**")
            st.write(f"Type: {goal['type']}")
            
            # Progress bar
            if goal['type'] == "Cardiovascular Fitness" and goal['name'].startswith("Run"):
                # For time-based goals, progress is inverse
                progress = max(0, (goal['current'] - goal['target']) / goal['current'] * 100) if goal['current'] > goal['target'] else 100
            else:
                progress = min(goal['current'] / goal['target'] * 100, 100)
            
            st.progress(progress / 100)
            st.write(f"Progress: {goal['current']}/{goal['target']} {goal['unit']} ({progress:.0f}%)")
        
        with col2:
            st.metric("Deadline", goal['deadline'])
            
            # Days remaining
            deadline_date = datetime.strptime(goal['deadline'], "%Y-%m-%d").date()
            days_remaining = (deadline_date - date.today()).days
            st.write(f"📅 {days_remaining} days left")
        
        with col3:
            status_colors = {"On Track": "green", "Needs Improvement": "orange", "At Risk": "red"}
            status_color = status_colors.get(goal['status'], "gray")
            
            st.markdown(f"**Status:** <span style='color:{status_color}'>{goal['status']}</span>", 
                       unsafe_allow_html=True)
            
            if st.button("📝 Update Progress", key=f"update_{goal['name']}"):
                st.info("Update progress form would open here")
        
        st.markdown("---")

def show_analytics():
    """Fitness analytics and insights"""
    st.header("📈 Fitness Analytics & Insights")
    
    # Get user's health records for analytics
    user_records = data_manager.get_user_health_records(st.session_state.user_id)
    
    if not user_records.empty and len(user_records) > 1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Health Metrics Trends")
            
            # Create multi-metric chart
            fig = go.Figure()
            
            if 'heart_rate' in user_records.columns and user_records['heart_rate'].notna().any():
                fig.add_trace(go.Scatter(
                    x=user_records['date'],
                    y=user_records['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate (BPM)',
                    line=dict(color='red')
                ))
            
            if 'weight' in user_records.columns and user_records['weight'].notna().any():
                fig.add_trace(go.Scatter(
                    x=user_records['date'],
                    y=user_records['weight'],
                    mode='lines+markers',
                    name='Weight (kg)',
                    yaxis='y2',
                    line=dict(color='blue')
                ))
            
            fig.update_layout(
                title="Health Metrics Over Time",
                xaxis_title="Date",
                yaxis_title="Heart Rate (BPM)",
                yaxis2=dict(
                    title="Weight (kg)",
                    overlaying='y',
                    side='right'
                ),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Fitness Insights")
            
            # AI-powered insights
            insights = generate_fitness_insights(user_records)
            
            for insight in insights:
                if "improvement" in insight.lower():
                    st.success(f"✅ {insight}")
                elif "concern" in insight.lower() or "high" in insight.lower():
                    st.warning(f"⚠️ {insight}")
                else:
                    st.info(f"💡 {insight}")
        
        # Weekly summary
        st.subheader("📅 Weekly Summary")
        
        col_week1, col_week2, col_week3, col_week4 = st.columns(4)
        
        with col_week1:
            st.metric("📊 Avg Heart Rate", "78 BPM", delta="-2")
        
        with col_week2:
            st.metric("⚖️ Weight Change", "-0.3 kg", delta="-0.3")
        
        with col_week3:
            st.metric("🏃‍♂️ Total Exercise", "180 min", delta="+30")
        
        with col_week4:
            st.metric("👣 Avg Daily Steps", "8,456", delta="+1,200")
        
        # Monthly comparison
        st.subheader("📊 Monthly Comparison")
        
        monthly_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Avg Weight': [72, 71.5, 71, 70.5, 70, 69.5],
            'Exercise Hours': [8, 12, 15, 18, 20, 22],
            'Avg Heart Rate': [80, 78, 76, 75, 74, 73]
        })
        
        # Weight trend
        fig_weight = px.line(monthly_data, x='Month', y='Avg Weight', 
                           title="Weight Trend", markers=True)
        st.plotly_chart(fig_weight, use_container_width=True)
        
        # Exercise hours
        fig_exercise = px.bar(monthly_data, x='Month', y='Exercise Hours',
                            title="Monthly Exercise Hours")
        st.plotly_chart(fig_exercise, use_container_width=True)
        
    else:
        st.info("📊 Not enough data for analytics. Start tracking your health metrics to see trends and insights!")
        
        # Show sample analytics
        st.subheader("📈 Sample Analytics (When You Have Data)")
        
        sample_data = pd.DataFrame({
            'Date': pd.date_range('2024-08-01', periods=30, freq='D'),
            'Weight': np.random.normal(70, 1, 30),
            'Heart_Rate': np.random.normal(75, 5, 30),
            'Steps': np.random.normal(8000, 2000, 30)
        })
        
        fig_sample = px.line(sample_data, x='Date', y='Weight', 
                           title="Sample Weight Trend")
        st.plotly_chart(fig_sample, use_container_width=True)

def generate_fitness_insights(health_records):
    """Generate AI-powered fitness insights"""
    insights = []
    
    if len(health_records) < 3:
        return ["Start tracking consistently to get personalized insights"]
    
    # Weight trend analysis
    if 'weight' in health_records.columns and health_records['weight'].notna().sum() > 2:
        recent_weights = health_records['weight'].dropna().tail(5)
        if len(recent_weights) > 1:
            weight_trend = recent_weights.iloc[-1] - recent_weights.iloc[0]
            if weight_trend < -1:
                insights.append("Great improvement in weight management! You've lost weight consistently.")
            elif weight_trend > 1:
                insights.append("Weight has increased recently. Consider reviewing diet and exercise routine.")
            else:
                insights.append("Weight is stable, which is good for maintenance goals.")
    
    # Heart rate analysis
    if 'heart_rate' in health_records.columns and health_records['heart_rate'].notna().sum() > 2:
        recent_hr = health_records['heart_rate'].dropna().tail(5).mean()
        if recent_hr < 70:
            insights.append("Excellent cardiovascular fitness indicated by low resting heart rate.")
        elif recent_hr < 80:
            insights.append("Good cardiovascular health. Continue regular exercise.")
        else:
            insights.append("Consider increasing cardiovascular exercise to improve heart health.")
    
    # Activity consistency
    total_records = len(health_records)
    if total_records > 7:
        insights.append(f"Great consistency! You've tracked health data {total_records} times.")
    
    # General recommendations
    insights.extend([
        "Maintain regular tracking for better health insights",
        "Consider setting specific fitness goals for motivation",
        "Remember that small consistent changes lead to big results"
    ])
    
    return insights

def show_achievements():
    """Display fitness achievements and badges"""
    st.header("🏆 Achievements & Badges")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏅 Your Achievements")
        
        # Achievement categories
        achievement_categories = {
            "🏃‍♂️ Activity Milestones": [
                {"name": "First Steps", "description": "Logged your first activity", "earned": True, "date": "2024-08-01"},
                {"name": "Consistency King", "description": "7 days of activity logging", "earned": True, "date": "2024-08-07"},
                {"name": "Century Club", "description": "100 total activities logged", "earned": False, "progress": "45/100"},
                {"name": "Marathon Prep", "description": "Run 42km in total", "earned": False, "progress": "15.2/42"},
            ],
            "💪 Strength Achievements": [
                {"name": "Push-up Pro", "description": "Complete 50 push-ups", "earned": True, "date": "2024-08-15"},
                {"name": "Weight Warrior", "description": "Strength training 20 sessions", "earned": False, "progress": "12/20"},
                {"name": "Muscle Builder", "description": "Gain 2kg muscle mass", "earned": False, "progress": "0.8/2"},
            ],
            "🎯 Goal Achievements": [
                {"name": "Goal Setter", "description": "Set your first fitness goal", "earned": True, "date": "2024-08-01"},
                {"name": "Goal Crusher", "description": "Complete 3 fitness goals", "earned": False, "progress": "1/3"},
                {"name": "Consistency Master", "description": "Meet weekly goals for 4 weeks", "earned": False, "progress": "2/4"},
            ],
            "📊 Tracking Achievements": [
                {"name": "Data Devotee", "description": "Track health metrics for 30 days", "earned": False, "progress": "18/30"},
                {"name": "Metric Master", "description": "Log all health metrics 50 times", "earned": False, "progress": "23/50"},
                {"name": "Trend Tracker", "description": "Identify 3 health trends", "earned": True, "date": "2024-08-20"},
            ]
        }
        
        for category, achievements in achievement_categories.items():
            with st.expander(category, expanded=True):
                for achievement in achievements:
                    show_achievement_badge(achievement)
    
    with col2:
        st.subheader("📊 Achievement Stats")
        
        # Calculate achievement statistics
        total_achievements = sum(len(achievements) for achievements in achievement_categories.values())
        earned_achievements = sum(1 for achievements in achievement_categories.values() 
                                for achievement in achievements if achievement['earned'])
        
        st.metric("🏆 Total Badges", f"{earned_achievements}/{total_achievements}")
        st.metric("📈 Completion Rate", f"{(earned_achievements/total_achievements*100):.0f}%")
        
        # Achievement progress
        progress = earned_achievements / total_achievements
        st.progress(progress)
        
        st.subheader("🎯 Next Targets")
        
        # Show closest achievements
        next_targets = [
            "🏃‍♂️ 55 more activities for Century Club",
            "💪 8 more strength sessions for Weight Warrior", 
            "📊 12 more days of tracking for Data Devotee"
        ]
        
        for target in next_targets:
            st.info(target)
        
        st.subheader("🌟 Recent Achievements")
        
        recent = [
            {"badge": "🏃‍♂️ Trend Tracker", "date": "Aug 20"},
            {"badge": "💪 Push-up Pro", "date": "Aug 15"},
            {"badge": "🏃‍♂️ Consistency King", "date": "Aug 07"},
        ]
        
        for item in recent:
            st.success(f"{item['badge']} - {item['date']}")
        
        st.subheader("💡 Achievement Tips")
        
        tips = [
            "🎯 Focus on one achievement at a time",
            "📊 Consistent tracking unlocks more badges",
            "💪 Challenge yourself with harder goals",
            "🏆 Celebrate every achievement earned"
        ]
        
        for tip in tips:
            st.info(tip)

def show_achievement_badge(achievement):
    """Display individual achievement badge"""
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if achievement['earned']:
                st.markdown("🏆")
            else:
                st.markdown("⭕")
        
        with col2:
            st.markdown(f"**{achievement['name']}**")
            st.write(achievement['description'])
            
            if achievement['earned']:
                st.success(f"✅ Earned on {achievement['date']}")
            else:
                st.info(f"📊 Progress: {achievement['progress']}")
        
        with col3:
            if achievement['earned']:
                st.markdown("✅")
            else:
                # Calculate progress percentage
                if 'progress' in achievement:
                    current, total = map(int, achievement['progress'].split('/'))
                    progress_pct = (current / total) * 100
                    st.metric("Progress", f"{progress_pct:.0f}%")
        
        st.markdown("---")

if __name__ == "__main__":
    main()
