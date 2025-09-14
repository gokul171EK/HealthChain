import streamlit as st

def add_app_styling():
    """Adds custom CSS for the main application."""
    st.markdown(r"""
        <style>
            /* --- General Styling & Background --- */
            .stApp {
                background-color: #e9eef7;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%23d1d8e8' fill-opacity='0.4'%3E%3Cpath opacity='.5' d='M96 95h4v1h-4v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4h-9v4h-1v-4H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15v-9H0v-1h15V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h9V0h1v15h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9zm-1 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10 0v-9h-9v9h9zm-10-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm-90-10h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9zm10 0h9v-9h-9v9z'/%3E%3Cpath d='M6 5V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h9V0h1v5h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1h-4v9h4v1H6v-1H5v-9H0v-1h5v-9H0v-1h5v-9H0v-1h5v-9H0v-1h5v-9H0v-1h5v-9H0v-1h5v-9H0v-1h5V5h1zM5 5v9h9V5H5zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zm10 0v9h9V5h-9zM5 15v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 25v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 35v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 45v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 55v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 65v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 75v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zM5 85v9h9v-9H5zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9zm10 0v9h9v-9h-9z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            }

            /* --- Animations --- */
            @keyframes fadeInUp {
                from {
                    transform: translate3d(0, 40px, 0);
                    opacity: 0;
                }
                to {
                    transform: translate3d(0, 0, 0);
                    opacity: 1;
                }
            }

            /* --- Component Styling --- */
            .content-container {
                animation: fadeInUp 1s ease-out;
            }

            .card {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.05);
                margin-bottom: 1.5rem;
                transition: transform 0.3s ease-in-out;
            }
            .card:hover {
                transform: translateY(-5px);
            }

            h1, h2, h3 {
                color: #0d2a4d;
            }

            .stButton>button {
                border-radius: 20px;
                border: 2px solid #0068C9;
                background-color: #0068C9;
                color: white;
                font-weight: bold;
                transition: all 0.3s;
                padding: 10px 20px;
            }
            .stButton>button:hover {
                background-color: #0052A0;
                color: white;
                border-color: #0052A0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transform: scale(1.05);
            }
        /* --- CSS for Emergency Page Alignment --- */
        .header-row > div[data-testid="stHorizontalBlock"] {
               align-items: baseline;
            }
        .contact-row {
               display: flex;
               align-items: center;
               padding: 10px 0;
            }
        .contact-divider {
                border-top: 1px solid #e0e0e0;
                margin-top: 0;
                margin-bottom: 10px;
            }
                        </style>
                """, unsafe_allow_html=True)
                