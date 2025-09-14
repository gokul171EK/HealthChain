import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

st.set_page_config(
    page_title="Health Education - HEALTHTECH",
    page_icon="📚",
    layout="wide"
)

def main():
    add_app_styling()
    st.title("📚 Health Education Center")
    st.markdown("### Learn About Health, Wellness, and Disease Prevention")
    
    # Tabs for different educational content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Health Articles", 
        "🎥 Video Library", 
        "❓ Health Q&A", 
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

def show_health_articles():
    """Display health articles and educational content"""
    st.header("📖 Health Articles & Resources")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search and filter
        st.subheader("🔍 Find Health Information")
        
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            search_query = st.text_input("🔍 Search articles", placeholder="Enter topic, condition, or keyword")
        
        with col_search2:
            category_filter = st.selectbox("📂 Category", [
                "All Categories", "Heart Health", "Diabetes", "Mental Health", "Nutrition", 
                "Exercise & Fitness", "Women's Health", "Men's Health", "Child Health", 
                "Senior Health", "Preventive Care", "Chronic Diseases"
            ])
        
        # Featured articles
        st.subheader("⭐ Featured Articles")
        
        featured_articles = [
            {
                "title": "10 Simple Ways to Improve Heart Health",
                "category": "Heart Health",
                "author": "Dr. Sarah Johnson",
                "date": "2024-08-20",
                "read_time": "5 min read",
                "summary": "Learn evidence-based strategies to keep your heart healthy and reduce cardiovascular disease risk.",
                "difficulty": "Beginner",
                "tags": ["heart", "prevention", "lifestyle"]
            },
            {
                "title": "Understanding Diabetes: Types, Symptoms, and Management",
                "category": "Diabetes",
                "author": "Dr. Michael Chen",
                "date": "2024-08-18",
                "read_time": "8 min read",
                "summary": "Comprehensive guide to diabetes types, early warning signs, and effective management strategies.",
                "difficulty": "Intermediate",
                "tags": ["diabetes", "blood sugar", "management"]
            },
            {
                "title": "Mental Health First Aid: Supporting Yourself and Others",
                "category": "Mental Health",
                "author": "Dr. Emily Davis",
                "date": "2024-08-15",
                "read_time": "6 min read",
                "summary": "Essential skills for recognizing mental health issues and providing appropriate support.",
                "difficulty": "Beginner",
                "tags": ["mental health", "support", "wellness"]
            }
        ]
        
        for article in featured_articles:
            if category_filter == "All Categories" or article["category"] == category_filter:
                if not search_query or search_query.lower() in article["title"].lower() or search_query.lower() in article["summary"].lower():
                    show_article_card(article, featured=True)
        
        st.markdown("---")
        
        # All articles by category
        st.subheader("📚 Health Articles by Category")
        
        # Health categories with articles
        health_categories = {
            "Heart Health": [
                {
                    "title": "High Blood Pressure: Silent Killer Prevention",
                    "author": "Dr. Rajesh Kumar",
                    "date": "2024-08-12",
                    "read_time": "4 min read",
                    "summary": "Learn how to prevent and manage high blood pressure effectively.",
                    "difficulty": "Beginner"
                },
                {
                    "title": "Cholesterol Management: Diet and Lifestyle Tips",
                    "author": "Dr. Priya Sharma",
                    "date": "2024-08-10",
                    "read_time": "6 min read",
                    "summary": "Natural ways to manage cholesterol levels through diet and exercise.",
                    "difficulty": "Intermediate"
                }
            ],
            "Diabetes": [
                {
                    "title": "Pre-diabetes: Early Warning Signs and Prevention",
                    "author": "Dr. Sarah Johnson",
                    "date": "2024-08-08",
                    "read_time": "5 min read",
                    "summary": "Recognize pre-diabetes symptoms and take preventive action.",
                    "difficulty": "Beginner"
                },
                {
                    "title": "Diabetes-Friendly Meal Planning Guide",
                    "author": "Nutritionist Lisa Wong",
                    "date": "2024-08-05",
                    "read_time": "7 min read",
                    "summary": "Create balanced meals that help manage blood sugar levels.",
                    "difficulty": "Intermediate"
                }
            ],
            "Mental Health": [
                {
                    "title": "Stress Management Techniques for Daily Life",
                    "author": "Dr. Emily Davis",
                    "date": "2024-08-03",
                    "read_time": "5 min read",
                    "summary": "Practical strategies to manage stress and improve mental well-being.",
                    "difficulty": "Beginner"
                },
                {
                    "title": "Understanding Anxiety: Symptoms and Coping Strategies",
                    "author": "Dr. Michael Chen",
                    "date": "2024-08-01",
                    "read_time": "8 min read",
                    "summary": "Comprehensive guide to recognizing and managing anxiety disorders.",
                    "difficulty": "Intermediate"
                }
            ],
            "Nutrition": [
                {
                    "title": "Balanced Diet Basics: Building Healthy Eating Habits",
                    "author": "Nutritionist Arun Patel",
                    "date": "2024-07-30",
                    "read_time": "6 min read",
                    "summary": "Foundation principles of healthy eating for optimal health.",
                    "difficulty": "Beginner"
                },
                {
                    "title": "Superfoods: Myth vs Reality",
                    "author": "Dr. Sarah Johnson",
                    "date": "2024-07-28",
                    "read_time": "4 min read",
                    "summary": "Separating fact from fiction about superfoods and their benefits.",
                    "difficulty": "Intermediate"
                }
            ]
        }
        
        # Display articles by category
        for category, articles in health_categories.items():
            if category_filter == "All Categories" or category_filter == category:
                with st.expander(f"📂 {category} ({len(articles)} articles)"):
                    for article in articles:
                        if not search_query or search_query.lower() in article["title"].lower():
                            show_article_card(article)
    
    with col2:
        st.subheader("🎯 Quick Health Tips")
        
        daily_tips = [
            "💧 Drink 8 glasses of water daily",
            "🚶‍♂️ Take 10,000 steps every day",
            "😴 Get 7-9 hours of quality sleep",
            "🥗 Eat 5 servings of fruits & vegetables",
            "🧘‍♀️ Practice 10 minutes of meditation",
            "🚭 Avoid smoking and excessive alcohol",
            "👥 Stay socially connected",
            "📱 Limit screen time before bed"
        ]
        
        for tip in daily_tips:
            st.info(tip)
        
        st.subheader("📊 Popular Topics")
        
        popular_topics = [
            "Weight Management",
            "High Blood Pressure", 
            "Diabetes Prevention",
            "Heart Disease",
            "Mental Health",
            "Healthy Aging",
            "Exercise Benefits",
            "Stress Management"
        ]
        
        for topic in popular_topics:
            if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                st.info(f"Showing articles about {topic}")
        
        st.subheader("📅 Recent Updates")
        
        recent_updates = [
            "New diabetes management guidelines",
            "Updated heart health recommendations",
            "Mental health awareness week content",
            "Nutrition facts database updated"
        ]
        
        for update in recent_updates:
            st.success(f"✅ {update}")

