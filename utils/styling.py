import streamlit as st

def add_app_styling(hide_sidebar=False, theme="light"):
    """
    Apply custom styling to the Streamlit app.
    Supports optional sidebar hiding and dark/light theme.
    """

    # --- Base CSS ---
    st.markdown(
        """
        <style>
        /* --- Global Styling --- */
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* --- Sidebar Styling --- */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            padding: 20px;
            border-right: 2px solid #eaeaea;
        }

        /* Sidebar Title */
        section[data-testid="stSidebar"] .css-1d391kg {
            font-size: 20px;
            font-weight: 700;
            color: #007bff;
        }

        /* --- Button Styling --- */
        div.stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }

        /* --- Card Styling --- */
        .card {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 15px 0;
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 6px 16px rgba(0,0,0,0.15);
        }

        /* --- Splash Screen Styling --- */
        .splash-container {
            position: fixed;
            top: 0; left: 0;
            height: 100vh;
            width: 100vw;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #ffffff;
            z-index: 9999; /* Stays above everything */
        }

        .splash-title {
            font-size: 4rem;
            font-weight: 800;
            color: #007bff;
            letter-spacing: 2px;
            animation: zoomFade 1.5s ease-out forwards;
        }

        .splash-subtitle {
            font-size: 1.5rem;
            color: #6c757d;
            animation: fadeInUp 2s ease forwards;
            animation-delay: 0.7s;
            opacity: 0;
        }

        @keyframes zoomFade {
            from { transform: scale(0.8); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        @keyframes fadeInUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Hide Sidebar Option ---
    if hide_sidebar:
        st.markdown(
            """
            <style>
            section[data-testid="stSidebar"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True
        )

    # --- Dark Theme Option ---
    if theme == "dark":
        st.markdown(
            """
            <style>
            body {
                background-color: #121212 !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


def splash_screen():
    """ Show splash screen for 3 seconds """
    st.markdown(
        """
        <div class="splash-container" id="splash">
            <div class="splash-title">HEALTHTECH</div>
            <div class="splash-subtitle">Empowering Your Health Journey</div>
        </div>

        <script>
        setTimeout(function(){
            var splash = document.getElementById("splash");
            if (splash) {
                splash.style.display = "none";
            }
        }, 3000); /* Hides splash after 3s */
        </script>
        """,
        unsafe_allow_html=True
    )
