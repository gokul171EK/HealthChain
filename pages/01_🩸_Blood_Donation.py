import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static
from utils.data_manager import DataManager

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Blood Donation - HEALTHTECH",
    page_icon="🩸",
    layout="wide"
)

def main():
    st.title("🩸 Blood Donation Center")
    st.markdown("### Save Lives Through Blood Donation")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access blood donation features")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Become Donor", 
        "🔍 Find Donors", 
        "🏥 Blood Banks", 
        "📢 Urgent Requests", 
        "📊 My Donations"
    ])
    
    with tab1:
        show_donor_registration()
    
    with tab2:
        show_find_donors()
    
    with tab3:
        show_blood_banks()
    
    with tab4:
        show_urgent_requests()
    
    with tab5:
        show_donation_history()

def show_donor_registration():
    """Blood donor registration form"""
    st.header("🎯 Register as Blood Donor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Donor Information")
        
        with st.form("donor_registration"):
            # Get user's blood group from profile
            user_data = st.session_state.user_data
            blood_group = st.selectbox(
                "🩸 Blood Group",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                index=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(user_data.get('blood_group', 'O+'))
            )
            
            location = st.text_input("📍 Location (City, State)", placeholder="e.g., Mumbai, Maharashtra")
            
            contact = st.text_input("📱 Contact Number", value=user_data.get('phone', ''))
            
            last_donation = st.date_input(
                "📅 Last Donation Date (if any)",
                value=None,
                help="Leave blank if you're a first-time donor"
            )
            
            # Health eligibility checklist
            st.subheader("✅ Health Eligibility Checklist")
            col_check1, col_check2 = st.columns(2)
            
            with col_check1:
                age_eligible = st.checkbox("I am between 18-65 years old")
                weight_eligible = st.checkbox("I weigh at least 50 kg")
                health_good = st.checkbox("I am in good health")
                
            with col_check2:
                no_diseases = st.checkbox("No major diseases or infections")
                no_recent_illness = st.checkbox("No recent illness or fever")
                consent = st.checkbox("I consent to donate blood voluntarily")
            
            submit_btn = st.form_submit_button("🩸 Register as Donor", use_container_width=True)
            
            if submit_btn:
                # Validate eligibility
                eligibility_checks = [age_eligible, weight_eligible, health_good, no_diseases, no_recent_illness, consent]
                
                if not all(eligibility_checks):
                    st.error("❌ Please complete all eligibility requirements")
                elif not location or not contact:
                    st.error("❌ Please fill in all required fields")
                else:
                    # Register donor
                    last_donation_str = last_donation.strftime("%Y-%m-%d") if last_donation else None
                    donor_id = data_manager.register_blood_donor(
                        st.session_state.user_id,
                        blood_group,
                        location,
                        contact,
                        last_donation_str
                    )
                    
                    if donor_id:
                        st.success("🎉 Successfully registered as blood donor!")
                        st.balloons()
                        st.info("You will be notified when someone needs your blood type in your area.")
                    else:
                        st.error("❌ Error registering as donor. Please try again.")
    
    with col2:
        st.subheader("📊 Blood Donation Facts")
        
        facts = [
            "🩸 One blood donation can save up to 3 lives",
            "⏰ Donation process takes only 10-15 minutes",
            "🔄 You can donate every 8-12 weeks",
            "💪 Your body replaces donated blood within 24-48 hours",
            "🌟 1 in 7 people entering hospitals need blood",
            "❤️ Only 3% of eligible people donate blood annually"
        ]
        
        for fact in facts:
            st.info(fact)
        
        st.subheader("🎁 Benefits of Donating")
        benefits = [
            "Free health screening",
            "Reduced risk of heart disease",
            "Burns calories (650 per donation)",
            "Sense of community service",
            "Regular health monitoring"
        ]
        
        for benefit in benefits:
            st.success(f"✅ {benefit}")