def show_article_card(article, featured=False):
    """Display individual article card"""
    with st.container():
        if featured:
            st.markdown("### ⭐ " + article["title"])
        else:
            st.markdown("### 📄 " + article["title"])
        
        col_article1, col_article2, col_article3 = st.columns([2, 1, 1])
        
        with col_article1:
            st.write(article["summary"])
            
            if "tags" in article:
                tags_html = " ".join([f"<span style='background-color:#e1f5fe; padding:2px 6px; border-radius:10px; font-size:12px;'>{tag}</span>" for tag in article["tags"]])
                st.markdown(tags_html, unsafe_allow_html=True)
        
        with col_article2:
            st.write(f"**Author:** {article['author']}")
            st.write(f"**Date:** {article['date']}")
            st.write(f"**Read Time:** {article['read_time']}")
            
            difficulty_colors = {"Beginner": "green", "Intermediate": "orange", "Advanced": "red"}
            difficulty_color = difficulty_colors.get(article['difficulty'], 'blue')
            st.markdown(f"**Level:** <span style='color:{difficulty_color}'>{article['difficulty']}</span>", 
                       unsafe_allow_html=True)
        
        with col_article3:
            if st.button("📖 Read Article", key=f"read_{article['title']}", use_container_width=True):
                show_full_article(article)
            
            if st.button("🔖 Bookmark", key=f"bookmark_{article['title']}", use_container_width=True):
                st.success("Article bookmarked!")
            
            if st.button("📤 Share", key=f"share_{article['title']}", use_container_width=True):
                st.success("Article shared!")
        
        st.markdown("---")

