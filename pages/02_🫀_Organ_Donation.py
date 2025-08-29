import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_manager import DataManager

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Organ Donation - HEALTHTECH",
    page_icon="🫀",
    layout="wide"
)

def main():
    st.title("🫀 Organ Donation Center")
    st.markdown("### Give the Gift of Life Through Organ Donation")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access organ donation features")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Register as Donor", 
        "🔍 Find Recipients", 
        "📊 Compatibility", 
        "📚 Information", 
        "🏥 My Registration"
    ])
    
    with tab1:
        show_donor_registration()
    
    with tab2:
        show_find_recipients()
    
    with tab3:
        show_compatibility_info()
    
    with tab4:
        show_organ_donation_info()
    
    with tab5:
        show_my_registration()

def show_donor_registration():
    """Organ donor registration form"""
    st.header("📝 Register as Organ Donor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🫀 Organ Donation Registration")
        
        with st.form("organ_donor_registration"):
            # Organ selection
            st.subheader("🫁 Select Organs to Donate")
            
            organs_list = [
                "Heart", "Liver", "Kidneys", "Lungs", "Pancreas", 
                "Intestines", "Corneas", "Skin", "Bone", "Heart Valves"
            ]
            
            col_organs1, col_organs2 = st.columns(2)
            selected_organs = []
            
            with col_organs1:
                for organ in organs_list[:5]:
                    if st.checkbox(f"🫀 {organ}"):
                        selected_organs.append(organ)
            
            with col_organs2:
                for organ in organs_list[5:]:
                    if st.checkbox(f"🫁 {organ}"):
                        selected_organs.append(organ)
            
            st.markdown("---")
            
            # Medical history
            st.subheader("🏥 Medical Information")
            
            medical_conditions = st.text_area(
                "🩺 Current Medical Conditions",
                placeholder="List any current medical conditions, medications, or surgeries"
            )
            
            allergies = st.text_input(
                "🚫 Known Allergies",
                placeholder="List any known allergies"
            )
            
            previous_surgeries = st.text_area(
                "🔧 Previous Surgeries",
                placeholder="List any previous surgeries or medical procedures"
            )
            
            # Emergency contact
            st.subheader("🚨 Emergency Contact")
            
            col_contact1, col_contact2 = st.columns(2)
            
            with col_contact1:
                emergency_name = st.text_input("👤 Full Name")
                emergency_relationship = st.selectbox(
                    "👥 Relationship",
                    ["Spouse", "Parent", "Child", "Sibling", "Other Family", "Friend"]
                )
            
            with col_contact2:
                emergency_phone = st.text_input("📱 Phone Number")
                emergency_email = st.text_input("📧 Email Address")
            
            # Legal consent
            st.subheader("⚖️ Legal Consent")
            
            legal_consent = st.checkbox(
                "I hereby consent to donate my organs after death for transplantation purposes"
            )
            
            family_informed = st.checkbox(
                "I have informed my family about my decision to donate organs"
            )
            
            understand_process = st.checkbox(
                "I understand the organ donation process and my rights"
            )
            
            # Age verification
            age_verification = st.checkbox(
                "I confirm that I am at least 18 years old"
            )
            
            submit_btn = st.form_submit_button("🫀 Register as Organ Donor", use_container_width=True)
            
            if submit_btn:
                # Validate form
                if not selected_organs:
                    st.error("❌ Please select at least one organ to donate")
                elif not all([emergency_name, emergency_phone, emergency_relationship]):
                    st.error("❌ Please fill in all emergency contact fields")
                elif not all([legal_consent, family_informed, understand_process, age_verification]):
                    st.error("❌ Please complete all consent requirements")
                else:
                    # Combine medical information
                    full_medical_info = f"Conditions: {medical_conditions}; Allergies: {allergies}; Surgeries: {previous_surgeries}"
                    emergency_contact_info = f"{emergency_name} ({emergency_relationship}) - Phone: {emergency_phone}, Email: {emergency_email}"
                    
                    # Register organ donor
                    donor_id = data_manager.register_organ_donor(
                        st.session_state.user_id,
                        selected_organs,
                        full_medical_info,
                        emergency_contact_info
                    )
                    
                    if donor_id:
                        st.success("🎉 Successfully registered as organ donor!")
                        st.balloons()
                        
                        # Display donor card
                        st.subheader("🆔 Digital Donor Card")
                        user_data = st.session_state.user_data
                        
                        card_html = f"""
                        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
                            <h3 style="color: #2E7D32; text-align: center;">🫀 ORGAN DONOR CARD</h3>
                            <hr>
                            <p><strong>Name:</strong> {user_data['name']}</p>
                            <p><strong>Blood Group:</strong> {user_data['blood_group']}</p>
                            <p><strong>Organs Donated:</strong> {', '.join(selected_organs)}</p>
                            <p><strong>Registration Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
                            <p><strong>Donor ID:</strong> {donor_id[:8]}</p>
                            <p style="font-size: 12px; color: #666; text-align: center;">Keep this card with you at all times</p>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                    else:
                        st.error("❌ Error registering as organ donor. Please try again.")
    
    with col2:
        st.subheader("📊 Organ Donation Impact")
        
        impact_stats = [
            {"stat": "Lives Saved", "number": "1", "description": "Each donor can save up to 8 lives"},
            {"stat": "People Helped", "number": "75", "description": "One donor can help up to 75 people"},
            {"stat": "Waiting List", "number": "100,000+", "description": "People waiting for organ transplants"},
            {"stat": "Daily Deaths", "number": "17", "description": "People die daily waiting for organs"}
        ]
        
        for stat in impact_stats:
            st.metric(
                label=stat["stat"],
                value=stat["number"],
                help=stat["description"]
            )
        
        st.markdown("---")
        
        st.subheader("💡 Why Donate Organs?")
        
        reasons = [
            "🌟 Save multiple lives with one donation",
            "❤️ Provide hope to families in need",
            "🎁 Give the ultimate gift of life",
            "🏥 Advance medical research and science",
            "👨‍👩‍👧‍👦 Create a lasting legacy",
            "🤝 Help your community"
        ]
        
        for reason in reasons:
            st.info(reason)

def show_find_recipients():
    """Show organ recipients needing donations"""
    st.header("🔍 Find Recipients in Need")
    
    # Sample recipient data (in real app, this would be anonymized and from database)
    recipients_data = [
        {
            "id": "R001",
            "organ_needed": "Kidney",
            "blood_group": "O+",
            "age_range": "35-45",
            "urgency": "Critical",
            "waiting_time": "2 years 3 months",
            "location": "Mumbai, Maharashtra",
            "compatibility": "High"
        },
        {
            "id": "R002",
            "organ_needed": "Liver",
            "blood_group": "A+",
            "age_range": "25-35",
            "urgency": "High",
            "waiting_time": "1 year 8 months",
            "location": "Delhi, NCR",
            "compatibility": "Medium"
        },
        {
            "id": "R003",
            "organ_needed": "Heart",
            "blood_group": "B-",
            "age_range": "45-55",
            "urgency": "Critical",
            "waiting_time": "6 months",
            "location": "Chennai, Tamil Nadu",
            "compatibility": "Low"
        },
        {
            "id": "R004",
            "organ_needed": "Cornea",
            "blood_group": "AB+",
            "age_range": "15-25",
            "urgency": "Medium",
            "waiting_time": "8 months",
            "location": "Bangalore, Karnataka",
            "compatibility": "High"
        }
    ]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("🎯 Filter Recipients")
        
        organ_filter = st.selectbox(
            "🫀 Organ Needed",
            ["All", "Heart", "Liver", "Kidney", "Lungs", "Cornea", "Pancreas"]
        )
        
        blood_group_filter = st.selectbox(
            "🩸 Blood Group",
            ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )
        
        urgency_filter = st.selectbox(
            "⚡ Urgency Level",
            ["All", "Critical", "High", "Medium", "Low"]
        )
        
        location_filter = st.text_input("📍 Location", placeholder="City or State")
    
    with col2:
        st.subheader("👥 Recipients Waiting")
        
        # Filter recipients based on criteria
        filtered_recipients = recipients_data
        
        if organ_filter != "All":
            filtered_recipients = [r for r in filtered_recipients if r['organ_needed'] == organ_filter]
        
        if blood_group_filter != "All":
            filtered_recipients = [r for r in filtered_recipients if r['blood_group'] == blood_group_filter]
        
        if urgency_filter != "All":
            filtered_recipients = [r for r in filtered_recipients if r['urgency'] == urgency_filter]
        
        if location_filter:
            filtered_recipients = [r for r in filtered_recipients 
                                 if location_filter.lower() in r['location'].lower()]
        
        if filtered_recipients:
            st.info(f"Found {len(filtered_recipients)} recipients matching your criteria")
            
            for recipient in filtered_recipients:
                with st.container():
                    # Color code by urgency
                    urgency_colors = {
                        "Critical": "red",
                        "High": "orange", 
                        "Medium": "yellow",
                        "Low": "green"
                    }
                    
                    urgency_color = urgency_colors.get(recipient['urgency'], 'blue')
                    
                    col_info, col_details, col_action = st.columns([2, 2, 1])
                    
                    with col_info:
                        st.markdown(f"🫀 **Organ Needed:** {recipient['organ_needed']}")
                        st.markdown(f"🩸 **Blood Group:** {recipient['blood_group']}")
                        st.markdown(f"👤 **Age Range:** {recipient['age_range']}")
                    
                    with col_details:
                        st.markdown(f"📍 **Location:** {recipient['location']}")
                        st.markdown(f"⏰ **Waiting Time:** {recipient['waiting_time']}")
                        st.markdown(f"⚡ **Urgency:** <span style='color:{urgency_color}'>{recipient['urgency']}</span>", 
                                   unsafe_allow_html=True)
                    
                    with col_action:
                        compatibility_color = "green" if recipient['compatibility'] == "High" else "orange" if recipient['compatibility'] == "Medium" else "red"
                        st.markdown(f"🔗 **Match:** <span style='color:{compatibility_color}'>{recipient['compatibility']}</span>", 
                                   unsafe_allow_html=True)
                        
                        if st.button(f"💌 Express Interest", key=f"interest_{recipient['id']}"):
                            st.success("Thank you for expressing interest! The transplant coordinator will contact you.")
                    
                    st.markdown("---")
        else:
            st.warning("No recipients found matching your criteria")
    
    # Statistics section
    st.markdown("---")
    st.subheader("📊 Transplant Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏰ People Waiting", "107,000+", help="Current number of people on organ waiting lists")
    
    with col2:
        st.metric("📈 Transplants/Day", "95", help="Average number of organ transplants performed daily")
    
    with col3:
        st.metric("⚰️ Deaths/Day", "17", help="Average number of people who die daily waiting for organs")
    
    with col4:
        st.metric("📊 Success Rate", "85-95%", help="Success rate of organ transplants")

def show_compatibility_info():
    """Show organ compatibility information"""
    st.header("📊 Organ Compatibility Information")
    
    tab1, tab2, tab3 = st.tabs(["🩸 Blood Compatibility", "🧬 Tissue Matching", "🔍 Matching Process"])
    
    with tab1:
        st.subheader("🩸 Blood Group Compatibility")
        
        # Blood compatibility chart
        compatibility_data = {
            "Recipient": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            "Can Receive From": [
                "A+, A-, O+, O-",
                "A-, O-",
                "B+, B-, O+, O-",
                "B-, O-",
                "All blood types",
                "A-, B-, AB-, O-",
                "O+, O-",
                "O- only"
            ]
        }
        
        compat_df = pd.DataFrame(compatibility_data)
        st.table(compat_df)
        
        st.info("💡 **Universal Donors (O-):** Can donate to anyone")
        st.info("💡 **Universal Recipients (AB+):** Can receive from anyone")
        
        # Interactive compatibility checker
        st.subheader("🔍 Check Blood Compatibility")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            donor_blood = st.selectbox("Donor Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        with col2:
            recipient_blood = st.selectbox("Recipient Blood Type", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        with col3:
            if st.button("Check Compatibility"):
                compatibility = check_blood_compatibility(donor_blood, recipient_blood)
                if compatibility:
                    st.success("✅ Compatible!")
                else:
                    st.error("❌ Not Compatible")
    
    with tab2:
        st.subheader("🧬 Human Leukocyte Antigen (HLA) Matching")
        
        st.markdown("""
        **HLA typing** is crucial for organ transplant success. The closer the HLA match between donor and recipient, 
        the better the chance of transplant success.
        
        ### Key HLA Factors:
        - **HLA-A, HLA-B, HLA-C**: Class I molecules
        - **HLA-DR, HLA-DQ, HLA-DP**: Class II molecules
        
        ### Matching Levels:
        - **6/6 Match**: Perfect match (rare, usually family members)
        - **5/6 Match**: Excellent match
        - **4/6 Match**: Good match
        - **3/6 Match**: Acceptable match
        """)
        
        # HLA matching simulator
        st.subheader("🎯 HLA Match Simulator")
        
        donor_hla = st.text_input("Donor HLA Type", placeholder="A1,A2;B7,B8;DR2,DR4")
        recipient_hla = st.text_input("Recipient HLA Type", placeholder="A1,A3;B7,B35;DR2,DR7")
        
        if donor_hla and recipient_hla:
            # Simple matching simulation
            matches = calculate_hla_matches(donor_hla, recipient_hla)
            st.info(f"🔗 HLA Match Score: {matches}/6")
            
            if matches >= 4:
                st.success("✅ Good HLA compatibility!")
            elif matches >= 2:
                st.warning("⚠️ Moderate HLA compatibility")
            else:
                st.error("❌ Poor HLA compatibility")
    
    with tab3:
        st.subheader("🔍 Organ Matching Process")
        
        st.markdown("""
        ### Step-by-Step Matching Process:
        
        1. **🩸 Blood Type Compatibility**
           - First and most critical factor
           - Must be compatible or universal
        
        2. **📏 Size and Weight Matching**
           - Organ size must fit recipient
           - Important for heart, liver, lungs
        
        3. **🧬 HLA Tissue Typing**
           - Genetic compatibility testing
           - Reduces rejection risk
        
        4. **📍 Geographic Location**
           - Proximity for organ viability
           - Transportation time limits
        
        5. **⏰ Time on Waiting List**
           - Priority given to longer wait times
           - Balanced with medical urgency
        
        6. **🏥 Medical Urgency**
           - Critical patients get priority
           - Based on severity of condition
        
        7. **👤 Age Considerations**
           - Age matching for optimal outcomes
           - Pediatric patients have priority
        """)
        
        # Matching score calculator
        st.subheader("🎯 Matching Score Calculator")
        
        with st.form("matching_calculator"):
            col1, col2 = st.columns(2)
            
            with col1:
                blood_compat = st.selectbox("Blood Compatibility", ["Perfect", "Compatible", "Incompatible"])
                hla_match = st.selectbox("HLA Match", ["6/6", "5/6", "4/6", "3/6", "2/6", "1/6", "0/6"])
                size_match = st.selectbox("Size Match", ["Perfect", "Good", "Acceptable", "Poor"])
            
            with col2:
                distance = st.selectbox("Distance", ["< 100 miles", "100-500 miles", "> 500 miles"])
                urgency = st.selectbox("Medical Urgency", ["Critical", "High", "Medium", "Low"])
                wait_time = st.selectbox("Wait Time", ["> 2 years", "1-2 years", "6-12 months", "< 6 months"])
            
            calculate_btn = st.form_submit_button("Calculate Match Score")
            
            if calculate_btn:
                score = calculate_matching_score(blood_compat, hla_match, size_match, distance, urgency, wait_time)
                
                st.metric("🎯 Overall Match Score", f"{score}/100")
                
                if score >= 80:
                    st.success("🌟 Excellent Match! High probability of successful transplant")
                elif score >= 60:
                    st.info("✅ Good Match! Reasonable chance of success")
                elif score >= 40:
                    st.warning("⚠️ Fair Match! Consider all options carefully")
                else:
                    st.error("❌ Poor Match! May not be suitable for transplant")

def show_organ_donation_info():
    """Educational information about organ donation"""
    st.header("📚 Organ Donation Information")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🫀 About Donation", "📋 Process", "❓ Myths & Facts", "📞 Resources"])
    
    with tab1:
        st.subheader("🫀 What is Organ Donation?")
        
        st.markdown("""
        Organ donation is the process of surgically removing an organ or tissue from one person (the donor) 
        and placing it into another person (the recipient). Transplantation is necessary when the recipient's 
        organ has failed or has been damaged by disease or injury.
        
        ### Types of Donations:
        
        **🫀 Deceased Donation:**
        - Organs donated after brain death or cardiac death
        - Can donate multiple organs and tissues
        - Most common type of donation
        
        **❤️ Living Donation:**
        - Donation from a living person
        - Usually kidney or part of liver
        - Can be directed or non-directed
        
        ### Organs That Can Be Donated:
        """)
        
        organs_info = {
            "🫀 Heart": "Can save one life. Transplanted within 4-6 hours of removal.",
            "🫁 Lungs": "Can save 1-2 lives. Must be transplanted within 4-6 hours.",
            "🫘 Liver": "Can save 1-2 lives. Can be split for two recipients.",
            "🫘 Kidneys": "Can save 2 lives. Most commonly transplanted organ.",
            "🍯 Pancreas": "Can save one life. Often transplanted with kidney.",
            "🦴 Intestines": "Can save one life. Less common but life-saving.",
            "👁️ Corneas": "Can restore sight to 2 people. Can be stored longer.",
            "🦴 Bone": "Can help many people with bone grafts and repairs.",
            "🩸 Skin": "Can help burn victims and wound healing.",
            "❤️ Heart Valves": "Can help children with heart defects."
        }
        
        for organ, info in organs_info.items():
            st.info(f"**{organ}**: {info}")
    
    with tab2:
        st.subheader("📋 Organ Donation Process")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏥 For Deceased Donation:")
            
            process_steps = [
                "🚨 Medical emergency occurs",
                "🏥 Patient taken to hospital",
                "👨‍⚕️ Medical team works to save life",
                "🧠 Brain death is declared by doctors",
                "📞 Organ procurement organization contacted",
                "🔍 Medical evaluation for donation",
                "👨‍👩‍👧‍👦 Family approached about donation",
                "📋 Consent obtained for donation",
                "🔬 Testing for organ function and matching",
                "🎯 Recipients identified and contacted",
                "🏥 Surgical removal of organs",
                "✈️ Organs transported to recipients",
                "🔧 Transplant surgery performed"
            ]
            
            for i, step in enumerate(process_steps, 1):
                st.write(f"{i}. {step}")
        
        with col2:
            st.markdown("### ❤️ For Living Donation:")
            
            living_steps = [
                "🤔 Decision to donate made",
                "📞 Contact transplant center",
                "📋 Initial screening questionnaire",
                "🩺 Medical evaluation begins",
                "🧪 Blood tests and imaging",
                "👨‍⚕️ Meet with transplant team",
                "🧠 Psychological evaluation",
                "📊 Final medical clearance",
                "📅 Surgery scheduled",
                "🏥 Donation surgery performed",
                "🔄 Post-operative care",
                "📈 Follow-up appointments",
                "💪 Full recovery monitoring"
            ]
            
            for i, step in enumerate(living_steps, 1):
                st.write(f"{i}. {step}")
        
        st.markdown("---")
        st.info("⏱️ **Time is Critical:** Organs must be transplanted quickly after removal to remain viable.")
    
    with tab3:
        st.subheader("❓ Common Myths and Facts")
        
        myths_facts = [
            {
                "myth": "❌ If I'm an organ donor, doctors won't try to save my life",
                "fact": "✅ Medical teams are completely separate from transplant teams. Doctors' first priority is always to save your life."
            },
            {
                "myth": "❌ I'm too old to be an organ donor",
                "fact": "✅ There's no age limit for organ donation. People in their 80s have been successful donors."
            },
            {
                "myth": "❌ Rich and famous people get organs faster",
                "fact": "✅ Organ allocation is based on medical criteria, not social status or wealth."
            },
            {
                "myth": "❌ My family will be charged for donation",
                "fact": "✅ There's no cost to donor families. All expenses are covered by the recipient's insurance."
            },
            {
                "myth": "❌ Open casket funeral isn't possible after donation",
                "fact": "✅ Organ donation doesn't interfere with funeral arrangements or open casket services."
            },
            {
                "myth": "❌ My religion doesn't support organ donation",
                "fact": "✅ Most major religions support organ donation as an act of charity and love."
            }
        ]
        
        for item in myths_facts:
            with st.expander(item["myth"]):
                st.success(item["fact"])
    
    with tab4:
        st.subheader("📞 Helpful Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏥 Transplant Centers")
            
            centers = [
                "🏥 Apollo Hospitals - Multiple locations",
                "🏥 Fortis Healthcare - Pan India",
                "🏥 Medanta - Gurugram",
                "🏥 AIIMS - New Delhi",
                "🏥 Christian Medical College - Vellore",
                "🏥 Narayana Health - Bangalore"
            ]
            
            for center in centers:
                st.info(center)
        
        with col2:
            st.markdown("### 📞 Emergency Contacts")
            
            contacts = [
                "🚨 National Organ Transplant Helpline: 1800-103-7100",
                "🩸 Blood Bank Emergency: 1910",
                "🏥 Medical Emergency: 102",
                "👮 Police Emergency: 100",
                "🚑 Ambulance Service: 108",
                "🔥 Fire Emergency: 101"
            ]
            
            for contact in contacts:
                st.error(contact)
        
        st.markdown("---")
        
        st.subheader("🌐 Online Resources")
        
        resources = [
            "📚 National Organ & Tissue Transplant Organization (NOTTO)",
            "📖 Indian Society of Organ Transplantation (ISOT)",
            "🎓 Organ Donation Day awareness campaigns",
            "💬 Support groups for donor families",
            "📱 Organ donation mobile apps",
            "📺 Educational videos and webinars"
        ]
        
        for resource in resources:
            st.info(resource)

def show_my_registration():
    """Show user's organ donation registration status"""
    st.header("🏥 My Organ Donation Registration")
    
    user_id = st.session_state.user_id
    
    # Check if user is registered as organ donor
    # For demo purposes, we'll simulate this
    try:
        # This would normally query the database
        st.info("Loading your organ donation registration...")
        
        # Simulate checking registration
        registration_exists = False  # This would come from database
        
        if registration_exists:
            show_existing_registration()
        else:
            st.warning("📝 You haven't registered as an organ donor yet.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📝 Register Now", use_container_width=True):
                    st.info("Please use the 'Register as Donor' tab to complete your registration.")
            
            with col2:
                if st.button("📚 Learn More", use_container_width=True):
                    st.info("Please check the 'Information' tab to learn more about organ donation.")
            
            # Show benefits of registration
            show_registration_benefits()
    
    except Exception as e:
        st.error("Error loading registration information. Please try again later.")

