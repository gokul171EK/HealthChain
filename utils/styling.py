import streamlit as st

def add_app_styling(hide_sidebar=False, theme="Light"):
    """
    Applies custom CSS based on the selected theme.
    """
    if theme == "Dark":
        background_color = "#1E1E1E"
        card_background = "#2C2C2C"
        text_color = "#FFFFFF"
        subtle_text_color = "#AAAAAA"
        sidebar_bg = "#252525"
        button_bg = "#007bff"
        button_hover_bg = "#0056b3"
        background_pattern_fill = "%23444444"
    else: # Light theme
        background_color = "#FFFFFF"
        card_background = "#FFFFFF"
        text_color = "#000000"
        subtle_text_color = "#555555"
        sidebar_bg = "#f8f9fa"
        button_bg = "#007bff"
        button_hover_bg = "#0056b3"
        background_pattern_fill = "%23d4e6f1"

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

            /* --- General App Styling --- */
            body {{
                font-family: 'Roboto', sans-serif;
                color: {text_color};
            }}

            .stApp {{
                background-color: {background_color};
            }}

            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='{background_pattern_fill}' fill-opacity='0.4'%3E%3Cpath opacity='.5' d='M96 95h4v1h-4v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4v-9H0v-1h4V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h9V0h1v4h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9zm-1 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10 0v-9h-9v9h9zm10-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm0-10v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9z'/%3E%3Cpath d='M6 5V0h1v5h95v1H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            }}

            [data-testid="stSidebar"] {{
                background-color: {sidebar_bg};
            }}
            .st-emotion-cache-16txtl3 {{ /* Sidebar link styling */
                color: {text_color};
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: {text_color};
            }}
            .st-emotion-cache-16idsys p {{ /* Paragraph text color */
                color: {text_color};
            }}
            
            .sidebar-content {{
                padding: 1rem;
            }}
            
            .main-content {{
                padding: 2rem;
                animation: fadeIn 1s ease-in-out;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}

            .card {{
                background-color: {card_background};
                border-radius: 10px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s;
            }}
            .card:hover {{
                transform: translateY(-5px);
            }}

            /* --- Splash Screen Styling --- */
            .splash-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                width: 100%;
            }}
            .splash-title {{
                font-size: 4rem;
                font-weight: 700;
                color: #007bff;
                animation: slideIn 1.5s forwards;
            }}
            .splash-subtitle {{
                font-size: 1.5rem;
                color: {subtle_text_color};
                animation: fadeIn 2s forwards;
                animation-delay: 0.5s;
                opacity: 0;
            }}
            @keyframes slideIn {{
                from {{ transform: translateY(-50px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            
            /* --- Button Styling --- */
            div[data-testid="stButton"] > button {{
                background-color: {button_bg};
                color: white;
                border-radius: 20px;
                padding: 0.5rem 1.5rem;
                border: none;
                transition: background-color 0.3s;
            }}
            div[data-testid="stButton"] > button:hover {{
                background-color: {button_hover_bg};
            }}

            /* --- Floating SOS Button Style --- */
            .sos-button-container {{
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
            }}
            .sos-button-container button {{
                background-color: #ff4b4b !important;
                color: white !important;
                border-radius: 50% !important;
                width: 70px !important;
                height: 70px !important;
                font-size: 1rem !important;
                font-weight: bold !important;
                border: 3px solid white !important;
                box-shadow: 0 4px 12px rgba(255, 0, 0, 0.4) !important;
                animation: pulse 1.5s infinite;
            }}
            @keyframes pulse {{
                0% {{
                    box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7);
                }}
                70% {{
                    box-shadow: 0 0 0 20px rgba(255, 75, 75, 0);
                }}
                100% {{
                    box-shadow: 0 0 0 0 rgba(255, 75, 75, 0);
                }}
            }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <script>
            const streamlitDoc = window.parent.document;
            const sidebar = streamlitDoc.querySelector('[data-testid="stSidebar"]');
            sidebar.style.display = "{'none' if hide_sidebar else 'block'}";
        </script>
        """,
        unsafe_allow_html=True
    )

