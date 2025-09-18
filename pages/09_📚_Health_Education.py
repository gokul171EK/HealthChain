import streamlit as st
from utils.styling import add_app_styling
from utils.gemini_client import get_gemini_response

# --- Mock DataManager for standalone page functionality ---
class DataManager:
    def add_health_record(self, user_id, notes):
        print(f"Adding record for {user_id}: {notes}")
        return True

data_manager = DataManager()
# -----------------------------------------------------------

def show_health_articles():
    """Display health articles and educational content."""
    st.header("📖 Health Articles & Resources")
    st.info("Browse our library of articles written by medical experts to learn more about various health topics.")

    # Article categories with mock content
    article_categories = {
        "Heart Health": [
            {"title": "10 Simple Ways to Improve Heart Health", "author": "Dr. Sarah Johnson", "summary": "Learn evidence-based strategies to keep your heart healthy and reduce cardiovascular disease risk."},
            {"title": "Understanding Cholesterol", "author": "Dr. Michael Chen", "summary": "A guide to understanding good vs. bad cholesterol and how to manage your levels through diet and exercise."}
        ],
        "Nutrition & Diet": [
            {"title": "The Beginner's Guide to a Balanced Diet", "author": "Nutritionist Lisa Wong", "summary": "Learn the fundamentals of macronutrients, micronutrients, and how to build a healthy eating plan that works for you."},
            {"title": "Debunking Common Nutrition Myths", "author": "Dr. Emily Davis", "summary": "Separating fact from fiction on popular diet trends and food choices."}
        ]
    }

    for category, articles in article_categories.items():
        st.subheader(category)
        for article in articles:
            with st.expander(f"**{article['title']}** - By {article['author']}"):
                st.write(article['summary'])
                if st.button("Read Full Article", key=f"read_{article['title']}"):
                    st.success("The full article would be displayed here.")
        st.markdown("---")


def show_video_library():
    """Display educational health videos."""
    st.header("🎥 Video Library")
    st.info("Watch short, informative videos from healthcare professionals on a variety of health topics.")

    video_content = {
        "Exercise & Fitness": [
            {"title": "5-Minute Morning Stretch Routine", "creator": "FitLife Physio", "duration": "5:32"},
            {"title": "Introduction to Strength Training", "creator": "Dr. Alex Carter", "duration": "8:15"}
        ],
        "Mental Wellness": [
            {"title": "Guided Meditation for Stress Relief", "creator": "Mindful Moments", "duration": "10:00"},
            {"title": "Understanding Anxiety", "creator": "Dr. Priya Sharma", "duration": "7:45"}
        ]
    }

    for category, videos in video_content.items():
        st.subheader(category)
        col1, col2 = st.columns(2)
        for i, video in enumerate(videos):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                with st.container(border=True):
                    st.markdown(f"**{video['title']}**")
                    st.caption(f"By {video['creator']} | Duration: {video['duration']}")
                    if st.button("▶️ Watch Video", key=f"watch_{video['title']}", use_container_width=True):
                        st.success(f"Playing '{video['title']}'...")


def show_health_qa():
    """Health Q&A section powered by Gemini AI"""
    st.header("❓ Ask Our AI Health Expert")
    
    st.info("💡 Have a health question? Get clear, informative answers from our AI assistant. This tool is for educational purposes and is not a substitute for professional medical advice.")

    # Use session state to store conversation history
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []

    # Display previous questions and answers
    for q, a in st.session_state.qa_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**AI Expert:** {a}")
        st.markdown("---")

    # User input
    user_question = st.text_area("Enter your health question here:", key="health_question", height=100)

    if st.button("Get Answer", use_container_width=True):
        if user_question:
            with st.spinner("Our AI is thinking..."):
                system_prompt = "You are a helpful and knowledgeable AI health expert. Your goal is to provide clear, safe, and easy-to-understand answers to general health questions. You must always include the disclaimer that you are not a medical professional and the user should consult a doctor for medical advice. Do not provide diagnoses or prescribe treatments."
                full_prompt = f"{system_prompt}\n\nUser's question: {user_question}"
                ai_answer = get_gemini_response(full_prompt)
                st.session_state.qa_history.append((user_question, ai_answer))
                st.rerun()
        else:
            st.warning("Please enter a question.")


def show_health_assessments():
    """Interactive health risk assessments."""
    st.header("📊 Health Risk Assessments")
    st.info("Answer a few simple questions to understand your risk for common health conditions. This is not a diagnosis.")

    with st.form("diabetes_risk_assessment"):
        st.subheader("Type 2 Diabetes Risk Test")
        age = st.selectbox("1. What is your age group?", ["Under 40", "40-49", "50-59", "60+"])
        activity = st.radio("2. What is your daily activity level?", ["Active", "Moderately Active", "Not very active"], horizontal=True)
        family_history = st.checkbox("3. Do you have a family history of diabetes (parent or sibling)?")
        
        if st.form_submit_button("Calculate Diabetes Risk", use_container_width=True):
            score = 0
            if age in ["50-59", "60+"]: score += 2
            if activity == "Not very active": score += 1
            if family_history: score += 1
            
            if score >= 3:
                st.warning("⚠️ **Moderate to High Risk**: Your answers indicate some risk factors for type 2 diabetes. Consider discussing this with your doctor.")
            else:
                st.success("✅ **Low Risk**: Your answers indicate a lower risk, but it's always good to maintain a healthy lifestyle.")


def show_health_courses():
    """Display available health education courses."""
    st.header("🎓 Health Education Courses")
    st.info("Enroll in our guided courses to take a deeper dive into important health topics.")

    courses = [
        {"title": "Heart Health 101", "instructor": "Dr. Sarah Johnson", "duration": "4 Weeks", "level": "Beginner"},
        {"title": "Nutrition for a Healthy Life", "instructor": "Lisa Wong, RD", "duration": "6 Weeks", "level": "Beginner"},
        {"title": "Mindfulness and Stress Reduction", "instructor": "Dr. Emily Davis", "duration": "3 Weeks", "level": "All Levels"}
    ]
    
    for course in courses:
        with st.container(border=True):
            st.markdown(f"**{course['title']}**")
            st.caption(f"Instructor: {course['instructor']} | Duration: {course['duration']} | Level: {course['level']}")
            if st.button("Enroll Now", key=f"enroll_{course['title']}", use_container_width=True):
                st.success(f"You have been enrolled in '{course['title']}'!")


def main():
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    add_app_styling(theme=st.session_state.theme)

    st.title("📚 Health Education Center")
    st.markdown("### Learn About Health, Wellness, and Disease Prevention")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Health Articles", 
        "🎥 Video Library", 
        "❓ Health Q&A (AI)", 
        "📊 Health Assessments", 
        "🎓 Courses"
    ])
    
    with tab1:
        show_health_articles()
    with tab2:
        show_video_library()
    with tab3:
        show_health_qa()
    with tab4:
        show_health_assessments()
    with tab5:
        show_health_courses()

if __name__ == "__main__":
    main()

