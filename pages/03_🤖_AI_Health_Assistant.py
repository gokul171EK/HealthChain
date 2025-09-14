import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from utils.ai_simulator import AISimulator
from utils.translator import Translator
from utils.styling import add_app_styling

# Initialize components
@st.cache_resource
def init_components():
    return DataManager(), AISimulator(), Translator()

data_manager, ai_simulator, translator = init_components()

st.set_page_config(
    page_title="AI Health Assistant - HEALTHTECH",
    page_icon="🤖",
    layout="wide"
)

def main():
    add_app_styling()
    st.title("🤖 AI Health Assistant")
    st.markdown("### Your Personal AI-Powered Health Companion")
    
    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to access AI Health Assistant features")
        st.info("Go to the main page to login or register")
        return
    
    # Tabs for different AI features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Symptom Checker", 
        "📊 Health Predictions", 
        "💊 Medicine Info", 
        "🌐 Medical Translator", 
        "📈 Health Insights"
    ])
    
    with tab1:
        show_symptom_checker()
    
    with tab2:
        show_health_predictions()
    
    with tab3:
        show_medicine_info()
    
    with tab4:
        show_medical_translator()
    
    with tab5:
        show_health_insights()

def show_symptom_checker():
    """AI-powered symptom checker"""
    st.header("🔍 AI Symptom Checker")
    st.warning("⚠️ This is a preliminary assessment tool. Always consult a healthcare professional for proper diagnosis.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Describe Your Symptoms")
        
        # Symptom selection interface
        st.markdown("**Select your symptoms from the list below:**")
        
        symptom_categories = {
            "🤒 General": ["Fever", "Fatigue", "Weakness", "Chills", "Sweating"],
            "🧠 Head & Neck": ["Headache", "Dizziness", "Sore throat", "Neck pain", "Eye pain"],
            "🫁 Respiratory": ["Cough", "Shortness of breath", "Chest pain", "Wheezing", "Runny nose"],
            "🫀 Cardiovascular": ["Chest pain", "Heart palpitations", "Irregular heartbeat", "Swelling"],
            "🤢 Digestive": ["Nausea", "Vomiting", "Stomach pain", "Diarrhea", "Constipation", "Loss of appetite"],
            "🦴 Musculoskeletal": ["Joint pain", "Muscle pain", "Back pain", "Stiffness", "Swelling"],
            "🧠 Neurological": ["Dizziness", "Confusion", "Memory problems", "Numbness", "Tingling"],
            "🌡️ Skin": ["Rash", "Itching", "Swelling", "Bruising", "Changes in skin color"]
        }
        
        selected_symptoms = []
        
        for category, symptoms in symptom_categories.items():
            with st.expander(category):
                for symptom in symptoms:
                    if st.checkbox(symptom, key=f"symptom_{symptom}"):
                        selected_symptoms.append(symptom)
        
        # Additional symptom input
        st.subheader("📝 Additional Symptoms")
        custom_symptoms = st.text_area(
            "Describe any other symptoms not listed above:",
            placeholder="e.g., unusual tiredness, specific pain location, duration of symptoms..."
        )
        
        # Symptom duration and severity
        col_duration, col_severity = st.columns(2)
        
        with col_duration:
            symptom_duration = st.selectbox(
                "⏰ How long have you had these symptoms?",
                ["Less than 1 day", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"]
            )
        
        with col_severity:
            symptom_severity = st.selectbox(
                "📊 How severe are your symptoms?",
                ["Mild", "Moderate", "Severe", "Very severe"]
            )
        
        # Additional health information
        st.subheader("🏥 Additional Information")
        
        col_age, col_temp = st.columns(2)
        
        with col_age:
            current_medications = st.text_input("💊 Current medications (if any)")
        
        with col_temp:
            body_temperature = st.number_input("🌡️ Body temperature (°F)", min_value=95.0, max_value=110.0, value=98.6, step=0.1)
        
        # Analyze symptoms button
        if st.button("🔍 Analyze Symptoms", use_container_width=True):
            if selected_symptoms or custom_symptoms:
                analyze_symptoms(selected_symptoms, custom_symptoms, symptom_duration, symptom_severity, body_temperature)
            else:
                st.error("❌ Please select or describe at least one symptom")
    
    with col2:
        st.subheader("🚨 Emergency Warning Signs")
        
        emergency_signs = [
            "🆘 Severe chest pain or pressure",
            "🫁 Difficulty breathing or shortness of breath",
            "🧠 Sudden confusion or loss of consciousness",
            "🩸 Severe bleeding that won't stop",
            "🤕 Signs of stroke (face drooping, arm weakness, speech difficulty)",
            "🔥 High fever with stiff neck",
            "🤮 Persistent vomiting with signs of dehydration",
            "⚡ Severe allergic reaction"
        ]
        
        st.error("If you experience any of these, seek immediate medical attention:")
        
        for sign in emergency_signs:
            st.markdown(f"- {sign}")
        
        if st.button("🚨 Call Emergency Services", use_container_width=True):
            st.error("🚨 Emergency: 102 | Ambulance: 108")
        
        st.markdown("---")
        
        st.subheader("💡 Health Tips")
        
        tips = [
            "💧 Stay hydrated - drink plenty of water",
            "😴 Get adequate rest and sleep",
            "🍎 Maintain a balanced diet",
            "🚶‍♂️ Regular light exercise if feeling well",
            "🧼 Practice good hygiene",
            "📱 Monitor your symptoms",
            "👨‍⚕️ Don't hesitate to consult a doctor"
        ]
        
        for tip in tips:
            st.info(tip)

def analyze_symptoms(selected_symptoms, custom_symptoms, duration, severity, temperature):
    """Analyze symptoms using AI simulator"""
    st.subheader("🤖 AI Analysis Results")
    
    # Combine all symptoms
    all_symptoms = selected_symptoms.copy()
    if custom_symptoms:
        all_symptoms.extend([s.strip() for s in custom_symptoms.split(',') if s.strip()])
    
    # Get AI analysis
    analysis = ai_simulator.check_symptoms(all_symptoms, {
        'duration': duration,
        'severity': severity,
        'temperature': temperature
    })
    
    if 'error' in analysis:
        st.error(f"❌ {analysis['error']}")
        return
    
    # Display overall assessment
    severity_colors = {
        "severe": "red",
        "moderate": "orange", 
        "mild": "green"
    }
    
    severity_color = severity_colors.get(analysis['overall_severity'], 'blue')
    
    st.markdown(f"### 📋 Overall Assessment: <span style='color:{severity_color}'>{analysis['overall_severity'].upper()}</span>", 
                unsafe_allow_html=True)
    
    # Overall assessment message
    if analysis['overall_severity'] == 'severe':
        st.error(analysis['overall_assessment'])
    elif analysis['overall_severity'] == 'moderate':
        st.warning(analysis['overall_assessment'])
    else:
        st.success(analysis['overall_assessment'])
    
    # Detailed symptom analysis
    st.subheader("🔍 Detailed Analysis")
    
    for symptom_result in analysis['symptoms_analyzed']:
        with st.expander(f"📊 {symptom_result['symptom']} Analysis"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Possible Causes:**")
                for cause in symptom_result['possible_causes']:
                    st.write(f"• {cause}")
            
            with col2:
                st.markdown("**💡 Recommendations:**")
                for rec in symptom_result['recommendations']:
                    st.write(f"• {rec}")
    
    # Next steps
    st.subheader("📋 Recommended Next Steps")
    
    if analysis['overall_severity'] == 'severe':
        st.error("🚨 **URGENT ACTION REQUIRED:**")
        st.write("• Seek immediate medical attention")
        st.write("• Go to emergency room or call ambulance")
        st.write("• Do not delay treatment")
    elif analysis['overall_severity'] == 'moderate':
        st.warning("⚠️ **MEDICAL CONSULTATION RECOMMENDED:**")
        st.write("• Schedule appointment with your doctor within 24-48 hours")
        st.write("• Monitor symptoms closely")
        st.write("• Seek immediate care if symptoms worsen")
    else:
        st.info("✅ **HOME CARE AND MONITORING:**")
        st.write("• Follow the recommendations above")
        st.write("• Monitor symptoms for any changes")
        st.write("• Consult doctor if symptoms persist or worsen")
    
    # Disclaimer
    st.info(analysis['disclaimer'])
    
    # Save analysis to health records
    if st.button("💾 Save Analysis to Health Records"):
        record_id = data_manager.add_health_record(
            st.session_state.user_id,
            notes=f"AI Symptom Analysis: {', '.join(all_symptoms)} - {analysis['overall_severity']} severity"
        )
        if record_id:
            st.success("✅ Analysis saved to your health records")

def show_health_predictions():
    """AI-powered health risk predictions"""
    st.header("📊 Health Risk Predictions")
    st.info("💡 AI-powered analysis to predict potential health risks based on your profile and lifestyle")
    
    user_data = st.session_state.user_data
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Lifestyle Assessment")
        
        with st.form("lifestyle_assessment"):
            st.markdown("**Answer these questions for personalized risk assessment:**")
            
            # Lifestyle factors
            col_life1, col_life2 = st.columns(2)
            
            with col_life1:
                smoking = st.selectbox("🚬 Smoking status", ["Never", "Former", "Current"])
                alcohol = st.selectbox("🍷 Alcohol consumption", ["None", "Occasional", "Moderate", "Heavy"])
                exercise = st.selectbox("🏃‍♂️ Exercise frequency", ["None", "1-2 times/week", "3-4 times/week", "Daily"])
                stress = st.selectbox("😰 Stress level", ["Low", "Moderate", "High", "Very high"])
            
            with col_life2:
                sleep = st.selectbox("😴 Sleep quality", ["Poor", "Fair", "Good", "Excellent"])
                diet = st.selectbox("🥗 Diet quality", ["Poor", "Fair", "Good", "Excellent"])
                family_history = st.multiselect("👨‍👩‍👧‍👦 Family history", 
                                               ["Diabetes", "Heart disease", "Cancer", "Hypertension", "None"])
                work_type = st.selectbox("💼 Work type", ["Sedentary", "Light physical", "Moderate physical", "Heavy physical"])
            
            # Additional factors
            st.subheader("🏥 Health Factors")
            
            col_health1, col_health2 = st.columns(2)
            
            with col_health1:
                bmi = st.number_input("⚖️ BMI (if known)", min_value=15.0, max_value=50.0, value=25.0)
                cholesterol = st.selectbox("🧪 Cholesterol level", ["Unknown", "Normal", "Borderline", "High"])
            
            with col_health2:
                blood_pressure = st.selectbox("🩺 Blood pressure", ["Unknown", "Normal", "Pre-hypertensive", "Hypertensive"])
                diabetes_risk = st.selectbox("🍯 Diabetes indicators", ["None", "Pre-diabetic", "Family history", "Symptoms present"])
            
            submit_assessment = st.form_submit_button("📊 Generate Risk Assessment")
            
            if submit_assessment:
                generate_risk_predictions(user_data, {
                    'smoking': smoking,
                    'alcohol': alcohol,
                    'exercise': exercise,
                    'stress': stress,
                    'sleep': sleep,
                    'diet': diet,
                    'family_history': family_history,
                    'work_type': work_type,
                    'bmi': bmi,
                    'cholesterol': cholesterol,
                    'blood_pressure': blood_pressure,
                    'diabetes_risk': diabetes_risk
                })
    
    with col2:
        st.subheader("🎯 Risk Assessment Benefits")
        
        benefits = [
            "🔮 Early disease detection",
            "📋 Personalized prevention plans",
            "💊 Targeted health recommendations",
            "📈 Track risk changes over time",
            "👨‍⚕️ Informed doctor discussions",
            "🎯 Focus on high-risk areas"
        ]
        
        for benefit in benefits:
            st.info(benefit)
        
        st.subheader("📚 About Risk Factors")
        
        st.markdown("""
        **Risk factors are characteristics that increase your likelihood of developing certain diseases:**
        
        🔴 **Modifiable factors:**
        - Diet and nutrition
        - Physical activity
        - Smoking and alcohol use
        - Stress management
        - Weight management
        
        🟡 **Non-modifiable factors:**
        - Age and gender
        - Family history
        - Genetic predisposition
        - Past medical history
        """)

def generate_risk_predictions(user_data, lifestyle_factors):
    """Generate health risk predictions"""
    st.subheader("🔮 Your Health Risk Assessment")
    
    # Get risk predictions from AI simulator
    risks = ai_simulator.predict_health_risks(user_data, lifestyle_factors)
    
    # Create risk visualization
    risk_data = []
    for condition, data in risks.items():
        risk_data.append({
            'Condition': condition.replace('_', ' ').title(),
            'Risk Percentage': data['risk_percentage'],
            'Risk Level': data['risk_level']
        })
    
    df_risks = pd.DataFrame(risk_data)
    
    # Risk level chart
    fig = px.bar(df_risks, x='Condition', y='Risk Percentage', 
                 color='Risk Level',
                 color_discrete_map={
                     'Low': 'green',
                     'Moderate': 'yellow', 
                     'High': 'orange',
                     'Very High': 'red'
                 },
                 title="Health Risk Assessment Results")
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed risk breakdown
    st.subheader("📋 Detailed Risk Analysis")
    
    for condition, data in risks.items():
        condition_name = condition.replace('_', ' ').title()
        risk_level = data['risk_level']
        risk_percentage = data['risk_percentage']
        
        # Color code by risk level
        colors = {'Low': 'green', 'Moderate': 'blue', 'High': 'orange', 'Very High': 'red'}
        color = colors.get(risk_level, 'gray')
        
        with st.expander(f"📊 {condition_name} - {risk_level} Risk ({risk_percentage}%)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Risk Level:** <span style='color:{color}'>{risk_level}</span>", unsafe_allow_html=True)
                st.metric("Risk Percentage", f"{risk_percentage}%")
                
                # Risk interpretation
                if risk_percentage < 25:
                    st.success("✅ Low risk - Continue healthy lifestyle")
                elif risk_percentage < 50:
                    st.info("ℹ️ Moderate risk - Consider preventive measures")
                elif risk_percentage < 75:
                    st.warning("⚠️ High risk - Consult healthcare provider")
                else:
                    st.error("🚨 Very high risk - Seek immediate medical advice")
            
            with col2:
                st.markdown("**🛡️ Prevention Tips:**")
                for tip in data['prevention_tips']:
                    st.write(f"• {tip}")
    
    # Overall recommendations
    st.subheader("💡 Overall Recommendations")
    
    # Calculate average risk
    avg_risk = sum(data['risk_percentage'] for data in risks.values()) / len(risks)
    
    if avg_risk < 30:
        st.success("🌟 **Excellent health profile!** Continue your healthy lifestyle.")
    elif avg_risk < 50:
        st.info("👍 **Good health profile** with room for improvement in some areas.")
    elif avg_risk < 70:
        st.warning("⚠️ **Moderate health risks** - consider lifestyle changes and regular check-ups.")
    else:
        st.error("🚨 **High health risks** - strongly recommend consulting healthcare professionals.")
    
    # Action plan
    st.subheader("📋 Personalized Action Plan")
    
    action_items = []
    
    for condition, data in risks.items():
        if data['risk_percentage'] > 50:  # High risk conditions
            action_items.extend(data['prevention_tips'][:2])  # Top 2 tips per condition
    
    if action_items:
        st.markdown("**🎯 Priority Actions:**")
        for i, action in enumerate(set(action_items)[:5], 1):  # Remove duplicates, max 5 actions
            st.write(f"{i}. {action}")
    
    # Save assessment
    if st.button("💾 Save Risk Assessment"):
        record_id = data_manager.add_health_record(
            st.session_state.user_id,
            notes=f"Health Risk Assessment - Average risk: {avg_risk:.1f}%"
        )
        if record_id:
            st.success("✅ Risk assessment saved to your health records")

def show_medicine_info():
    """Medicine information and interaction checker"""
    st.header("💊 Medicine Information & Interaction Checker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Medicine Search")
        
        medicine_name = st.text_input("💊 Enter medicine name:", placeholder="e.g., Paracetamol, Aspirin, Metformin")
        
        if medicine_name:
            show_medicine_details(medicine_name)
        
        st.markdown("---")
        
        st.subheader("⚠️ Drug Interaction Checker")
        
        st.info("Check for potential interactions between multiple medications")
        
        # Medicine list for interaction checking
        medicines_list = st.text_area(
            "📝 List your current medications (one per line):",
            placeholder="Paracetamol 500mg\nAspirin 100mg\nMetformin 500mg"
        )
        
        if st.button("🔍 Check Interactions") and medicines_list:
            check_drug_interactions(medicines_list)
    
    with col2:
        st.subheader("🚨 Important Reminders")
        
        reminders = [
            "👨‍⚕️ Always consult your doctor before starting new medications",
            "📖 Read medicine labels carefully",
            "⏰ Take medicines at prescribed times",
            "🚫 Never share prescription medicines",
            "📞 Call your doctor if you experience side effects",
            "💧 Store medicines in cool, dry places",
            "📅 Check expiration dates regularly"
        ]
        
        for reminder in reminders:
            st.warning(reminder)
        
        st.subheader("☎️ Emergency Contacts")
        
        st.error("🚨 Poison Control: 1066")
        st.error("🏥 Medical Emergency: 102")
        st.error("🚑 Ambulance: 108")

def show_medicine_details(medicine_name):
    """Show detailed medicine information"""
    st.subheader(f"📋 Information for: {medicine_name}")
    
    # Simulated medicine database (in real app, this would query a medicine API)
    medicine_db = {
        'paracetamol': {
            'generic_name': 'Acetaminophen',
            'brand_names': ['Tylenol', 'Panadol', 'Crocin'],
            'uses': ['Pain relief', 'Fever reduction', 'Headache treatment'],
            'dosage': 'Adults: 500-1000mg every 4-6 hours (max 4000mg/day)',
            'side_effects': ['Nausea', 'Stomach upset', 'Allergic reactions (rare)'],
            'warnings': ['Do not exceed recommended dose', 'Avoid alcohol', 'Liver damage risk with overdose'],
            'interactions': ['Warfarin', 'Alcohol', 'Other acetaminophen-containing drugs']
        },
        'aspirin': {
            'generic_name': 'Acetylsalicylic acid',
            'brand_names': ['Bayer', 'Ecosprin', 'Disprin'],
            'uses': ['Pain relief', 'Anti-inflammatory', 'Heart attack prevention', 'Stroke prevention'],
            'dosage': 'Adults: 325-650mg every 4 hours for pain; 75-100mg daily for cardiovascular protection',
            'side_effects': ['Stomach upset', 'Heartburn', 'Bleeding risk', 'Ringing in ears'],
            'warnings': ['Avoid in children under 16', 'Bleeding risk', 'Stomach ulcer risk'],
            'interactions': ['Blood thinners', 'Diabetes medications', 'Blood pressure medications']
        },
        'metformin': {
            'generic_name': 'Metformin hydrochloride',
            'brand_names': ['Glucophage', 'Glycomet', 'Obimet'],
            'uses': ['Type 2 diabetes management', 'PCOS treatment', 'Prediabetes prevention'],
            'dosage': 'Adults: Start 500mg twice daily, may increase to 2000mg daily',
            'side_effects': ['Nausea', 'Diarrhea', 'Stomach upset', 'Metallic taste'],
            'warnings': ['Kidney function monitoring required', 'Lactic acidosis risk', 'Vitamin B12 deficiency'],
            'interactions': ['Alcohol', 'Contrast dyes', 'Certain antibiotics']
        }
    }
    
    medicine_key = medicine_name.lower().strip()
    
    if medicine_key in medicine_db:
        med_info = medicine_db[medicine_key]
        
        # Display medicine information in organized tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Basic Info", "💊 Dosage", "⚠️ Side Effects", "🤝 Interactions"])
        
        with tab1:
            st.write(f"**Generic Name:** {med_info['generic_name']}")
            st.write(f"**Brand Names:** {', '.join(med_info['brand_names'])}")
            st.write("**Uses:**")
            for use in med_info['uses']:
                st.write(f"• {use}")
        
        with tab2:
            st.write("**Recommended Dosage:**")
            st.info(med_info['dosage'])
            st.warning("⚠️ Always follow your doctor's prescribed dosage")
        
        with tab3:
            st.write("**Common Side Effects:**")
            for effect in med_info['side_effects']:
                st.write(f"• {effect}")
            
            st.write("**Important Warnings:**")
            for warning in med_info['warnings']:
                st.error(f"⚠️ {warning}")
        
        with tab4:
            st.write("**Known Drug Interactions:**")
            for interaction in med_info['interactions']:
                st.write(f"• {interaction}")
            
            st.warning("⚠️ This is not a complete list. Always inform your doctor about all medications you're taking.")
    
    else:
        st.warning(f"⚠️ Medicine information for '{medicine_name}' not found in our database.")
        st.info("💡 For comprehensive medicine information, consult your pharmacist or doctor.")

def check_drug_interactions(medicines_list):
    """Check for potential drug interactions"""
    st.subheader("🔍 Drug Interaction Analysis")
    
    medicines = [med.strip() for med in medicines_list.split('\n') if med.strip()]
    
    if len(medicines) < 2:
        st.warning("⚠️ Please enter at least 2 medications to check for interactions")
        return
    
    st.info(f"Checking interactions for {len(medicines)} medications...")
    
    # Simulated interaction checker (in real app, this would use a drug interaction API)
    potential_interactions = [
        {
            'drug1': 'Aspirin',
            'drug2': 'Warfarin', 
            'severity': 'High',
            'description': 'Increased bleeding risk when taken together',
            'recommendation': 'Monitor closely for bleeding. Consider alternative pain relief.'
        },
        {
            'drug1': 'Metformin',
            'drug2': 'Alcohol',
            'severity': 'Moderate',
            'description': 'Increased risk of lactic acidosis',
            'recommendation': 'Limit alcohol consumption. Monitor for symptoms of lactic acidosis.'
        }
    ]
    
    # Display interaction results
    if potential_interactions:
        st.warning(f"⚠️ Found {len(potential_interactions)} potential interactions:")
        
        for interaction in potential_interactions:
            severity_colors = {'High': 'red', 'Moderate': 'orange', 'Low': 'yellow'}
            color = severity_colors.get(interaction['severity'], 'gray')
            
            with st.expander(f"⚠️ {interaction['drug1']} + {interaction['drug2']} - {interaction['severity']} Risk"):
                st.markdown(f"**Severity:** <span style='color:{color}'>{interaction['severity']}</span>", unsafe_allow_html=True)
                st.write(f"**Description:** {interaction['description']}")
                st.info(f"**Recommendation:** {interaction['recommendation']}")
    else:
        st.success("✅ No major interactions found between the listed medications")
    
    # General recommendations
    st.subheader("💡 General Recommendations")
    
    recommendations = [
        "👨‍⚕️ Always inform all healthcare providers about all medications you're taking",
        "📝 Keep an updated list of all medications, including over-the-counter drugs",
        "⏰ Take medications as prescribed and at the right times",
        "🚫 Don't stop medications without consulting your doctor",
        "📞 Contact your healthcare provider if you experience unusual symptoms"
    ]
    
    for rec in recommendations:
        st.info(rec)

def show_medical_translator():
    """Medical terminology translator"""
    st.header("🌐 Medical Translator")
    st.info("Translate medical terms and phrases into different languages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Term Translation")
        
        source_language = st.selectbox("From Language", ["English"], index=0)
        target_language = st.selectbox("To Language", translator.get_available_languages())
        
        # Term translation
        medical_term = st.text_input("Enter medical term:", placeholder="e.g., fever, headache, doctor")
        
        if medical_term and st.button("🔤 Translate Term"):
            translation = translator.translate_term(medical_term, target_language)
            
            col_orig, col_trans = st.columns(2)
            with col_orig:
                st.info(f"**English:** {medical_term}")
            with col_trans:
                st.success(f"**{target_language.title()}:** {translation}")
        
        st.markdown("---")
        
        # Phrase translation
        st.subheader("💬 Phrase Translation")
        
        medical_phrase = st.text_input("Enter medical phrase:", placeholder="e.g., how are you feeling, take this medicine")
        
        if medical_phrase and st.button("🔤 Translate Phrase"):
            translation = translator.translate_phrase(medical_phrase, target_language)
            
            col_orig, col_trans = st.columns(2)
            with col_orig:
                st.info(f"**English:** {medical_phrase}")
            with col_trans:
                st.success(f"**{target_language.title()}:** {translation}")
        
        # Prescription translation
        st.markdown("---")
        st.subheader("📋 Prescription Translation")
        
        prescription_text = st.text_area("Enter prescription instructions:", 
                                       placeholder="Take one tablet twice daily after meals")
        
        if prescription_text and st.button("🔤 Translate Prescription"):
            translation = translator.translate_prescription(prescription_text, target_language)
            st.success(f"**Translation:** {translation}")
    
    with col2:
        st.subheader("🚨 Emergency Phrases")
        
        if target_language != "English":
            emergency_phrases = translator.get_emergency_phrases(target_language)
            
            st.warning("Important emergency phrases:")
            for phrase in emergency_phrases:
                st.write(phrase)
        else:
            st.info("Select a target language to see emergency phrases")
        
        st.markdown("---")
        
        st.subheader("📚 Common Medical Terms")
        
        common_terms = [
            "doctor", "hospital", "medicine", "patient", "nurse", "pharmacy",
            "fever", "headache", "cough", "pain", "nausea", "dizziness",
            "heart", "chest", "stomach", "head", "emergency", "urgent"
        ]
        
        st.info("Click on any term to translate:")
        
        # Create a grid of clickable terms
        cols = st.columns(3)
        for i, term in enumerate(common_terms):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(term, key=f"term_{term}"):
                    if target_language != "English":
                        translation = translator.translate_term(term, target_language)
                        st.success(f"{term} → {translation}")

def show_health_insights():
    """Personalized health insights and recommendations"""
    st.header("📈 Personalized Health Insights")
    
    user_data = st.session_state.user_data
    user_id = st.session_state.user_id
    
    # Get user's health records
    health_records = data_manager.get_user_health_records(user_id)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Health Trends Analysis")
        
        if not health_records.empty and len(health_records) > 1:
            # Create health trends visualization
            fig = go.Figure()
            
            if 'heart_rate' in health_records.columns and health_records['heart_rate'].notna().any():
                fig.add_trace(go.Scatter(
                    x=health_records['date'],
                    y=health_records['heart_rate'],
                    mode='lines+markers',
                    name='Heart Rate (BPM)',
                    line=dict(color='red')
                ))
            
            if 'weight' in health_records.columns and health_records['weight'].notna().any():
                fig.add_trace(go.Scatter(
                    x=health_records['date'],
                    y=health_records['weight'],
                    mode='lines+markers',
                    name='Weight (kg)',
                    yaxis='y2',
                    line=dict(color='blue')
                ))
            
            fig.update_layout(
                title="Health Metrics Trends",
                xaxis_title="Date",
                yaxis_title="Heart Rate (BPM)",
                yaxis2=dict(
                    title="Weight (kg)",
                    overlaying='y',
                    side='right'
                ),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Health insights based on trends
            st.subheader("🔍 Trend Analysis")
            
            # Analyze heart rate trend
            if health_records['heart_rate'].notna().sum() > 1:
                recent_hr = health_records['heart_rate'].dropna().tail(3).mean()
                older_hr = health_records['heart_rate'].dropna().head(3).mean()
                
                if recent_hr > older_hr + 5:
                    st.warning(f"📈 Your heart rate has increased recently (avg: {recent_hr:.1f} vs {older_hr:.1f})")
                elif recent_hr < older_hr - 5:
                    st.success(f"📉 Your heart rate has improved recently (avg: {recent_hr:.1f} vs {older_hr:.1f})")
                else:
                    st.info(f"➡️ Your heart rate is stable (avg: {recent_hr:.1f})")
            
            # Analyze weight trend
            if health_records['weight'].notna().sum() > 1:
                recent_weight = health_records['weight'].dropna().tail(3).mean()
                older_weight = health_records['weight'].dropna().head(3).mean()
                
                weight_change = recent_weight - older_weight
                
                if weight_change > 2:
                    st.warning(f"📈 Weight increase detected: +{weight_change:.1f} kg")
                elif weight_change < -2:
                    st.info(f"📉 Weight decrease detected: {weight_change:.1f} kg")
                else:
                    st.success(f"➡️ Weight is stable: {weight_change:+.1f} kg")
        
        else:
            st.info("📝 Not enough health data for trend analysis. Start tracking your health metrics!")
        
        st.markdown("---")
        
        # AI-powered recommendations
        st.subheader("🤖 AI-Powered Recommendations")
        
        recommendations = ai_simulator.get_health_recommendations(user_data)
        
        for i, rec in enumerate(recommendations, 1):
            st.success(f"{i}. {rec}")
        
        # Weekly health report
        st.subheader("📅 Weekly Health Summary")
        
        # Calculate weekly stats (simulated)
        weekly_stats = {
            "Health Records": len(health_records) if not health_records.empty else 0,
            "AI Consultations": 3,  # Simulated
            "Symptom Checks": 1,   # Simulated
            "Risk Assessments": 1  # Simulated
        }
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("📋 Records", weekly_stats["Health Records"])
        
        with col_stat2:
            st.metric("🤖 AI Consults", weekly_stats["AI Consultations"])
        
        with col_stat3:
            st.metric("🔍 Symptom Checks", weekly_stats["Symptom Checks"])
        
        with col_stat4:
            st.metric("📊 Risk Checks", weekly_stats["Risk Assessments"])
    
    with col2:
        st.subheader("🎯 Health Goals")
        
        # Health goal setting
        with st.form("health_goals"):
            st.write("Set your health goals:")
            
            weight_goal = st.number_input("🎯 Target Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
            exercise_goal = st.selectbox("🏃‍♂️ Exercise Goal", ["Daily walk", "3x/week gym", "Daily yoga", "Weekend sports"])
            diet_goal = st.selectbox("🥗 Diet Goal", ["Reduce sugar", "More vegetables", "Smaller portions", "Balanced meals"])
            sleep_goal = st.selectbox("😴 Sleep Goal", ["7-8 hours", "Earlier bedtime", "Better quality", "Regular schedule"])
            
            submit_goals = st.form_submit_button("🎯 Set Goals")
            
            if submit_goals:
                st.success("✅ Health goals set! Track your progress daily.")
        
        st.markdown("---")
        
        st.subheader("💡 Daily Health Tips")
        
        daily_tips = [
            "💧 Drink a glass of water first thing in the morning",
            "🚶‍♂️ Take a 10-minute walk after meals",
            "🥗 Include one extra serving of vegetables today",
            "😴 Set a consistent bedtime routine",
            "🧘‍♀️ Practice 5 minutes of deep breathing",
            "📱 Take breaks from screens every hour",
            "👥 Connect with a friend or family member"
        ]
        
        import random
        today_tip = random.choice(daily_tips)
        st.info(f"**Today's Tip:** {today_tip}")
        
        st.subheader("🏆 Health Achievements")
        
        achievements = [
            "🥇 Completed first health assessment",
            "📊 7 days of health tracking",
            "🤖 Used AI health assistant 5 times",
            "💪 Set health goals"
        ]
        
        for achievement in achievements:
            st.success(achievement)

if __name__ == "__main__":
    main()
