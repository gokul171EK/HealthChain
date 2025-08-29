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
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def ensure_data_files(self):
        """Create CSV files with headers if they don't exist"""
        files_and_headers = {
            "users.csv": ["user_id", "name", "email", "phone", "age", "gender", "blood_group", "password_hash", "created_date"],
            "blood_donors.csv": ["donor_id", "user_id", "blood_group", "last_donation", "total_donations", "available", "location", "contact"],
            "organ_donors.csv": ["donor_id", "user_id", "organs", "medical_conditions", "emergency_contact", "registered_date", "status"],
            "health_records.csv": ["record_id", "user_id", "date", "heart_rate", "blood_pressure", "weight", "height", "temperature", "notes"],
            "appointments.csv": ["appointment_id", "user_id", "doctor_name", "specialty", "date", "time", "status", "consultation_type", "notes"],
            "blood_banks.csv": ["bank_id", "name", "address", "phone", "email", "blood_types_available", "operating_hours"],
            "hospitals.csv": ["hospital_id", "name", "address", "phone", "emergency_number", "specialties", "rating"],
            "pharmacies.csv": ["pharmacy_id", "name", "address", "phone", "delivery_available", "operating_hours", "rating"],
            "feedback.csv": ["feedback_id", "user_id", "service_type", "rating", "comment", "date", "response"],
            "community_posts.csv": ["post_id", "user_id", "author", "title", "content", "category", "date", "likes", "comments"]
        }
        
        for filename, headers in files_and_headers.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                df = pd.DataFrame(columns=headers)
                df.to_csv(filepath, index=False)
    
    def hash_password(self, password):
        """Hash password for secure storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name, email, phone, age, gender, blood_group, password):
        """Create a new user"""
        try:
            users_df = pd.read_csv(os.path.join(self.data_dir, "users.csv"))
            
            # Check if email already exists
            if email in users_df['email'].values:
                return None
            
            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)
            
            new_user = {
                "user_id": user_id,
                "name": name,
                "email": email,
                "phone": phone,
                "age": age,
                "gender": gender,
                "blood_group": blood_group,
                "password_hash": password_hash,
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
            users_df.to_csv(os.path.join(self.data_dir, "users.csv"), index=False)
            
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        try:
            users_df = pd.read_csv(os.path.join(self.data_dir, "users.csv"))
            password_hash = self.hash_password(password)
            
            user = users_df[(users_df['email'] == email) & (users_df['password_hash'] == password_hash)]
            
            if not user.empty:
                return user.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            users_df = pd.read_csv(os.path.join(self.data_dir, "users.csv"))
            user = users_df[users_df['user_id'] == user_id]
            return user.iloc[0].to_dict() if not user.empty else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def register_blood_donor(self, user_id, blood_group, location, contact, last_donation=None):
        """Register a blood donor"""
        try:
            donors_df = pd.read_csv(os.path.join(self.data_dir, "blood_donors.csv"))
            
            donor_id = str(uuid.uuid4())
            new_donor = {
                "donor_id": donor_id,
                "user_id": user_id,
                "blood_group": blood_group,
                "last_donation": last_donation or "",
                "total_donations": 0,
                "available": True,
                "location": location,
                "contact": contact
            }
            
            donors_df = pd.concat([donors_df, pd.DataFrame([new_donor])], ignore_index=True)
            donors_df.to_csv(os.path.join(self.data_dir, "blood_donors.csv"), index=False)
            
            return donor_id
        except Exception as e:
            print(f"Error registering blood donor: {e}")
            return None
    
    def register_organ_donor(self, user_id, organs, medical_conditions, emergency_contact):
        """Register an organ donor"""
        try:
            donors_df = pd.read_csv(os.path.join(self.data_dir, "organ_donors.csv"))
            
            donor_id = str(uuid.uuid4())
            new_donor = {
                "donor_id": donor_id,
                "user_id": user_id,
                "organs": ",".join(organs),
                "medical_conditions": medical_conditions,
                "emergency_contact": emergency_contact,
                "registered_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "Active"
            }
            
            donors_df = pd.concat([donors_df, pd.DataFrame([new_donor])], ignore_index=True)
            donors_df.to_csv(os.path.join(self.data_dir, "organ_donors.csv"), index=False)
            
            return donor_id
        except Exception as e:
            print(f"Error registering organ donor: {e}")
            return None
    
    def add_health_record(self, user_id, heart_rate=None, blood_pressure=None, weight=None, height=None, temperature=None, notes=""):
        """Add a health record"""
        try:
            records_df = pd.read_csv(os.path.join(self.data_dir, "health_records.csv"))
            
            record_id = str(uuid.uuid4())
            new_record = {
                "record_id": record_id,
                "user_id": user_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "heart_rate": heart_rate,
                "blood_pressure": blood_pressure,
                "weight": weight,
                "height": height,
                "temperature": temperature,
                "notes": notes
            }
            
            records_df = pd.concat([records_df, pd.DataFrame([new_record])], ignore_index=True)
            records_df.to_csv(os.path.join(self.data_dir, "health_records.csv"), index=False)
            
            return record_id
        except Exception as e:
            print(f"Error adding health record: {e}")
            return None
    
    def get_user_health_records(self, user_id):
        """Get health records for a user"""
        try:
            records_df = pd.read_csv(os.path.join(self.data_dir, "health_records.csv"))
            user_records = records_df[records_df['user_id'] == user_id]
            return user_records.sort_values('date')
        except Exception as e:
            print(f"Error getting health records: {e}")
            return pd.DataFrame()
    
    def book_appointment(self, user_id, doctor_name, specialty, date, time, consultation_type):
        """Book an appointment"""
        try:
            appointments_df = pd.read_csv(os.path.join(self.data_dir, "appointments.csv"))
            
            appointment_id = str(uuid.uuid4())
            new_appointment = {
                "appointment_id": appointment_id,
                "user_id": user_id,
                "doctor_name": doctor_name,
                "specialty": specialty,
                "date": date,
                "time": time,
                "status": "Scheduled",
                "consultation_type": consultation_type,
                "notes": ""
            }
            
            appointments_df = pd.concat([appointments_df, pd.DataFrame([new_appointment])], ignore_index=True)
            appointments_df.to_csv(os.path.join(self.data_dir, "appointments.csv"), index=False)
            
            return appointment_id
        except Exception as e:
            print(f"Error booking appointment: {e}")
            return None
    
    def get_user_appointments(self, user_id):
        """Get appointments for a user"""
        try:
            appointments_df = pd.read_csv(os.path.join(self.data_dir, "appointments.csv"))
            user_appointments = appointments_df[appointments_df['user_id'] == user_id]
            return user_appointments.sort_values('date', ascending=False)
        except Exception as e:
            print(f"Error getting appointments: {e}")
            return pd.DataFrame()
    
    def add_feedback(self, user_id, service_type, rating, comment):
        """Add user feedback"""
        try:
            feedback_df = pd.read_csv(os.path.join(self.data_dir, "feedback.csv"))
            
            feedback_id = str(uuid.uuid4())
            new_feedback = {
                "feedback_id": feedback_id,
                "user_id": user_id,
                "service_type": service_type,
                "rating": rating,
                "comment": comment,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "response": ""
            }
            
            feedback_df = pd.concat([feedback_df, pd.DataFrame([new_feedback])], ignore_index=True)
            feedback_df.to_csv(os.path.join(self.data_dir, "feedback.csv"), index=False)
            
            return feedback_id
        except Exception as e:
            print(f"Error adding feedback: {e}")
            return None
    
    def create_community_post(self, user_id, author, title, content, category):
        """Create a community post"""
        try:
            posts_df = pd.read_csv(os.path.join(self.data_dir, "community_posts.csv"))
            
            post_id = str(uuid.uuid4())
            new_post = {
                "post_id": post_id,
                "user_id": user_id,
                "author": author,
                "title": title,
                "content": content,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "likes": 0,
                "comments": 0
            }
            
            posts_df = pd.concat([posts_df, pd.DataFrame([new_post])], ignore_index=True)
            posts_df.to_csv(os.path.join(self.data_dir, "community_posts.csv"), index=False)
            
            return post_id
        except Exception as e:
            print(f"Error creating community post: {e}")
            return None
    
    def get_recent_community_posts(self, limit=10):
        """Get recent community posts"""
        try:
            posts_df = pd.read_csv(os.path.join(self.data_dir, "community_posts.csv"))
            if not posts_df.empty:
                return posts_df.sort_values('date', ascending=False).head(limit)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error getting community posts: {e}")
            return pd.DataFrame()
    
    def get_blood_donors(self, blood_group=None):
        """Get blood donors"""
        try:
            donors_df = pd.read_csv(os.path.join(self.data_dir, "blood_donors.csv"))
            if blood_group:
                return donors_df[donors_df['blood_group'] == blood_group]
            return donors_df
        except Exception as e:
            print(f"Error getting blood donors: {e}")
            return pd.DataFrame()
    
    def get_blood_donors_count(self):
        """Get total blood donors count"""
        try:
            donors_df = pd.read_csv(os.path.join(self.data_dir, "blood_donors.csv"))
            return len(donors_df)
        except Exception as e:
            return 0
    
    def get_organ_donors_count(self):
        """Get total organ donors count"""
        try:
            donors_df = pd.read_csv(os.path.join(self.data_dir, "organ_donors.csv"))
            return len(donors_df)
        except Exception as e:
            return 0
    
    def get_users_count(self):
        """Get total users count"""
        try:
            users_df = pd.read_csv(os.path.join(self.data_dir, "users.csv"))
            return len(users_df)
        except Exception as e:
            return 0
    
    def get_health_records_count(self):
        """Get total health records count"""
        try:
            records_df = pd.read_csv(os.path.join(self.data_dir, "health_records.csv"))
            return len(records_df)
        except Exception as e:
            return 0
    
    def get_blood_banks(self):
        """Get blood banks"""
        try:
            banks_df = pd.read_csv(os.path.join(self.data_dir, "blood_banks.csv"))
            return banks_df
        except Exception as e:
            return pd.DataFrame()
    
    def get_hospitals(self):
        """Get hospitals"""
        try:
            hospitals_df = pd.read_csv(os.path.join(self.data_dir, "hospitals.csv"))
            return hospitals_df
        except Exception as e:
            return pd.DataFrame()
    
    def get_pharmacies(self):
        """Get pharmacies"""
        try:
            pharmacies_df = pd.read_csv(os.path.join(self.data_dir, "pharmacies.csv"))
            return pharmacies_df
        except Exception as e:
            return pd.DataFrame()