def show_full_article(article):
    """Display full article content"""
    st.subheader(f"📖 {article['title']}")
    
    # Article metadata
    col_meta1, col_meta2, col_meta3 = st.columns(3)
    
    with col_meta1:
        st.write(f"**👨‍⚕️ Author:** {article['author']}")
    
    with col_meta2:
        st.write(f"**📅 Published:** {article['date']}")
    
    with col_meta3:
        st.write(f"**⏱️ Read Time:** {article['read_time']}")
    
    st.markdown("---")
    
    # Sample article content (in real app, this would come from database)
    article_content = """
    ## Introduction
    
    Heart health is one of the most important aspects of overall wellness. Cardiovascular disease remains the leading cause of death globally, but the good news is that many heart conditions are preventable through simple lifestyle changes.
    
    ## 10 Ways to Improve Heart Health
    
    ### 1. **Regular Physical Activity**
    Aim for at least 150 minutes of moderate-intensity exercise per week. This can include:
    - Brisk walking
    - Swimming
    - Cycling
    - Dancing
    
    ### 2. **Eat a Heart-Healthy Diet**
    Focus on:
    - Fruits and vegetables
    - Whole grains
    - Lean proteins
    - Healthy fats (olive oil, nuts, avocados)
    
    ### 3. **Maintain a Healthy Weight**
    - Calculate your BMI
    - Set realistic weight goals
    - Track your progress
    
    ### 4. **Don't Smoke**
    - Smoking damages blood vessels
    - Increases risk of heart disease
    - Seek help to quit if needed
    
    ### 5. **Limit Alcohol**
    - Moderate consumption: 1 drink/day for women, 2 for men
    - Excessive alcohol can damage the heart
    
    ### 6. **Manage Stress**
    - Practice relaxation techniques
    - Exercise regularly
    - Get adequate sleep
    - Consider meditation or yoga
    
    ### 7. **Get Regular Check-ups**
    - Monitor blood pressure
    - Check cholesterol levels
    - Screen for diabetes
    - Discuss family history with your doctor
    
    ### 8. **Get Quality Sleep**
    - Aim for 7-9 hours per night
    - Maintain consistent sleep schedule
    - Create a relaxing bedtime routine
    
    ### 9. **Stay Hydrated**
    - Drink plenty of water
    - Limit sugary drinks
    - Monitor fluid intake if you have heart conditions
    
    ### 10. **Take Medications as Prescribed**
    - Follow doctor's instructions
    - Don't skip doses
    - Discuss side effects with healthcare provider
    
    ## Conclusion
    
    Improving heart health doesn't require drastic changes. Small, consistent steps can make a significant difference in your cardiovascular wellness. Start with one or two changes and gradually incorporate more healthy habits into your routine.
    
    Remember to consult with your healthcare provider before making significant changes to your diet or exercise routine, especially if you have existing health conditions.
    """
    
    st.markdown(article_content)
    
    # Article actions
    st.markdown("---")
    
    col_action1, col_action2, col_action3, col_action4 = st.columns(4)
    
    with col_action1:
        if st.button("👍 Helpful"):
            st.success("Thank you for your feedback!")
    
    with col_action2:
        if st.button("🔖 Save"):
            st.success("Article saved to your library!")
    
    with col_action3:
        if st.button("📧 Email"):
            st.success("Article emailed!")
    
    with col_action4:
        if st.button("🖨️ Print"):
            st.success("Article ready to print!")

def show_video_library():
    """Video educational content"""
    st.header("🎥 Health Education Videos")
    
    # Video categories and content
    video_categories = {
        "Exercise & Fitness": [
            {
                "title": "10-Minute Morning Workout for Beginners",
                "duration": "10:25",
                "instructor": "Fitness Coach Sarah",
                "description": "Simple exercises to start your day with energy",
                "difficulty": "Beginner",
                "views": "2.3K"
            },
            {
                "title": "Yoga for Heart Health",
                "duration": "15:40",
                "instructor": "Yoga Instructor Maya",
                "description": "Gentle yoga poses to improve cardiovascular health",
                "difficulty": "Beginner",
                "views": "1.8K"
            },
            {
                "title": "Strength Training for Seniors",
                "duration": "20:15",
                "instructor": "PT John Wilson",
                "description": "Safe and effective strength exercises for older adults",
                "difficulty": "Intermediate",
                "views": "965"
            }
        ],
        "Nutrition & Diet": [
            {
                "title": "Healthy Meal Prep for Busy People",
                "duration": "12:30",
                "instructor": "Nutritionist Lisa Chen",
                "description": "Quick and nutritious meal preparation tips",
                "difficulty": "Beginner",
                "views": "3.1K"
            },
            {
                "title": "Understanding Food Labels",
                "duration": "8:45",
                "instructor": "Dr. Michael Roberts",
                "description": "How to read and understand nutrition labels",
                "difficulty": "Beginner",
                "views": "1.5K"
            },
            {
                "title": "Diabetes-Friendly Cooking",
                "duration": "18:20",
                "instructor": "Chef Maria Rodriguez",
                "description": "Delicious recipes for diabetic meal planning",
                "difficulty": "Intermediate",
                "views": "2.7K"
            }
        ],
        "Mental Health": [
            {
                "title": "5-Minute Breathing Exercise for Anxiety",
                "duration": "5:30",
                "instructor": "Dr. Emily Davis",
                "description": "Quick relaxation technique for managing anxiety",
                "difficulty": "Beginner",
                "views": "4.2K"
            },
            {
                "title": "Sleep Hygiene: Better Sleep Tonight",
                "duration": "11:15",
                "instructor": "Sleep Specialist Dr. Kim",
                "description": "Evidence-based tips for improving sleep quality",
                "difficulty": "Beginner",
                "views": "2.9K"
            },
            {
                "title": "Mindfulness Meditation for Beginners",
                "duration": "14:50",
                "instructor": "Meditation Teacher Alex",
                "description": "Introduction to mindfulness practice",
                "difficulty": "Beginner",
                "views": "3.5K"
            }
        ],
        "Chronic Disease Management": [
            {
                "title": "Living Well with Diabetes",
                "duration": "16:45",
                "instructor": "Dr. Sarah Johnson",
                "description": "Comprehensive guide to diabetes management",
                "difficulty": "Intermediate",
                "views": "1.9K"
            },
            {
                "title": "Heart Disease Prevention",
                "duration": "13:20",
                "instructor": "Cardiologist Dr. Patel",
                "description": "Evidence-based prevention strategies",
                "difficulty": "Intermediate",
                "views": "2.1K"
            }
        ]
    }
    
    # Video filter and search
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        video_search = st.text_input("🔍 Search videos", placeholder="Enter topic or keyword")
    
    with col_filter2:
        video_category = st.selectbox("📂 Category", ["All Categories"] + list(video_categories.keys()))
    
    # Display videos
    for category, videos in video_categories.items():
        if video_category == "All Categories" or video_category == category:
            st.subheader(f"🎬 {category}")
            
            for video in videos:
                if not video_search or video_search.lower() in video["title"].lower() or video_search.lower() in video["description"].lower():
                    show_video_card(video)

