import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime, time
from utils.data_manager import DataManager

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Pharmacy Locator - HEALTHTECH",
    page_icon="🏥",
    layout="wide"
)

def main():
    st.title("🏥 Pharmacy Locator")
    st.markdown("### Find Pharmacies and Manage Your Medications")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.warning("🔒 Some features require login. You can still browse pharmacies and basic information.")
    
    # Tabs for different pharmacy features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Find Pharmacies", 
        "💊 Medication Reminders", 
        "🛒 Medicine Orders", 
        "💰 Price Comparison", 
        "📱 Digital Prescriptions"
    ])
    
    with tab1:
        show_pharmacy_locator()
    
    with tab2:
        show_medication_reminders()
    
    with tab3:
        show_medicine_orders()
    
    with tab4:
        show_price_comparison()
    
    with tab5:
        show_digital_prescriptions()

def show_pharmacy_locator():
    """Find and locate nearby pharmacies"""
    st.header("🔍 Find Nearby Pharmacies")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pharmacy database
        pharmacies_data = [
            {
                "name": "MedPlus Pharmacy",
                "address": "123 Health Street, Medical District",
                "phone": "+91-123-456-7890",
                "distance": "0.5 km",
                "rating": 4.5,
                "delivery": "Available",
                "hours": "24/7",
                "services": ["Prescription", "OTC", "Health Checkup", "Home Delivery"],
                "coordinates": [28.6139, 77.2090],
                "specialties": ["Diabetes Care", "Heart Medications", "Pediatric Medicines"]
            },
            {
                "name": "Apollo Pharmacy",
                "address": "456 Wellness Avenue, Central Area",
                "phone": "+91-987-654-3210",
                "distance": "0.8 km",
                "rating": 4.7,
                "delivery": "Available",
                "hours": "6 AM - 12 AM",
                "services": ["Prescription", "OTC", "Lab Tests", "Consultation"],
                "coordinates": [28.6219, 77.2273],
                "specialties": ["Women's Health", "Chronic Care", "Supplements"]
            },
            {
                "name": "HealthMart Pharmacy",
                "address": "789 Care Lane, Suburb Area",
                "phone": "+91-555-123-4567",
                "distance": "1.2 km",
                "rating": 4.3,
                "delivery": "Available",
                "hours": "8 AM - 10 PM",
                "services": ["Prescription", "OTC", "Vaccination", "Health Products"],
                "coordinates": [28.6061, 77.2025],
                "specialties": ["Senior Care", "Mental Health", "Dermatology"]
            },
            {
                "name": "QuickMed Express",
                "address": "321 Fast Lane, Business District",
                "phone": "+91-444-567-8901",
                "distance": "1.5 km",
                "rating": 4.2,
                "delivery": "Express Delivery",
                "hours": "24/7",
                "services": ["Emergency Medicines", "Express Delivery", "Online Orders"],
                "coordinates": [28.5755, 77.1925],
                "specialties": ["Emergency Medicines", "Critical Care", "Rare Drugs"]
            }
        ]
        
        # Search and filter options
        st.subheader("🎯 Search & Filter")
        
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            location_search = st.text_input("📍 Search by location", placeholder="Enter area, pincode, or landmark")
            medicine_search = st.text_input("💊 Search for specific medicine", placeholder="Medicine name")
        
        with col_search2:
            delivery_filter = st.selectbox("🚚 Delivery Options", ["All", "Home Delivery", "Express Delivery", "Pickup Only"])
            hours_filter = st.selectbox("🕐 Operating Hours", ["All", "24/7", "Open Now", "Open Late"])
        
        # Advanced filters
        with st.expander("🔧 Advanced Filters"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                rating_filter = st.slider("⭐ Minimum Rating", 1.0, 5.0, 4.0, 0.1)
                distance_filter = st.slider("📏 Maximum Distance (km)", 0.5, 10.0, 5.0, 0.5)
            
            with col_adv2:
                services_filter = st.multiselect("🎯 Required Services", 
                    ["Prescription", "OTC", "Health Checkup", "Home Delivery", "Lab Tests", "Consultation", "Vaccination"])
                specialties_filter = st.multiselect("🩺 Specialties", 
                    ["Diabetes Care", "Heart Medications", "Women's Health", "Chronic Care", "Senior Care", "Mental Health"])
        
        st.markdown("---")
        
        # Display pharmacy results
        st.subheader("🏥 Pharmacy Results")
        
        # Filter pharmacies based on criteria
        filtered_pharmacies = pharmacies_data.copy()
        
        if location_search:
            filtered_pharmacies = [p for p in filtered_pharmacies 
                                 if location_search.lower() in p['address'].lower()]
        
        if delivery_filter != "All":
            if delivery_filter == "Home Delivery":
                filtered_pharmacies = [p for p in filtered_pharmacies if "delivery" in p['delivery'].lower()]
            elif delivery_filter == "Express Delivery":
                filtered_pharmacies = [p for p in filtered_pharmacies if "express" in p['delivery'].lower()]
        
        if hours_filter == "24/7":
            filtered_pharmacies = [p for p in filtered_pharmacies if "24/7" in p['hours']]
        
        filtered_pharmacies = [p for p in filtered_pharmacies if p['rating'] >= rating_filter]
        
        if services_filter:
            filtered_pharmacies = [p for p in filtered_pharmacies 
                                 if any(service in p['services'] for service in services_filter)]
        
        if specialties_filter:
            filtered_pharmacies = [p for p in filtered_pharmacies 
                                 if any(specialty in p['specialties'] for specialty in specialties_filter)]
        
        if filtered_pharmacies:
            st.success(f"Found {len(filtered_pharmacies)} pharmacies matching your criteria")
            
            for pharmacy in filtered_pharmacies:
                with st.container():
                    col_info, col_details, col_actions = st.columns([2, 2, 1])
                    
                    with col_info:
                        st.markdown(f"### 🏥 {pharmacy['name']}")
                        st.write(f"📍 {pharmacy['address']}")
                        st.write(f"📞 {pharmacy['phone']}")
                        st.write(f"📏 Distance: {pharmacy['distance']}")
                        
                        # Rating display
                        stars = "⭐" * int(pharmacy['rating'])
                        st.write(f"{stars} {pharmacy['rating']}/5.0")
                    
                    with col_details:
                        st.write(f"🕐 **Hours:** {pharmacy['hours']}")
                        st.write(f"🚚 **Delivery:** {pharmacy['delivery']}")
                        
                        st.write("**🎯 Services:**")
                        for service in pharmacy['services']:
                            st.write(f"• {service}")
                        
                        st.write("**🩺 Specialties:**")
                        for specialty in pharmacy['specialties']:
                            st.write(f"• {specialty}")
                    
                    with col_actions:
                        if st.button(f"📞 Call", key=f"call_{pharmacy['name']}", use_container_width=True):
                            st.success(f"Calling {pharmacy['phone']}")
                        
                        if st.button(f"🗺️ Directions", key=f"directions_{pharmacy['name']}", use_container_width=True):
                            st.info(f"Opening directions to {pharmacy['name']}")
                        
                        if st.button(f"🛒 Order", key=f"order_{pharmacy['name']}", use_container_width=True):
                            show_order_interface(pharmacy)
                        
                        if medicine_search:
                            if st.button(f"💊 Check Stock", key=f"stock_{pharmacy['name']}", use_container_width=True):
                                check_medicine_availability(pharmacy, medicine_search)
                    
                    st.markdown("---")
        else:
            st.warning("No pharmacies found matching your criteria. Please adjust your filters.")
    
    with col2:
        st.subheader("🗺️ Pharmacy Locations")
        
        # Create map with pharmacy locations
        m = folium.Map(location=[28.6139, 77.2090], zoom_start=13)
        
        for pharmacy in filtered_pharmacies if 'filtered_pharmacies' in locals() else pharmacies_data:
            # Color based on rating
            if pharmacy['rating'] >= 4.5:
                color = 'green'
            elif pharmacy['rating'] >= 4.0:
                color = 'blue'
            else:
                color = 'orange'
            
            popup_text = f"""
            🏥 {pharmacy['name']}
            ⭐ {pharmacy['rating']}/5.0
            📞 {pharmacy['phone']}
            🕐 {pharmacy['hours']}
            🚚 {pharmacy['delivery']}
            """
            
            folium.Marker(
                pharmacy['coordinates'],
                popup=popup_text,
                tooltip=pharmacy['name'],
                icon=folium.Icon(color=color, icon='plus-square')
            ).add_to(m)
        
        folium_static(m, width=350, height=400)
        
        st.subheader("🚚 Delivery Information")
        
        delivery_info = [
            {"service": "Standard Delivery", "time": "2-4 hours", "fee": "₹25"},
            {"service": "Express Delivery", "time": "30-60 minutes", "fee": "₹50"},
            {"service": "Free Delivery", "time": "Next day", "fee": "Free (₹500+)"},
            {"service": "Emergency Delivery", "time": "15-30 minutes", "fee": "₹100"}
        ]
        
        for info in delivery_info:
            st.info(f"**{info['service']}**: {info['time']} - {info['fee']}")
        
        st.subheader("💡 Pharmacy Tips")
        
        tips = [
            "💊 Always carry original prescription",
            "🆔 Keep ID proof for controlled medicines",
            "💰 Compare prices before purchasing",
            "📱 Use pharmacy apps for discounts",
            "🔄 Check expiry dates before buying",
            "📞 Call ahead to check medicine availability"
        ]
        
        for tip in tips:
            st.info(tip)

def check_medicine_availability(pharmacy, medicine_name):
    """Check medicine availability at pharmacy"""
    st.subheader(f"💊 Medicine Availability at {pharmacy['name']}")
    
    # Simulate medicine availability check
    availability_status = "In Stock"  # This would be real API call
    
    if availability_status == "In Stock":
        st.success(f"✅ {medicine_name} is available at {pharmacy['name']}")
        
        # Mock pricing info
        price_info = {
            "medicine": medicine_name,
            "price": "₹120.00",
            "discount": "10% off",
            "final_price": "₹108.00",
            "quantity": "Available: 50+ units"
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Price:** {price_info['price']}")
            st.write(f"**Discount:** {price_info['discount']}")
            st.write(f"**Final Price:** {price_info['final_price']}")
        
        with col2:
            st.write(f"**Availability:** {price_info['quantity']}")
            
            if st.button("🛒 Add to Cart", key=f"add_cart_{medicine_name}"):
                st.success(f"Added {medicine_name} to cart")
    else:
        st.warning(f"⚠️ {medicine_name} is currently out of stock at {pharmacy['name']}")
        st.info("We'll notify you when it becomes available")

def show_order_interface(pharmacy):
    """Show medicine ordering interface"""
    st.subheader(f"🛒 Order from {pharmacy['name']}")
    
    with st.form(f"order_form_{pharmacy['name']}"):
        st.write("**📝 Order Details**")
        
        # Prescription upload
        has_prescription = st.checkbox("📄 I have a prescription")
        
        if has_prescription:
            prescription_file = st.file_uploader("📤 Upload Prescription", type=['pdf', 'jpg', 'png'])
        
        # Manual medicine entry
        st.write("**💊 Add Medicines Manually**")
        
        medicine_name = st.text_input("Medicine Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        
        # Contact details
        st.write("**📞 Contact Information**")
        
        col_contact1, col_contact2 = st.columns(2)
        
        with col_contact1:
            customer_name = st.text_input("Name")
            phone_number = st.text_input("Phone Number")
        
        with col_contact2:
            delivery_address = st.text_area("Delivery Address")
            delivery_time = st.selectbox("Preferred Delivery Time", [
                "ASAP", "Within 2 hours", "Today Evening", "Tomorrow Morning"
            ])
        
        # Order notes
        special_instructions = st.text_area("Special Instructions (optional)")
        
        # Submit order
        if st.form_submit_button("🛒 Place Order", use_container_width=True):
            if customer_name and phone_number and delivery_address:
                st.success("✅ Order placed successfully!")
                
                # Order confirmation details
                order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                st.info(f"""
                **Order Confirmation**
                
                Order ID: {order_id}
                Pharmacy: {pharmacy['name']}
                Customer: {customer_name}
                Phone: {phone_number}
                Delivery Time: {delivery_time}
                
                You will receive a confirmation call shortly.
                """)
            else:
                st.error("❌ Please fill in all required fields")

def show_medication_reminders():
    """Medication reminder system"""
    st.header("💊 Medication Reminders")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access medication reminders")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💊 Add New Medication Reminder")
        
        with st.form("medication_reminder_form"):
            # Basic medication info
            col_med1, col_med2 = st.columns(2)
            
            with col_med1:
                med_name = st.text_input("💊 Medication Name")
                med_dosage = st.text_input("📏 Dosage", placeholder="e.g., 500mg, 2 tablets")
                med_type = st.selectbox("💊 Type", ["Tablet", "Capsule", "Syrup", "Injection", "Drops", "Inhaler"])
            
            with col_med2:
                med_frequency = st.selectbox("⏰ Frequency", [
                    "Once daily", "Twice daily", "Three times daily", "Four times daily",
                    "Every 4 hours", "Every 6 hours", "Every 8 hours", "Every 12 hours", "As needed"
                ])
                
                med_duration = st.number_input("📅 Duration (days)", min_value=1, max_value=365, value=7)
                
                with_food = st.selectbox("🍽️ With food?", ["Before meals", "After meals", "With meals", "Empty stomach", "Anytime"])
            
            # Reminder times
            st.write("**⏰ Reminder Times**")
            
            if med_frequency == "Once daily":
                time1 = st.time_input("Time 1", value=time(9, 0))
                reminder_times = [time1]
            elif med_frequency == "Twice daily":
                col_time1, col_time2 = st.columns(2)
                with col_time1:
                    time1 = st.time_input("Morning", value=time(9, 0))
                with col_time2:
                    time2 = st.time_input("Evening", value=time(21, 0))
                reminder_times = [time1, time2]
            elif med_frequency == "Three times daily":
                col_time1, col_time2, col_time3 = st.columns(3)
                with col_time1:
                    time1 = st.time_input("Morning", value=time(8, 0))
                with col_time2:
                    time2 = st.time_input("Afternoon", value=time(14, 0))
                with col_time3:
                    time3 = st.time_input("Evening", value=time(20, 0))
                reminder_times = [time1, time2, time3]
            else:
                reminder_times = [time(9, 0)]  # Default
            
            # Additional settings
            st.write("**🔔 Reminder Settings**")
            
            col_settings1, col_settings2 = st.columns(2)
            
            with col_settings1:
                reminder_methods = st.multiselect("📱 Reminder Method", 
                    ["App Notification", "SMS", "Email", "Phone Call"], default=["App Notification"])
                
                snooze_enabled = st.checkbox("⏰ Enable snooze (10 minutes)", value=True)
            
            with col_settings2:
                advance_reminder = st.number_input("⏰ Advance reminder (minutes)", min_value=0, max_value=60, value=15)
                
                auto_refill_alert = st.checkbox("🔄 Auto refill alert (3 days before)", value=True)
            
            # Medical information
            med_purpose = st.text_input("🎯 Purpose/Condition", placeholder="What is this medication for?")
            
            med_notes = st.text_area("📝 Additional Notes", 
                                   placeholder="Doctor instructions, side effects to watch for, etc.")
            
            # Submit reminder
            if st.form_submit_button("💾 Set Reminder", use_container_width=True):
                if med_name and med_dosage:
                    # Save medication reminder
                    reminder_data = {
                        "name": med_name,
                        "dosage": med_dosage,
                        "type": med_type,
                        "frequency": med_frequency,
                        "duration": med_duration,
                        "with_food": with_food,
                        "times": [t.strftime("%H:%M") for t in reminder_times],
                        "methods": reminder_methods,
                        "purpose": med_purpose,
                        "notes": med_notes
                    }
                    
                    # Save as health record
                    reminder_log = f"Medication Reminder Set: {med_name} {med_dosage}, {med_frequency} for {med_duration} days. Times: {', '.join([t.strftime('%H:%M') for t in reminder_times])}. Purpose: {med_purpose}"
                    
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=reminder_log
                    )
                    
                    if record_id:
                        st.success("✅ Medication reminder set successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Error setting reminder")
                else:
                    st.error("❌ Please enter medication name and dosage")
        
        st.markdown("---")
        
        # Current reminders
        st.subheader("📋 Current Medication Reminders")
        
        # Mock current reminders (would come from database)
        current_reminders = [
            {
                "name": "Metformin",
                "dosage": "500mg",
                "frequency": "Twice daily",
                "times": ["08:00", "20:00"],
                "next_dose": "Today 20:00",
                "days_left": 25,
                "status": "Active"
            },
            {
                "name": "Vitamin D",
                "dosage": "2000 IU",
                "frequency": "Once daily", 
                "times": ["09:00"],
                "next_dose": "Tomorrow 09:00",
                "days_left": 60,
                "status": "Active"
            },
            {
                "name": "Paracetamol",
                "dosage": "500mg",
                "frequency": "As needed",
                "times": ["--"],
                "next_dose": "As needed",
                "days_left": 0,
                "status": "Completed"
            }
        ]
        
        for reminder in current_reminders:
            with st.container():
                col_rem1, col_rem2, col_rem3 = st.columns([2, 1, 1])
                
                with col_rem1:
                    st.markdown(f"**💊 {reminder['name']} {reminder['dosage']}**")
                    st.write(f"Frequency: {reminder['frequency']}")
                    st.write(f"Times: {', '.join(reminder['times'])}")
                
                with col_rem2:
                    st.write(f"**Next Dose:** {reminder['next_dose']}")
                    if reminder['days_left'] > 0:
                        st.write(f"**Days Left:** {reminder['days_left']}")
                    
                    status_color = "green" if reminder['status'] == "Active" else "gray"
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{reminder['status']}</span>", 
                               unsafe_allow_html=True)
                
                with col_rem3:
                    if reminder['status'] == "Active":
                        if st.button("✅ Taken", key=f"taken_{reminder['name']}", use_container_width=True):
                            st.success(f"✅ {reminder['name']} marked as taken")
                        
                        if st.button("✏️ Edit", key=f"edit_{reminder['name']}", use_container_width=True):
                            st.info("Edit functionality would open here")
                    
                    if st.button("🗑️ Delete", key=f"delete_{reminder['name']}", use_container_width=True):
                        st.warning(f"Reminder for {reminder['name']} deleted")
                
                st.markdown("---")
    
    with col2:
        st.subheader("📅 Today's Schedule")
        
        # Today's medication schedule
        todays_schedule = [
            {"time": "08:00", "medicine": "Metformin 500mg", "status": "taken"},
            {"time": "09:00", "medicine": "Vitamin D 2000 IU", "status": "taken"},
            {"time": "14:00", "medicine": "B-Complex", "status": "upcoming"},
            {"time": "20:00", "medicine": "Metformin 500mg", "status": "upcoming"}
        ]
        
        for schedule in todays_schedule:
            if schedule['status'] == "taken":
                st.success(f"✅ {schedule['time']} - {schedule['medicine']}")
            else:
                st.info(f"⏰ {schedule['time']} - {schedule['medicine']}")
        
        st.subheader("📊 Adherence Statistics")
        
        # Adherence metrics
        adherence_stats = {
            "This Week": "95%",
            "This Month": "92%",
            "Overall": "89%",
            "Streak": "12 days"
        }
        
        for stat, value in adherence_stats.items():
            st.metric(stat, value)
        
        st.subheader("🏆 Achievements")
        
        achievements = [
            "🎯 Perfect Week - 7 days 100% adherence",
            "💪 Consistency Champion - 30 days streak",
            "⏰ On Time - 95% on-time doses this month"
        ]
        
        for achievement in achievements:
            st.success(achievement)
        
        st.subheader("🔔 Quick Actions")
        
        if st.button("📱 Test Notification", use_container_width=True):
            st.success("📱 Test notification sent!")
        
        if st.button("📊 View Full Report", use_container_width=True):
            st.info("📊 Opening detailed adherence report")
        
        if st.button("🛒 Refill Reminders", use_container_width=True):
            st.info("🛒 Checking medicines that need refilling")

