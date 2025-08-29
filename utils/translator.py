class MedicalTranslator:
    def __init__(self):
        # Medical terms translations (English to other languages)
        self.translations = {
            "hindi": {
                # Basic terms
                "doctor": "डॉक्टर",
                "hospital": "अस्पताल",
                "medicine": "दवा",
                "patient": "मरीज़",
                "nurse": "नर्स",
                "pharmacy": "दवाखाना",
                "appointment": "अपॉइंटमेंट",
                "prescription": "नुस्खा",
                "diagnosis": "निदान",
                "treatment": "इलाज",
                
                # Symptoms
                "fever": "बुखार",
                "headache": "सिरदर्द",
                "cough": "खांसी",
                "cold": "सर्दी",
                "pain": "दर्द",
                "nausea": "जी मिचलाना",
                "dizziness": "चक्कर आना",
                "fatigue": "थकान",
                "chest pain": "सीने में दर्द",
                "shortness of breath": "सांस लेने में तकलीफ",
                "stomach pain": "पेट दर्द",
                
                # Body parts
                "head": "सिर",
                "chest": "सीना",
                "stomach": "पेट",
                "back": "पीठ",
                "leg": "पैर",
                "arm": "बाँह",
                "hand": "हाथ",
                "foot": "पैर",
                "eye": "आंख",
                "ear": "कान",
                "nose": "नाक",
                "mouth": "मुंह",
                "throat": "गला",
                
                # Common instructions
                "take medicine": "दवा लें",
                "rest": "आराम करें",
                "drink water": "पानी पिएं",
                "emergency": "आपातकाल",
                "urgent": "तत्काल",
                "blood donation": "रक्तदान",
                "blood group": "रक्त समूह",
                "donor": "दाता",
                "organ donation": "अंगदान"
            },
            "spanish": {
                # Basic terms
                "doctor": "médico",
                "hospital": "hospital",
                "medicine": "medicina",
                "patient": "paciente",
                "nurse": "enfermera",
                "pharmacy": "farmacia",
                "appointment": "cita",
                "prescription": "receta",
                "diagnosis": "diagnóstico",
                "treatment": "tratamiento",
                
                # Symptoms
                "fever": "fiebre",
                "headache": "dolor de cabeza",
                "cough": "tos",
                "cold": "resfriado",
                "pain": "dolor",
                "nausea": "náusea",
                "dizziness": "mareo",
                "fatigue": "fatiga",
                "chest pain": "dolor en el pecho",
                "shortness of breath": "falta de aire",
                "stomach pain": "dolor de estómago",
                
                # Body parts
                "head": "cabeza",
                "chest": "pecho",
                "stomach": "estómago",
                "back": "espalda",
                "leg": "pierna",
                "arm": "brazo",
                "hand": "mano",
                "foot": "pie",
                "eye": "ojo",
                "ear": "oído",
                "nose": "nariz",
                "mouth": "boca",
                "throat": "garganta",
                
                # Common instructions
                "take medicine": "tomar medicina",
                "rest": "descansar",
                "drink water": "beber agua",
                "emergency": "emergencia",
                "urgent": "urgente",
                "blood donation": "donación de sangre",
                "blood group": "grupo sanguíneo",
                "donor": "donante",
                "organ donation": "donación de órganos"
            },
            "french": {
                # Basic terms
                "doctor": "médecin",
                "hospital": "hôpital",
                "medicine": "médicament",
                "patient": "patient",
                "nurse": "infirmière",
                "pharmacy": "pharmacie",
                "appointment": "rendez-vous",
                "prescription": "ordonnance",
                "diagnosis": "diagnostic",
                "treatment": "traitement",
                
                # Symptoms
                "fever": "fièvre",
                "headache": "mal de tête",
                "cough": "toux",
                "cold": "rhume",
                "pain": "douleur",
                "nausea": "nausée",
                "dizziness": "vertige",
                "fatigue": "fatigue",
                "chest pain": "douleur thoracique",
                "shortness of breath": "essoufflement",
                "stomach pain": "mal d'estomac",
                
                # Body parts
                "head": "tête",
                "chest": "poitrine",
                "stomach": "estomac",
                "back": "dos",
                "leg": "jambe",
                "arm": "bras",
                "hand": "main",
                "foot": "pied",
                "eye": "œil",
                "ear": "oreille",
                "nose": "nez",
                "mouth": "bouche",
                "throat": "gorge",
                
                # Common instructions
                "take medicine": "prendre un médicament",
                "rest": "se reposer",
                "drink water": "boire de l'eau",
                "emergency": "urgence",
                "urgent": "urgent",
                "blood donation": "don de sang",
                "blood group": "groupe sanguin",
                "donor": "donneur",
                "organ donation": "don d'organes"
            },
            "german": {
                # Basic terms
                "doctor": "Arzt",
                "hospital": "Krankenhaus",
                "medicine": "Medizin",
                "patient": "Patient",
                "nurse": "Krankenschwester",
                "pharmacy": "Apotheke",
                "appointment": "Termin",
                "prescription": "Rezept",
                "diagnosis": "Diagnose",
                "treatment": "Behandlung",
                
                # Symptoms
                "fever": "Fieber",
                "headache": "Kopfschmerzen",
                "cough": "Husten",
                "cold": "Erkältung",
                "pain": "Schmerz",
                "nausea": "Übelkeit",
                "dizziness": "Schwindel",
                "fatigue": "Müdigkeit",
                "chest pain": "Brustschmerzen",
                "shortness of breath": "Atemnot",
                "stomach pain": "Bauchschmerzen",
                
                # Body parts
                "head": "Kopf",
                "chest": "Brust",
                "stomach": "Magen",
                "back": "Rücken",
                "leg": "Bein",
                "arm": "Arm",
                "hand": "Hand",
                "foot": "Fuß",
                "eye": "Auge",
                "ear": "Ohr",
                "nose": "Nase",
                "mouth": "Mund",
                "throat": "Hals",
                
                # Common instructions
                "take medicine": "Medizin nehmen",
                "rest": "ausruhen",
                "drink water": "Wasser trinken",
                "emergency": "Notfall",
                "urgent": "dringend",
                "blood donation": "Blutspende",
                "blood group": "Blutgruppe",
                "donor": "Spender",
                "organ donation": "Organspende"
            }
        }
        
        # Common medical phrases
        self.common_phrases = {
            "hindi": {
                "how are you feeling": "आप कैसा महसूस कर रहे हैं",
                "what is your problem": "आपकी क्या समस्या है",
                "take this medicine": "यह दवा लें",
                "come back tomorrow": "कल वापस आएं",
                "you need rest": "आपको आराम की जरूरत है",
                "drink plenty of water": "खूब पानी पिएं",
                "avoid spicy food": "मसालेदार खाना न खाएं",
                "take medicine after food": "खाने के बाद दवा लें"
            },
            "spanish": {
                "how are you feeling": "¿cómo te sientes?",
                "what is your problem": "¿cuál es tu problema?",
                "take this medicine": "toma esta medicina",
                "come back tomorrow": "vuelve mañana",
                "you need rest": "necesitas descansar",
                "drink plenty of water": "bebe mucha agua",
                "avoid spicy food": "evita comida picante",
                "take medicine after food": "toma medicina después de comer"
            },
            "french": {
                "how are you feeling": "comment vous sentez-vous?",
                "what is your problem": "quel est votre problème?",
                "take this medicine": "prenez ce médicament",
                "come back tomorrow": "revenez demain",
                "you need rest": "vous avez besoin de repos",
                "drink plenty of water": "buvez beaucoup d'eau",
                "avoid spicy food": "évitez la nourriture épicée",
                "take medicine after food": "prenez le médicament après le repas"
            },
            "german": {
                "how are you feeling": "Wie fühlen Sie sich?",
                "what is your problem": "Was ist Ihr Problem?",
                "take this medicine": "nehmen Sie diese Medizin",
                "come back tomorrow": "kommen Sie morgen wieder",
                "you need rest": "Sie brauchen Ruhe",
                "drink plenty of water": "trinken Sie viel Wasser",
                "avoid spicy food": "vermeiden Sie scharfes Essen",
                "take medicine after food": "nehmen Sie Medizin nach dem Essen"
            }
        }
    
    def translate_term(self, term, target_language):
        """Translate a medical term to target language"""
        term_lower = term.lower()
        target_lang = target_language.lower()
        
        if target_lang in self.translations:
            return self.translations[target_lang].get(term_lower, f"Translation not available for '{term}'")
        else:
            return f"Language '{target_language}' not supported"
    
    def translate_phrase(self, phrase, target_language):
        """Translate a medical phrase to target language"""
        phrase_lower = phrase.lower()
        target_lang = target_language.lower()
        
        if target_lang in self.common_phrases:
            return self.common_phrases[target_lang].get(phrase_lower, f"Translation not available for '{phrase}'")
        else:
            return f"Language '{target_language}' not supported"
    
    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def translate_prescription(self, prescription_text, target_language):
        """Translate prescription instructions"""
        # Simple word-by-word translation for demonstration
        words = prescription_text.lower().split()
        translated_words = []
        
        target_lang = target_language.lower()
        if target_lang not in self.translations:
            return f"Language '{target_language}' not supported"
        
        for word in words:
            # Remove punctuation for translation
            clean_word = word.strip('.,!?;:')
            translated = self.translations[target_lang].get(clean_word, word)
            translated_words.append(translated)
        
        return ' '.join(translated_words)
    
    def get_emergency_phrases(self, language):
        """Get emergency medical phrases in specified language"""
        emergency_phrases = {
            "hindi": [
                "मुझे डॉक्टर की जरूरत है - I need a doctor",
                "यह एक आपातकाल है - This is an emergency",
                "एम्बुलेंस बुलाएं - Call an ambulance",
                "मुझे सांस लेने में तकलीफ है - I have trouble breathing",
                "मेरे सीने में दर्द है - I have chest pain",
                "मुझे बहुत दर्द हो रहा है - I am in severe pain"
            ],
            "spanish": [
                "Necesito un médico - I need a doctor",
                "Esto es una emergencia - This is an emergency",
                "Llamen una ambulancia - Call an ambulance",
                "Tengo problemas para respirar - I have trouble breathing",
                "Tengo dolor en el pecho - I have chest pain",
                "Tengo mucho dolor - I am in severe pain"
            ],
            "french": [
                "J'ai besoin d'un médecin - I need a doctor",
                "C'est une urgence - This is an emergency",
                "Appelez une ambulance - Call an ambulance",
                "J'ai du mal à respirer - I have trouble breathing",
                "J'ai mal à la poitrine - I have chest pain",
                "J'ai très mal - I am in severe pain"
            ],
            "german": [
                "Ich brauche einen Arzt - I need a doctor",
                "Das ist ein Notfall - This is an emergency",
                "Rufen Sie einen Krankenwagen - Call an ambulance",
                "Ich habe Atemnot - I have trouble breathing",
                "Ich habe Brustschmerzen - I have chest pain",
                "Ich habe starke Schmerzen - I am in severe pain"
            ]
        }
        
        return emergency_phrases.get(language.lower(), ["Language not supported"])
