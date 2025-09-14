import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta, date, time
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Virtual Consultations - HEALTHTECH",
    page_icon="👨‍⚕️",
    layout="wide"
)

def main():
    add_app_styling()
    st.title("👨‍⚕️ Virtual Consultations")
    st.markdown("### Connect with Healthcare Professionals from Anywhere")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access virtual consultation features")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different consultation features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Book Consultation", 
        "👨‍⚕️ Find Doctors", 
        "📋 My Appointments", 
        "💬 Active Sessions", 
        "📊 Consultation History"
    ])
    
    with tab1:
        show_book_consultation()
    
    with tab2:
        show_find_doctors()
    
    with tab3:
        show_my_appointments()
    
    with tab4:
        show_active_sessions()
    
    with tab5:
        show_consultation_history()

def show_book_consultation():
    """Book a new virtual consultation"""
    st.header("📅 Book Virtual Consultation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Select Consultation Type")
        
        consultation_types = {
            "🩺 General Consultation": {
                "description": "General health issues, routine check-ups, health advice",
                "duration": "15-30 minutes",
                "fee": "₹500"
            },
            "🫀 Cardiology": {
                "description": "Heart-related issues, blood pressure, chest pain",
                "duration": "30-45 minutes", 
                "fee": "₹1200"
            },
            "🧠 Neurology": {
                "description": "Headaches, seizures, neurological symptoms",
                "duration": "30-45 minutes",
                "fee": "₹1500"
            },
            "👶 Pediatrics": {
                "description": "Child health, growth, vaccinations, pediatric issues",
                "duration": "20-30 minutes",
                "fee": "₹800"
            },
            "🦴 Orthopedics": {
                "description": "Bone, joint, muscle problems, injuries",
                "duration": "20-30 minutes",
                "fee": "₹1000"
            },
            "👁️ Ophthalmology": {
                "description": "Eye problems, vision issues, eye infections",
                "duration": "15-25 minutes",
                "fee": "₹900"
            },
            "🦷 Dentistry": {
                "description": "Dental problems, oral health, tooth pain",
                "duration": "15-20 minutes",
                "fee": "₹700"
            },
            "🧠 Psychology/Psychiatry": {
                "description": "Mental health, counseling, psychiatric consultation",
                "duration": "45-60 minutes",
                "fee": "₹1800"
            },
            "👩‍⚕️ Gynecology": {
                "description": "Women's health, pregnancy, reproductive health",
                "duration": "20-30 minutes",
                "fee": "₹1100"
            },
            "🍯 Endocrinology": {
                "description": "Diabetes, thyroid, hormonal disorders",
                "duration": "30-40 minutes",
                "fee": "₹1300"
            }
        }
        
        selected_type = st.selectbox(
            "Choose consultation type:",
            list(consultation_types.keys())
        )
        
        # Display consultation details
        if selected_type:
            consult_info = consultation_types[selected_type]
            
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.info(f"⏰ **Duration:** {consult_info['duration']}")
            
            with col_info2:
                st.info(f"💰 **Fee:** {consult_info['fee']}")
            
            with col_info3:
                st.info("📱 **Mode:** Video Call")
            
            st.write(f"**Description:** {consult_info['description']}")
        
        st.markdown("---")
        
        # Booking form
        st.subheader("📝 Book Your Consultation")
        
        with st.form("consultation_booking"):
            # Date and time selection
            col_date, col_time = st.columns(2)
            
            with col_date:
                consultation_date = st.date_input(
                    "📅 Select Date",
                    min_value=date.today(),
                    max_value=date.today() + timedelta(days=30)
                )
            
            with col_time:
                # Available time slots
                time_slots = [
                    "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
                    "12:00 PM", "12:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",
                    "04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM",
                    "07:00 PM", "07:30 PM", "08:00 PM"
                ]
                
                consultation_time = st.selectbox("🕐 Select Time", time_slots)
            
            # Doctor preference
            doctor_preference = st.selectbox(
                "👨‍⚕️ Doctor Preference",
                ["Any Available", "Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Priya Sharma", "Dr. Rajesh Kumar", "Dr. Emily Davis"]
            )
            
            # Consultation reason
            consultation_reason = st.text_area(
                "📝 Reason for Consultation",
                placeholder="Briefly describe your symptoms or health concerns...",
                height=100
            )
            
            # Medical history
            relevant_history = st.text_area(
                "🏥 Relevant Medical History",
                placeholder="Any relevant medical history, current medications, allergies...",
                height=80
            )
            
            # Urgency level
            urgency = st.selectbox(
                "⚡ Urgency Level",
                ["Routine", "Urgent (within 24 hours)", "Emergency (immediate attention needed)"]
            )
            
            # Contact preferences
            st.subheader("📞 Contact Preferences")
            
            col_phone, col_email = st.columns(2)
            
            with col_phone:
                phone_number = st.text_input("📱 Phone Number", value=st.session_state.user_data.get('phone', ''))
            
            with col_email:
                email_address = st.text_input("📧 Email Address", value=st.session_state.user_data.get('email', ''))
            
            # Terms and conditions
            terms_accepted = st.checkbox("✅ I agree to the terms and conditions of virtual consultation")
            
            # Submit button
            submit_booking = st.form_submit_button("📅 Book Consultation", use_container_width=True)
            
            if submit_booking:
                if not consultation_reason.strip():
                    st.error("❌ Please provide a reason for consultation")
                elif not terms_accepted:
                    st.error("❌ Please accept the terms and conditions")
                elif urgency == "Emergency (immediate attention needed)":
                    st.error("🚨 For emergencies, please call 102 or visit the nearest emergency room")
                else:
                    book_consultation(
                        selected_type, consultation_date, consultation_time,
                        doctor_preference, consultation_reason, relevant_history,
                        urgency, phone_number, email_address
                    )
    
    with col2:
        st.subheader("💡 Consultation Guidelines")
        
        guidelines = [
            "📱 Ensure stable internet connection",
            "🎥 Test your camera and microphone",
            "📋 Prepare list of symptoms and questions",
            "💊 Have current medications ready",
            "🆔 Keep ID and insurance documents handy",
            "📝 Take notes during consultation",
            "🔒 Ensure privacy during the call"
        ]
        
        for guideline in guidelines:
            st.info(guideline)
        
        st.subheader("🔧 Technical Requirements")
        
        requirements = [
            "💻 Computer, tablet, or smartphone",
            "🌐 Stable internet connection (min 1 Mbps)",
            "🎥 Working camera",
            "🎤 Working microphone",
            "🔊 Speakers or headphones",
            "📱 Latest browser version"
        ]
        
        for req in requirements:
            st.success(req)
        
        st.subheader("⚠️ Important Notes")
        
        st.warning("📋 Virtual consultations are suitable for non-emergency medical consultations")
        st.error("🚨 For emergencies, call 102 or visit nearest emergency room")
        st.info("💊 Prescriptions will be sent digitally after consultation")

