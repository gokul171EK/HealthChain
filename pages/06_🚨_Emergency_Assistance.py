import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Emergency Assistance - HEALTHTECH",
    page_icon="🚨",
    layout="wide"
)

def main():
    add_app_styling()
    st.title("🚨 Emergency Assistance")
    st.markdown("### Instant Access to Emergency Services and Support")
    
    # Emergency banner
    st.error("🚨 **FOR LIFE-THREATENING EMERGENCIES, CALL 102 OR GO TO THE NEAREST HOSPITAL IMMEDIATELY**")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.warning("🔒 Some features require login. You can still access emergency contacts and basic information.")
    
    # Tabs for different emergency features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Emergency Contacts", 
        "🏥 Nearby Hospitals", 
        "🚑 Emergency Guide", 
        "📱 SOS Features", 
        "💊 Medical Alert"
    ])
    
    with tab1:
        show_emergency_contacts()
    
    with tab2:
        show_nearby_hospitals()
    
    with tab3:
        show_emergency_guide()
    
    with tab4:
        show_sos_features()
    
    with tab5:
        show_medical_alert()
        
def show_emergency_contacts():
    """Display emergency contact numbers"""
    st.header("📞 Emergency Contact Numbers")

    st.markdown('<div class="header-row">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚨 National Emergency Numbers")
    with col2:
        st.subheader("🏥 Specialized Emergency Services")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        national_contacts = [
            {"service": "🚑 Medical Emergency", "number": "102", "description": "Ambulance and medical emergencies"},
            {"service": "👮 Police Emergency", "number": "100", "description": "Crime, accidents, public safety"},
            {"service": "🔥 Fire Emergency", "number": "101", "description": "Fire, explosions, rescue operations"},
            {"service": "🚨 Unified Emergency", "number": "112", "description": "All emergency services (mobile)"},
            {"service": "🩸 Blood Helpline", "number": "1910", "description": "Blood bank and donation assistance"},
            {"service": "☠️ Poison Control", "number": "1066", "description": "Poisoning and overdose emergencies"}
        ]

        for i, contact in enumerate(national_contacts):
            st.markdown('<div class="contact-row">', unsafe_allow_html=True)
            with st.container():
                col_icon, col_details, col_call = st.columns([1, 4, 2])
                with col_icon:
                    st.markdown(f"### {contact['service'].split()[0]}")
                with col_details:
                    st.markdown(f"**{contact['service']}**")
                    st.write(contact['description'])
                with col_call:
                    if st.button(f"📞 {contact['number']}", key=f"call_{i}", use_container_width=True):
                        st.success(f"Calling {contact['number']}...")
            st.markdown('</div><hr class="contact-divider">', unsafe_allow_html=True)

    with col2:
        specialized_contacts = [
            {"service": "👶 Child Helpline", "number": "1098", "description": "Child abuse and emergency"},
            {"service": "👩 Women Helpline", "number": "1091", "description": "Women in distress"},
            {"service": "🧠 Mental Health", "number": "9152987821", "description": "Mental health crisis support"},
            {"service": "👴 Senior Citizen", "number": "1091", "description": "Elder abuse and assistance"},
            {"service": "🚗 Road Accident", "number": "1073", "description": "Traffic accidents and rescue"},
            {"service": "⛽ Gas Leak", "number": "1906", "description": "Gas leakage emergency"}
        ]

        for i, contact in enumerate(specialized_contacts):
            st.markdown('<div class="contact-row">', unsafe_allow_html=True)
            with st.container():
                col_icon, col_details, col_call = st.columns([1, 4, 2])
                with col_icon:
                    st.markdown(f"### {contact['service'].split()[0]}")
                with col_details:
                    st.markdown(f"**{contact['service']}**")
                    st.write(contact['description'])
                with col_call:
                    if st.button(f"📞 {contact['number']}", key=f"call_spec_{i}", use_container_width=True):
                        st.success(f"Calling {contact['number']}...")
            st.markdown('</div><hr class="contact-divider">', unsafe_allow_html=True)

    # Quick dial section at the bottom for better flow
    st.subheader("⚡ Quick Emergency Dial")
    col_quick1, col_quick2, col_quick3, col_quick4 = st.columns(4)
    with col_quick1:
        if st.button("🚑 MEDICAL\n102", key="quick_medical", use_container_width=True):
            st.error("🚑 Calling Medical Emergency: 102")
    with col_quick2:
        if st.button("👮 POLICE\n100", key="quick_police", use_container_width=True):
            st.error("👮 Calling Police: 100")
    with col_quick3:
        if st.button("🔥 FIRE\n101", key="quick_fire", use_container_width=True):
            st.error("🔥 Calling Fire Emergency: 101")
    with col_quick4:
        if st.button("🚨 ALL\n112", key="quick_all", use_container_width=True):
            st.error("🚨 Calling Unified Emergency: 112")

def show_nearby_hospitals():
    """Display nearby hospitals and medical facilities"""
    st.header("🏥 Nearby Hospitals & Medical Facilities")
    
    # Sample hospitals data
    hospitals_data = [
        {
            "name": "City General Hospital",
            "type": "Multi-specialty",
            "distance": "1.2 km",
            "emergency": "24/7",
            "phone": "+91-123-456-7890",
            "address": "123 Health Street, Medical District",
            "specialties": ["Emergency", "Cardiology", "Neurology", "Orthopedics"],
            "rating": 4.5,
            "ambulance": "Available",
            "coordinates": [28.6139, 77.2090]
        },
        {
            "name": "Metro Emergency Center",
            "type": "Emergency Only",
            "distance": "0.8 km",
            "emergency": "24/7",
            "phone": "+91-987-654-3210",
            "address": "456 Urgent Care Avenue",
            "specialties": ["Emergency", "Trauma", "Critical Care"],
            "rating": 4.7,
            "ambulance": "Available",
            "coordinates": [28.6219, 77.2273]
        },
        {
            "name": "Sunrise Medical Center",
            "type": "Multi-specialty",
            "distance": "2.1 km",
            "emergency": "24/7",
            "phone": "+91-555-123-4567",
            "address": "789 Wellness Boulevard",
            "specialties": ["Emergency", "Pediatrics", "Gynecology", "Surgery"],
            "rating": 4.3,
            "ambulance": "Available",
            "coordinates": [28.6061, 77.2025]
        },
        {
            "name": "Heart Care Hospital",
            "type": "Specialty",
            "distance": "3.5 km",
            "emergency": "Cardiac Only",
            "phone": "+91-444-567-8901",
            "address": "321 Cardiac Center Road",
            "specialties": ["Cardiology", "Cardiac Surgery", "Emergency Cardiac Care"],
            "rating": 4.8,
            "ambulance": "Cardiac Ambulance",
            "coordinates": [28.5755, 77.1925]
        }
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏥 Hospital Directory")
        
        for hospital in hospitals_data:
            with st.expander(f"🏥 {hospital['name']} - {hospital['distance']} away", expanded=True):
                col_info, col_action = st.columns([3, 1])
                
                with col_info:
                    st.write(f"**Type:** {hospital['type']}")
                    st.write(f"**Address:** {hospital['address']}")
                    st.write(f"**Emergency Services:** {hospital['emergency']}")
                    st.write(f"**Specialties:** {', '.join(hospital['specialties'])}")
                    st.write(f"**Rating:** {'⭐' * int(hospital['rating'])} ({hospital['rating']}/5)")
                    st.write(f"**Ambulance:** {hospital['ambulance']}")
                
                with col_action:
                    if st.button(f"📞 Call", key=f"call_hospital_{hospital['name']}", use_container_width=True):
                        st.success(f"Calling {hospital['phone']}")
                    
                    if st.button(f"🗺️ Directions", key=f"directions_{hospital['name']}", use_container_width=True):
                        st.info(f"Opening directions to {hospital['name']}")
                    
                    if st.button(f"🚑 Ambulance", key=f"ambulance_{hospital['name']}", use_container_width=True):
                        st.error(f"Requesting ambulance from {hospital['name']}")
    
    with col2:
        st.subheader("🗺️ Hospital Locations")
        
        # Create map with hospital locations
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=12)
        
        for hospital in hospitals_data:
            # Color based on hospital type
            color = 'red' if hospital['type'] == 'Emergency Only' else 'blue' if hospital['type'] == 'Multi-specialty' else 'green'
            
            folium.Marker(
                hospital['coordinates'],
                popup=f"🏥 {hospital['name']}\n📞 {hospital['phone']}\n🚑 {hospital['emergency']}",
                tooltip=hospital['name'],
                icon=folium.Icon(color=color, icon='plus')
            ).add_to(m)
        
        folium_static(m, width=350, height=400)
        
        st.subheader("🚨 Emergency Room Status")
        
        # Emergency room waiting times (mock data)
        er_status = [
            {"hospital": "City General", "wait_time": "15 min", "status": "Moderate"},
            {"hospital": "Metro Emergency", "wait_time": "5 min", "status": "Low"},
            {"hospital": "Sunrise Medical", "wait_time": "25 min", "status": "High"},
            {"hospital": "Heart Care", "wait_time": "Immediate", "status": "Available"}
        ]
        
        for status in er_status:
            status_color = "green" if status["status"] == "Low" or status["status"] == "Available" else "orange" if status["status"] == "Moderate" else "red"
            
            st.markdown(f"**{status['hospital']}:** <span style='color:{status_color}'>{status['wait_time']} ({status['status']})</span>", 
                       unsafe_allow_html=True)

def show_emergency_guide():
    """Show emergency response guide and first aid"""
    st.header("📋 Emergency Response Guide")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚨 Emergency Response", "🩹 First Aid", "💊 Overdose/Poisoning", "🫀 CPR Guide"])
    
    with tab1:
        st.subheader("🚨 Emergency Response Steps")
        
        emergency_scenarios = {
            "🫀 Heart Attack": {
                "signs": ["Chest pain or pressure", "Shortness of breath", "Nausea", "Sweating", "Pain in arms/jaw"],
                "immediate_actions": [
                    "Call 102 immediately",
                    "Give aspirin if person is conscious and not allergic",
                    "Help person sit upright",
                    "Loosen tight clothing",
                    "Stay with person until help arrives"
                ]
            },
            "🧠 Stroke": {
                "signs": ["Face drooping", "Arm weakness", "Speech difficulty", "Sudden confusion", "Severe headache"],
                "immediate_actions": [
                    "Call 102 immediately",
                    "Note time symptoms started",
                    "Keep person upright",
                    "Do not give food or water",
                    "Monitor breathing and pulse"
                ]
            },
            "🤕 Severe Injury": {
                "signs": ["Heavy bleeding", "Broken bones", "Head injury", "Unconsciousness", "Severe burns"],
                "immediate_actions": [
                    "Call 102 immediately",
                    "Control bleeding with direct pressure",
                    "Do not move person unless necessary",
                    "Keep person warm",
                    "Monitor vital signs"
                ]
            },
            "😵 Unconsciousness": {
                "signs": ["Not responding to voice", "Not responding to touch", "Irregular breathing", "No pulse"],
                "immediate_actions": [
                    "Call 102 immediately",
                    "Check airway and breathing",
                    "Place in recovery position if breathing",
                    "Begin CPR if no pulse",
                    "Do not leave person alone"
                ]
            }
        }
        
        for scenario, details in emergency_scenarios.items():
            with st.expander(scenario, expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🚨 Warning Signs:**")
                    for sign in details["signs"]:
                        st.write(f"• {sign}")
                
                with col2:
                    st.markdown("**⚡ Immediate Actions:**")
                    for i, action in enumerate(details["immediate_actions"], 1):
                        st.write(f"{i}. {action}")
    
    with tab2:
        st.subheader("🩹 Basic First Aid Guide")
        
        first_aid_procedures = {
            "🩸 Bleeding Control": [
                "Apply direct pressure with clean cloth",
                "Elevate the wound above heart level if possible",
                "Apply pressure to pressure points if bleeding continues",
                "Do not remove embedded objects",
                "Seek medical attention for severe bleeding"
            ],
            "🔥 Burns": [
                "Remove from heat source immediately",
                "Cool burn with running water for 10-20 minutes",
                "Do not use ice or butter",
                "Cover with sterile gauze",
                "Seek medical attention for severe burns"
            ],
            "🦴 Fractures": [
                "Do not move the injured area",
                "Immobilize the area with splints",
                "Apply ice to reduce swelling",
                "Do not try to realign bones",
                "Seek immediate medical attention"
            ],
            "🤮 Choking": [
                "Encourage coughing if person can speak",
                "Give 5 back blows between shoulder blades",
                "Give 5 abdominal thrusts (Heimlich maneuver)",
                "Alternate back blows and abdominal thrusts",
                "Call 102 if obstruction doesn't clear"
            ]
        }
        
        for procedure, steps in first_aid_procedures.items():
            with st.expander(procedure):
                for i, step in enumerate(steps, 1):
                    st.write(f"{i}. {step}")
    
    with tab3:
        st.subheader("☠️ Poisoning & Overdose Response")
        
        st.error("🚨 For all poisoning cases, call Poison Control: 1066 immediately")
        
        poisoning_types = {
            "💊 Drug Overdose": [
                "Call 102 and poison control immediately",
                "Try to identify the substance",
                "Keep person awake and breathing",
                "Do not induce vomiting unless instructed",
                "Save containers and pills for medical team"
            ],
            "🧪 Chemical Poisoning": [
                "Remove person from contaminated area",
                "Remove contaminated clothing",
                "Rinse affected areas with water",
                "Do not induce vomiting for corrosive substances",
                "Get fresh air if inhaled"
            ],
            "🍄 Food Poisoning": [
                "Call poison control for guidance",
                "Save samples of suspected food",
                "Monitor symptoms closely",
                "Keep person hydrated if not vomiting",
                "Seek medical attention if severe"
            ]
        }
        
        for poison_type, response in poisoning_types.items():
            with st.expander(poison_type):
                for i, step in enumerate(response, 1):
                    st.write(f"{i}. {step}")
    
    with tab4:
        st.subheader("🫀 CPR (Cardiopulmonary Resuscitation)")
        
        st.warning("⚠️ CPR should only be performed if you are trained. This is for reference only.")
        
        cpr_steps = [
            "Check responsiveness and breathing",
            "Call 102 immediately",
            "Place person on firm, flat surface",
            "Tilt head back, lift chin to open airway",
            "Place heel of hand on center of chest",
            "Place other hand on top, interlace fingers",
            "Push hard and fast at least 2 inches deep",
            "Allow complete chest recoil between compressions",
            "Compress at rate of 100-120 per minute",
            "Give 30 compressions, then 2 rescue breaths",
            "Continue until help arrives or person responds"
        ]
        
        for i, step in enumerate(cpr_steps, 1):
            st.write(f"**{i}.** {step}")
        
        st.info("💡 **Remember:** Push to the beat of 'Stayin' Alive' by Bee Gees for correct rhythm")
        
        st.error("🚨 **Important:** Get proper CPR training from certified instructors")

def show_sos_features():
    """Show SOS and emergency alert features"""
    st.header("📱 SOS Emergency Features")
    
    # Check if user is logged in for personalized features
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.warning("🔒 Please login to access personalized SOS features")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚨 Emergency Alert System")
        
        # Emergency contact management
        st.markdown("**👥 Emergency Contacts**")
        
        # Sample emergency contacts (would be stored in database)
        emergency_contacts = [
            {"name": "John Doe (Spouse)", "phone": "+91-987-654-3210", "relationship": "Spouse"},
            {"name": "Dr. Sarah Smith", "phone": "+91-123-456-7890", "relationship": "Doctor"},
            {"name": "Jane Doe (Sister)", "phone": "+91-555-123-4567", "relationship": "Family"}
        ]
        
        for contact in emergency_contacts:
            col_contact, col_action = st.columns([3, 1])
            
            with col_contact:
                st.write(f"**{contact['name']}** - {contact['phone']}")
                st.write(f"Relationship: {contact['relationship']}")
            
            with col_action:
                if st.button(f"📞 Call", key=f"emergency_call_{contact['name']}", use_container_width=True):
                    st.success(f"Emergency call to {contact['name']}")
            
            st.markdown("---")
        
        # Add new emergency contact
        with st.expander("➕ Add Emergency Contact"):
            with st.form("add_emergency_contact"):
                new_name = st.text_input("👤 Contact Name")
                new_phone = st.text_input("📱 Phone Number")
                new_relationship = st.selectbox("👥 Relationship", 
                    ["Family", "Friend", "Doctor", "Spouse", "Parent", "Child", "Other"])
                
                if st.form_submit_button("➕ Add Contact"):
                    if new_name and new_phone:
                        st.success(f"✅ Added {new_name} as emergency contact")
                    else:
                        st.error("❌ Please fill in all fields")
        
        st.markdown("---")
        
        # SOS Alert System
        st.subheader("🆘 Send SOS Alert")
        
        alert_types = [
            "🚨 Medical Emergency",
            "🚗 Accident",
            "🏠 Home Emergency", 
            "👤 Personal Safety",
            "🔥 Fire Emergency",
            "💊 Medicine Emergency"
        ]
        
        selected_alert = st.selectbox("🚨 Emergency Type", alert_types)
        
        location_sharing = st.checkbox("📍 Share my current location", value=True)
        
        additional_info = st.text_area("📝 Additional Information (optional)", 
                                     placeholder="Describe the emergency situation...")
        
        col_sos1, col_sos2 = st.columns(2)
        
        with col_sos1:
            if st.button("🆘 SEND SOS ALERT", use_container_width=True, type="primary"):
                send_sos_alert(selected_alert, location_sharing, additional_info)
        
        with col_sos2:
            if st.button("❌ Cancel Alert", use_container_width=True):
                st.info("SOS alert cancelled")
    
    with col2:
        st.subheader("📱 Quick Actions")
        
        # Quick emergency buttons
        quick_actions = [
            {"action": "🚑 Call Ambulance", "number": "102"},
            {"action": "👮 Call Police", "number": "100"},
            {"action": "🔥 Call Fire Dept", "number": "101"},
            {"action": "☠️ Poison Control", "number": "1066"}
        ]
        
        for action in quick_actions:
            if st.button(action["action"], key=f"quick_{action['number']}", use_container_width=True):
                st.error(f"Calling {action['number']}...")
        
        st.subheader("🎯 Emergency Preparedness")
        
        preparedness_items = [
            "📋 Keep medical information updated",
            "💊 List current medications",
            "🆔 Have ID documents accessible",
            "📱 Keep phone charged",
            "🏠 Know nearest hospital route",
            "👥 Update emergency contacts"
        ]
        
        st.markdown("**Checklist:**")
        for item in preparedness_items:
            st.checkbox(item, key=f"prep_{item}")
        
        st.subheader("📊 Emergency Statistics")
        
        st.metric("Response Time", "8 min avg")
        st.metric("Hospitals Nearby", "4 facilities")
        st.metric("Emergency Contacts", "3 contacts")

def send_sos_alert(alert_type, share_location, additional_info):
    """Send SOS alert to emergency contacts"""
    st.error("🆘 SOS ALERT SENT!")
    
    # Mock alert details
    alert_details = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": alert_type,
        "location": "Current location shared" if share_location else "Location not shared",
        "additional_info": additional_info if additional_info else "No additional information provided"
    }
    
    st.subheader("📧 Alert Sent To:")
    
    recipients = [
        "John Doe (Spouse) - SMS & Call",
        "Dr. Sarah Smith - SMS",
        "Jane Doe (Sister) - SMS & Call",
        "Emergency Services - Automatic dispatch"
    ]
    
    for recipient in recipients:
        st.success(f"✅ {recipient}")
    
    st.subheader("📋 Alert Details:")
    for key, value in alert_details.items():
        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    st.info("🔔 Your emergency contacts will be notified immediately. Help is on the way!")

def show_medical_alert():
    """Show medical alert and allergy information"""
    st.header("💊 Medical Alert & Allergy Information")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.warning("🔒 Please login to manage your medical alert information")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🆔 Medical Alert Profile")
        
        # Medical alert form
        with st.form("medical_alert_profile"):
            st.markdown("**⚠️ Critical Medical Information**")
            
            # Allergies
            st.markdown("**🚫 Allergies & Reactions**")
            
            drug_allergies = st.text_area("💊 Drug Allergies", 
                placeholder="List medications you're allergic to (e.g., Penicillin, Aspirin)")
            
            food_allergies = st.text_area("🥜 Food Allergies",
                placeholder="List food allergies (e.g., Nuts, Shellfish, Dairy)")
            
            other_allergies = st.text_area("🌿 Other Allergies",
                placeholder="Other allergies (e.g., Latex, Bee stings)")
            
            # Medical conditions
            st.markdown("**🏥 Medical Conditions**")
            
            chronic_conditions = st.text_area("🔄 Chronic Conditions",
                placeholder="Ongoing medical conditions (e.g., Diabetes, Hypertension)")
            
            current_medications = st.text_area("💊 Current Medications",
                placeholder="List all current medications with dosages")
            
            medical_devices = st.text_area("🔧 Medical Devices",
                placeholder="Pacemaker, insulin pump, etc.")
            
            # Emergency information
            st.markdown("**🚨 Emergency Information**")
            
            blood_type = st.selectbox("🩸 Blood Type", 
                ["Unknown", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            
            emergency_doctor = st.text_input("👨‍⚕️ Primary Doctor", 
                placeholder="Dr. Name, Phone number")
            
            insurance_info = st.text_input("🏥 Insurance Information",
                placeholder="Insurance provider and policy number")
            
            special_instructions = st.text_area("📋 Special Instructions",
                placeholder="Any special medical instructions for emergencies")
            
            # ICE contacts
            st.markdown("**📞 In Case of Emergency (ICE) Contacts**")
            
            ice_contact1 = st.text_input("👤 ICE Contact 1", 
                placeholder="Name, Relationship, Phone")
            
            ice_contact2 = st.text_input("👤 ICE Contact 2",
                placeholder="Name, Relationship, Phone")
            
            if st.form_submit_button("💾 Save Medical Alert Profile", use_container_width=True):
                # Save medical alert information
                medical_data = {
                    "drug_allergies": drug_allergies,
                    "food_allergies": food_allergies,
                    "other_allergies": other_allergies,
                    "chronic_conditions": chronic_conditions,
                    "current_medications": current_medications,
                    "medical_devices": medical_devices,
                    "blood_type": blood_type,
                    "emergency_doctor": emergency_doctor,
                    "insurance_info": insurance_info,
                    "special_instructions": special_instructions,
                    "ice_contact1": ice_contact1,
                    "ice_contact2": ice_contact2
                }
                
                # Save as health record
                notes = f"Medical Alert Profile: Allergies: {drug_allergies}; Conditions: {chronic_conditions}; Medications: {current_medications}"
                record_id = data_manager.add_health_record(
                    st.session_state.user_id,
                    notes=notes
                )
                
                if record_id:
                    st.success("✅ Medical alert profile saved successfully!")
                    
                    # Show digital medical alert card
                    show_medical_alert_card(medical_data)
                else:
                    st.error("❌ Error saving medical alert profile")
    
    with col2:
        st.subheader("🆔 Digital Medical Alert Card")
        
        # Sample medical alert card
        user_data = st.session_state.user_data
        
        card_html = f"""
        <div style="border: 3px solid #FF0000; border-radius: 10px; padding: 15px; background: #FFE6E6;">
            <h3 style="color: #CC0000; text-align: center; margin: 0;">⚠️ MEDICAL ALERT ⚠️</h3>
            <hr style="border-color: #FF0000;">
            <p><strong>Name:</strong> {user_data['name']}</p>
            <p><strong>Blood Type:</strong> {user_data['blood_group']}</p>
            <p><strong>DOB:</strong> Age {user_data['age']}</p>
            <p><strong>Allergies:</strong> Penicillin, Shellfish</p>
            <p><strong>Conditions:</strong> Diabetes Type 2</p>
            <p><strong>Medications:</strong> Metformin 500mg</p>
            <p><strong>ICE:</strong> John Doe +91-987-654-3210</p>
            <p style="font-size: 10px; color: #666; text-align: center; margin: 5px 0;">
                Show this to emergency responders
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Card actions
        col_card1, col_card2 = st.columns(2)
        
        with col_card1:
            if st.button("📧 Email Card", use_container_width=True):
                st.success("📧 Medical alert card emailed!")
        
        with col_card2:
            if st.button("📱 Download", use_container_width=True):
                st.success("📱 Card saved to device!")
        
        st.subheader("💡 Medical Alert Tips")
        
        tips = [
            "🆔 Keep medical alert card accessible",
            "📱 Set medical info on phone lock screen",
            "👥 Inform family about medical conditions",
            "💊 Keep medication list updated",
            "🏥 Register with local hospitals",
            "📞 Program ICE contacts in phone"
        ]
        
        for tip in tips:
            st.info(tip)
        
        st.subheader("🚨 When to Use")
        
        scenarios = [
            "🚑 Before ambulance arrival",
            "🏥 At hospital admission",
            "👨‍⚕️ During medical procedures",
            "💊 When unconscious",
            "🚗 After accidents",
            "🔄 Regular medical checkups"
        ]
        
        for scenario in scenarios:
            st.write(f"• {scenario}")

def show_medical_alert_card(medical_data):
    """Display digital medical alert card"""
    st.subheader("🆔 Your Medical Alert Card")
    
    user_data = st.session_state.user_data
    
    card_html = f"""
    <div style="border: 3px solid #FF0000; border-radius: 10px; padding: 15px; background: #FFE6E6; margin: 10px 0;">
        <h3 style="color: #CC0000; text-align: center; margin: 0;">⚠️ MEDICAL ALERT ⚠️</h3>
        <hr style="border-color: #FF0000;">
        <p><strong>Name:</strong> {user_data['name']}</p>
        <p><strong>Blood Type:</strong> {medical_data.get('blood_type', 'Unknown')}</p>
        <p><strong>Age:</strong> {user_data['age']}</p>
        <p><strong>Drug Allergies:</strong> {medical_data.get('drug_allergies', 'None listed')}</p>
        <p><strong>Food Allergies:</strong> {medical_data.get('food_allergies', 'None listed')}</p>
        <p><strong>Medical Conditions:</strong> {medical_data.get('chronic_conditions', 'None listed')}</p>
        <p><strong>Current Medications:</strong> {medical_data.get('current_medications', 'None listed')}</p>
        <p><strong>Emergency Doctor:</strong> {medical_data.get('emergency_doctor', 'Not specified')}</p>
        <p><strong>ICE Contact 1:</strong> {medical_data.get('ice_contact1', 'Not specified')}</p>
        <p><strong>ICE Contact 2:</strong> {medical_data.get('ice_contact2', 'Not specified')}</p>
        <p style="font-size: 10px; color: #666; text-align: center; margin: 5px 0;">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | HEALTHTECH
        </p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    st.success("✅ Medical alert card ready! Save this information for emergencies.")

if __name__ == "__main__":
    main()