def show_video_card(video):
    """Display video card"""
    with st.container():
        col_video1, col_video2, col_video3 = st.columns([2, 2, 1])
        
        with col_video1:
            st.markdown(f"### 🎥 {video['title']}")
            st.write(video['description'])
            
            difficulty_color = "green" if video['difficulty'] == "Beginner" else "orange"
            st.markdown(f"**Level:** <span style='color:{difficulty_color}'>{video['difficulty']}</span>", 
                       unsafe_allow_html=True)
        
        with col_video2:
            st.write(f"**👨‍🏫 Instructor:** {video['instructor']}")
            st.write(f"**⏱️ Duration:** {video['duration']}")
            st.write(f"**👁️ Views:** {video['views']}")
        
        with col_video3:
            if st.button("▶️ Watch", key=f"watch_{video['title']}", use_container_width=True):
                st.success("Video player would open here")
            
            if st.button("📚 Add to Playlist", key=f"playlist_{video['title']}", use_container_width=True):
                st.success("Added to playlist!")
        
        st.markdown("---")

def show_health_qa():
    """Health Q&A section"""
    st.header("❓ Health Questions & Answers")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("❓ Ask a Health Question")
        
        with st.form("ask_question_form"):
            question_category = st.selectbox("📂 Category", [
                "General Health", "Heart Health", "Diabetes", "Mental Health", 
                "Nutrition", "Exercise", "Women's Health", "Men's Health", "Other"
            ])
            
            question_title = st.text_input("📝 Question Title")
            question_details = st.text_area("❓ Your Question", 
                                           placeholder="Please provide details about your health question...")
            
            if 'user_id' in st.session_state and st.session_state.user_id:
                user_name = st.session_state.user_data['name']
                ask_anonymously = st.checkbox("🤐 Ask anonymously")
            else:
                user_name = st.text_input("👤 Your Name")
                ask_anonymously = False
            
            if st.form_submit_button("❓ Ask Question", use_container_width=True):
                if question_title and question_details:
                    st.success("✅ Your question has been submitted!")
                    st.info("Our medical experts will review and answer your question within 24-48 hours.")
                    
                    # Save question (in real app)
                    if 'user_id' in st.session_state and st.session_state.user_id:
                        question_log = f"Health Q&A Question: {question_title} - Category: {question_category}. Details: {question_details}"
                        data_manager.add_health_record(
                            st.session_state.user_id,
                            notes=question_log
                        )
                else:
                    st.error("❌ Please fill in all fields")
        
        st.markdown("---")
        
        # Recent Q&A
        st.subheader("💬 Recent Questions & Answers")
        
        qa_items = [
            {
                "question": "What are the early signs of diabetes?",
                "category": "Diabetes",
                "author": "Anonymous",
                "date": "2024-08-20",
                "answer": "Early signs include increased thirst, frequent urination, fatigue, and blurred vision. If you experience these symptoms, consult a healthcare provider for proper testing.",
                "answered_by": "Dr. Sarah Johnson",
                "helpful_votes": 15
            },
            {
                "question": "How much exercise is recommended for heart health?",
                "category": "Heart Health",
                "author": "Rajesh K.",
                "date": "2024-08-18",
                "answer": "The American Heart Association recommends at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous activity per week, plus muscle-strengthening activities at least 2 days per week.",
                "answered_by": "Dr. Michael Chen",
                "helpful_votes": 12
            },
            {
                "question": "What foods help reduce stress naturally?",
                "category": "Mental Health",
                "author": "Priya S.",
                "date": "2024-08-15",
                "answer": "Foods rich in omega-3 fatty acids (fish, walnuts), complex carbohydrates (oats, quinoa), and antioxidants (berries, dark chocolate) can help manage stress levels. Also, limit caffeine and alcohol.",
                "answered_by": "Nutritionist Lisa Wong",
                "helpful_votes": 9
            }
        ]
        
        for qa in qa_items:
            with st.expander(f"❓ {qa['question']}", expanded=False):
                col_qa1, col_qa2 = st.columns([3, 1])
                
                with col_qa1:
                    st.write(f"**Category:** {qa['category']}")
                    st.write(f"**Asked by:** {qa['author']} on {qa['date']}")
                    
                    st.markdown("**Answer:**")
                    st.write(qa['answer'])
                    st.write(f"*- Answered by {qa['answered_by']}*")
                
                with col_qa2:
                    st.metric("👍 Helpful", qa['helpful_votes'])
                    
                    if st.button("👍 Helpful", key=f"helpful_{qa['question']}", use_container_width=True):
                        st.success("Thank you for your feedback!")
                    
                    if st.button("📤 Share", key=f"share_qa_{qa['question']}", use_container_width=True):
                        st.success("Q&A shared!")
    
    with col2:
        st.subheader("💡 Health Tips")
        
        health_tips = [
            "🥤 Drink water before feeling thirsty",
            "🍎 Eat colorful fruits and vegetables",
            "😴 Maintain a regular sleep schedule",
            "🧘‍♀️ Practice stress management daily",
            "🚶‍♂️ Take regular movement breaks",
            "📱 Limit screen time before bed",
            "🤝 Stay socially connected",
            "📖 Read health information from reliable sources"
        ]
        
        for tip in health_tips:
            st.info(tip)
        
        st.subheader("🏥 Expert Panel")
        
        experts = [
            "Dr. Sarah Johnson - Cardiology",
            "Dr. Michael Chen - Endocrinology", 
            "Dr. Emily Davis - Psychology",
            "Dr. Rajesh Kumar - Internal Medicine",
            "Lisa Wong - Clinical Nutrition"
        ]
        
        for expert in experts:
            st.success(f"✅ {expert}")
        
        st.subheader("📋 Popular Topics")
        
        popular_qa_topics = [
            "Blood pressure management",
            "Weight loss strategies",
            "Diabetes prevention",
            "Heart healthy foods",
            "Stress management",
            "Exercise for beginners"
        ]
        
        for topic in popular_qa_topics:
            if st.button(topic, key=f"qa_topic_{topic}", use_container_width=True):
                st.info(f"Showing Q&A about {topic}")

