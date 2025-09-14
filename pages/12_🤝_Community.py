import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.styling import add_app_styling

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

data_manager = init_data_manager()

def main():
    """Main function to display the community page."""
    add_app_styling()

    # Make sure this session state check is at the top of the function
    if 'theme' not in st.session_state:
      st.session_state.theme = "Light"

    add_app_styling(theme=st.session_state.theme)

    st.title("🤝 Community & Support Forum")
    st.markdown("### Connect with others, share your journey, and find support.")

    # Check if user is logged in
    if 'user_id' not in st.session_state or st.session_state.user_id is None:
        st.error("🔒 Please login to participate in the community.")
        st.info("Go to the Home page to login or register.")
        return

    # --- TABS FOR COMMUNITY FEATURES ---
    tab1, tab2 = st.tabs(["💬 Community Feed", "📝 Create a Post"])

    with tab1:
        show_community_feed()

    with tab2:
        create_new_post()


def show_community_feed():
    """Display the feed of recent community posts."""
    st.header("💬 Recent Community Posts")

    # Filter options
    category_filter = st.selectbox(
        "Filter by category",
        ["All", "General Health", "Mental Wellness", "Fitness Journey", "Nutrition Tips", "Success Stories"]
    )

    # Fetch recent posts
    posts_df = data_manager.get_recent_community_posts()

    if posts_df.empty:
        st.info("No community posts yet. Be the first to start a conversation!")
        return

    # Filter posts if a category is selected
    if category_filter != "All":
        posts_df = posts_df[posts_df['category'] == category_filter]

    if posts_df.empty:
        st.info(f"No posts found in the '{category_filter}' category yet.")
        return
        
    # Display each post
    for index, post in posts_df.iterrows():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        st.subheader(post['title'])
        st.caption(f"Posted by **{post['author']}** in *{post['category']}* on {pd.to_datetime(post['date']).strftime('%B %d, %Y')}")
        st.markdown("---")
        st.write(post['content'])
        
        # Action buttons (like, comment, share)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
        with col1:
            if st.button(f"👍 Like ({post.get('likes', 0)})", key=f"like_{post['post_id']}"):
                st.toast("Liked!")
        with col2:
            if st.button(f"💬 Comment ({post.get('comments', 0)})", key=f"comment_{post['post_id']}"):
                st.toast("Comment feature coming soon!")
        with col3:
            if st.button("🔗 Share", key=f"share_{post['post_id']}"):
                st.toast("Link copied to clipboard!")
        
        st.markdown("</div>", unsafe_allow_html=True)


def create_new_post():
    """Display a form to create a new community post."""
    st.header("📝 Create a New Post")
    
    with st.form("new_post_form"):
        title = st.text_input("Post Title")
        category = st.selectbox(
            "Category",
            ["General Health", "Mental Wellness", "Fitness Journey", "Nutrition Tips", "Success Stories", "Ask the Community"]
        )
        content = st.text_area("Your Message", height=200)

        submitted = st.form_submit_button("✅ Submit Post", use_container_width=True)
        if submitted:
            if title and content:
                user_name = st.session_state.user_data.get('name', 'Anonymous')
                post_id = data_manager.create_community_post(
                    st.session_state.user_id,
                    user_name,
                    title,
                    content,
                    category
                )
                if post_id:
                    st.success("🎉 Your post has been published successfully!")
                    st.balloons()
                else:
                    st.error("❌ There was an error publishing your post. Please try again.")
            else:
                st.warning("Please fill in both the title and message for your post.")

if __name__ == "__main__":
    main()