def book_consultation(consult_type, consult_date, consult_time, doctor, reason, history, urgency, phone, email):
    """Process consultation booking"""
    
    # Assign doctor based on preference and availability
    if doctor == "Any Available":
        available_doctors = ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Priya Sharma", "Dr. Rajesh Kumar"]
        import random
        assigned_doctor = random.choice(available_doctors)
    else:
        assigned_doctor = doctor
    
    # Book appointment in database
    appointment_id = data_manager.book_appointment(
        st.session_state.user_id,
        assigned_doctor,
        consult_type,
        consult_date.strftime("%Y-%m-%d"),
        consult_time,
        "Virtual Consultation"
    )
    
    if appointment_id:
        st.success("🎉 Consultation booked successfully!")
        
        # Display booking confirmation
        st.subheader("📋 Booking Confirmation")
        
        confirmation_data = {
            "Appointment ID": appointment_id[:8],
            "Doctor": assigned_doctor,
            "Consultation Type": consult_type,
            "Date": consult_date.strftime("%B %d, %Y"),
            "Time": consult_time,
            "Mode": "Virtual (Video Call)",
            "Status": "Confirmed"
        }
        
        for key, value in confirmation_data.items():
            st.write(f"**{key}:** {value}")
        
        # Next steps
        st.subheader("📋 Next Steps")
        
        next_steps = [
            "📧 Confirmation email will be sent to your registered email",
            "📱 You'll receive an SMS reminder 1 hour before consultation",
            "💻 Join the video call using the link in your email",
            "💊 Digital prescription will be provided if needed",
            "📋 Consultation notes will be saved to your health records"
        ]
        
        for step in next_steps:
            st.info(step)
        
        # Payment information
        if urgency != "Emergency (immediate attention needed)":
            st.subheader("💳 Payment Information")
            st.info("💰 Payment can be made during or after the consultation")
            st.info("🏥 Insurance claims will be processed automatically if applicable")
    
    else:
        st.error("❌ Error booking consultation. Please try again.")

