import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from utils.data_manager import DataManager

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Health Records - HEALTHTECH",
    page_icon="📋",
    layout="wide"
)

def main():
    st.title("📋 Health Records Management")
    st.markdown("### Secure Digital Storage of Your Medical Information")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access your health records")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different health record features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Health Overview", 
        "📝 Add Records", 
        "📈 Health Trends", 
        "📄 Medical Reports", 
        "🔒 Privacy & Sharing"
    ])
    
    with tab1:
        show_health_overview()
    
    with tab2:
        show_add_records()
    
    with tab3:
        show_health_trends()
    
    with tab4:
        show_medical_reports()
    
    with tab5:
        show_privacy_sharing()

def show_health_overview():
    """Display comprehensive health overview"""
    st.header("📊 Health Records Overview")
    
    user_id = st.session_state.user_id
    user_data = st.session_state.user_data
    
    # Get user's health records
    health_records = data_manager.get_user_health_records(user_id)
    appointments = data_manager.get_user_appointments(user_id)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total Records", len(health_records))
    
    with col2:
        st.metric("👨‍⚕️ Consultations", len(appointments))
    
    with col3:
        last_update = health_records['date'].max() if not health_records.empty else "Never"
        st.metric("📅 Last Updated", last_update)
    
    with col4:
        days_tracked = len(health_records['date'].unique()) if not health_records.empty else 0
        st.metric("📊 Days Tracked", days_tracked)
    
    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📈 Recent Health Metrics")
        
        if not health_records.empty:
            # Display recent records in a table
            recent_records = health_records.tail(10).copy()
            
            # Format the display
            display_records = recent_records[['date', 'heart_rate', 'blood_pressure', 'weight', 'temperature']].copy()
            display_records.columns = ['Date', 'Heart Rate', 'Blood Pressure', 'Weight (kg)', 'Temperature (°F)']
            
            st.dataframe(display_records, use_container_width=True)
            
            # Latest vital signs
            if not recent_records.empty:
                latest = recent_records.iloc[-1]
                
                st.subheader("🔍 Latest Vital Signs")
                
                col_vital1, col_vital2, col_vital3, col_vital4 = st.columns(4)
                
                with col_vital1:
                    if pd.notna(latest.get('heart_rate')):
                        hr_status = get_heart_rate_status(latest['heart_rate'])
                        st.metric("❤️ Heart Rate", f"{latest['heart_rate']} BPM", help=hr_status)
                
                with col_vital2:
                    if pd.notna(latest.get('blood_pressure')):
                        bp_status = get_blood_pressure_status(latest['blood_pressure'])
                        st.metric("🩺 Blood Pressure", latest['blood_pressure'], help=bp_status)
                
                with col_vital3:
                    if pd.notna(latest.get('weight')):
                        st.metric("⚖️ Weight", f"{latest['weight']} kg")
                
                with col_vital4:
                    if pd.notna(latest.get('temperature')):
                        temp_status = get_temperature_status(latest['temperature'])
                        st.metric("🌡️ Temperature", f"{latest['temperature']}°F", help=temp_status)
        
        else:
            st.info("📝 No health records found. Start tracking your health metrics!")
            
            if st.button("➕ Add Your First Record", use_container_width=True):
                st.info("Please use the 'Add Records' tab to start tracking")
    
    with col_right:
        st.subheader("👤 Profile Summary")
        
        # User profile information
        profile_info = {
            "Name": user_data['name'],
            "Age": f"{user_data['age']} years",
            "Gender": user_data['gender'],
            "Blood Group": user_data['blood_group'],
            "Email": user_data['email'],
            "Phone": user_data['phone']
        }
        
        for key, value in profile_info.items():
            st.write(f"**{key}:** {value}")
        
        st.subheader("🏥 Medical Summary")
        
        # Calculate health insights
        if not health_records.empty:
            insights = calculate_health_insights(health_records)
            
            for insight in insights:
                if "Normal" in insight or "Good" in insight:
                    st.success(f"✅ {insight}")
                elif "Monitor" in insight or "Elevated" in insight:
                    st.warning(f"⚠️ {insight}")
                else:
                    st.info(f"ℹ️ {insight}")
        else:
            st.info("Start tracking to see health insights")
        
        st.subheader("📅 Upcoming")
        
        # Show upcoming appointments
        if not appointments.empty:
            today = date.today()
            upcoming = appointments[pd.to_datetime(appointments['date']).dt.date >= today]
            
            if not upcoming.empty:
                next_appointment = upcoming.iloc[0]
                st.info(f"👨‍⚕️ **Next Appointment**\n{next_appointment['doctor_name']} on {next_appointment['date']}")
            else:
                st.info("No upcoming appointments")
        else:
            st.info("No appointments scheduled")

