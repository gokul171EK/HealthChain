import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils.data_manager import DataManager
from utils.ai_simulator import AISimulator
from utils.translator import MedicalTranslator

# Initialize page configuration
st.set_page_config(
    page_title="HEALTHTECH - Complete Healthcare Solution",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

@st.cache_resource
def init_ai_simulator():
    return AISimulator()

@st.cache_resource
def init_translator():
    return MedicalTranslator()

data_manager = init_data_manager()
ai_simulator = init_ai_simulator()
translator = init_translator()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'language' not in st.session_state:
    st.session_state.language = 'English'

def main():
    # Header with logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏥 HEALTHTECH")
        st.subheader("A Complete Healthcare Solution for All")
        st.markdown("---")
    
    # Language selector in sidebar
    with st.sidebar:
        st.header("🌐 Language / भाषा")
        st.session_state.language = st.selectbox(
            "Select Language",
            ["English", "Hindi", "Spanish", "French", "German"],
            key="lang_selector"
        )
        
        # User authentication
        st.header("👤 User Login")
        if st.session_state.user_id is None:
            show_login_form()
        else:
            show_user_info()
    
    # Main content area
    if st.session_state.user_id is None:
        show_welcome_page()
    else:
        show_dashboard()

def show_login_form():
    """Display login/registration form"""
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                user_data = data_manager.authenticate_user(email, password)
                if user_data is not None:
                    st.session_state.user_id = user_data['user_id']
                    st.session_state.user_data = user_data
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Create New Account")
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email Address")
            phone = st.text_input("📱 Phone Number")
            age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25)
            gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
            blood_group = st.selectbox("🩸 Blood Group", 
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
            password = st.text_input("🔒 Password", type="password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password")
            
            register_btn = st.form_submit_button("Register")
            
            if register_btn:
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif not all([name, email, phone, password]):
                    st.error("❌ Please fill all required fields")
                else:
                    user_id = data_manager.create_user(name, email, phone, age, gender, blood_group, password)
                    if user_id:
                        st.success("✅ Registration successful! Please login.")
                    else:
                        st.error("❌ Email already exists")

def show_user_info():
    """Display logged-in user information"""
    st.success(f"👋 Welcome, {st.session_state.user_data['name']}!")
    if st.button("🚪 Logout"):
        st.session_state.user_id = None
        st.session_state.user_data = None
        st.rerun()

def show_welcome_page():
    """Display welcome page for non-authenticated users"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌟 Welcome to HEALTHTECH")
        st.markdown("""
        ### Your Complete Healthcare Companion
        
        HEALTHTECH is designed to make healthcare accessible to everyone, regardless of education level or technical expertise.
        
        #### 🎯 Our Mission
        To digitize and simplify healthcare services, making them available to all users through an intuitive platform.
        
        #### ⭐ Key Features:
        - 🩸 **Blood & Organ Donation**: Connect with donors and save lives
        - 🤖 **AI Health Assistant**: Get instant health guidance
        - 👨‍⚕️ **Virtual Consultations**: Consult doctors from anywhere
        - 💪 **Fitness Tracking**: Monitor your health metrics
        - 🚨 **Emergency Assistance**: Instant access to emergency services
        - 📋 **Health Records**: Secure storage of medical history
        - 🏥 **Pharmacy Locator**: Find medicines near you
        - 📚 **Health Education**: Learn about health and wellness
        - 🧠 **Mental Health Support**: Get psychological wellness help
        - 🥗 **Nutrition Planning**: Personalized diet recommendations
        - 💬 **Community Support**: Connect with others on health journeys
        
        ### 🚀 Getting Started
        1. **Register** your account using the sidebar
        2. **Complete** your health profile
        3. **Explore** all available features
        4. **Connect** with healthcare services
        """)
    
    with col2:
        st.header("📊 Quick Stats")
        
        # Show some statistics
        stats_data = {
            "Blood Donors": data_manager.get_blood_donors_count(),
            "Organ Donors": data_manager.get_organ_donors_count(),
            "Total Users": data_manager.get_users_count(),
            "Health Records": data_manager.get_health_records_count()
        }
        
        for stat_name, stat_value in stats_data.items():
            st.metric(stat_name, stat_value)
        
        st.header("🔥 Recent Activity")
        recent_activity = data_manager.get_recent_community_posts(5)
        if not recent_activity.empty:
            for _, post in recent_activity.iterrows():
                st.info(f"💬 {post['title'][:50]}...")
        else:
            st.info("No recent activity")

def show_dashboard():
    """Display main dashboard for authenticated users"""
    st.header(f"🏠 Dashboard - Welcome {st.session_state.user_data['name']}!")
    
    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🩸 Donate Blood", use_container_width=True):
            st.switch_page("pages/01_🩸_Blood_Donation.py")
    
    with col2:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("pages/03_🤖_AI_Health_Assistant.py")
    
    with col3:
        if st.button("👨‍⚕️ Book Consultation", use_container_width=True):
            st.switch_page("pages/04_👨‍⚕️_Virtual_Consultations.py")
    
    with col4:
        if st.button("🚨 Emergency", use_container_width=True):
            st.switch_page("pages/06_🚨_Emergency_Assistance.py")
    
    st.markdown("---")
    
    # Health overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Your Health Overview")
        
        # Get user's recent health data
        health_records = data_manager.get_user_health_records(st.session_state.user_id)
        
        if not health_records.empty:
            # Display recent vitals
            latest_record = health_records.iloc[-1]
            
            col_metrics = st.columns(4)
            with col_metrics[0]:
                st.metric("❤️ Heart Rate", f"{latest_record.get('heart_rate', 'N/A')} bpm")
            with col_metrics[1]:
                st.metric("🩺 Blood Pressure", f"{latest_record.get('blood_pressure', 'N/A')}")
            with col_metrics[2]:
                st.metric("⚖️ Weight", f"{latest_record.get('weight', 'N/A')} kg")
            with col_metrics[3]:
                st.metric("🌡️ Temperature", f"{latest_record.get('temperature', 'N/A')}°F")
            
            # Health trend chart
            if len(health_records) > 1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=health_records['date'],
                    y=health_records['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate',
                    line=dict(color='red')
                ))
                fig.update_layout(
                    title="Heart Rate Trend",
                    xaxis_title="Date",
                    yaxis_title="BPM",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📝 No health records found. Start tracking your health metrics!")
    
    with col2:
        st.subheader("🎯 Health Goals")
        
        # AI-generated health recommendations
        recommendations = ai_simulator.get_health_recommendations(st.session_state.user_data)
        
        st.success("💡 Today's Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            st.write(f"{i}. {rec}")
        
        st.subheader("📊 Weekly Summary")
        
        # Mock weekly stats
        weekly_stats = {
            "Steps": "8,450 avg/day",
            "Sleep": "7.2 hrs avg",
            "Water": "2.1L avg/day",
            "Exercise": "4 days"
        }
        
        for stat, value in weekly_stats.items():
            st.info(f"**{stat}**: {value}")
    
    st.markdown("---")
    
    # Recent notifications
    st.subheader("🔔 Recent Notifications")
    notifications = [
        "💊 Medication reminder: Take your vitamins",
        "🩸 Blood donation drive near you tomorrow",
        "📅 Upcoming consultation: Dr. Smith on Friday",
        "💪 Great job! You achieved your step goal yesterday"
    ]
    
    for notification in notifications:
        st.info(notification)
    
    # Community highlights
    st.subheader("🌟 Community Highlights")
    recent_posts = data_manager.get_recent_community_posts(3)
    
    if not recent_posts.empty:
        for _, post in recent_posts.iterrows():
            with st.container():
                st.write(f"**{post['title']}** - *by {post['author']}*")
                st.write(post['content'][:150] + "...")
                st.caption(f"Posted on {post['date']}")
                st.markdown("---")
    else:
        st.info("No recent community posts. Be the first to share!")

if __name__ == "__main__":
    main()