def show_find_doctors():
    """Find and browse available doctors"""
    st.header("👨‍⚕️ Find Healthcare Professionals")
    
    # Sample doctors database
    doctors_data = [
        {
            "name": "Dr. Sarah Johnson",
            "specialty": "General Medicine",
            "experience": "12 years",
            "rating": 4.8,
            "qualification": "MBBS, MD",
            "languages": ["English", "Hindi"],
            "availability": "Available today",
            "consultation_fee": "₹500",
            "next_slot": "10:30 AM",
            "about": "Experienced general physician specializing in preventive care and chronic disease management."
        },
        {
            "name": "Dr. Michael Chen",
            "specialty": "Cardiology",
            "experience": "15 years",
            "rating": 4.9,
            "qualification": "MBBS, MD, DM (Cardiology)",
            "languages": ["English", "Mandarin"],
            "availability": "Available tomorrow",
            "consultation_fee": "₹1200",
            "next_slot": "02:00 PM",
            "about": "Leading cardiologist with expertise in interventional cardiology and heart disease prevention."
        },
        {
            "name": "Dr. Priya Sharma",
            "specialty": "Pediatrics",
            "experience": "10 years",
            "rating": 4.7,
            "qualification": "MBBS, MD (Pediatrics)",
            "languages": ["English", "Hindi", "Punjabi"],
            "availability": "Available today",
            "consultation_fee": "₹800",
            "next_slot": "04:00 PM",
            "about": "Dedicated pediatrician focusing on child development, vaccination, and pediatric care."
        },
        {
            "name": "Dr. Rajesh Kumar",
            "specialty": "Orthopedics",
            "experience": "18 years",
            "rating": 4.6,
            "qualification": "MBBS, MS (Orthopedics)",
            "languages": ["English", "Hindi", "Tamil"],
            "availability": "Available today",
            "consultation_fee": "₹1000",
            "next_slot": "11:00 AM",
            "about": "Expert orthopedic surgeon specializing in joint replacement and sports medicine."
        },
        {
            "name": "Dr. Emily Davis",
            "specialty": "Psychology",
            "experience": "8 years",
            "rating": 4.9,
            "qualification": "PhD in Clinical Psychology",
            "languages": ["English", "French"],
            "availability": "Available tomorrow",
            "consultation_fee": "₹1800",
            "next_slot": "06:00 PM",
            "about": "Licensed clinical psychologist specializing in anxiety, depression, and cognitive behavioral therapy."
        }
    ]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🔍 Filter Doctors")
        
        # Specialty filter
        specialties = ["All Specialties"] + list(set([doc["specialty"] for doc in doctors_data]))
        specialty_filter = st.selectbox("🩺 Specialty", specialties)
        
        # Availability filter
        availability_filter = st.selectbox("📅 Availability", ["All", "Available today", "Available tomorrow"])
        
        # Rating filter
        rating_filter = st.slider("⭐ Minimum Rating", 0.0, 5.0, 4.0, 0.1)
        
        # Language filter
        all_languages = set()
        for doc in doctors_data:
            all_languages.update(doc["languages"])
        
        language_filter = st.selectbox("🌐 Language", ["All Languages"] + sorted(list(all_languages)))
        
        # Fee range filter
        fee_range = st.slider("💰 Maximum Fee (₹)", 0, 2000, 2000, 100)
    
    with col2:
        st.subheader("👨‍⚕️ Available Doctors")
        
        # Filter doctors based on criteria
        filtered_doctors = doctors_data.copy()
        
        if specialty_filter != "All Specialties":
            filtered_doctors = [doc for doc in filtered_doctors if doc["specialty"] == specialty_filter]
        
        if availability_filter != "All":
            filtered_doctors = [doc for doc in filtered_doctors if doc["availability"] == availability_filter]
        
        filtered_doctors = [doc for doc in filtered_doctors if doc["rating"] >= rating_filter]
        
        if language_filter != "All Languages":
            filtered_doctors = [doc for doc in filtered_doctors if language_filter in doc["languages"]]
        
        # Filter by fee
        filtered_doctors = [doc for doc in filtered_doctors 
                          if int(doc["consultation_fee"].replace("₹", "")) <= fee_range]
        
        if filtered_doctors:
            st.info(f"Found {len(filtered_doctors)} doctors matching your criteria")
            
            for doctor in filtered_doctors:
                with st.container():
                    col_info, col_action = st.columns([3, 1])
                    
                    with col_info:
                        st.markdown(f"### {doctor['name']}")
                        
                        col_detail1, col_detail2 = st.columns(2)
                        
                        with col_detail1:
                            st.write(f"🩺 **Specialty:** {doctor['specialty']}")
                            st.write(f"🎓 **Qualification:** {doctor['qualification']}")
                            st.write(f"📅 **Experience:** {doctor['experience']}")
                            st.write(f"⭐ **Rating:** {doctor['rating']}/5.0")
                        
                        with col_detail2:
                            st.write(f"🌐 **Languages:** {', '.join(doctor['languages'])}")
                            st.write(f"💰 **Fee:** {doctor['consultation_fee']}")
                            st.write(f"📅 **Availability:** {doctor['availability']}")
                            st.write(f"🕐 **Next Slot:** {doctor['next_slot']}")
                        
                        st.write(f"📋 **About:** {doctor['about']}")
                    
                    with col_action:
                        st.metric("Rating", f"{doctor['rating']}/5.0")
                        
                        if st.button(f"📅 Book with {doctor['name'].split()[-1]}", 
                                   key=f"book_{doctor['name']}", use_container_width=True):
                            st.success(f"Redirecting to book consultation with {doctor['name']}")
                        
                        if st.button(f"👁️ View Profile", 
                                   key=f"profile_{doctor['name']}", use_container_width=True):
                            show_doctor_profile(doctor)
                    
                    st.markdown("---")
        else:
            st.warning("No doctors found matching your criteria. Please adjust your filters.")

