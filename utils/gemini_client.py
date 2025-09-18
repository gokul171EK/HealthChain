import streamlit as st
import google.generativeai as genai

def get_gemini_response(prompt: str):
    """
    Sends a prompt to the Gemini API and returns the response.

    Args:
        prompt (str): The text prompt to send to the model.

    Returns:
        str: The generated text response from the model.
    """
    try:
        # Configure the Gemini API with the key from st.secrets
        # This will work both locally and when deployed.
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: Gemini API key not found. Please configure it in your secrets."
            
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content(prompt)
        
        return response.text

    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I am unable to process your request at the moment."
