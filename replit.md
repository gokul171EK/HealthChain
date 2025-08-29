# HEALTHTECH - Complete Healthcare Solution

## Overview

HEALTHTECH is a comprehensive healthcare platform built with Streamlit that provides a complete digital healthcare ecosystem. The application offers multiple healthcare services including blood and organ donation management, AI-powered health assistance, virtual consultations, fitness tracking, emergency services, health record management, pharmacy services, health education, and mental health support. The platform serves as a one-stop solution for users to manage their healthcare needs digitally, connecting patients with healthcare providers and facilitating various medical services through an intuitive web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with multi-page navigation
- **Page Structure**: Modular design with dedicated pages for each healthcare service (10 main service pages)
- **UI Components**: Plotly for data visualization, Folium for map-based features, and custom Streamlit components
- **State Management**: Session-based state management for user authentication and data persistence
- **Navigation**: Tab-based interface within each service page for organized feature access

### Backend Architecture
- **Application Layer**: Python-based business logic with utility modules for core functionality
- **Data Management**: CSV-based data storage with pandas for data manipulation and management
- **Authentication**: Simple hash-based authentication system with password hashing using SHA256
- **Session Management**: Streamlit session state for maintaining user context across pages

### Core Utility Modules
- **DataManager**: Handles all data operations including user management, CRUD operations for health records, appointments, and various healthcare data
- **AISimulator**: Provides AI-powered features including symptom checking, health predictions, and medical recommendations
- **MedicalTranslator**: Multilingual support for medical terms and content translation (currently supporting Hindi)

### Data Storage Architecture
- **Storage Type**: File-based CSV storage system
- **Data Organization**: Separate CSV files for different data entities (users, health records, appointments, blood donors, etc.)
- **Data Models**: Structured data schemas for users, medical records, appointments, blood/organ donation data, pharmacy information, and community features

### Service Modules
- **Blood Donation**: Donor registration, recipient matching, blood bank management
- **Organ Donation**: Organ donor registration, compatibility checking, recipient management
- **AI Health Assistant**: Symptom analysis, health predictions, medical information lookup
- **Virtual Consultations**: Doctor appointment booking, consultation management
- **Fitness Tracking**: Health metrics monitoring, activity tracking, goal management
- **Emergency Services**: Emergency contact management, hospital locator, crisis support
- **Health Records**: Medical history management, health trend analysis
- **Pharmacy Services**: Pharmacy locator, medication management, prescription handling
- **Health Education**: Educational content management, health assessments
- **Mental Health**: Mental wellness tracking, stress management, crisis support resources

## External Dependencies

### Core Framework Dependencies
- **Streamlit**: Web application framework for the entire frontend interface
- **Pandas**: Data manipulation and analysis for all healthcare data processing
- **Plotly (Express & Graph Objects)**: Interactive data visualization for health analytics and reporting
- **Folium**: Map visualization for location-based services (hospitals, pharmacies, blood banks)
- **NumPy**: Numerical computing for health data analysis and calculations

### Python Standard Libraries
- **datetime**: Date and time operations for appointments, health records, and scheduling
- **os**: File system operations for data management
- **hashlib**: Password hashing and security features
- **uuid**: Unique identifier generation for records and users
- **random**: Data simulation and AI prediction features

### Streamlit Extensions
- **streamlit-folium**: Integration between Streamlit and Folium for map-based features
- **@st.cache_resource**: Caching decorator for performance optimization of resource-intensive operations

### Data Storage
- **CSV Files**: Primary data storage mechanism for all application data
- **File System**: Local file-based storage for user data, medical records, and application state

Note: The application currently uses CSV-based storage but is architected in a way that would allow easy migration to a proper database system like PostgreSQL in the future.