def show_existing_registration():
    """Show existing organ donor registration details"""
    st.success("✅ You are registered as an organ donor!")
    
    # Mock registration data
    registration_data = {
        "Registration Date": "2024-06-15",
        "Organs Registered": ["Heart", "Liver", "Kidneys", "Corneas"],
        "Status": "Active",
        "Last Updated": "2024-08-01"
    }
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Registration Details")
        
        for key, value in registration_data.items():
            if key == "Organs Registered":
                st.write(f"**{key}:** {', '.join(value)}")
            else:
                st.write(f"**{key}:** {value}")
        
        # Digital donor card
        st.subheader("🆔 Digital Donor Card")
        
        user_data = st.session_state.user_data
        card_html = f"""
        <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
            <h3 style="color: #2E7D32; text-align: center;">🫀 ORGAN DONOR CARD</h3>
            <hr>
            <p><strong>Name:</strong> {user_data['name']}</p>
            <p><strong>Blood Group:</strong> {user_data['blood_group']}</p>
            <p><strong>Organs:</strong> Heart, Liver, Kidneys, Corneas</p>
            <p><strong>Registration:</strong> 2024-06-15</p>
            <p><strong>Status:</strong> Active Donor</p>
            <p style="font-size: 12px; color: #666; text-align: center;">This person has consented to organ donation</p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    with col2:
        st.subheader("⚙️ Manage Registration")
        
        if st.button("✏️ Update Information", use_container_width=True):
            st.info("Update functionality would open here")
        
        if st.button("📧 Email Card", use_container_width=True):
            st.success("Digital donor card emailed to you!")
        
        if st.button("📱 Download Card", use_container_width=True):
            st.success("Digital donor card downloaded!")
        
        if st.button("⚠️ Deactivate Registration", use_container_width=True):
            st.error("Are you sure? This action cannot be undone.")

def show_registration_benefits():
    """Show benefits of organ donor registration"""
    st.subheader("🌟 Benefits of Registration")
    
    benefits = [
        {
            "title": "💖 Save Lives",
            "description": "One donor can save up to 8 lives and help 75+ people"
        },
        {
            "title": "🎁 Leave a Legacy", 
            "description": "Create a lasting impact that continues after you're gone"
        },
        {
            "title": "🏥 Priority Access",
            "description": "Some regions give transplant priority to registered donors"
        },
        {
            "title": "📱 Digital Card",
            "description": "Carry your donor status on your phone"
        },
        {
            "title": "👨‍👩‍👧‍👦 Family Peace",
            "description": "Your family will know your wishes in difficult times"
        },
        {
            "title": "🌍 Community Impact",
            "description": "Inspire others to consider organ donation"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, benefit in enumerate(benefits):
        column = col1 if i % 2 == 0 else col2
        with column:
            st.info(f"**{benefit['title']}**\n\n{benefit['description']}")

# Helper functions
def check_blood_compatibility(donor_blood, recipient_blood):
    """Check if donor blood is compatible with recipient"""
    compatibility_rules = {
        "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        "O+": ["O+", "A+", "B+", "AB+"],
        "A-": ["A-", "A+", "AB-", "AB+"],
        "A+": ["A+", "AB+"],
        "B-": ["B-", "B+", "AB-", "AB+"],
        "B+": ["B+", "AB+"],
        "AB-": ["AB-", "AB+"],
        "AB+": ["AB+"]
    }
    
    return recipient_blood in compatibility_rules.get(donor_blood, [])

def calculate_hla_matches(donor_hla, recipient_hla):
    """Calculate HLA matches (simplified simulation)"""
    # This is a simplified simulation - real HLA matching is much more complex
    import random
    return random.randint(0, 6)

def calculate_matching_score(blood_compat, hla_match, size_match, distance, urgency, wait_time):
    """Calculate overall matching score"""
    score = 0
    
    # Blood compatibility (40% of score)
    if blood_compat == "Perfect":
        score += 40
    elif blood_compat == "Compatible":
        score += 30
    
    # HLA match (25% of score)
    hla_scores = {"6/6": 25, "5/6": 20, "4/6": 15, "3/6": 10, "2/6": 5, "1/6": 2, "0/6": 0}
    score += hla_scores.get(hla_match, 0)
    
    # Size match (15% of score)
    size_scores = {"Perfect": 15, "Good": 10, "Acceptable": 5, "Poor": 0}
    score += size_scores.get(size_match, 0)
    
    # Distance (10% of score)
    distance_scores = {"< 100 miles": 10, "100-500 miles": 5, "> 500 miles": 0}
    score += distance_scores.get(distance, 0)
    
    # Urgency and wait time adjustments (10% of score)
    if urgency == "Critical":
        score += 5
    if wait_time == "> 2 years":
        score += 5
    
    return min(score, 100)

if __name__ == "__main__":
    main()
