import streamlit as st
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

def main():
    """Main function to display the profile page."""
    
    add_app_styling()

    # Make sure this session state check is at the top of the function
    if 'theme' not in st.session_state:
      st.session_state.theme = "Light"

    add_app_styling(theme=st.session_state.theme)

    st.title("👤 User Profile")
    st.markdown("### Manage your account details and preferences.")

    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to view your profile.")
        st.info("Go to the Home page to login or register.")
        return

    # Load user data from session state
    user_data = st.session_state.user_data

    # --- TABS FOR DIFFERENT PROFILE SECTIONS ---
    tab1, tab2, tab3 = st.tabs(["📋 My Details", "🔒 Change Password", "📊 Account Stats"])

    with tab1:
        show_profile_details(user_data)

    with tab2:
        show_password_change(user_data['user_id'])

    with tab3:
        show_account_stats(user_data)


def show_profile_details(user_data):
    """Display and edit user profile details."""
    st.header("📋 My Details")
    
    with st.form("edit_profile_form"):
        st.markdown("##### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=user_data.get('name', ''))
            age = st.number_input("Age", min_value=1, max_value=120, value=int(user_data.get('age', 25)))
            blood_group = st.selectbox(
                "Blood Group",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"],
                index=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"].index(user_data.get('blood_group', 'Unknown'))
            )

        with col2:
            phone = st.text_input("Phone Number", value=user_data.get('phone', ''))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user_data.get('gender', 'Male')))
            email = st.text_input("Email Address (cannot be changed)", value=user_data.get('email', ''), disabled=True)

        st.markdown("---")
        
        submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
        if submitted:
            # Call the DataManager to update the user's profile
            success = data_manager.update_user_profile(
                user_data['user_id'], name, phone, age, gender, blood_group
            )

            if success:
                st.success("✅ Profile updated successfully!")
                # IMPORTANT: Update the session state so the user sees the changes immediately
                st.session_state.user_data['name'] = name
                st.session_state.user_data['phone'] = phone
                st.session_state.user_data['age'] = age
                st.session_state.user_data['gender'] = gender
                st.session_state.user_data['blood_group'] = blood_group
                st.rerun()
            else:
                st.error("❌ Failed to update profile. Please try again.")

def show_password_change(user_id):
    """Handle password change."""
    st.header("🔒 Change Password")

    with st.form("change_password_form"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        submitted = st.form_submit_button("🔑 Update Password", use_container_width=True)
        if submitted:
            if not new_password or len(new_password) < 8:
                st.warning("Password must be at least 8 characters long.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Call DataManager to update the password
                success = data_manager.update_user_password(user_id, new_password)
                if success:
                    st.success("🎉 Password updated successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to update password. Please try again.")


def show_account_stats(user_data):
    """Display user account statistics."""
    st.header("📊 Account Statistics")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Account Created", value=user_data.get('created_date', 'N/A'))
        
    with col2:
        # Get total health records
        health_records = data_manager.get_user_health_records(user_data['user_id'])
        st.metric(label="Total Health Records", value=len(health_records))

    with col3:
        # Get total appointments
        appointments = data_manager.get_user_appointments(user_data['user_id'])
        st.metric(label="Total Appointments", value=len(appointments))

if __name__ == "__main__":
    main()