def show_doctor_profile(doctor):
    """Show detailed doctor profile"""
    st.subheader(f"👨‍⚕️ {doctor['name']} - Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Specialty:** {doctor['specialty']}")
        st.markdown(f"**Experience:** {doctor['experience']}")
        st.markdown(f"**Qualification:** {doctor['qualification']}")
        st.markdown(f"**Languages:** {', '.join(doctor['languages'])}")
        st.markdown(f"**About:** {doctor['about']}")
        
        # Sample reviews
        st.subheader("💬 Patient Reviews")
        
        reviews = [
            {"patient": "Anonymous", "rating": 5, "comment": "Excellent doctor, very thorough and caring."},
            {"patient": "Anonymous", "rating": 4, "comment": "Professional and knowledgeable, would recommend."},
            {"patient": "Anonymous", "rating": 5, "comment": "Great communication skills and patient care."}
        ]
        
        for review in reviews:
            st.write(f"⭐ **{review['rating']}/5** - {review['comment']}")
    
    with col2:
        st.metric("Overall Rating", f"{doctor['rating']}/5.0")
        st.metric("Consultation Fee", doctor['consultation_fee'])
        st.metric("Next Available", doctor['next_slot'])
        
        if st.button("📅 Book Consultation", use_container_width=True):
            st.success("Redirecting to booking page...")