def show_find_donors():
    """Find blood donors in the system"""
    st.header("🔍 Find Blood Donors")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Search Criteria")
        
        blood_group_needed = st.selectbox(
            "🩸 Blood Group Required",
            ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )
        
        location_filter = st.text_input("📍 Location Filter", placeholder="City or State")
        
        search_btn = st.button("🔍 Search Donors", use_container_width=True)
    
    with col2:
        st.subheader("👥 Available Donors")
        
        if search_btn or blood_group_needed != "All":
            # Get donors from database
            if blood_group_needed == "All":
                donors_df = data_manager.get_blood_donors()
            else:
                donors_df = data_manager.get_blood_donors(blood_group_needed)
            
            if not donors_df.empty:
                # Filter by location if specified
                if location_filter:
                    donors_df = donors_df[donors_df['location'].str.contains(location_filter, case=False, na=False)]
                
                if not donors_df.empty:
                    st.success(f"Found {len(donors_df)} donors")
                    
                    for _, donor in donors_df.iterrows():
                        with st.container():
                            col_info, col_contact = st.columns([2, 1])
                            
                            with col_info:
                                st.write(f"🩸 **Blood Group:** {donor['blood_group']}")
                                st.write(f"📍 **Location:** {donor['location']}")
                                st.write(f"📊 **Total Donations:** {donor['total_donations']}")
                                if donor['last_donation']:
                                    st.write(f"📅 **Last Donation:** {donor['last_donation']}")
                            
                            with col_contact:
                                if st.button(f"📞 Contact", key=f"contact_{donor['donor_id']}"):
                                    st.info(f"Contact: {donor['contact']}")
                                
                                available_status = "✅ Available" if donor['available'] else "❌ Not Available"
                                st.write(available_status)
                            
                            st.markdown("---")
                else:
                    st.warning("No donors found for the specified criteria")
            else:
                st.info("No donors registered yet. Be the first to register!")
        else:
            st.info("Use the search criteria to find blood donors")

def show_blood_banks():
    """Display blood banks and their information"""
    st.header("🏥 Blood Banks Directory")
    
    # Sample blood banks data (in real app, this would come from database)
    blood_banks_data = [
        {
            "name": "City General Hospital Blood Bank",
            "address": "123 Main Street, Downtown",
            "phone": "+91-123-456-7890",
            "email": "bloodbank@cityhospital.com",
            "available_types": "All blood types",
            "hours": "24/7"
        },
        {
            "name": "Red Cross Blood Center",
            "address": "456 Health Avenue, Medical District",
            "phone": "+91-987-654-3210",
            "email": "donate@redcross.org",
            "available_types": "A+, B+, O+, AB-",
            "hours": "8 AM - 6 PM"
        },
        {
            "name": "Community Blood Bank",
            "address": "789 Care Lane, Suburb Area",
            "phone": "+91-555-123-4567",
            "email": "info@communityblood.org",
            "available_types": "O-, A-, B-",
            "hours": "9 AM - 5 PM"
        }
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for i, bank in enumerate(blood_banks_data):
            with st.expander(f"🏥 {bank['name']}", expanded=i==0):
                col_info, col_action = st.columns([3, 1])
                
                with col_info:
                    st.write(f"📍 **Address:** {bank['address']}")
                    st.write(f"📞 **Phone:** {bank['phone']}")
                    st.write(f"📧 **Email:** {bank['email']}")
                    st.write(f"🩸 **Available Types:** {bank['available_types']}")
                    st.write(f"🕐 **Hours:** {bank['hours']}")
                
                with col_action:
                    if st.button("📞 Call", key=f"call_bank_{i}"):
                        st.success(f"Calling {bank['phone']}")
                    
                    if st.button("📧 Email", key=f"email_bank_{i}"):
                        st.success(f"Opening email to {bank['email']}")
    
    with col2:
        st.subheader("🗺️ Blood Bank Locations")
        
        # Create a simple map showing blood bank locations
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)  # Default to Delhi coordinates
        
        # Sample coordinates for blood banks
        bank_coords = [
            [28.6139, 77.2090],
            [28.6219, 77.2273],
            [28.6061, 77.2025]
        ]
        
        for i, (bank, coord) in enumerate(zip(blood_banks_data, bank_coords)):
            folium.Marker(
                coord,
                popup=f"🏥 {bank['name']}\n📞 {bank['phone']}",
                tooltip=bank['name'],
                icon=folium.Icon(color='red', icon='plus')
            ).add_to(m)
        
        folium_static(m, width=300, height=400)
        
        st.subheader("📊 Blood Inventory Status")
        
        # Sample blood inventory data
        inventory_data = {
            "Blood Type": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            "Units Available": [45, 12, 38, 8, 15, 5, 62, 18],
            "Status": ["Good", "Low", "Good", "Critical", "Fair", "Critical", "Good", "Fair"]
        }
        
        inventory_df = pd.DataFrame(inventory_data)
        
        for _, row in inventory_df.iterrows():
            color = "green" if row['Status'] == "Good" else "orange" if row['Status'] == "Fair" else "red"
            st.markdown(f"🩸 **{row['Blood Type']}**: {row['Units Available']} units - "
                       f"<span style='color:{color}'>{row['Status']}</span>", unsafe_allow_html=True)