def get_heart_rate_status(heart_rate):
    """Get heart rate status interpretation"""
    if heart_rate < 60:
        return "Below normal range (Bradycardia)"
    elif heart_rate <= 100:
        return "Normal resting heart rate"
    else:
        return "Above normal range (Tachycardia)"

def get_blood_pressure_status(bp_reading):
    """Get blood pressure status interpretation"""
    try:
        systolic, diastolic = map(int, bp_reading.split('/'))
        
        if systolic < 120 and diastolic < 80:
            return "Normal blood pressure"
        elif systolic < 130 and diastolic < 80:
            return "Elevated blood pressure"
        elif systolic < 140 or diastolic < 90:
            return "Stage 1 Hypertension"
        else:
            return "Stage 2 Hypertension"
    except:
        return "Unable to interpret reading"

def get_temperature_status(temperature):
    """Get temperature status interpretation"""
    if temperature < 97.0:
        return "Below normal (Hypothermia)"
    elif temperature <= 99.5:
        return "Normal body temperature"
    elif temperature <= 100.4:
        return "Low-grade fever"
    else:
        return "High fever - seek medical attention"

def calculate_health_insights(health_records):
    """Calculate health insights from records"""
    insights = []
    
    # Heart rate analysis
    if 'heart_rate' in health_records.columns and health_records['heart_rate'].notna().any():
        avg_hr = health_records['heart_rate'].dropna().mean()
        if 60 <= avg_hr <= 100:
            insights.append("Heart rate is in normal range")
        else:
            insights.append("Heart rate requires monitoring")
    
    # Weight trend
    if 'weight' in health_records.columns and health_records['weight'].notna().sum() > 2:
        weight_series = health_records['weight'].dropna()
        if len(weight_series) > 1:
            weight_change = weight_series.iloc[-1] - weight_series.iloc[0]
            if abs(weight_change) < 1:
                insights.append("Weight is stable")
            elif weight_change > 2:
                insights.append("Weight gain trend detected")
            else:
                insights.append("Weight loss trend detected")
    
    # Tracking consistency
    total_days = len(health_records)
    if total_days > 7:
        insights.append("Good tracking consistency")
    elif total_days > 0:
        insights.append("Start tracking more regularly")
    
    return insights if insights else ["Start tracking to see health insights"]