def show_health_assessments():
    """Health assessment tools"""
    st.header("📊 Health Assessment Tools")
    
    st.info("💡 These assessments are for educational purposes only and do not replace professional medical advice.")
    
    # Assessment categories
    assessment_categories = {
        "🫀 Heart Health": [
            {
                "name": "Heart Disease Risk Assessment",
                "description": "Evaluate your risk factors for heart disease",
                "duration": "5-10 minutes",
                "questions": 15
            },
            {
                "name": "Blood Pressure Risk Calculator",
                "description": "Assess your risk for developing high blood pressure",
                "duration": "3-5 minutes",
                "questions": 10
            }
        ],
        "🍯 Diabetes": [
            {
                "name": "Diabetes Risk Test",
                "description": "Determine your risk for developing type 2 diabetes",
                "duration": "3-5 minutes",
                "questions": 8
            },
            {
                "name": "Pre-diabetes Screening",
                "description": "Check if you might have pre-diabetes",
                "duration": "5-7 minutes",
                "questions": 12
            }
        ],
        "🧠 Mental Health": [
            {
                "name": "Stress Level Assessment",
                "description": "Evaluate your current stress levels and coping mechanisms",
                "duration": "7-10 minutes",
                "questions": 20
            },
            {
                "name": "Depression Screening (PHQ-9)",
                "description": "Self-assessment for depression symptoms",
                "duration": "5-7 minutes",
                "questions": 9
            }
        ],
        "⚖️ General Health": [
            {
                "name": "Overall Health Risk Assessment",
                "description": "Comprehensive evaluation of your health risks",
                "duration": "10-15 minutes",
                "questions": 25
            },
            {
                "name": "Lifestyle Health Score",
                "description": "Rate your lifestyle factors affecting health",
                "duration": "5-8 minutes",
                "questions": 15
            }
        ]
    }
    
    # Display assessment categories
    for category, assessments in assessment_categories.items():
        st.subheader(category)
        
        for assessment in assessments:
            with st.container():
                col_assess1, col_assess2, col_assess3 = st.columns([2, 1, 1])
                
                with col_assess1:
                    st.markdown(f"### 📋 {assessment['name']}")
                    st.write(assessment['description'])
                
                with col_assess2:
                    st.write(f"**⏱️ Duration:** {assessment['duration']}")
                    st.write(f"**❓ Questions:** {assessment['questions']}")
                
                with col_assess3:
                    if st.button("📊 Start Assessment", key=f"start_{assessment['name']}", use_container_width=True):
                        run_health_assessment(assessment)
                
                st.markdown("---")
    
    # Assessment history
    if 'user_id' in st.session_state and st.session_state.user_id:
        st.subheader("📈 Your Assessment History")
        
        # Mock assessment history
        assessment_history = [
            {"name": "Heart Disease Risk Assessment", "date": "2024-08-15", "score": "Low Risk", "result": "Continue healthy lifestyle"},
            {"name": "Stress Level Assessment", "date": "2024-08-10", "score": "Moderate", "result": "Consider stress management techniques"},
            {"name": "Diabetes Risk Test", "date": "2024-08-05", "score": "Low Risk", "result": "Maintain current diet and exercise"}
        ]
        
        for history in assessment_history:
            col_hist1, col_hist2, col_hist3 = st.columns([2, 1, 1])
            
            with col_hist1:
                st.write(f"**{history['name']}**")
                st.write(f"Date: {history['date']}")
            
            with col_hist2:
                score_color = "green" if "Low" in history['score'] else "orange" if "Moderate" in history['score'] else "red"
                st.markdown(f"**Score:** <span style='color:{score_color}'>{history['score']}</span>", 
                           unsafe_allow_html=True)
            
            with col_hist3:
                if st.button("📄 View Report", key=f"view_{history['name']}_{history['date']}", use_container_width=True):
                    st.info(f"Report: {history['result']}")
            
            st.markdown("---")