def show_my_appointments():
    """Show user's upcoming and past appointments"""
    st.header("📋 My Appointments")
    
    user_id = st.session_state.user_id
    appointments = data_manager.get_user_appointments(user_id)
    
    if not appointments.empty:
        # Separate upcoming and past appointments
        today = datetime.now().date()
        
        upcoming_appointments = appointments[pd.to_datetime(appointments['date']).dt.date >= today]
        past_appointments = appointments[pd.to_datetime(appointments['date']).dt.date < today]
        
        tab1, tab2 = st.tabs(["📅 Upcoming", "📜 Past"])
        
        with tab1:
            st.subheader("📅 Upcoming Appointments")
            
            if not upcoming_appointments.empty:
                for _, appointment in upcoming_appointments.iterrows():
                    show_appointment_card(appointment, is_upcoming=True)
            else:
                st.info("📅 No upcoming appointments. Book a consultation to get started!")
                
                if st.button("📅 Book New Consultation"):
                    st.info("Redirecting to booking page...")
        
        with tab2:
            st.subheader("📜 Past Appointments")
            
            if not past_appointments.empty:
                for _, appointment in past_appointments.iterrows():
                    show_appointment_card(appointment, is_upcoming=False)
            else:
                st.info("📜 No past appointments found.")
    
    else:
        st.info("📋 No appointments found. Book your first consultation!")
        
        if st.button("📅 Book Your First Consultation", use_container_width=True):
            st.info("Redirecting to booking page...")

