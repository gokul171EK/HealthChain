
import streamlit as st
import time
from datetime import datetime
from utils.data_manager import DataManager
from utils.translator import Translator
from utils.validators import is_valid_email, is_valid_phone
from utils.styling import add_app_styling, splash_screen


# --- Resource Initialization (with caching) ---
@st.cache_resource
def init_data_manager():
    return DataManager()

@st.cache_resource
def init_translator():
    return Translator()

data_manager = init_data_manager()
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
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
# Add session state keys for SOS dialogs
if 'show_sos_dialog' not in st.session_state:
    st.session_state.show_sos_dialog = False
if 'show_login_sos_dialog' not in st.session_state:
    st.session_state.show_login_sos_dialog = False


# --- Splash Screen Function ---
def splash_screen():
    st.markdown(
        """
        <div class="splash-container">
            <div class="splash-title">HEALTHTECH</div>
            <div class="splash-subtitle">A Complete Healthcare Solution For All</div>
        </div>
        <style>
        /* Hide sidebar during splash */
        section[data-testid="stSidebar"] {display: none;}
        </style>
        <style>
        .splash-container {
            position: fixed;
            top: 0; left: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #ffffff;
            z-index: 9999;
        }
        .splash-title {
            font-size: 4rem;
            font-weight: 800;
            color: #007bff;
            animation: zoomFade 1.5s ease-out forwards;
        }
        .splash-subtitle {
            font-size: 1.5rem;
            color: #6c757d;
            animation: fadeInUp 2s ease forwards;
            animation-delay: 0.7s;
            opacity: 0;
        }
        @keyframes zoomFade {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        @keyframes fadeInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def send_sos_alert():
    """Displays a confirmation after an SOS alert is sent."""
    st.toast("🆘 SOS ALERT SENT!", icon="🚨")
    st.session_state.show_sos_dialog = False # Close dialog after sending
    st.rerun()


def run_app():
    """Main application logic after splash screen."""
    # Apply theme from session state
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    add_app_styling(theme=st.session_state.theme)
    # Fix: set translator language and alias get()
    translator.set_language(st.session_state.language)
    T = translator.get

    # --- Hero Section ---
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #f0f8ff, #e6f2ff);
            border-radius: 16px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        ">
            <h1 style="color:#007bff; font-weight:800; font-size:3rem; margin-bottom:10px;">
                Welcome to HEALTHTECH
            </h1>
            <h3 style="color:#6c757d; font-weight:400; margin-bottom:20px;">
                Empowering Your Health Journey
            </h3>
            <p style="max-width:700px; margin:0 auto; font-size:1.1rem; color:#333;">
                Our mission is to provide an accessible and comprehensive digital health platform 
                that empowers you to take control of your well-being.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- Styled SOS Button ---
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color:#dc3545;
            color:white;
            font-size:1.5rem;
            font-weight:700;
            padding:15px 40px;
            border:none;
            border-radius:12px;
            cursor:pointer;
            transition:all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            background-color:#b02a37;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='text-align:center; margin-top:20px;'>", unsafe_allow_html=True)
    if st.button("🚨 SOS"):
        if st.session_state.user_id:
            st.session_state.show_sos_dialog = True
        else:
            st.session_state.show_login_sos_dialog = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # --- SOS Dialogs ---
    if st.session_state.get('show_sos_dialog', False):
        with st.container():
            st.markdown("### 🚨 Confirm Emergency Alert")
            st.warning("Are you sure you want to send an SOS alert?")
            st.info("This will immediately notify your emergency contacts and share your location.")
            col1, col2 = st.columns(2)
            if col1.button("✅ Confirm"):
                send_sos_alert()
            if col2.button("❌ Cancel"):
                st.session_state.show_sos_dialog = False
                st.rerun()

    if st.session_state.get('show_login_sos_dialog', False):
        with st.container():
            st.markdown("### 🚨 Emergency Alert")
            st.error("You are not logged in.")
            st.info("Please call emergency services directly: **102** for Ambulance, **100** for Police.")
            if st.button("Close"):
                st.session_state.show_login_sos_dialog = False
                st.rerun()
            

    # Sidebar
    with st.sidebar:
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.header(f"🌐 {T('language_header')}")
        st.session_state.language = st.selectbox(
            T("language_select_label"),
            ["English", "Tamil", "Hindi", "Spanish"],
            key="lang_selector"
        )
        st.markdown("---")

        st.header(f"👤 {T('user_login_header')}")
        if st.session_state.user_id is None:
            show_login_form(T)
        else:
            show_user_info(T)
        
        st.markdown("---")
        st.markdown("### Connect With Me")
        st.markdown(
            """
            <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
                <a href="https://www.linkedin.com/" target="_blank" style="text-decoration: none;">
                    <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="LinkedIn" width="32">
                </a>
                <a href="https://github.com/" target="_blank" style="text-decoration: none;">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" width="32">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    if st.session_state.user_id is None:
        show_welcome_page(T)
    else:
        show_dashboard(T)
    st.markdown("</div>", unsafe_allow_html=True)

def show_login_form(T):
    """Display login/registration form with validation, security, and social login options."""
    tab1, tab2 = st.tabs([f"🔑 {T('login_tab')}", f"📝 {T('register_tab')}"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input(f"📧 {T('email')}")
            password = st.text_input(f"🔒 {T('password')}", type="password")
            login_btn = st.form_submit_button(T('login_button'), use_container_width=True)

            if login_btn:
                user_data = data_manager.authenticate_user(email, password)
                if user_data:
                    st.session_state.user_id = user_data['user_id']
                    st.session_state.user_data = user_data
                    st.success(f"✅ {T('login_success')}")
                    st.rerun()
                else:
                    st.error(f"❌ {T('invalid_credentials')}")
        
        st.markdown("<div style='text-align: center; margin: 1rem 0;'>or continue with</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Google", use_container_width=True):
                st.info("Social login feature coming soon!")
        with col2:
            if st.button("Facebook", use_container_width=True):
                st.info("Social login feature coming soon!")
        with col3:
            if st.button("X", use_container_width=True):
                st.info("Social login feature coming soon!")

    with tab2:
        with st.form("register_form"):
            st.subheader(T('create_account_subheader'))
            name = st.text_input(f"👤 {T('full_name')}")
            email = st.text_input(f"📧 {T('email')}")
            phone = st.text_input(f"📱 {T('phone_number')}")
            age = st.number_input(f"🎂 {T('age')}", min_value=1, max_value=120, value=25)
            gender = st.selectbox(f"⚧ {T('gender')}", ["Male", "Female", "Other"])
            password = st.text_input(f"🔒 {T('password')}", type="password")
            confirm_password = st.text_input(f"🔒 {T('confirm_password')}", type="password")
            register_btn = st.form_submit_button(T('register_button'), use_container_width=True)

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
        
        st.markdown("<div style='text-align: center; margin: 1rem 0;'>or sign up with</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Google ", use_container_width=True):
                st.info("Social login feature coming soon!")
        with col2:
            if st.button("Facebook ", use_container_width=True):
                st.info("Social login feature coming soon!")
        with col3:
            if st.button("X ", use_container_width=True):
                st.info("Social login feature coming soon!")

def show_user_info(T):
    """Display logged-in user information and logout button."""
    if st.session_state.user_data:
        st.success(f"👋 {T('welcome_message', name=st.session_state.user_data['name'])}")
    if st.button(f"🚪 {T('logout_button')}", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.user_data = None
        st.rerun()

def show_welcome_page(T):
    """Display welcome page for non-authenticated users."""
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Key Features:")
    st.markdown("""
    - **🤖 AI Health Assistant**: Get instant insights with our AI-powered symptom checker.
    - **👨‍⚕️ Virtual Consultations**: Connect with healthcare professionals from home.
    - **💪 Fitness & Mood Tracking**: Monitor your physical and mental health seamlessly.
    - **🚨 Emergency Support**: Quick access to helplines and nearby hospitals.
    """)
    st.markdown("</div>", unsafe_allow_html=True)


def show_dashboard(T):
    """Display main dashboard with dynamic data."""
    st.header(f"🏠 {T('dashboard_title', name=st.session_state.user_data.get('name', 'User'))}")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"⚡ {T('quick_actions')}")
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button(f"🩸 {T('donate_blood')}", use_container_width=True): st.switch_page("pages/01_🩸_Blood_Donation.py")
    if col2.button(f"🤖 {T('ai_assistant')}", use_container_width=True): st.switch_page("pages/03_🤖_AI_Health_Assistant.py")
    if col3.button(f"👨‍⚕️ {T('book_consultation')}", use_container_width=True): st.switch_page("pages/04_👨‍⚕️_Virtual_Consultations.py")
    if col4.button(f"🚨 {T('emergency')}", use_container_width=True): st.switch_page("pages/06_🚨_Emergency_Assistance.py")
    if col5.button("🤝 Community", use_container_width=True): st.switch_page("pages/12_🤝_Community.py")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"📈 {T('health_overview')}")
        st.info(f"📝 {T('no_health_records')}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"🎯 {T('health_goals')}")
        st.success(f"💡 {T('todays_recommendations')}")
        st.write("1. Drink 8 glasses of water.")
        st.write("2. Take a 30-minute walk.")
        st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main function to run the app."""
        # --- Entry point ---
if "splash_done" not in st.session_state:
    splash_screen()
    time.sleep(3)
    st.session_state.splash_done = True
    st.rerun()
else:
    run_app()

if __name__ == "__main__":
    main()
