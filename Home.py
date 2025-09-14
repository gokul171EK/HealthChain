import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import bcrypt
import time
from utils.data_manager import DataManager
from utils.ai_simulator import AISimulator
from utils.translator import Translator
from utils.styling import add_app_styling
from utils.validators import is_valid_email, is_valid_phone

# --- Page Configuration ---
st.set_page_config(
    page_title="HEALTHTECH - Complete Healthcare Solution",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Resource Initialization (with caching) ---
@st.cache_resource
def init_data_manager():
    return DataManager()

@st.cache_resource
def init_ai_simulator():
    return AISimulator()

@st.cache_resource
def init_translator():
    return Translator()

data_manager = init_data_manager()
ai_simulator = init_ai_simulator()
translator = init_translator()

# --- Session State Initialization ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'splash_screen_done' not in st.session_state:
    st.session_state.splash_screen_done = False

# --- Main Application Logic ---
def main():
    add_app_styling()
    """Handles the display of the splash screen or the main app."""
    if not st.session_state.splash_screen_done:
        show_splash_screen()
    else:
        run_app()

def show_splash_screen():
    """Displays the splash screen and hides the sidebar."""
    # Custom CSS to hide the sidebar and style the splash screen
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
            .stApp {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: scale(0.9); }
                100% { opacity: 1; transform: scale(1); }
            }
            .splash-container {
                animation: fadeIn 1.5s ease-in-out;
                text-align: center;
            }
            .splash-title {
                font-size: 5em;
                color: #0068C9;
                font-weight: bold;
            }
            .splash-subtitle {
                font-size: 1.5em;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div class="splash-container">
                <div class="splash-title">🏥 HEALTHTECH</div>
                <p class="splash-subtitle">Your Complete Healthcare Solution</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.spinner('Loading your personalized dashboard...'):
            time.sleep(3)
    
    st.session_state.splash_screen_done = True
    st.rerun()

def run_app():
    """The main application logic after the splash screen."""
    translator.set_language(st.session_state.language)
    T = translator.get

    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏥 HEALTHTECH")
        st.subheader(T("app_subheader"))
        st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header(f"🌐 {T('language_header')}")
        st.session_state.language = st.selectbox(
            T("language_select_label"),
            ["Tamil", "English", "Hindi", "Spanish"],
            key="lang_selector"
        )

        st.header(f"👤 {T('user_login_header')}")
        if st.session_state.user_id is None:
            show_login_form(T)
        else:
            show_user_info(T)
        
        st.markdown("---")
        st.markdown("### Connect With Me")
        st.markdown(
            "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)"
        )
        st.markdown(
            "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)"
        )


    # Main content area
    if st.session_state.user_id is None:
        show_welcome_page(T)
    else:
        show_dashboard(T)

def show_login_form(T):
    """Display login/registration form with validation and security."""
    tab1, tab2 = st.tabs([f"🔑 {T('login_tab')}", f"📝 {T('register_tab')}"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input(f"📧 {T('email')}")
            password = st.text_input(f"🔒 {T('password')}", type="password")
            login_btn = st.form_submit_button(T('login_button'))

            if login_btn:
                user_data = data_manager.authenticate_user(email, password)
                if user_data:
                    st.session_state.user_id = user_data['user_id']
                    st.session_state.user_data = user_data
                    st.success(f"✅ {T('login_success')}")
                    st.rerun()
                else:
                    st.error(f"❌ {T('invalid_credentials')}")

    with tab2:
        with st.form("register_form"):
            st.subheader(T('create_account_subheader'))
            name = st.text_input(f"👤 {T('full_name')}")
            email = st.text_input(f"📧 {T('email')}")
            phone = st.text_input(f"📱 {T('phone_number')}")
            age = st.number_input(f"🎂 {T('age')}", min_value=1, max_value=120, value=25)
            gender = st.selectbox(f"⚧ {T('gender')}", [T('male'), T('female'), T('other')])
            password = st.text_input(f"🔒 {T('password')}", type="password")
            confirm_password = st.text_input(f"🔒 {T('confirm_password')}", type="password")
            register_btn = st.form_submit_button(T('register_button'))

            if register_btn:
                if password != confirm_password:
                    st.error(T('passwords_no_match'))
                elif len(password) < 8:
                    st.error(T('password_too_short'))
                elif not is_valid_email(email):
                    st.error(T('invalid_email'))
                elif not is_valid_phone(phone):
                    st.error(T('invalid_phone'))
                elif not all([name, email, phone, password]):
                    st.error(T('fill_all_fields'))
                else:
                    user_id = data_manager.create_user(name, email, phone, age, gender, 'Unknown', password)
                    
                    if user_id:
                        st.success(f"✅ {T('registration_success')}")
                        st.session_state.user_id = user_id
                        st.session_state.user_data = data_manager.get_user_by_id(user_id)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(T('email_exists'))

def show_user_info(T):
    """Display logged-in user information and logout button."""
    st.success(f"👋 {T('welcome_message', name=st.session_state.user_data['name'])}")
    if st.button(f"🚪 {T('logout_button')}"):
        st.session_state.user_id = None
        st.session_state.user_data = None
        st.session_state.splash_screen_done = False
        st.rerun()

def show_welcome_page(T):
    """Display welcome page for non-authenticated users."""
    st.header(f"🌟 {T('welcome_header')}")
    st.markdown("Your one-stop solution for managing health records, connecting with doctors, and accessing vital health services.")
    st.markdown("""
    **Our Mission:** To empower individuals to take control of their health through accessible and intuitive technology.
    
    **Key Features:**
    - **🏥 Health Records:** Securely store and manage your medical history.
    - **👨‍⚕️ Virtual Consultations:** Connect with doctors from the comfort of your home.
    - **🤖 AI Health Assistant:** Get instant insights with our AI-powered symptom checker.
    - **🩸 Donation Center:** Find or become a blood/organ donor and save lives.
    - **💪 Fitness Tracker:** Monitor your activity, set goals, and stay motivated.
    """)

def show_dashboard(T):
    """Display main dashboard with dynamic data."""
    st.header(f"🏠 {T('dashboard_title', name=st.session_state.user_data['name'])}")

    st.subheader(f"⚡ {T('quick_actions')}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(f"🩸 {T('donate_blood')}", use_container_width=True): st.switch_page("pages/blood_donation.py")
    with col2:
        if st.button(f"🤖 {T('ai_assistant')}", use_container_width=True): st.switch_page("pages/ai_health_assistant.py")
    with col3:
        if st.button(f"👨‍⚕️ {T('book_consultation')}", use_container_width=True): st.switch_page("pages/consultation.py")
    with col4:
        if st.button(f"🚨 {T('emergency')}", use_container_width=true): st.switch_page("pages/emergency.py")
    
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"📈 {T('health_overview')}")
        health_records = data_manager.get_user_health_records(st.session_state.user_id)
        if not health_records.empty:
            weight_data = health_records.dropna(subset=['weight']).tail(5)
            if not weight_data.empty:
                fig = go.Figure(go.Scatter(x=weight_data['date'], y=weight_data['weight'], mode='lines+markers'))
                fig.update_layout(title="Recent Weight Trend", xaxis_title="Date", yaxis_title="Weight (kg)")
                st.plotly_chart(fig, use_container_width=True)
            else:
                 st.info(f"📝 {T('no_health_records')}")
        else:
            st.info(f"📝 {T('no_health_records')}")

    with col2:
        st.subheader(f"🎯 {T('health_goals')}")
        recommendations = ai_simulator.get_health_recommendations(st.session_state.user_data)
        st.success(f"💡 {T('todays_recommendations')}")
        for i, rec in enumerate(recommendations[:3], 1):
            st.write(f"{i}. {rec}")

        st.subheader(f"📊 {T('weekly_summary')}")
        weekly_stats = {
            "Steps": "45,678",
            "Sleep": "7.2h avg",
            "Water": "2.1L avg",
            "Exercise": "4 sessions"
        }
        for stat, value in weekly_stats.items():
            st.info(f"**{T(stat.lower())}**: {value}")

if __name__ == "__main__":
    main()

