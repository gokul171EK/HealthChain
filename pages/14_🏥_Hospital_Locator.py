import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils.styling import add_app_styling
from utils.gemini_client import get_gemini_response
import json

def parse_ai_response(response_text):
    """Safely parse the JSON response from the AI model."""
    try:
        # The AI might return the JSON within a code block, so we clean it up
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        
        hospitals = json.loads(response_text)
        
        # Basic validation to ensure we have a list of dictionaries
        if isinstance(hospitals, list) and all(isinstance(h, dict) for h in hospitals):
            return hospitals
        else:
            return None
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error parsing JSON: {e}")
        return None

def show_hospital_finder():
    """Main tab for finding and filtering hospitals using AI-fetched data."""
    st.header("Find Hospitals in Your City")
    
    location = st.text_input("Enter a city name (e.g., Salem, Chennai, Madurai)", "Coimbatore")

    if st.button("Find Hospitals", use_container_width=True):
        with st.spinner(f"Searching for top hospitals in {location}..."):
            # Construct a prompt to get structured JSON data from Gemini
            prompt = f"""
            You are a helpful assistant that provides structured geographic and business data.
            Find the top 4-5 well-known, multi-specialty hospitals in the city of "{location}".
            Your response MUST be a valid JSON array of objects. Do not include any text before or after the JSON array.
            Each object in the array must represent a hospital and have the following keys:
            - "name" (string)
            - "address" (string)
            - "phone" (string, if available, otherwise "N/A")
            - "specialties" (array of 5-6 key specialty strings)
            - "rating" (number, between 1.0 and 5.0)
            - "coordinates" (array of two numbers, [latitude, longitude])
            """
            
            response = get_gemini_response(prompt)
            hospitals = parse_ai_response(response)
            
            if hospitals:
                st.session_state.hospitals = hospitals
                st.session_state.location_center = [hospitals[0]['coordinates'][0], hospitals[0]['coordinates'][1]]
            else:
                st.session_state.hospitals = []
                st.error("Sorry, I couldn't retrieve hospital data for that location. Please try another city.")

    if 'hospitals' in st.session_state and st.session_state.hospitals:
        hospitals = st.session_state.hospitals
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Hospital Locations in {location}")
            if 'location_center' in st.session_state:
                m = folium.Map(location=st.session_state.location_center, zoom_start=12)
                for hospital in hospitals:
                    folium.Marker(
                        hospital["coordinates"],
                        popup=f"<strong>{hospital['name']}</strong><br>Rating: {hospital.get('rating', 'N/A')}",
                        tooltip=hospital['name'],
                        icon=folium.Icon(color="red", icon="hospital")
                    ).add_to(m)
                folium_static(m, height=400)

        with col2:
            st.subheader("Filter Results")
            all_specialties = sorted(list(set(s for h in hospitals for s in h.get("specialties", []))))
            specialty_filter = st.selectbox("Filter by Specialty", ["All"] + all_specialties)
            min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.1)

        st.markdown("---")
        st.subheader("Hospital Directory")

        filtered_hospitals = [h for h in hospitals if h.get("rating", 0) >= min_rating]
        if specialty_filter != "All":
            filtered_hospitals = [h for h in filtered_hospitals if specialty_filter in h.get("specialties", [])]

        if not filtered_hospitals:
            st.warning("No hospitals match your criteria.")
        else:
            for hospital in filtered_hospitals:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{hospital.get('name', 'N/A')}**")
                        st.caption(hospital.get('address', 'N/A'))
                        rating = hospital.get('rating', 0)
                        st.markdown(f"**Rating:** {'⭐' * int(rating)} ({rating})")
                    with col2:
                        st.markdown(f"**Specialties:** {', '.join(hospital.get('specialties', [])[:3])}...")
                        st.markdown(f"**Phone:** {hospital.get('phone', 'N/A')}")
                    with col3:
                        if st.button("View Details", key=f"details_{hospital.get('name')}"):
                            st.info("Details view would open here.")


def show_ai_assistant():
    """AI-powered hospital recommendation assistant."""
    st.header("🤖 AI Hospital Assistant")
    
    if 'hospitals' not in st.session_state or not st.session_state.hospitals:
        st.warning("Please find hospitals in a city first using the 'Find Hospitals' tab.")
        return

    st.info("Describe your medical need, and our AI will recommend the best hospital for you from the list we found.")
    
    user_query = st.text_area(
        "What kind of medical help do you need?",
        placeholder="e.g., 'My father has chest pain and needs a good heart doctor', 'I need a hospital for my child's fever', 'Which hospital is best for a broken leg?'",
        height=100
    )

    if st.button("Get Recommendation", use_container_width=True):
        if user_query:
            with st.spinner("AI is analyzing your request..."):
                hospital_info_text = ""
                for h in st.session_state.hospitals:
                    hospital_info_text += f"- Hospital: {h.get('name')}, Specialties: {', '.join(h.get('specialties', []))}, Rating: {h.get('rating')}.\n"

                system_prompt = f"""
                You are an expert AI Hospital Recommendation Assistant. Your task is to analyze a user's medical query and recommend the most suitable hospital from the provided list.

                Here is the list of available hospitals:
                {hospital_info_text}

                Analyze the user's query below. Your response should be in three parts:
                1.  **Analysis:** Briefly explain which medical specialty you identified from the user's query.
                2.  **Top Recommendation:** State the single best hospital for the user's need. Justify your choice based on its specialties and high rating.
                3.  **Other Good Options:** List one or two other suitable hospitals as alternatives.

                Your tone must be helpful, empathetic, and clear. Always conclude with a disclaimer to call emergency services for critical situations.
                """
                
                full_prompt = f"{system_prompt}\n\nUser's Query: \"{user_query}\""
                ai_response = get_gemini_response(full_prompt)
                st.markdown(ai_response)
        else:
            st.warning("Please describe your medical need.")


def show_admission_guide():
    """Static guide to the hospital admission process."""
    st.header("📋 General Hospital Admission Guide")
    st.info("Understanding the admission process can help reduce stress during a hospital visit.")

    st.subheader("Step 1: Registration")
    st.markdown("""
    -   Proceed to the hospital's reception or admissions desk.
    -   Provide the patient's personal details and a valid ID proof.
    -   If you have a doctor's referral letter, provide it here.
    """)

    st.subheader("Step 2: Insurance & Billing")
    st.markdown("""
    -   Present your health insurance card.
    -   The hospital's insurance desk (TPA desk) will verify your coverage.
    -   You may be required to pay an initial deposit.
    """)

    st.subheader("Step 3: Medical Assessment & Room Allocation")
    st.markdown("""
    -   A nurse or doctor will conduct an initial medical assessment.
    -   Based on the doctor's recommendation, you will be allocated a room.
    """)
    
    st.error("**In an Emergency:** Proceed directly to the Emergency/Casualty department. Registration will be handled simultaneously while the patient receives immediate care.")


def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    add_app_styling(theme=st.session_state.theme)

    st.title("🏥 Hospital Locator & Assistant")
    st.markdown("### Find, Compare, and Get Information on Hospitals Near You")
    
    tab1, tab2, tab3 = st.tabs([
        "🔍 Find Hospitals", 
        "🤖 AI Assistant", 
        "📋 Admission Guide"
    ])
    
    with tab1:
        show_hospital_finder()
    with tab2:
        show_ai_assistant()
    with tab3:
        show_admission_guide()

if __name__ == "__main__":
    main()

