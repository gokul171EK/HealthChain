import random
from datetime import datetime, timedelta

class AISimulator:
    def __init__(self):
        # Symptom checker database
        self.symptoms_database = {
            "fever": {
                "common_causes": ["Viral infection", "Bacterial infection", "Flu", "COVID-19"],
                "recommendations": [
                    "Rest and stay hydrated",
                    "Take paracetamol for fever reduction",
                    "Monitor temperature regularly",
                    "Consult doctor if fever persists over 3 days"
                ],
                "severity": "moderate"
            },
            "headache": {
                "common_causes": ["Tension", "Dehydration", "Stress", "Migraine", "Sleep deprivation"],
                "recommendations": [
                    "Drink plenty of water",
                    "Rest in a dark, quiet room",
                    "Apply cold compress to forehead",
                    "Consider mild pain reliever"
                ],
                "severity": "mild"
            },
            "cough": {
                "common_causes": ["Common cold", "Allergies", "Bronchitis", "Asthma"],
                "recommendations": [
                    "Stay hydrated with warm fluids",
                    "Use honey for soothing throat",
                    "Avoid smoke and irritants",
                    "Consult doctor if cough persists over 2 weeks"
                ],
                "severity": "mild"
            },
            "chest_pain": {
                "common_causes": ["Heart disease", "Muscle strain", "Anxiety", "Acid reflux"],
                "recommendations": [
                    "Seek immediate medical attention",
                    "Do not ignore chest pain",
                    "Call emergency services if severe",
                    "Avoid physical exertion"
                ],
                "severity": "severe"
            },
            "shortness_of_breath": {
                "common_causes": ["Asthma", "Anxiety", "Heart problems", "Lung infection"],
                "recommendations": [
                    "Seek immediate medical attention",
                    "Sit upright and try to stay calm",
                    "Use prescribed inhaler if available",
                    "Call emergency if severe difficulty breathing"
                ],
                "severity": "severe"
            },
            "stomach_pain": {
                "common_causes": ["Indigestion", "Food poisoning", "Gastritis", "Appendicitis"],
                "recommendations": [
                    "Avoid solid foods temporarily",
                    "Stay hydrated with clear fluids",
                    "Apply warm compress",
                    "Seek medical attention if severe or persistent"
                ],
                "severity": "moderate"
            },
            "nausea": {
                "common_causes": ["Food poisoning", "Motion sickness", "Pregnancy", "Medication side effects"],
                "recommendations": [
                    "Sip clear fluids slowly",
                    "Try ginger tea or candies",
                    "Eat bland foods like toast or crackers",
                    "Rest and avoid strong odors"
                ],
                "severity": "mild"
            },
            "dizziness": {
                "common_causes": ["Dehydration", "Low blood pressure", "Inner ear problems", "Medication effects"],
                "recommendations": [
                    "Sit or lie down immediately",
                    "Drink water slowly",
                    "Avoid sudden movements",
                    "Consult doctor if episodes are frequent"
                ],
                "severity": "moderate"
            }
        }
        
        # Health recommendations database
        self.health_recommendations = {
            "general": [
                "Drink at least 8 glasses of water daily",
                "Aim for 7-9 hours of quality sleep",
                "Take a 30-minute walk daily",
                "Include fruits and vegetables in every meal",
                "Practice deep breathing for 5 minutes",
                "Limit processed food consumption",
                "Schedule regular health check-ups",
                "Maintain good posture while working"
            ],
            "fitness": [
                "Start with 10 minutes of exercise daily",
                "Take stairs instead of elevators",
                "Do stretching exercises every morning",
                "Try bodyweight exercises at home",
                "Set achievable fitness goals",
                "Track your daily steps",
                "Include strength training twice a week",
                "Stay active throughout the day"
            ],
            "mental_health": [
                "Practice mindfulness meditation",
                "Connect with friends and family regularly",
                "Limit social media usage before bed",
                "Engage in hobbies you enjoy",
                "Practice gratitude daily",
                "Seek support when feeling overwhelmed",
                "Maintain a regular sleep schedule",
                "Spend time in nature"
            ],
            "nutrition": [
                "Eat a variety of colorful foods",
                "Limit sugar and salt intake",
                "Include lean proteins in your diet",
                "Choose whole grains over refined ones",
                "Eat smaller, frequent meals",
                "Avoid eating late at night",
                "Include healthy fats like nuts and seeds",
                "Read food labels carefully"
            ]
        }
        
        # Risk assessment factors
        self.risk_factors = {
            "diabetes": ["family_history", "obesity", "sedentary_lifestyle", "age_over_45"],
            "heart_disease": ["smoking", "high_cholesterol", "hypertension", "family_history"],
            "hypertension": ["high_sodium_diet", "stress", "obesity", "family_history"],
            "osteoporosis": ["low_calcium", "sedentary_lifestyle", "smoking", "age_over_50"]
        }
    
    def check_symptoms(self, symptoms, additional_info=None):
        """Analyze symptoms and provide recommendations"""
        if not symptoms:
            return {"error": "No symptoms provided"}
        
        # Convert symptoms to lowercase for matching
        symptoms = [s.lower().replace(" ", "_") for s in symptoms]
        
        results = []
        max_severity = "mild"
        
        for symptom in symptoms:
            if symptom in self.symptoms_database:
                symptom_info = self.symptoms_database[symptom]
                results.append({
                    "symptom": symptom.replace("_", " ").title(),
                    "possible_causes": symptom_info["common_causes"],
                    "recommendations": symptom_info["recommendations"],
                    "severity": symptom_info["severity"]
                })
                
                # Track highest severity
                if symptom_info["severity"] == "severe":
                    max_severity = "severe"
                elif symptom_info["severity"] == "moderate" and max_severity != "severe":
                    max_severity = "moderate"
        
        # Generate overall assessment
        overall_assessment = self._generate_overall_assessment(results, max_severity)
        
        return {
            "symptoms_analyzed": results,
            "overall_severity": max_severity,
            "overall_assessment": overall_assessment,
            "disclaimer": "This is an AI-based preliminary assessment. Please consult a healthcare professional for proper diagnosis and treatment."
        }
    
    def _generate_overall_assessment(self, results, severity):
        """Generate overall health assessment"""
        if severity == "severe":
            return "⚠️ URGENT: Some of your symptoms require immediate medical attention. Please seek emergency care or consult a doctor immediately."
        elif severity == "moderate":
            return "⚡ MODERATE: Your symptoms suggest you should consult a healthcare provider within the next day or two for proper evaluation."
        else:
            return "✅ MILD: Your symptoms appear to be mild. Home care and rest may help, but consult a doctor if symptoms worsen or persist."
    
    def get_health_recommendations(self, user_data):
        """Get personalized health recommendations based on user profile"""
        recommendations = []
        
        # Get random recommendations from different categories
        categories = ["general", "fitness", "mental_health", "nutrition"]
        
        for category in categories:
            if category in self.health_recommendations:
                rec = random.choice(self.health_recommendations[category])
                recommendations.append(f"💡 {rec}")
        
        # Add personalized recommendations based on user data
        if user_data:
            age = user_data.get('age', 25)
            gender = user_data.get('gender', 'Unknown')
            
            if age > 40:
                recommendations.append("💡 Consider regular cardiovascular screening")
            if age > 50:
                recommendations.append("💡 Include calcium-rich foods for bone health")
            if gender == "Female":
                recommendations.append("💡 Ensure adequate iron intake")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def predict_health_risks(self, user_data, lifestyle_factors):
        """Predict health risks based on user profile and lifestyle"""
        risks = {}
        
        age = user_data.get('age', 25)
        gender = user_data.get('gender', 'Unknown')
        
        # Simulate risk calculation (in real app, this would use ML models)
        base_risk = random.randint(10, 30)
        
        for condition, factors in self.risk_factors.items():
            risk_score = base_risk
            
            # Adjust risk based on age
            if age > 40:
                risk_score += 10
            if age > 60:
                risk_score += 20
            
            # Adjust risk based on lifestyle factors
            for factor in factors:
                if factor in lifestyle_factors:
                    risk_score += random.randint(5, 15)
            
            # Cap risk at 100%
            risk_score = min(risk_score, 100)
            
            risks[condition] = {
                "risk_percentage": risk_score,
                "risk_level": self._get_risk_level(risk_score),
                "prevention_tips": self._get_prevention_tips(condition)
            }
        
        return risks
    
    def _get_risk_level(self, score):
        """Convert risk score to risk level"""
        if score < 25:
            return "Low"
        elif score < 50:
            return "Moderate"
        elif score < 75:
            return "High"
        else:
            return "Very High"
    
    def _get_prevention_tips(self, condition):
        """Get prevention tips for specific conditions"""
        tips = {
            "diabetes": [
                "Maintain a healthy weight",
                "Exercise regularly",
                "Eat a balanced diet low in sugar",
                "Monitor blood sugar levels regularly"
            ],
            "heart_disease": [
                "Quit smoking if you smoke",
                "Exercise at least 150 minutes per week",
                "Eat heart-healthy foods",
                "Manage stress effectively"
            ],
            "hypertension": [
                "Reduce sodium intake",
                "Exercise regularly",
                "Maintain healthy weight",
                "Limit alcohol consumption"
            ],
            "osteoporosis": [
                "Consume adequate calcium and vitamin D",
                "Engage in weight-bearing exercises",
                "Avoid smoking and excessive alcohol",
                "Get regular bone density screenings"
            ]
        }
        
        return tips.get(condition, ["Maintain a healthy lifestyle", "Regular check-ups with healthcare provider"])
    
    def generate_meal_plan(self, user_preferences, health_conditions=None):
        """Generate a personalized meal plan"""
        # Sample meal database
        meals = {
            "breakfast": [
                "Oatmeal with berries and nuts",
                "Greek yogurt with honey and granola",
                "Whole grain toast with avocado",
                "Scrambled eggs with vegetables",
                "Smoothie with spinach and banana"
            ],
            "lunch": [
                "Grilled chicken salad with mixed greens",
                "Quinoa bowl with roasted vegetables",
                "Lentil soup with whole grain bread",
                "Turkey and vegetable wrap",
                "Brown rice with steamed fish and broccoli"
            ],
            "dinner": [
                "Baked salmon with sweet potato",
                "Lean beef stir-fry with vegetables",
                "Grilled tofu with quinoa and vegetables",
                "Chicken breast with roasted vegetables",
                "Vegetable curry with brown rice"
            ],
            "snacks": [
                "Mixed nuts and seeds",
                "Apple slices with almond butter",
                "Carrot sticks with hummus",
                "Greek yogurt with berries",
                "Whole grain crackers with cheese"
            ]
        }
        
        # Generate meal plan for 3 days
        meal_plan = {}
        for day in range(1, 4):
            meal_plan[f"Day {day}"] = {
                "breakfast": random.choice(meals["breakfast"]),
                "lunch": random.choice(meals["lunch"]),
                "dinner": random.choice(meals["dinner"]),
                "snack": random.choice(meals["snacks"])
            }
        
        return meal_plan
    
    def get_exercise_recommendations(self, fitness_level, health_conditions=None):
        """Get personalized exercise recommendations"""
        exercises = {
            "beginner": [
                "10-minute daily walk",
                "Basic stretching routine",
                "Wall push-ups",
                "Chair exercises",
                "Gentle yoga poses"
            ],
            "intermediate": [
                "30-minute brisk walk",
                "Bodyweight exercises",
                "Swimming",
                "Cycling",
                "Strength training with light weights"
            ],
            "advanced": [
                "High-intensity interval training",
                "Weight lifting",
                "Running or jogging",
                "Advanced yoga poses",
                "Sports activities"
            ]
        }
        
        level = fitness_level.lower() if fitness_level else "beginner"
        return exercises.get(level, exercises["beginner"])