def run_health_assessment(assessment):
    """Run a health assessment"""
    st.subheader(f"📊 {assessment['name']}")
    
    # Sample assessment questions (would be dynamic in real app)
    if "Heart Disease" in assessment['name']:
        run_heart_disease_assessment()
    elif "Stress" in assessment['name']:
        run_stress_assessment()
    elif "Diabetes" in assessment['name']:
        run_diabetes_assessment()
    else:
        st.info("Assessment functionality would be implemented here")

def run_heart_disease_assessment():
    """Sample heart disease risk assessment"""
    st.write("**Answer the following questions to assess your heart disease risk:**")
    
    with st.form("heart_assessment"):
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        
        smoking = st.radio("Do you smoke?", ["No", "Yes, occasionally", "Yes, regularly"])
        exercise = st.radio("How often do you exercise?", ["Never", "1-2 times/week", "3-4 times/week", "Daily"])
        
        family_history = st.checkbox("Family history of heart disease")
        high_cholesterol = st.checkbox("High cholesterol")
        high_bp = st.checkbox("High blood pressure")
        diabetes = st.checkbox("Diabetes")
        
        diet_quality = st.selectbox("Diet quality", ["Poor", "Fair", "Good", "Excellent"])
        stress_level = st.selectbox("Stress level", ["Low", "Moderate", "High", "Very High"])
        
        if st.form_submit_button("📊 Calculate Risk"):
            # Simple risk calculation
            risk_score = 0
            
            if age > 45:
                risk_score += 2
            if gender == "Male":
                risk_score += 1
            if smoking != "No":
                risk_score += 3
            if exercise == "Never":
                risk_score += 2
            if family_history:
                risk_score += 2
            if high_cholesterol:
                risk_score += 2
            if high_bp:
                risk_score += 2
            if diabetes:
                risk_score += 3
            if diet_quality in ["Poor", "Fair"]:
                risk_score += 1
            if stress_level in ["High", "Very High"]:
                risk_score += 1
            
            # Risk interpretation
            if risk_score <= 3:
                risk_level = "Low"
                color = "green"
                recommendations = [
                    "Continue your healthy lifestyle",
                    "Regular health check-ups",
                    "Maintain current exercise routine"
                ]
            elif risk_score <= 7:
                risk_level = "Moderate"
                color = "orange"
                recommendations = [
                    "Consider lifestyle modifications",
                    "Increase physical activity",
                    "Improve diet quality",
                    "Consult with healthcare provider"
                ]
            else:
                risk_level = "High"
                color = "red"
                recommendations = [
                    "Consult healthcare provider immediately",
                    "Consider comprehensive cardiac evaluation",
                    "Implement aggressive lifestyle changes",
                    "May need medication management"
                ]
            
            st.markdown(f"### 📊 Your Heart Disease Risk: <span style='color:{color}'>{risk_level}</span>", 
                       unsafe_allow_html=True)
            
            st.write("**🎯 Recommendations:**")
            for rec in recommendations:
                st.write(f"• {rec}")
            
            # Save assessment result
            if 'user_id' in st.session_state and st.session_state.user_id:
                assessment_log = f"Heart Disease Risk Assessment: Score {risk_score}, Risk Level: {risk_level}"
                data_manager.add_health_record(
                    st.session_state.user_id,
                    notes=assessment_log
                )

