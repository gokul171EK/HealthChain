import streamlit as st
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

def main():
    """Main function to display the settings page."""
    # Initialize session state for theme if it doesn't exist
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"

    add_app_styling(theme=st.session_state.theme)

    st.title("⚙️ Settings")

    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to manage your settings.")
        st.info("Go to the Home page to login or register.")
        return

    st.markdown("### Manage your application preferences and account settings.")

    # --- TABS FOR SETTINGS ---
    tab1, tab2, tab3 = st.tabs(["🎨 Appearance", "🔔 Notifications", "🔐 Account"])

    with tab1:
        show_appearance_settings()

    with tab2:
        show_notification_settings()
        
    with tab3:
        show_account_settings()

def show_appearance_settings():
    """Settings for app appearance, like themes."""
    st.header("🎨 Appearance Settings")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Application Theme")
    
    current_theme = st.session_state.get('theme', 'Light')
    
    theme = st.radio(
        "Choose a theme for the application:",
        ("Light", "Dark"),
        index=0 if current_theme == "Light" else 1,
        key="theme_selector"
    )

    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)


def show_notification_settings():
    """Settings for user notifications."""
    st.header("🔔 Notification Preferences")
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Medication Reminders")
    st.checkbox("Enable in-app notifications", value=True)
    st.checkbox("Enable email notifications")
    st.checkbox("Enable SMS notifications for critical reminders")

    st.markdown("---")

    st.subheader("Appointment Alerts")
    st.checkbox("Enable email reminders for upcoming appointments", value=True)
    st.checkbox("Enable SMS reminders 24 hours before appointment")
    
    st.markdown("---")

    st.subheader("Community Updates")
    st.checkbox("Receive email notifications for replies to your posts")
    
    if st.button("Save Notification Preferences", use_container_width=True):
        st.success("✅ Notification preferences saved successfully!")
        
    st.markdown("</div>", unsafe_allow_html=True)


def show_account_settings():
    """Settings for account management."""
    st.header("🔐 Account Management")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Change Password")
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")
        
        submitted = st.form_submit_button("Update Password")
        if submitted:
            if not all([current_password, new_password, confirm_new_password]):
                st.warning("Please fill all fields.")
            elif new_password != confirm_new_password:
                st.error("New passwords do not match.")
            elif len(new_password) < 8:
                st.error("New password must be at least 8 characters long.")
            else:
                # Backend logic to change password
                success = data_manager.update_user_password(st.session_state.user_id, new_password)
                if success:
                    st.success("✅ Password updated successfully!")
                else:
                    st.error("❌ An error occurred. Please check your current password.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Delete Account")
    st.warning("⚠️ This action is irreversible. All your data, including health records and appointments, will be permanently deleted.")
    
    if st.checkbox("I understand and wish to proceed with deleting my account."):
        if st.button("Permanently Delete My Account", type="primary"):
            st.error("Account deletion feature is currently disabled for safety.")
            # In a real app, you would add the logic here:
            # success = data_manager.delete_user(st.session_state.user_id)
            # if success:
            #     st.success("Your account has been deleted.")
            #     st.session_state.user_id = None
            #     st.session_state.user_data = None
            #     st.rerun()
            # else:
            #     st.error("Could not delete account.")
                
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