def show_urgent_requests():
    """Display urgent blood requests"""
    st.header("📢 Urgent Blood Requests")
    
    # Sample urgent requests
    urgent_requests = [
        {
            "patient": "Emergency Patient #1",
            "blood_type": "O-",
            "units_needed": 3,
            "hospital": "City General Hospital",
            "urgency": "Critical",
            "time_posted": "2 hours ago",
            "contact": "+91-911-emergency"
        },
        {
            "patient": "Surgery Patient #2",
            "blood_type": "A+",
            "units_needed": 2,
            "hospital": "Care Medical Center",
            "urgency": "High",
            "time_posted": "5 hours ago",
            "contact": "+91-987-654-3210"
        },
        {
            "patient": "Accident Victim #3",
            "blood_type": "B+",
            "units_needed": 4,
            "hospital": "Trauma Center",
            "urgency": "Critical",
            "time_posted": "1 hour ago",
            "contact": "+91-123-456-7890"
        }
    ]
    
    st.warning("⚠️ These are urgent requests that need immediate attention!")
    
    for i, request in enumerate(urgent_requests):
        urgency_color = "red" if request['urgency'] == "Critical" else "orange"
        
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"🏥 **Hospital:** {request['hospital']}")
                st.markdown(f"🩸 **Blood Type Needed:** {request['blood_type']}")
                st.markdown(f"📊 **Units Required:** {request['units_needed']}")
                st.markdown(f"🕐 **Posted:** {request['time_posted']}")
            
            with col2:
                st.markdown(f"⚡ **Urgency:** <span style='color:{urgency_color}'>{request['urgency']}</span>", 
                           unsafe_allow_html=True)
                st.markdown(f"📞 **Contact:** {request['contact']}")
            
            with col3:
                if st.button(f"🆘 Respond", key=f"respond_{i}", use_container_width=True):
                    st.success("Thank you for responding! The hospital will be notified of your willingness to donate.")
                
                if st.button(f"📞 Call Hospital", key=f"call_{i}", use_container_width=True):
                    st.info(f"Calling {request['contact']}")
            
            st.markdown("---")
    
    st.subheader("📝 Create Urgent Request")
    
    with st.expander("🏥 For Healthcare Providers"):
        with st.form("urgent_request"):
            col1, col2 = st.columns(2)
            
            with col1:
                hospital_name = st.text_input("🏥 Hospital Name")
                blood_type_req = st.selectbox("🩸 Blood Type Required", 
                                            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
                units_required = st.number_input("📊 Units Required", min_value=1, max_value=10, value=1)
            
            with col2:
                urgency_level = st.selectbox("⚡ Urgency Level", ["High", "Critical"])
                contact_number = st.text_input("📞 Contact Number")
                additional_notes = st.text_area("📝 Additional Notes")
            
            submit_request = st.form_submit_button("📢 Post Urgent Request")
            
            if submit_request:
                if all([hospital_name, blood_type_req, contact_number]):
                    st.success("✅ Urgent request posted successfully!")
                    st.info("Registered donors with matching blood type will be notified immediately.")
                else:
                    st.error("❌ Please fill all required fields")

def show_donation_history():
    """Show user's donation history and statistics"""
    st.header("📊 My Donation History")
    
    user_id = st.session_state.user_id
    
    # Check if user is registered as donor
    donors_df = data_manager.get_blood_donors()
    user_donor = donors_df[donors_df['user_id'] == user_id]
    
    if user_donor.empty:
        st.info("🎯 You haven't registered as a blood donor yet.")
        if st.button("Register as Donor"):
            st.experimental_rerun()
        return
    
    donor_info = user_donor.iloc[0]
    
    # Display donor statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🩸 Blood Group", donor_info['blood_group'])
    
    with col2:
        st.metric("📊 Total Donations", donor_info['total_donations'])
    
    with col3:
        last_donation = donor_info['last_donation'] if donor_info['last_donation'] else "Never"
        st.metric("📅 Last Donation", last_donation)
    
    with col4:
        status = "✅ Available" if donor_info['available'] else "❌ Not Available"
        st.metric("📋 Status", status)
    
    st.markdown("---")
    
    # Sample donation history
    donation_history = [
        {"date": "2024-08-15", "location": "City Hospital", "units": 1, "purpose": "Emergency Surgery"},
        {"date": "2024-05-10", "location": "Red Cross Center", "units": 1, "purpose": "Blood Drive"},
        {"date": "2024-02-22", "location": "Community Center", "units": 1, "purpose": "Accident Victim"},
        {"date": "2023-11-08", "location": "City Hospital", "units": 1, "purpose": "Cancer Patient"}
    ]
    
    if donation_history:
        st.subheader("📈 Donation Timeline")
        
        # Create timeline chart
        df_history = pd.DataFrame(donation_history)
        df_history['date'] = pd.to_datetime(df_history['date'])
        
        fig = px.scatter(df_history, x='date', y='units', 
                        hover_data=['location', 'purpose'],
                        title="Donation History Timeline",
                        labels={'date': 'Date', 'units': 'Units Donated'})
        
        fig.update_traces(marker=dict(size=15, color='red'))
        st.plotly_chart(fig, use_container_width=True)
        
        # Display detailed history
        st.subheader("📋 Detailed History")
        
        for donation in donation_history:
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
                
                with col1:
                    st.write(f"📅 {donation['date']}")
                
                with col2:
                    st.write(f"🏥 {donation['location']}")
                
                with col3:
                    st.write(f"🩸 {donation['units']} unit(s)")
                
                with col4:
                    st.write(f"🎯 {donation['purpose']}")
                
                st.markdown("---")
        
        # Achievements and badges
        st.subheader("🏆 Achievements")
        
        total_donations = len(donation_history)
        achievements = []
        
        if total_donations >= 1:
            achievements.append("🥉 First Time Donor")
        if total_donations >= 5:
            achievements.append("🥈 Regular Donor")
        if total_donations >= 10:
            achievements.append("🥇 Frequent Donor")
        if total_donations >= 25:
            achievements.append("🏆 Super Donor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            for achievement in achievements:
                st.success(achievement)
        
        with col2:
            st.info("💡 **Next Goal**: Reach 5 donations to earn 'Regular Donor' badge!")
    
    else:
        st.info("No donation history found. Your first donation will appear here!")
    
    # Next eligible donation date
    if donor_info['last_donation']:
        last_date = pd.to_datetime(donor_info['last_donation'])
        next_eligible = last_date + timedelta(weeks=8)  # 8 weeks gap
        
        if datetime.now().date() >= next_eligible.date():
            st.success("✅ You are eligible to donate again!")
        else:
            days_remaining = (next_eligible.date() - datetime.now().date()).days
            st.info(f"⏰ You can donate again in {days_remaining} days ({next_eligible.strftime('%Y-%m-%d')})")

if __name__ == "__main__":
    main()