def run_stress_assessment():
    """Sample stress level assessment"""
    st.write("**Rate how often you experience these situations:**")
    
    with st.form("stress_assessment"):
        stress_questions = [
            "Feel overwhelmed by daily responsibilities",
            "Have trouble sleeping due to worries",
            "Feel irritable or short-tempered",
            "Have difficulty concentrating",
            "Feel physically tense or have headaches",
            "Avoid social situations due to stress",
            "Use unhealthy coping mechanisms",
            "Feel out of control in your life"
        ]
        
        responses = []
        for i, question in enumerate(stress_questions):
            response = st.radio(f"{i+1}. {question}", 
                              ["Never", "Rarely", "Sometimes", "Often", "Always"], 
                              key=f"stress_q_{i}")
            responses.append(response)
        
        if st.form_submit_button("📊 Calculate Stress Level"):
            # Calculate stress score
            score_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
            total_score = sum(score_map[response] for response in responses)
            
            if total_score <= 8:
                stress_level = "Low"
                color = "green"
                advice = "You're managing stress well. Continue healthy coping strategies."
            elif total_score <= 16:
                stress_level = "Moderate"
                color = "orange"
                advice = "Some stress management techniques could be helpful."
            else:
                stress_level = "High"
                color = "red"
                advice = "Consider speaking with a mental health professional."
            
            st.markdown(f"### 📊 Your Stress Level: <span style='color:{color}'>{stress_level}</span>", 
                       unsafe_allow_html=True)
            st.write(f"**Score:** {total_score}/32")
            st.write(f"**Advice:** {advice}")

def run_diabetes_assessment():
    """Sample diabetes risk assessment"""
    st.write("**Answer these questions to assess your diabetes risk:**")
    
    with st.form("diabetes_assessment"):
        age_group = st.selectbox("Age group", ["Under 40", "40-49", "50-59", "60+"])
        bmi_category = st.selectbox("BMI category", ["Normal (18.5-24.9)", "Overweight (25-29.9)", "Obese (30+)"])
        
        family_diabetes = st.checkbox("Family history of diabetes")
        gestational_diabetes = st.checkbox("History of gestational diabetes (women)")
        high_bp_med = st.checkbox("Taking medication for high blood pressure")
        
        physical_activity = st.radio("Physical activity level", 
                                   ["Very active", "Moderately active", "Somewhat active", "Not active"])
        
        if st.form_submit_button("📊 Calculate Diabetes Risk"):
            risk_score = 0
            
            if age_group in ["50-59", "60+"]:
                risk_score += 2
            if age_group == "60+":
                risk_score += 1
            
            if "Overweight" in bmi_category:
                risk_score += 1
            elif "Obese" in bmi_category:
                risk_score += 2
            
            if family_diabetes:
                risk_score += 1
            if gestational_diabetes:
                risk_score += 1
            if high_bp_med:
                risk_score += 1
            
            if physical_activity == "Not active":
                risk_score += 1
            
            if risk_score <= 2:
                risk_level = "Low"
                color = "green"
            elif risk_score <= 4:
                risk_level = "Moderate"
                color = "orange"
            else:
                risk_level = "High"
                color = "red"
            
            st.markdown(f"### 📊 Your Diabetes Risk: <span style='color:{color}'>{risk_level}</span>", 
                       unsafe_allow_html=True)
            
            if risk_level in ["Moderate", "High"]:
                st.warning("Consider consulting with a healthcare provider about diabetes screening.")