def show_add_records():
    """Add new health records"""
    st.header("📝 Add Health Records")
    
    tab1, tab2, tab3 = st.tabs(["📊 Daily Metrics", "💊 Medication Log", "🏥 Visit Records"])
    
    with tab1:
        st.subheader("📊 Record Daily Health Metrics")
        
        with st.form("daily_metrics_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🫀 Vital Signs**")
                heart_rate = st.number_input("❤️ Heart Rate (BPM)", min_value=40, max_value=220, value=None)
                
                bp_systolic = st.number_input("🩺 Systolic BP", min_value=70, max_value=250, value=None)
                bp_diastolic = st.number_input("🩺 Diastolic BP", min_value=40, max_value=150, value=None)
                
                temperature = st.number_input("🌡️ Temperature (°F)", min_value=95.0, max_value=110.0, value=None, step=0.1)
                
                respiratory_rate = st.number_input("🫁 Respiratory Rate (breaths/min)", min_value=8, max_value=40, value=None)
            
            with col2:
                st.markdown("**📏 Physical Measurements**")
                weight = st.number_input("⚖️ Weight (kg)", min_value=20.0, max_value=300.0, value=None, step=0.1)
                
                height = st.number_input("📏 Height (cm)", min_value=100.0, max_value=250.0, value=None, step=0.1)
                
                if weight and height:
                    bmi = round(weight / ((height/100) ** 2), 2)
                    st.metric("🧮 BMI", bmi)
                
                blood_glucose = st.number_input("🍯 Blood Glucose (mg/dL)", min_value=50, max_value=500, value=None)
                
                oxygen_saturation = st.number_input("🫁 Oxygen Saturation (%)", min_value=80, max_value=100, value=None)
            
            # Symptoms and notes
            st.markdown("**📝 Additional Information**")
            
            symptoms = st.multiselect("🤒 Symptoms (if any)", [
                "Headache", "Fever", "Cough", "Fatigue", "Nausea", "Dizziness",
                "Chest pain", "Shortness of breath", "Stomach pain", "Joint pain",
                "Sleep issues", "Stress", "Other"
            ])
            
            mood = st.selectbox("😊 Mood/Energy Level", [
                "Excellent", "Good", "Average", "Poor", "Very Poor"
            ])
            
            notes = st.text_area("📝 Additional Notes", 
                                placeholder="Any observations, medications taken, activities, etc.")
            
            record_date = st.date_input("📅 Record Date", value=date.today())
            
            submit_metrics = st.form_submit_button("💾 Save Health Record", use_container_width=True)
            
            if submit_metrics:
                # Create blood pressure reading
                blood_pressure = None
                if bp_systolic and bp_diastolic:
                    blood_pressure = f"{bp_systolic}/{bp_diastolic}"
                
                # Compile notes
                full_notes = notes or ""
                if symptoms:
                    full_notes += f" Symptoms: {', '.join(symptoms)}."
                if mood:
                    full_notes += f" Mood: {mood}."
                if respiratory_rate:
                    full_notes += f" Respiratory Rate: {respiratory_rate}/min."
                if blood_glucose:
                    full_notes += f" Blood Glucose: {blood_glucose} mg/dL."
                if oxygen_saturation:
                    full_notes += f" Oxygen Saturation: {oxygen_saturation}%."
                
                # Save record
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    heart_rate=heart_rate,
                    blood_pressure=blood_pressure,
                    weight=weight,
                    height=height,
                    temperature=temperature,
                    notes=full_notes
                )
                
                if record_id:
                    st.success("✅ Health record saved successfully!")
                    
                    # Show health assessment
                    if any([heart_rate, blood_pressure, temperature]):
                        show_quick_assessment(heart_rate, blood_pressure, temperature)
                else:
                    st.error("❌ Error saving health record. Please try again.")
    
    with tab2:
        st.subheader("💊 Medication Log")
        
        with st.form("medication_log_form"):
            medication_name = st.text_input("💊 Medication Name")
            
            col_med1, col_med2 = st.columns(2)
            
            with col_med1:
                dosage = st.text_input("📏 Dosage", placeholder="e.g., 500mg, 2 tablets")
                frequency = st.selectbox("⏰ Frequency", [
                    "Once daily", "Twice daily", "Three times daily", "Four times daily",
                    "Every 6 hours", "Every 8 hours", "Every 12 hours", "As needed"
                ])
            
            with col_med2:
                time_taken = st.time_input("🕐 Time Taken")
                taken_with_food = st.selectbox("🍽️ Taken with food?", ["Yes", "No", "Before meals", "After meals"])
            
            purpose = st.text_input("🎯 Purpose/Condition", placeholder="What is this medication for?")
            
            side_effects = st.text_area("⚠️ Side Effects (if any)", 
                                      placeholder="Any side effects experienced")
            
            effectiveness = st.selectbox("📊 Effectiveness", [
                "Very effective", "Effective", "Somewhat effective", "Not effective", "Too early to tell"
            ])
            
            med_notes = st.text_area("📝 Additional Notes")
            
            if st.form_submit_button("💾 Log Medication", use_container_width=True):
                if medication_name:
                    # Create medication log entry
                    med_log = f"Medication: {medication_name} {dosage}, {frequency} at {time_taken}, {taken_with_food} food. Purpose: {purpose}. Effectiveness: {effectiveness}."
                    if side_effects:
                        med_log += f" Side effects: {side_effects}."
                    if med_notes:
                        med_log += f" Notes: {med_notes}."
                    
                    # Save as health record
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=med_log
                    )
                    
                    if record_id:
                        st.success("✅ Medication log saved successfully!")
                    else:
                        st.error("❌ Error saving medication log")
                else:
                    st.error("❌ Please enter medication name")
    
    with tab3:
        st.subheader("🏥 Medical Visit Records")
        
        with st.form("visit_record_form"):
            visit_type = st.selectbox("🏥 Visit Type", [
                "General Consultation", "Specialist Consultation", "Emergency Visit",
                "Lab Tests", "Imaging", "Procedure", "Surgery", "Follow-up", "Vaccination"
            ])
            
            col_visit1, col_visit2 = st.columns(2)
            
            with col_visit1:
                visit_date = st.date_input("📅 Visit Date")
                doctor_name = st.text_input("👨‍⚕️ Doctor/Provider Name")
                facility_name = st.text_input("🏥 Facility Name")
            
            with col_visit2:
                specialty = st.text_input("🩺 Medical Specialty")
                visit_reason = st.text_input("🎯 Reason for Visit")
                duration = st.number_input("⏰ Duration (minutes)", min_value=5, max_value=480, value=30)
            
            # Visit details
            chief_complaint = st.text_area("📝 Chief Complaint/Symptoms")
            
            diagnosis = st.text_area("🔍 Diagnosis/Assessment")
            
            treatment_plan = st.text_area("💊 Treatment Plan/Recommendations")
            
            prescriptions = st.text_area("💊 Prescriptions", 
                                       placeholder="List medications prescribed")
            
            follow_up = st.text_area("📅 Follow-up Instructions")
            
            test_results = st.text_area("🧪 Test Results (if any)")
            
            visit_cost = st.number_input("💰 Visit Cost (₹)", min_value=0.0, value=0.0)
            
            visit_notes = st.text_area("📝 Additional Notes")
            
            if st.form_submit_button("💾 Save Visit Record", use_container_width=True):
                if doctor_name and visit_reason:
                    # Create comprehensive visit record
                    visit_record = f"Medical Visit: {visit_type} on {visit_date} with {doctor_name} at {facility_name}. "
                    visit_record += f"Specialty: {specialty}. Reason: {visit_reason}. Duration: {duration}min. "
                    
                    if chief_complaint:
                        visit_record += f"Complaint: {chief_complaint}. "
                    if diagnosis:
                        visit_record += f"Diagnosis: {diagnosis}. "
                    if treatment_plan:
                        visit_record += f"Treatment: {treatment_plan}. "
                    if prescriptions:
                        visit_record += f"Prescriptions: {prescriptions}. "
                    if follow_up:
                        visit_record += f"Follow-up: {follow_up}. "
                    if test_results:
                        visit_record += f"Results: {test_results}. "
                    if visit_cost > 0:
                        visit_record += f"Cost: ₹{visit_cost}. "
                    if visit_notes:
                        visit_record += f"Notes: {visit_notes}."
                    
                    # Save as health record
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=visit_record
                    )
                    
                    if record_id:
                        st.success("✅ Visit record saved successfully!")
                    else:
                        st.error("❌ Error saving visit record")
                else:
                    st.error("❌ Please fill in doctor name and reason for visit")