def show_medicine_orders():
    """Medicine ordering and delivery tracking"""
    st.header("🛒 Medicine Orders & Delivery")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to view your medicine orders")
        return
    
    tab1, tab2, tab3 = st.tabs(["🛒 New Order", "📦 Order History", "🚚 Track Delivery"])
    
    with tab1:
        st.subheader("🛒 Place New Medicine Order")
        
        # Quick reorder from previous orders
        st.markdown("**⚡ Quick Reorder**")
        
        previous_orders = [
            {"medicine": "Metformin 500mg", "last_ordered": "2024-08-15", "pharmacy": "MedPlus"},
            {"medicine": "Vitamin D 2000 IU", "last_ordered": "2024-08-10", "pharmacy": "Apollo"},
            {"medicine": "Paracetamol 500mg", "last_ordered": "2024-08-01", "pharmacy": "HealthMart"}
        ]
        
        for order in previous_orders:
            col_med, col_action = st.columns([3, 1])
            
            with col_med:
                st.write(f"💊 **{order['medicine']}**")
                st.write(f"Last ordered: {order['last_ordered']} from {order['pharmacy']}")
            
            with col_action:
                if st.button("🔄 Reorder", key=f"reorder_{order['medicine']}", use_container_width=True):
                    st.success(f"Added {order['medicine']} to cart")
        
        st.markdown("---")
        
        # New order form
        st.markdown("**📝 Create New Order**")
        
        with st.form("new_order_form"):
            # Medicine selection
            order_type = st.radio("📋 Order Type", ["Upload Prescription", "Select Medicines Manually"])
            
            if order_type == "Upload Prescription":
                prescription_file = st.file_uploader("📤 Upload Prescription", type=['pdf', 'jpg', 'png'])
                
                if prescription_file:
                    st.success("✅ Prescription uploaded successfully")
                    st.info("Our pharmacist will review and add medicines to your order")
            
            else:
                st.write("**💊 Add Medicines**")
                
                # Medicine search and add interface
                medicine_search = st.text_input("🔍 Search Medicine")
                
                # Mock medicine suggestions
                if medicine_search:
                    suggestions = [
                        f"{medicine_search} 500mg Tablet",
                        f"{medicine_search} 250mg Capsule",
                        f"{medicine_search} Syrup"
                    ]
                    
                    selected_medicine = st.selectbox("Select Medicine", suggestions)
                    quantity = st.number_input("Quantity", min_value=1, value=1)
                    
                    if st.button("➕ Add to Cart"):
                        st.success(f"Added {selected_medicine} (Qty: {quantity}) to cart")
            
            # Delivery details
            st.write("**🚚 Delivery Information**")
            
            col_delivery1, col_delivery2 = st.columns(2)
            
            with col_delivery1:
                delivery_address = st.text_area("📍 Delivery Address")
                delivery_phone = st.text_input("📱 Contact Number")
            
            with col_delivery2:
                delivery_time = st.selectbox("⏰ Preferred Delivery Time", [
                    "Standard (2-4 hours)", "Express (30-60 minutes)", "Next Day", "Schedule Later"
                ])
                
                if delivery_time == "Schedule Later":
                    scheduled_date = st.date_input("📅 Delivery Date")
                    scheduled_time = st.time_input("🕐 Delivery Time")
            
            # Payment method
            payment_method = st.selectbox("💳 Payment Method", [
                "Cash on Delivery", "Online Payment", "UPI", "Card Payment"
            ])
            
            # Special instructions
            special_instructions = st.text_area("📝 Special Instructions (optional)")
            
            # Submit order
            if st.form_submit_button("🛒 Place Order", use_container_width=True):
                if delivery_address and delivery_phone:
                    st.success("✅ Order placed successfully!")
                    
                    # Generate order ID
                    order_id = f"MED{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    st.info(f"""
                    **Order Confirmation**
                    
                    Order ID: {order_id}
                    Delivery Time: {delivery_time}
                    Payment: {payment_method}
                    
                    You will receive updates via SMS and app notifications.
                    """)
                else:
                    st.error("❌ Please fill in delivery address and phone number")
    
    with tab2:
        st.subheader("📦 Order History")
        
        # Mock order history
        order_history = [
            {
                "order_id": "MED20240820001",
                "date": "2024-08-20",
                "pharmacy": "MedPlus Pharmacy",
                "items": ["Metformin 500mg x10", "Vitamin D 2000 IU x30"],
                "total": "₹245.00",
                "status": "Delivered",
                "delivery_date": "2024-08-20"
            },
            {
                "order_id": "MED20240815002", 
                "date": "2024-08-15",
                "pharmacy": "Apollo Pharmacy",
                "items": ["Paracetamol 500mg x20"],
                "total": "₹85.00",
                "status": "Delivered",
                "delivery_date": "2024-08-15"
            },
            {
                "order_id": "MED20240825003",
                "date": "2024-08-25",
                "pharmacy": "HealthMart Pharmacy",
                "items": ["B-Complex x30", "Calcium tablets x60"],
                "total": "₹180.00",
                "status": "In Transit",
                "delivery_date": "Expected today"
            }
        ]
        
        for order in order_history:
            with st.expander(f"📦 Order {order['order_id']} - {order['status']}", expanded=False):
                col_order1, col_order2, col_order3 = st.columns([2, 1, 1])
                
                with col_order1:
                    st.write(f"**📅 Order Date:** {order['date']}")
                    st.write(f"**🏥 Pharmacy:** {order['pharmacy']}")
                    st.write("**💊 Items:**")
                    for item in order['items']:
                        st.write(f"• {item}")
                
                with col_order2:
                    st.write(f"**💰 Total:** {order['total']}")
                    st.write(f"**🚚 Delivery:** {order['delivery_date']}")
                    
                    status_color = "green" if order['status'] == "Delivered" else "orange" if order['status'] == "In Transit" else "red"
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{order['status']}</span>", 
                               unsafe_allow_html=True)
                
                with col_order3:
                    if order['status'] == "Delivered":
                        if st.button("⭐ Rate Order", key=f"rate_{order['order_id']}", use_container_width=True):
                            st.info("Rating interface would open")
                        
                        if st.button("🔄 Reorder", key=f"reorder_history_{order['order_id']}", use_container_width=True):
                            st.success("Items added to cart")
                    
                    elif order['status'] == "In Transit":
                        if st.button("📍 Track", key=f"track_{order['order_id']}", use_container_width=True):
                            st.info("Opening tracking details")
                    
                    if st.button("📄 Invoice", key=f"invoice_{order['order_id']}", use_container_width=True):
                        st.success("Invoice downloaded")
    
    with tab3:
        st.subheader("🚚 Track Your Delivery")
        
        # Order ID input for tracking
        track_order_id = st.text_input("📦 Enter Order ID", placeholder="e.g., MED20240825003")
        
        if track_order_id or st.button("🔍 Track Order"):
            # Mock tracking information
            if track_order_id:
                st.success(f"📦 Tracking Order: {track_order_id}")
                
                # Delivery timeline
                tracking_steps = [
                    {"step": "Order Placed", "time": "Today 10:30 AM", "status": "completed"},
                    {"step": "Order Confirmed", "time": "Today 10:45 AM", "status": "completed"},
                    {"step": "Medicines Packed", "time": "Today 11:15 AM", "status": "completed"},
                    {"step": "Out for Delivery", "time": "Today 12:00 PM", "status": "current"},
                    {"step": "Delivered", "time": "Expected by 2:00 PM", "status": "pending"}
                ]
                
                st.subheader("📍 Delivery Timeline")
                
                for i, step in enumerate(tracking_steps):
                    if step['status'] == 'completed':
                        st.success(f"✅ {step['step']} - {step['time']}")
                    elif step['status'] == 'current':
                        st.warning(f"🚚 {step['step']} - {step['time']}")
                    else:
                        st.info(f"⏳ {step['step']} - {step['time']}")
                
                # Delivery details
                col_track1, col_track2 = st.columns(2)
                
                with col_track1:
                    st.subheader("🚚 Delivery Details")
                    st.write("**Delivery Person:** Rajesh Kumar")
                    st.write("**Phone:** +91-987-654-3210")
                    st.write("**Vehicle:** Bike - MH01AB1234")
                    st.write("**Estimated Time:** 2:00 PM")
                
                with col_track2:
                    st.subheader("📦 Order Summary")
                    st.write("**Order ID:** MED20240825003")
                    st.write("**Items:** 2 medicines")
                    st.write("**Total:** ₹180.00")
                    st.write("**Payment:** Cash on Delivery")
                
                # Live tracking map (mock)
                st.subheader("🗺️ Live Tracking")
                
                # Mock delivery location map
                delivery_map = folium.Map(location=[28.6139, 77.2090], zoom_start=14)
                
                # Add delivery person location
                folium.Marker(
                    [28.6150, 77.2100],
                    popup="🚚 Delivery Person Location",
                    tooltip="Rajesh Kumar - Out for Delivery",
                    icon=folium.Icon(color='blue', icon='bicycle')
                ).add_to(delivery_map)
                
                # Add destination
                folium.Marker(
                    [28.6139, 77.2090],
                    popup="📍 Delivery Address",
                    tooltip="Your Location",
                    icon=folium.Icon(color='red', icon='home')
                ).add_to(delivery_map)
                
                folium_static(delivery_map, width=700, height=300)
                
                # Contact options
                st.subheader("📞 Need Help?")
                
                col_help1, col_help2, col_help3 = st.columns(3)
                
                with col_help1:
                    if st.button("📞 Call Delivery Person", use_container_width=True):
                        st.success("Calling Rajesh Kumar...")
                
                with col_help2:
                    if st.button("🏥 Call Pharmacy", use_container_width=True):
                        st.success("Calling HealthMart Pharmacy...")
                
                with col_help3:
                    if st.button("💬 Customer Support", use_container_width=True):
                        st.success("Connecting to customer support...")
            else:
                st.warning("Please enter a valid Order ID")

def show_price_comparison():
    """Medicine price comparison across pharmacies"""
    st.header("💰 Medicine Price Comparison")
    
    st.info("💡 Compare prices across different pharmacies to find the best deals")
    
    # Medicine search for price comparison
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Search Medicine for Price Comparison")
        
        medicine_name = st.text_input("💊 Enter Medicine Name", placeholder="e.g., Paracetamol, Metformin")
        
        if medicine_name:
            show_price_comparison_results(medicine_name)
    
    with col2:
        st.subheader("💡 Price Comparison Tips")
        
        tips = [
            "💊 Generic medicines are usually cheaper",
            "🏥 Different pharmacies may have different prices",
            "📦 Bulk purchases often have discounts",
            "💳 Some payment methods offer cashback",
            "🎯 Look for pharmacy-specific offers",
            "📱 Use pharmacy apps for additional discounts"
        ]
        
        for tip in tips:
            st.info(tip)
        
        st.subheader("🏆 Best Price Guarantee")
        
        st.success("If you find a lower price elsewhere, we'll match it!")
        
        if st.button("📞 Price Match Request", use_container_width=True):
            st.info("Price match request form would open")

def show_price_comparison_results(medicine_name):
    """Show price comparison results for a medicine"""
    st.subheader(f"💰 Price Comparison for {medicine_name}")
    
    # Mock price comparison data
    price_data = [
        {
            "pharmacy": "MedPlus Pharmacy",
            "price": "₹85.00",
            "discount": "10%",
            "final_price": "₹76.50",
            "delivery_fee": "₹25",
            "total": "₹101.50",
            "rating": 4.5,
            "delivery_time": "2-4 hours",
            "in_stock": True
        },
        {
            "pharmacy": "Apollo Pharmacy", 
            "price": "₹90.00",
            "discount": "15%",
            "final_price": "₹76.50",
            "delivery_fee": "Free",
            "total": "₹76.50",
            "rating": 4.7,
            "delivery_time": "3-5 hours",
            "in_stock": True
        },
        {
            "pharmacy": "HealthMart Pharmacy",
            "price": "₹88.00",
            "discount": "5%",
            "final_price": "₹83.60",
            "delivery_fee": "₹20",
            "total": "₹103.60",
            "rating": 4.3,
            "delivery_time": "1-2 hours",
            "in_stock": True
        },
        {
            "pharmacy": "QuickMed Express",
            "price": "₹95.00",
            "discount": "20%",
            "final_price": "₹76.00",
            "delivery_fee": "₹50",
            "total": "₹126.00",
            "rating": 4.2,
            "delivery_time": "30-60 min",
            "in_stock": False
        }
    ]
    
    # Sort by total price
    price_data.sort(key=lambda x: float(x['total'].replace('₹', '')))
    
    # Display comparison table
    for i, pharmacy in enumerate(price_data):
        # Highlight best price
        if i == 0:
            st.success("🏆 **BEST PRICE**")
        
        with st.container():
            col_pharm, col_price, col_details, col_action = st.columns([2, 2, 2, 1])
            
            with col_pharm:
                st.markdown(f"### 🏥 {pharmacy['pharmacy']}")
                stars = "⭐" * int(pharmacy['rating'])
                st.write(f"{stars} {pharmacy['rating']}/5.0")
                
                if pharmacy['in_stock']:
                    st.success("✅ In Stock")
                else:
                    st.error("❌ Out of Stock")
            
            with col_price:
                st.write(f"**Original Price:** {pharmacy['price']}")
                st.write(f"**Discount:** {pharmacy['discount']}")
                st.write(f"**Medicine Price:** {pharmacy['final_price']}")
                st.write(f"**Delivery Fee:** {pharmacy['delivery_fee']}")
                
                # Highlight total price
                if i == 0:
                    st.success(f"**TOTAL: {pharmacy['total']}**")
                else:
                    st.write(f"**Total:** {pharmacy['total']}")
            
            with col_details:
                st.write(f"**Delivery Time:** {pharmacy['delivery_time']}")
                
                # Calculate savings compared to highest price
                highest_price = max(float(p['total'].replace('₹', '')) for p in price_data if p['in_stock'])
                current_price = float(pharmacy['total'].replace('₹', ''))
                savings = highest_price - current_price
                
                if savings > 0:
                    st.success(f"**Savings:** ₹{savings:.2f}")
                else:
                    st.write("**Savings:** --")
            
            with col_action:
                if pharmacy['in_stock']:
                    if st.button("🛒 Order", key=f"order_price_{i}", use_container_width=True):
                        st.success(f"Redirecting to {pharmacy['pharmacy']}")
                    
                    if st.button("📞 Call", key=f"call_price_{i}", use_container_width=True):
                        st.success(f"Calling {pharmacy['pharmacy']}")
                else:
                    st.error("Out of Stock")
            
            st.markdown("---")
    
    # Price history chart (mock)
    st.subheader("📈 Price History")
    
    # Create a simple price trend chart
    import plotly.graph_objects as go
    
    dates = ['2024-08-01', '2024-08-08', '2024-08-15', '2024-08-22']
    prices = [88, 85, 87, 85]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines+markers',
        name=f'{medicine_name} Price Trend',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title=f"Price Trend for {medicine_name}",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_digital_prescriptions():
    """Digital prescription management"""
    st.header("📱 Digital Prescriptions")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access digital prescriptions")
        return
    
    tab1, tab2, tab3 = st.tabs(["📱 My Prescriptions", "📤 Upload Prescription", "🔄 Prescription History"])
    
    with tab1:
        st.subheader("📱 Current Digital Prescriptions")
        
        # Mock digital prescriptions
        prescriptions = [
            {
                "id": "RX20240820001",
                "doctor": "Dr. Sarah Johnson",
                "date": "2024-08-20",
                "hospital": "City General Hospital",
                "medicines": [
                    {"name": "Metformin", "dosage": "500mg", "frequency": "Twice daily", "duration": "30 days"},
                    {"name": "Vitamin D", "dosage": "2000 IU", "frequency": "Once daily", "duration": "90 days"}
                ],
                "status": "Active",
                "expires": "2024-11-20"
            },
            {
                "id": "RX20240815002",
                "doctor": "Dr. Michael Chen",
                "date": "2024-08-15", 
                "hospital": "Heart Care Clinic",
                "medicines": [
                    {"name": "Paracetamol", "dosage": "500mg", "frequency": "As needed", "duration": "7 days"}
                ],
                "status": "Completed",
                "expires": "2024-08-22"
            }
        ]
        
        for prescription in prescriptions:
            with st.expander(f"📋 Prescription {prescription['id']} - {prescription['status']}", expanded=prescription['status']=='Active'):
                col_rx1, col_rx2 = st.columns([2, 1])
                
                with col_rx1:
                    st.write(f"**👨‍⚕️ Doctor:** {prescription['doctor']}")
                    st.write(f"**🏥 Hospital:** {prescription['hospital']}")
                    st.write(f"**📅 Date:** {prescription['date']}")
                    st.write(f"**⏰ Expires:** {prescription['expires']}")
                    
                    st.write("**💊 Prescribed Medicines:**")
                    for medicine in prescription['medicines']:
                        st.write(f"• {medicine['name']} {medicine['dosage']} - {medicine['frequency']} for {medicine['duration']}")
                
                with col_rx2:
                    status_color = "green" if prescription['status'] == "Active" else "gray"
                    st.markdown(f"**Status:** <span style='color:{status_color}'>{prescription['status']}</span>", 
                               unsafe_allow_html=True)
                    
                    if prescription['status'] == "Active":
                        if st.button("🛒 Order Medicines", key=f"order_rx_{prescription['id']}", use_container_width=True):
                            st.success("Redirecting to medicine order page")
                        
                        if st.button("📧 Share", key=f"share_rx_{prescription['id']}", use_container_width=True):
                            st.success("Prescription shared successfully")
                    
                    if st.button("📱 Download", key=f"download_rx_{prescription['id']}", use_container_width=True):
                        st.success("Prescription downloaded")
                    
                    if st.button("📞 Call Doctor", key=f"call_doc_{prescription['id']}", use_container_width=True):
                        st.success(f"Calling {prescription['doctor']}")
    
    with tab2:
        st.subheader("📤 Upload New Prescription")
        
        with st.form("upload_prescription_form"):
            # Prescription details
            st.write("**📋 Prescription Information**")
            
            col_upload1, col_upload2 = st.columns(2)
            
            with col_upload1:
                doctor_name = st.text_input("👨‍⚕️ Doctor Name")
                hospital_name = st.text_input("🏥 Hospital/Clinic Name")
                prescription_date = st.date_input("📅 Prescription Date")
            
            with col_upload2:
                doctor_phone = st.text_input("📞 Doctor's Phone")
                specialization = st.text_input("🩺 Doctor's Specialization")
                visit_reason = st.text_input("🎯 Reason for Visit")
            
            # File upload
            st.write("**📁 Upload Prescription Image/PDF**")
            
            prescription_file = st.file_uploader("📤 Choose file", type=['pdf', 'jpg', 'jpeg', 'png'])
            
            if prescription_file:
                st.success("✅ Prescription file uploaded successfully")
            
            # Manual medicine entry (optional)
            st.write("**💊 Add Medicines (Optional)**")
            
            medicines_list = st.text_area("📝 List of Medicines", 
                                        placeholder="Medicine Name - Dosage - Frequency - Duration\ne.g., Paracetamol 500mg - Twice daily - 5 days")
            
            # Additional notes
            prescription_notes = st.text_area("📝 Additional Notes")
            
            # Submit prescription
            if st.form_submit_button("📤 Upload Prescription", use_container_width=True):
                if doctor_name and hospital_name and (prescription_file or medicines_list):
                    st.success("✅ Prescription uploaded successfully!")
                    
                    # Generate prescription ID
                    rx_id = f"RX{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Save prescription info
                    prescription_info = f"Digital Prescription {rx_id}: Doctor: {doctor_name} from {hospital_name} on {prescription_date}. Reason: {visit_reason}."
                    if medicines_list:
                        prescription_info += f" Medicines: {medicines_list}."
                    if prescription_notes:
                        prescription_info += f" Notes: {prescription_notes}."
                    
                    record_id = data_manager.add_health_record(
                        st.session_state.user_id,
                        notes=prescription_info
                    )
                    
                    if record_id:
                        st.info(f"""
                        **Prescription Uploaded Successfully**
                        
                        Prescription ID: {rx_id}
                        Doctor: {doctor_name}
                        Hospital: {hospital_name}
                        
                        Your prescription has been digitized and is now available in your health records.
                        """)
                    else:
                        st.error("❌ Error saving prescription")
                else:
                    st.error("❌ Please fill in required fields and upload prescription file")
    
    with tab3:
        st.subheader("🔄 Prescription History")
        
        # Filter options
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            date_range_filter = st.selectbox("📅 Date Range", [
                "All Time", "Last 30 days", "Last 3 months", "Last 6 months", "Last year"
            ])
        
        with col_filter2:
            doctor_filter = st.selectbox("👨‍⚕️ Doctor", [
                "All Doctors", "Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Priya Sharma"
            ])
        
        # Prescription statistics
        st.subheader("📊 Prescription Statistics")
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("📋 Total Prescriptions", "15")
        
        with col_stat2:
            st.metric("👨‍⚕️ Doctors Consulted", "5")
        
        with col_stat3:
            st.metric("💊 Medicines Prescribed", "42")
        
        with col_stat4:
            st.metric("🔄 Refills", "28")
        
        # Prescription timeline
        st.subheader("📅 Prescription Timeline")
        
        # Mock timeline data
        timeline_data = [
            {"date": "2024-08-20", "doctor": "Dr. Sarah Johnson", "medicines": 2, "type": "Regular Checkup"},
            {"date": "2024-08-15", "doctor": "Dr. Michael Chen", "medicines": 1, "type": "Emergency Visit"},
            {"date": "2024-08-01", "doctor": "Dr. Priya Sharma", "medicines": 3, "type": "Follow-up"},
            {"date": "2024-07-20", "doctor": "Dr. Sarah Johnson", "medicines": 2, "type": "Regular Checkup"}
        ]
        
        for item in timeline_data:
            with st.container():
                col_time1, col_time2, col_time3 = st.columns([1, 2, 1])
                
                with col_time1:
                    st.write(f"📅 **{item['date']}**")
                
                with col_time2:
                    st.write(f"👨‍⚕️ {item['doctor']}")
                    st.write(f"🎯 {item['type']}")
                
                with col_time3:
                    st.write(f"💊 {item['medicines']} medicines")
                
                st.markdown("---")
        
        # Export options
        st.subheader("📤 Export Prescription History")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📧 Email Complete History", use_container_width=True):
                st.success("📧 Prescription history emailed successfully!")
        
        with col_export2:
            if st.button("📱 Download PDF Report", use_container_width=True):
                st.success("📱 Prescription history PDF downloaded!")

if __name__ == "__main__":
    main()