def show_health_courses():
    """Health education courses"""
    st.header("🎓 Health Education Courses")
    
    st.info("💡 Structured learning programs to improve your health knowledge")
    
    # Course categories
    course_categories = {
        "🫀 Heart Health Mastery": {
            "duration": "4 weeks",
            "lessons": 12,
            "level": "Beginner",
            "description": "Comprehensive course on maintaining cardiovascular health",
            "topics": ["Heart anatomy", "Risk factors", "Prevention strategies", "Exercise for heart health", "Heart-healthy nutrition"],
            "instructor": "Dr. Sarah Johnson",
            "rating": 4.8,
            "students": 1250
        },
        "🍯 Diabetes Prevention & Management": {
            "duration": "6 weeks", 
            "lessons": 18,
            "level": "Intermediate",
            "description": "Complete guide to understanding and managing diabetes",
            "topics": ["Types of diabetes", "Blood sugar monitoring", "Meal planning", "Exercise guidelines", "Medication management"],
            "instructor": "Dr. Michael Chen",
            "rating": 4.9,
            "students": 987
        },
        "🧠 Mental Wellness Foundation": {
            "duration": "5 weeks",
            "lessons": 15,
            "level": "Beginner",
            "description": "Building emotional resilience and mental health awareness",
            "topics": ["Stress management", "Mindfulness", "Sleep hygiene", "Relationship health", "When to seek help"],
            "instructor": "Dr. Emily Davis",
            "rating": 4.7,
            "students": 1456
        },
        "🥗 Nutrition Fundamentals": {
            "duration": "3 weeks",
            "lessons": 9,
            "level": "Beginner", 
            "description": "Science-based approach to healthy eating",
            "topics": ["Macronutrients", "Meal planning", "Reading labels", "Portion control", "Special diets"],
            "instructor": "Nutritionist Lisa Wong",
            "rating": 4.6,
            "students": 2103
        },
        "💪 Fitness for Life": {
            "duration": "8 weeks",
            "lessons": 24,
            "level": "Beginner to Advanced",
            "description": "Progressive fitness program for all levels",
            "topics": ["Exercise basics", "Strength training", "Cardio workouts", "Flexibility", "Injury prevention"],
            "instructor": "Fitness Coach Sarah",
            "rating": 4.8,
            "students": 876
        }
    }
    
    # Display courses
    for course_name, course_info in course_categories.items():
        with st.container():
            col_course1, col_course2, col_course3 = st.columns([2, 1, 1])
            
            with col_course1:
                st.markdown(f"### 🎓 {course_name}")
                st.write(course_info['description'])
                
                st.write("**📚 Course Topics:**")
                for topic in course_info['topics']:
                    st.write(f"• {topic}")
            
            with col_course2:
                st.write(f"**👨‍🏫 Instructor:** {course_info['instructor']}")
                st.write(f"**⏱️ Duration:** {course_info['duration']}")
                st.write(f"**📖 Lessons:** {course_info['lessons']}")
                st.write(f"**📊 Level:** {course_info['level']}")
                
                stars = "⭐" * int(course_info['rating'])
                st.write(f"**Rating:** {stars} {course_info['rating']}/5")
                st.write(f"**👥 Students:** {course_info['students']}")
            
            with col_course3:
                if st.button("🎓 Enroll Now", key=f"enroll_{course_name}", use_container_width=True):
                    enroll_in_course(course_name, course_info)
                
                if st.button("👁️ Preview", key=f"preview_{course_name}", use_container_width=True):
                    show_course_preview(course_name, course_info)
                
                if st.button("📋 Syllabus", key=f"syllabus_{course_name}", use_container_width=True):
                    show_course_syllabus(course_name, course_info)
            
            st.markdown("---")
    
    # User's enrolled courses
    if 'user_id' in st.session_state and st.session_state.user_id:
        st.subheader("📚 My Enrolled Courses")
        
        # Mock enrolled courses
        enrolled_courses = [
            {"name": "Heart Health Mastery", "progress": 75, "completed_lessons": 9, "total_lessons": 12},
            {"name": "Mental Wellness Foundation", "progress": 40, "completed_lessons": 6, "total_lessons": 15}
        ]
        
        if enrolled_courses:
            for course in enrolled_courses:
                col_enrolled1, col_enrolled2, col_enrolled3 = st.columns([2, 1, 1])
                
                with col_enrolled1:
                    st.write(f"**📖 {course['name']}**")
                    st.progress(course['progress'] / 100)
                    st.write(f"Progress: {course['progress']}%")
                
                with col_enrolled2:
                    st.write(f"**Lessons:** {course['completed_lessons']}/{course['total_lessons']}")
                
                with col_enrolled3:
                    if st.button("📖 Continue", key=f"continue_{course['name']}", use_container_width=True):
                        st.success("Resuming course...")
                
                st.markdown("---")
        else:
            st.info("No enrolled courses yet. Browse available courses above!")

def enroll_in_course(course_name, course_info):
    """Enroll user in a course"""
    st.success(f"🎉 Successfully enrolled in {course_name}!")
    
    if 'user_id' in st.session_state and st.session_state.user_id:
        enrollment_log = f"Course Enrollment: {course_name} - Duration: {course_info['duration']}, Instructor: {course_info['instructor']}"
        data_manager.add_health_record(
            st.session_state.user_id,
            notes=enrollment_log
        )
    
    st.info(f"""
    **Course Details:**
    - Duration: {course_info['duration']}
    - Lessons: {course_info['lessons']}
    - Instructor: {course_info['instructor']}
    
    You can start the first lesson immediately!
    """)

def show_course_preview(course_name, course_info):
    """Show course preview"""
    st.subheader(f"👁️ Course Preview: {course_name}")
    
    st.write(f"**Instructor:** {course_info['instructor']}")
    st.write(f"**Level:** {course_info['level']}")
    st.write(f"**Duration:** {course_info['duration']}")
    
    st.write("**Course Overview:**")
    st.write(course_info['description'])
    
    st.write("**What You'll Learn:**")
    for i, topic in enumerate(course_info['topics'], 1):
        st.write(f"{i}. {topic}")
    
    st.success("Ready to start your health education journey?")

def show_course_syllabus(course_name, course_info):
    """Show detailed course syllabus"""
    st.subheader(f"📋 Syllabus: {course_name}")
    
    # Mock detailed syllabus
    if "Heart Health" in course_name:
        syllabus = [
            {"week": 1, "title": "Understanding Your Heart", "lessons": ["Heart anatomy", "How your heart works", "Common heart problems"]},
            {"week": 2, "title": "Risk Factors", "lessons": ["Controllable risks", "Non-controllable risks", "Risk assessment"]},
            {"week": 3, "title": "Prevention Strategies", "lessons": ["Diet for heart health", "Exercise guidelines", "Stress management"]},
            {"week": 4, "title": "Living Heart-Healthy", "lessons": ["Daily habits", "Long-term strategies", "When to seek help"]}
        ]
        
        for week_info in syllabus:
            st.write(f"**Week {week_info['week']}: {week_info['title']}**")
            for lesson in week_info['lessons']:
                st.write(f"  • {lesson}")
            st.write("")
    
    else:
        st.info("Detailed syllabus would be displayed here")

if __name__ == "__main__":
    main()
