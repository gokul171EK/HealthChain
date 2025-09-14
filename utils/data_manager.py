import pandas as pd
import os
import hashlib
from datetime import datetime
import uuid

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        self.ensure_data_files()
    
    # ... (all your existing functions like __init__, ensure_data_directory, etc.) ...

    def get_pharmacies(self):
        """Get pharmacies"""
        try:
            pharmacies_df = pd.read_csv(os.path.join(self.data_dir, "pharmacies.csv"))
            return pharmacies_df
        except Exception as e:
            return pd.DataFrame()

    # --- ADD THE TWO NEW FUNCTIONS BELOW THIS LINE ---

    def update_user_profile(self, user_id, name, phone, age, gender, blood_group):
        """Update a user's profile information."""
        try:
            filepath = os.path.join(self.data_dir, "users.csv")
            users_df = pd.read_csv(filepath)
            
            # Find the user by user_id
            user_index = users_df.index[users_df['user_id'] == user_id].tolist()
            if not user_index:
                return False

            # Update the user's data
            users_df.loc[user_index[0], 'name'] = name
            users_df.loc[user_index[0], 'phone'] = phone
            users_df.loc[user_index[0], 'age'] = age
            users_df.loc[user_index[0], 'gender'] = gender
            users_df.loc[user_index[0], 'blood_group'] = blood_group
            
            # Save the updated dataframe back to the CSV
            users_df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False

    def update_user_password(self, user_id, new_password):
        """Update a user's password."""
        try:
            filepath = os.path.join(self.data_dir, "users.csv")
            users_df = pd.read_csv(filepath)

            # Find the user by user_id
            user_index = users_df.index[users_df['user_id'] == user_id].tolist()
            if not user_index:
                return False

            # Hash the new password and update it
            new_password_hash = self.hash_password(new_password)
            users_df.loc[user_index[0], 'password_hash'] = new_password_hash
            
            # Save the updated dataframe
            users_df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

    # --- ADD THE TWO NEW FUNCTIONS BELOW THIS LINE ---

    def create_community_post(self, user_id, author, title, content, category):
        """Create a new community post."""
        try:
            filepath = os.path.join(self.data_dir, "community_posts.csv")
            posts_df = pd.read_csv(filepath)
            
            post_id = str(uuid.uuid4())
            new_post = {
                "post_id": post_id,
                "user_id": user_id,
                "author": author,
                "title": title,
                "content": content,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "likes": 0,
                "comments": 0
            }
            
            posts_df = pd.concat([posts_df, pd.DataFrame([new_post])], ignore_index=True)
            posts_df.to_csv(filepath, index=False)
            return post_id
        except Exception as e:
            print(f"Error creating community post: {e}")
            return None

    def get_recent_community_posts(self, limit=20):
        """Get recent community posts, sorted by date."""
        try:
            filepath = os.path.join(self.data_dir, "community_posts.csv")
            if not os.path.exists(filepath):
                return pd.DataFrame()
                
            posts_df = pd.read_csv(filepath)
            if not posts_df.empty:
                posts_df['date'] = pd.to_datetime(posts_df['date'])
                return posts_df.sort_values('date', ascending=False).head(limit)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error getting community posts: {e}")
            return pd.DataFrame()

