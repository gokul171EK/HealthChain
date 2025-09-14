import streamlit as st
import time
from datetime import datetime
from utils.data_manager import DataManager
from utils.translator import Translator
from utils.validators import is_valid_email, is_valid_phone
from utils.styling import add_app_styling

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

def show_splash_screen():
    """Displays a splash screen for a few seconds."""
    add_app_styling(hide_sidebar=True, theme=st.session_state.theme)
    with st.container():
        st.markdown("<div class='splash-container'>", unsafe_allow_html=True)
        st.markdown("<h1 class='splash-title'>🏥 HEALTHTECH</h1>", unsafe_allow_html=True)
        st.markdown("<p class='splash-subtitle'>Your Complete Healthcare Solution</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    time.sleep(3)
    st.session_state.splash_screen_done = True
    st.rerun()

def send_sos_alert(alert_type="Medical Emergency", share_location=True, additional_info=""):
    """Displays a confirmation after an SOS alert is sent."""
    st.error("🆘 SOS ALERT SENT!")
    
    alert_details = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Type": alert_type,
        "Location": "Current location shared" if share_location else "Location not shared",
        "Additional Info": additional_info if additional_info else "No additional information provided"
    }
    
    st.subheader("📧 Alert Sent To Your Emergency Contacts")
    st.info("Help is on the way. Please stay calm and in a safe place if possible.")
    
    st.subheader("📋 Alert Details:")
    for key, value in alert_details.items():
        st.write(f"**{key}:** {value}")

def run_app():
    """Main application logic after splash screen."""
    # Apply theme from session state
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    add_app_styling(theme=st.session_state.theme)
    
    # Set language from session state
    translator.set_language(st.session_state.language)
    T = translator.get

    # --- FLOATING SOS BUTTON ---
    st.markdown('<div class="sos-button-container">', unsafe_allow_html=True)
    if st.button("SOS"):
        if 'user_id' in st.session_state and st.session_state.user_id:
            with st.dialog("Confirm Emergency Alert"):
                st.warning("Are you sure you want to send an SOS alert?")
                st.info("This will immediately notify your emergency contacts and share your location.")
                col1, col2 = st.columns(2)
                if col1.button("✅ Confirm"):
                    send_sos_alert()
                if col2.button("❌ Cancel"):
                    st.rerun()
        else:
            with st.dialog("Emergency Alert"):
                st.error("You are not logged in.")
                st.info("Please call emergency services directly: **102** for Ambulance, **100** for Police.")
                if st.button("Close"):
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


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
            if st.button("Google ", use_container_width=True): # Space to make key unique
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
    st.header(f"🌟 {T('welcome_header')}")
    st.markdown(T('welcome_subheader'))
    st.markdown("Our mission is to provide an accessible and comprehensive digital health platform that empowers you to take control of your well-being.")
    st.markdown("---")
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
    col1, col2, col3, col4, col5 = st.columns(5) # Changed to 5 columns
    if col1.button(f"🩸 {T('donate_blood')}", use_container_width=True): st.switch_page("pages/01_🩸_Blood_Donation.py")
    if col2.button(f"🤖 {T('ai_assistant')}", use_container_width=True): st.switch_page("pages/03_🤖_AI_Health_Assistant.py")
    if col3.button(f"👨‍⚕️ {T('book_consultation')}", use_container_width=True): st.switch_page("pages/04_👨‍⚕️_Virtual_Consultations.py")
    if col4.button(f"🚨 {T('emergency')}", use_container_width=True): st.switch_page("pages/06_🚨_Emergency_Assistance.py")
    if col5.button("🤝 Community", use_container_width=True): st.switch_page("pages/12_🤝_Community.py") # Added Community button
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"📈 {T('health_overview')}")
        # Add chart logic here later
        st.info(f"📝 {T('no_health_records')}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader(f"🎯 {T('health_goals')}")
        st.success(f"💡 {T('todays_recommendations')}")
        # Add recommendation logic here
        st.write("1. Drink 8 glasses of water.")
        st.write("2. Take a 30-minute walk.")
        st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Main function to run the app."""
    if not st.session_state.splash_screen_done:
        show_splash_screen()
    else:
        run_app()

if __name__ == "__main__":
    main()