def show_appointment_card(appointment, is_upcoming=True):
    """Display appointment information card"""
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**👨‍⚕️ {appointment['doctor_name']}**")
            st.write(f"🩺 {appointment['specialty']}")
            st.write(f"📅 {appointment['date']} at {appointment['time']}")
            st.write(f"💻 {appointment['consultation_type']}")
        
        with col2:
            status_colors = {
                "Scheduled": "blue",
                "Completed": "green", 
                "Cancelled": "red",
                "In Progress": "orange"
            }
            
            status = appointment['status']
            color = status_colors.get(status, "gray")
            
            st.markdown(f"**Status:** <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
            
            if appointment.get('notes'):
                st.write(f"📝 {appointment['notes'][:50]}...")
        
        with col3:
            if is_upcoming and status == "Scheduled":
                if st.button(f"🔗 Join Call", key=f"join_{appointment['appointment_id']}"):
                    st.success("Joining consultation...")
                
                if st.button(f"❌ Cancel", key=f"cancel_{appointment['appointment_id']}"):
                    st.error("Appointment cancelled")
            
            elif not is_upcoming and status == "Completed":
                if st.button(f"📋 View Report", key=f"report_{appointment['appointment_id']}"):
                    show_consultation_report(appointment)
                
                if st.button(f"⭐ Rate", key=f"rate_{appointment['appointment_id']}"):
                    show_rating_form(appointment)
        
        st.markdown("---")

def show_consultation_report(appointment):
    """Show consultation report and prescription"""
    st.subheader("📋 Consultation Report")
    
    # Sample consultation report
    report = {
        "Date": appointment['date'],
        "Doctor": appointment['doctor_name'],
        "Chief Complaint": "Headache and fatigue for 3 days",
        "Diagnosis": "Tension headache, likely stress-related",
        "Treatment Plan": "Rest, stress management, follow-up in 1 week",
        "Prescription": "Paracetamol 500mg twice daily for 3 days",
        "Follow-up": "Schedule follow-up if symptoms persist",
        "Doctor's Notes": "Patient advised to maintain regular sleep schedule and manage stress levels"
    }
    
    for key, value in report.items():
        st.write(f"**{key}:** {value}")
    
    # Download options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📧 Email Report"):
            st.success("📧 Report emailed to your registered email address")
    
    with col2:
        if st.button("📱 Download PDF"):
            st.success("📱 PDF downloaded to your device")

def show_rating_form(appointment):
    """Show rating and feedback form"""
    st.subheader("⭐ Rate Your Consultation")
    
    with st.form("consultation_rating"):
        rating = st.select_slider(
            "Overall Experience",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "⭐" * x
        )
        
        aspects = {
            "Doctor's Knowledge": st.select_slider("Doctor's Knowledge", [1, 2, 3, 4, 5], 5),
            "Communication": st.select_slider("Communication Skills", [1, 2, 3, 4, 5], 5),
            "Listening": st.select_slider("Listening & Understanding", [1, 2, 3, 4, 5], 5),
            "Technical Quality": st.select_slider("Video/Audio Quality", [1, 2, 3, 4, 5], 5)
        }
        
        feedback = st.text_area("Additional Comments", placeholder="Share your experience...")
        
        recommend = st.checkbox("Would you recommend this doctor to others?")
        
        submit_rating = st.form_submit_button("⭐ Submit Rating")
        
        if submit_rating:
            # Save feedback
            feedback_id = data_manager.add_feedback(
                st.session_state.user_id,
                "Virtual Consultation",
                rating,
                feedback
            )
            
            if feedback_id:
                st.success("✅ Thank you for your feedback!")
            else:
                st.error("❌ Error submitting feedback. Please try again.")

def show_active_sessions():
    """Show active consultation sessions"""
    st.header("💬 Active Consultation Sessions")
    
    # Check for active sessions (mock implementation)
    active_sessions = []  # This would come from a real-time database
    
    if active_sessions:
        for session in active_sessions:
            show_active_session_interface(session)
    else:
        st.info("💬 No active consultation sessions")
        
        # Show next upcoming appointment
        user_id = st.session_state.user_id
        appointments = data_manager.get_user_appointments(user_id)
        
        if not appointments.empty:
            today = datetime.now().date()
            upcoming = appointments[pd.to_datetime(appointments['date']).dt.date >= today]
            
            if not upcoming.empty:
                next_appointment = upcoming.iloc[0]
                
                st.subheader("📅 Next Upcoming Consultation")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**👨‍⚕️ Doctor:** {next_appointment['doctor_name']}")
                    st.write(f"**📅 Date:** {next_appointment['date']}")
                    st.write(f"**🕐 Time:** {next_appointment['time']}")
                    st.write(f"**🩺 Type:** {next_appointment['specialty']}")
                
                with col2:
                    # Calculate time until appointment
                    appointment_datetime = pd.to_datetime(f"{next_appointment['date']} {next_appointment['time']}")
                    time_until = appointment_datetime - datetime.now()
                    
                    if time_until.total_seconds() > 0:
                        hours_until = int(time_until.total_seconds() // 3600)
                        minutes_until = int((time_until.total_seconds() % 3600) // 60)
                        
                        st.metric("Time Until", f"{hours_until}h {minutes_until}m")
                        
                        if hours_until == 0 and minutes_until <= 30:
                            if st.button("🔗 Join Consultation", use_container_width=True):
                                start_consultation_session(next_appointment)
                        else:
                            st.info("⏰ Join button will be available 30 minutes before appointment")
                    else:
                        st.error("⚠️ Appointment time has passed")
        
        # Pre-consultation checklist
        st.subheader("✅ Pre-Consultation Checklist")
        
        checklist = [
            "📱 Test your camera and microphone",
            "🌐 Check internet connection",
            "📋 Prepare list of symptoms and questions", 
            "💊 Have current medications ready",
            "🆔 Keep identification documents handy",
            "📝 Find a quiet, private space",
            "🔋 Ensure device is charged"
        ]
        
        for item in checklist:
            st.checkbox(item, key=f"checklist_{item}")

def start_consultation_session(appointment):
    """Start a consultation session"""
    st.success("🔗 Starting consultation session...")
    
    # Mock video consultation interface
    st.subheader(f"💻 Video Consultation with {appointment['doctor_name']}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Mock video interface
        st.markdown("""
        <div style="background-color: #f0f0f0; height: 400px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <h3>📹 Video Call Interface</h3>
            <p>This would be the actual video call interface</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Call controls
        col_controls = st.columns(5)
        
        with col_controls[0]:
            st.button("🎤 Mute")
        
        with col_controls[1]:
            st.button("📹 Video Off")
        
        with col_controls[2]:
            st.button("💬 Chat")
        
        with col_controls[3]:
            st.button("📷 Screenshot")
        
        with col_controls[4]:
            if st.button("📞 End Call"):
                st.error("Call ended")
    
    with col2:
        st.subheader("📋 Session Info")
        
        st.write(f"**Doctor:** {appointment['doctor_name']}")
        st.write(f"**Start Time:** {datetime.now().strftime('%H:%M')}")
        st.write(f"**Duration:** 00:15:32")
        
        st.subheader("📝 Quick Notes")
        
        session_notes = st.text_area("Take notes during consultation:", height=150)
        
        if st.button("💾 Save Notes"):
            st.success("Notes saved!")
        
        st.subheader("📋 Prescription")
        
        st.info("Prescription will appear here after doctor provides it")

def show_consultation_history():
    """Show detailed consultation history and analytics"""
    st.header("📊 Consultation History & Analytics")
    
    user_id = st.session_state.user_id
    appointments = data_manager.get_user_appointments(user_id)
    
    if not appointments.empty:
        # Analytics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_consultations = len(appointments)
            st.metric("📋 Total Consultations", total_consultations)
        
        with col2:
            completed = len(appointments[appointments['status'] == 'Completed'])
            st.metric("✅ Completed", completed)
        
        with col3:
            # Calculate average rating (mock)
            avg_rating = 4.6  # This would be calculated from actual ratings
            st.metric("⭐ Average Rating", f"{avg_rating}/5.0")
        
        with col4:
            total_spent = total_consultations * 800  # Mock calculation
            st.metric("💰 Total Spent", f"₹{total_spent}")
        
        # Consultation trends
        st.subheader("📈 Consultation Trends")
        
        # Create trend chart
        appointments['date'] = pd.to_datetime(appointments['date'])
        monthly_counts = appointments.groupby(appointments['date'].dt.to_period('M')).size()
        
        if len(monthly_counts) > 1:
            fig = px.line(
                x=monthly_counts.index.astype(str),
                y=monthly_counts.values,
                title="Monthly Consultation Trends",
                labels={'x': 'Month', 'y': 'Number of Consultations'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Specialty breakdown
        st.subheader("🩺 Consultations by Specialty")
        
        specialty_counts = appointments['specialty'].value_counts()
        
        fig_pie = px.pie(
            values=specialty_counts.values,
            names=specialty_counts.index,
            title="Distribution of Consultations by Medical Specialty"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed history table
        st.subheader("📋 Detailed History")
        
        # Display appointments in a formatted table
        display_appointments = appointments[['date', 'doctor_name', 'specialty', 'status', 'consultation_type']].copy()
        display_appointments.columns = ['Date', 'Doctor', 'Specialty', 'Status', 'Type']
        
        st.dataframe(display_appointments, use_container_width=True)
        
        # Export options
        st.subheader("📤 Export Options")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📧 Email Complete History"):
                st.success("📧 Complete consultation history emailed!")
        
        with col_export2:
            if st.button("📱 Download PDF Report"):
                st.success("📱 PDF report downloaded!")
    
    else:
        st.info("📊 No consultation history available")
        
        # Show getting started tips
        st.subheader("🚀 Get Started with Virtual Consultations")
        
        tips = [
            "📅 Book your first consultation with a general physician",
            "🩺 Choose specialty consultations for specific health concerns",
            "💬 Use virtual consultations for follow-ups and routine check-ups",
            "📱 Ensure you have a stable internet connection",
            "📋 Prepare your questions and symptoms list before consultation"
        ]
        
        for tip in tips:
            st.info(tip)

if __name__ == "__main__":
    main()