def show_quick_assessment(heart_rate, blood_pressure, temperature):
    """Show quick health assessment"""
    st.subheader("🤖 Quick Health Assessment")
    
    assessments = []
    
    if heart_rate:
        hr_status = get_heart_rate_status(heart_rate)
        if "normal" in hr_status.lower():
            assessments.append(f"✅ Heart rate: {hr_status}")
        else:
            assessments.append(f"⚠️ Heart rate: {hr_status}")
    
    if blood_pressure:
        bp_status = get_blood_pressure_status(blood_pressure)
        if "normal" in bp_status.lower():
            assessments.append(f"✅ Blood pressure: {bp_status}")
        else:
            assessments.append(f"⚠️ Blood pressure: {bp_status}")
    
    if temperature:
        temp_status = get_temperature_status(temperature)
        if "normal" in temp_status.lower():
            assessments.append(f"✅ Temperature: {temp_status}")
        else:
            assessments.append(f"⚠️ Temperature: {temp_status}")
    
    for assessment in assessments:
        if "✅" in assessment:
            st.success(assessment)
        else:
            st.warning(assessment)

def show_health_trends():
    """Display health trends and analytics"""
    st.header("📈 Health Trends & Analytics")
    
    user_id = st.session_state.user_id
    health_records = data_manager.get_user_health_records(user_id)
    
    if health_records.empty:
        st.info("📈 No data available for trends. Start tracking your health metrics!")
        return
    
    if len(health_records) < 2:
        st.info("📈 Need at least 2 records to show trends. Keep tracking!")
        return
    
    # Time range selector
    col_range1, col_range2 = st.columns(2)
    
    with col_range1:
        time_range = st.selectbox("📅 Time Range", [
            "Last 7 days", "Last 30 days", "Last 3 months", "Last 6 months", "All time"
        ])
    
    with col_range2:
        metrics_to_show = st.multiselect("📊 Metrics to Display", [
            "Heart Rate", "Weight", "Blood Pressure", "Temperature"
        ], default=["Heart Rate", "Weight"])
    
    # Filter data based on time range
    end_date = datetime.now().date()
    
    if time_range == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif time_range == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    elif time_range == "Last 3 months":
        start_date = end_date - timedelta(days=90)
    elif time_range == "Last 6 months":
        start_date = end_date - timedelta(days=180)
    else:
        start_date = health_records['date'].min()
    
    # Filter records
    health_records['date'] = pd.to_datetime(health_records['date'])
    filtered_records = health_records[
        (health_records['date'].dt.date >= pd.to_datetime(start_date).date()) &
        (health_records['date'].dt.date <= end_date)
    ].copy()
    
    if filtered_records.empty:
        st.warning("No data available for the selected time range")
        return
    
    # Create trend charts
    if metrics_to_show:
        fig = go.Figure()
        
        if "Heart Rate" in metrics_to_show and 'heart_rate' in filtered_records.columns:
            hr_data = filtered_records.dropna(subset=['heart_rate'])
            if not hr_data.empty:
                fig.add_trace(go.Scatter(
                    x=hr_data['date'],
                    y=hr_data['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate (BPM)',
                    line=dict(color='red')
                ))
        
        if "Weight" in metrics_to_show and 'weight' in filtered_records.columns:
            weight_data = filtered_records.dropna(subset=['weight'])
            if not weight_data.empty:
                fig.add_trace(go.Scatter(
                    x=weight_data['date'],
                    y=weight_data['weight'],
                    mode='lines+markers',
                    name='Weight (kg)',
                    yaxis='y2',
                    line=dict(color='blue')
                ))
        
        if "Temperature" in metrics_to_show and 'temperature' in filtered_records.columns:
            temp_data = filtered_records.dropna(subset=['temperature'])
            if not temp_data.empty:
                fig.add_trace(go.Scatter(
                    x=temp_data['date'],
                    y=temp_data['temperature'],
                    mode='lines+markers',
                    name='Temperature (°F)',
                    yaxis='y3',
                    line=dict(color='green')
                ))
        
        # Update layout
        fig.update_layout(
            title=f"Health Trends - {time_range}",
            xaxis_title="Date",
            yaxis=dict(title="Heart Rate (BPM)", side="left"),
            yaxis2=dict(title="Weight (kg)", overlaying="y", side="right"),
            yaxis3=dict(title="Temperature (°F)", overlaying="y", side="right", position=0.85),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Blood pressure trends (separate chart due to different format)
    if "Blood Pressure" in metrics_to_show and 'blood_pressure' in filtered_records.columns:
        bp_data = filtered_records.dropna(subset=['blood_pressure'])
        
        if not bp_data.empty:
            # Parse blood pressure readings
            systolic_values = []
            diastolic_values = []
            dates = []
            
            for _, row in bp_data.iterrows():
                try:
                    systolic, diastolic = map(int, row['blood_pressure'].split('/'))
                    systolic_values.append(systolic)
                    diastolic_values.append(diastolic)
                    dates.append(row['date'])
                except:
                    continue
            
            if systolic_values:
                fig_bp = go.Figure()
                
                fig_bp.add_trace(go.Scatter(
                    x=dates,
                    y=systolic_values,
                    mode='lines+markers',
                    name='Systolic BP',
                    line=dict(color='red')
                ))
                
                fig_bp.add_trace(go.Scatter(
                    x=dates,
                    y=diastolic_values,
                    mode='lines+markers',
                    name='Diastolic BP',
                    line=dict(color='blue')
                ))
                
                fig_bp.update_layout(
                    title="Blood Pressure Trends",
                    xaxis_title="Date",
                    yaxis_title="mmHg",
                    height=400
                )
                
                st.plotly_chart(fig_bp, use_container_width=True)
    
    # Statistics summary
    st.subheader("📊 Statistical Summary")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    if 'heart_rate' in filtered_records.columns and filtered_records['heart_rate'].notna().any():
        with col_stat1:
            hr_avg = filtered_records['heart_rate'].mean()
            hr_min = filtered_records['heart_rate'].min()
            hr_max = filtered_records['heart_rate'].max()
            
            st.metric("❤️ Heart Rate", f"{hr_avg:.0f} BPM avg")
            st.write(f"Range: {hr_min:.0f} - {hr_max:.0f}")
    
    if 'weight' in filtered_records.columns and filtered_records['weight'].notna().any():
        with col_stat2:
            weight_avg = filtered_records['weight'].mean()
            weight_change = filtered_records['weight'].iloc[-1] - filtered_records['weight'].iloc[0]
            
            st.metric("⚖️ Weight", f"{weight_avg:.1f} kg avg", delta=f"{weight_change:+.1f} kg")
    
    if 'temperature' in filtered_records.columns and filtered_records['temperature'].notna().any():
        with col_stat3:
            temp_avg = filtered_records['temperature'].mean()
            temp_min = filtered_records['temperature'].min()
            temp_max = filtered_records['temperature'].max()
            
            st.metric("🌡️ Temperature", f"{temp_avg:.1f}°F avg")
            st.write(f"Range: {temp_min:.1f} - {temp_max:.1f}")
    
    with col_stat4:
        tracking_days = len(filtered_records['date'].dt.date.unique())
        total_records = len(filtered_records)
        
        st.metric("📊 Tracking", f"{tracking_days} days")
        st.write(f"Total records: {total_records}")

def show_medical_reports():
    """Display and manage medical reports"""
    st.header("📄 Medical Reports & Documents")
    
    # Sample medical reports (in real app, these would be stored files/links)
    sample_reports = [
        {
            "type": "Lab Report",
            "title": "Complete Blood Count (CBC)",
            "date": "2024-08-20",
            "doctor": "Dr. Sarah Johnson",
            "facility": "City Lab Center",
            "status": "Normal",
            "file_type": "PDF"
        },
        {
            "type": "Imaging",
            "title": "Chest X-Ray",
            "date": "2024-08-15",
            "doctor": "Dr. Michael Chen",
            "facility": "Metro Radiology",
            "status": "Normal",
            "file_type": "DICOM"
        },
        {
            "type": "Prescription",
            "title": "Hypertension Medication",
            "date": "2024-08-10",
            "doctor": "Dr. Priya Sharma",
            "facility": "Heart Care Clinic",
            "status": "Active",
            "file_type": "PDF"
        },
        {
            "type": "Test Report",
            "title": "Lipid Profile",
            "date": "2024-08-05",
            "doctor": "Dr. Rajesh Kumar",
            "facility": "Wellness Lab",
            "status": "Review Required",
            "file_type": "PDF"
        }
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Your Medical Reports")
        
        # Filter options
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            report_type_filter = st.selectbox("📂 Report Type", 
                ["All Types", "Lab Report", "Imaging", "Prescription", "Test Report"])
        
        with col_filter2:
            date_range = st.selectbox("📅 Date Range", 
                ["All Time", "Last 30 days", "Last 3 months", "Last 6 months"])
        
        # Display reports
        for report in sample_reports:
            if report_type_filter == "All Types" or report["type"] == report_type_filter:
                with st.expander(f"📄 {report['title']} - {report['date']}", expanded=False):
                    col_report1, col_report2 = st.columns([2, 1])
                    
                    with col_report1:
                        st.write(f"**Type:** {report['type']}")
                        st.write(f"**Doctor:** {report['doctor']}")
                        st.write(f"**Facility:** {report['facility']}")
                        st.write(f"**Date:** {report['date']}")
                        
                        # Status with color coding
                        status_color = "green" if report['status'] == "Normal" else "orange" if report['status'] == "Review Required" else "blue"
                        st.markdown(f"**Status:** <span style='color:{status_color}'>{report['status']}</span>", 
                                   unsafe_allow_html=True)
                    
                    with col_report2:
                        st.write(f"**File Type:** {report['file_type']}")
                        
                        if st.button(f"👁️ View", key=f"view_{report['title']}", use_container_width=True):
                            st.success(f"Opening {report['title']}")
                        
                        if st.button(f"📧 Share", key=f"share_{report['title']}", use_container_width=True):
                            st.success(f"Sharing {report['title']}")
                        
                        if st.button(f"📱 Download", key=f"download_{report['title']}", use_container_width=True):
                            st.success(f"Downloaded {report['title']}")
        
        # Upload new report
        st.subheader("📤 Upload New Report")
        
        with st.form("upload_report_form"):
            uploaded_file = st.file_uploader("📁 Choose file", type=['pdf', 'jpg', 'png', 'doc', 'docx'])
            
            col_upload1, col_upload2 = st.columns(2)
            
            with col_upload1:
                report_title = st.text_input("📝 Report Title")
                report_type = st.selectbox("📂 Report Type", 
                    ["Lab Report", "Imaging", "Prescription", "Test Report", "Consultation Notes", "Other"])
                report_date = st.date_input("📅 Report Date", value=date.today())
            
            with col_upload2:
                doctor_name = st.text_input("👨‍⚕️ Doctor Name")
                facility_name = st.text_input("🏥 Facility Name")
                report_notes = st.text_area("📝 Notes")
            
            if st.form_submit_button("📤 Upload Report", use_container_width=True):
                if uploaded_file and report_title:
                    st.success(f"✅ {report_title} uploaded successfully!")
                    
                    # In real implementation, save file and metadata
                    file_info = f"Uploaded: {report_title} ({report_type}) from {doctor_name} at {facility_name} on {report_date}"
                    if report_notes:
                        file_info += f". Notes: {report_notes}"
                    
                    # Save as health record
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=file_info
                    )
                else:
                    st.error("❌ Please select a file and enter report title")
    
    with col2:
        st.subheader("📊 Reports Summary")
        
        # Report statistics
        report_counts = {}
        for report in sample_reports:
            report_type = report['type']
            report_counts[report_type] = report_counts.get(report_type, 0) + 1
        
        for report_type, count in report_counts.items():
            st.metric(report_type, count)
        
        st.subheader("🔍 Recent Activity")
        
        activities = [
            "📄 Lab Report uploaded (Aug 20)",
            "👁️ Chest X-Ray viewed (Aug 18)",
            "📧 Prescription shared with Dr. Smith (Aug 15)",
            "📱 Lipid Profile downloaded (Aug 12)"
        ]
        
        for activity in activities:
            st.info(activity)
        
        st.subheader("💡 Report Management Tips")
        
        tips = [
            "📁 Organize reports by type and date",
            "☁️ Keep digital backups of all reports",
            "📧 Share reports with doctors before visits",
            "🔒 Ensure privacy when sharing",
            "📱 Keep important reports on your phone",
            "📅 Set reminders for follow-up tests"
        ]
        
        for tip in tips:
            st.info(tip)

def show_privacy_sharing():
    """Privacy settings and sharing options"""
    st.header("🔒 Privacy & Data Sharing Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔒 Privacy Settings", "📤 Data Sharing", "🔐 Data Export"])
    
    with tab1:
        st.subheader("🛡️ Privacy & Security Settings")
        
        # Privacy preferences
        st.markdown("**🔒 Data Access Permissions**")
        
        col_privacy1, col_privacy2 = st.columns(2)
        
        with col_privacy1:
            family_access = st.checkbox("👨‍👩‍👧‍👦 Allow family member access", help="Emergency contacts can view basic health info")
            
            doctor_access = st.checkbox("👨‍⚕️ Allow doctor access", value=True, help="Healthcare providers can access relevant records")
            
            research_participation = st.checkbox("🔬 Participate in anonymous health research", help="Anonymized data may be used for medical research")
        
        with col_privacy2:
            emergency_access = st.checkbox("🚨 Emergency access override", value=True, help="Allow access during medical emergencies")
            
            analytics_tracking = st.checkbox("📊 Allow usage analytics", value=True, help="Help improve the platform with usage data")
            
            marketing_emails = st.checkbox("📧 Receive health tips and updates", help="Get health information and platform updates")
        
        # Data retention settings
        st.markdown("**🗃️ Data Retention**")
        
        retention_period = st.selectbox("📅 Data Retention Period", [
            "1 year", "2 years", "5 years", "10 years", "Indefinitely"
        ], index=2)
        
        auto_delete = st.checkbox("🗑️ Auto-delete old records", help="Automatically delete records older than retention period")
        
        # Encryption settings
        st.markdown("**🔐 Security Options**")
        
        encryption_level = st.selectbox("🔒 Encryption Level", [
            "Standard (AES-256)", "High Security (AES-256 + Additional Keys)", "Maximum (End-to-End)"
        ], index=1)
        
        two_factor = st.checkbox("🔐 Enable Two-Factor Authentication", value=True)
        
        if st.button("💾 Save Privacy Settings", use_container_width=True):
            st.success("✅ Privacy settings saved successfully!")
    
    with tab2:
        st.subheader("📤 Data Sharing & Permissions")
        
        # Active sharing permissions
        st.markdown("**👥 Current Sharing Permissions**")
        
        # Sample shared access list
        shared_access = [
            {"name": "Dr. Sarah Johnson", "type": "Doctor", "access": "Full medical records", "expires": "2024-12-31"},
            {"name": "City General Hospital", "type": "Hospital", "access": "Emergency records only", "expires": "Ongoing"},
            {"name": "John Doe (Spouse)", "type": "Family", "access": "Basic health info", "expires": "Ongoing"}
        ]
        
        for access in shared_access:
            with st.container():
                col_share1, col_share2, col_share3 = st.columns([2, 2, 1])
                
                with col_share1:
                    st.write(f"**{access['name']}** ({access['type']})")
                    st.write(f"Access: {access['access']}")
                
                with col_share2:
                    st.write(f"Expires: {access['expires']}")
                
                with col_share3:
                    if st.button("❌ Revoke", key=f"revoke_{access['name']}", use_container_width=True):
                        st.success(f"Access revoked for {access['name']}")
                
                st.markdown("---")
        
        # Grant new access
        st.markdown("**➕ Grant New Access**")
        
        with st.form("grant_access_form"):
            col_grant1, col_grant2 = st.columns(2)
            
            with col_grant1:
                recipient_name = st.text_input("👤 Recipient Name")
                recipient_type = st.selectbox("👥 Recipient Type", ["Doctor", "Hospital", "Family", "Caregiver", "Other"])
                access_level = st.selectbox("🔑 Access Level", [
                    "View only", "Basic health info", "Full medical records", "Emergency records only"
                ])
            
            with col_grant2:
                access_duration = st.selectbox("⏰ Access Duration", [
                    "1 month", "3 months", "6 months", "1 year", "Ongoing"
                ])
                
                specific_records = st.multiselect("📋 Specific Records (optional)", [
                    "Vital signs", "Medications", "Lab results", "Visit records", "Allergies"
                ])
                
                notify_access = st.checkbox("📧 Notify when data is accessed", value=True)
            
            reason = st.text_input("📝 Reason for Access")
            
            if st.form_submit_button("✅ Grant Access", use_container_width=True):
                if recipient_name and reason:
                    st.success(f"✅ Access granted to {recipient_name}")
                    
                    # Log the access grant
                    access_log = f"Data access granted to {recipient_name} ({recipient_type}) - {access_level} for {access_duration}. Reason: {reason}"
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=access_log
                    )
                else:
                    st.error("❌ Please fill in recipient name and reason")
        
        # Access log
        st.markdown("**📋 Recent Access Log**")
        
        access_logs = [
            "👨‍⚕️ Dr. Sarah Johnson viewed lab results (Aug 20, 2024)",
            "🏥 City General Hospital accessed emergency info (Aug 18, 2024)",
            "👤 John Doe viewed basic health summary (Aug 15, 2024)",
            "👨‍⚕️ Dr. Michael Chen downloaded chest X-ray (Aug 12, 2024)"
        ]
        
        for log in access_logs:
            st.info(log)
    
    with tab3:
        st.subheader("📁 Data Export & Backup")
        
        st.markdown("**📤 Export Your Health Data**")
        
        export_formats = st.multiselect("📂 Export Format", [
            "PDF Report", "CSV Data", "JSON Format", "HL7 FHIR", "Medical Summary"
        ], default=["PDF Report"])
        
        export_data_types = st.multiselect("📊 Data to Export", [
            "Health metrics", "Medical visits", "Medications", "Lab results", 
            "Appointments", "Emergency contacts", "Medical alerts"
        ], default=["Health metrics", "Medical visits"])
        
        date_range_export = st.selectbox("📅 Date Range", [
            "All data", "Last 30 days", "Last 3 months", "Last year", "Custom range"
        ])
        
        if date_range_export == "Custom range":
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                start_date_export = st.date_input("Start Date")
            with col_date2:
                end_date_export = st.date_input("End Date")
        
        include_sensitive = st.checkbox("🔒 Include sensitive data (mental health, etc.)", 
                                      help="Include all data including sensitive medical information")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📧 Email Export", use_container_width=True):
                st.success("📧 Health data export will be emailed to your registered email address")
        
        with col_export2:
            if st.button("📱 Download Export", use_container_width=True):
                st.success("📱 Preparing your health data export for download...")
        
        # Backup settings
        st.markdown("**☁️ Automatic Backup Settings**")
        
        auto_backup = st.checkbox("🔄 Enable automatic backups", value=True)
        
        if auto_backup:
            backup_frequency = st.selectbox("⏰ Backup Frequency", [
                "Daily", "Weekly", "Monthly"
            ], index=1)
            
            backup_location = st.selectbox("📍 Backup Location", [
                "Secure cloud storage", "Email", "Both"
            ])
            
            if st.button("⚙️ Save Backup Settings", use_container_width=True):
                st.success("✅ Backup settings saved!")
        
        # Data portability
        st.markdown("**🔄 Data Portability**")
        
        st.info("💡 **Your Right to Data Portability**: You have the right to receive your personal health data in a structured, commonly used format and transmit it to another healthcare provider.")
        
        if st.button("📋 Request Data Portability Package", use_container_width=True):
            st.success("📋 Data portability request submitted. You will receive a comprehensive package within 5-7 business days.")

if __name__ == "__main__":
    main()
