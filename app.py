
import requests

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            st.error(f"Failed to load Lottie from URL. Status code: {r.status_code}")
            return None
    except Exception as e:
        st.error(f"Exception while loading Lottie animation: {e}")
        return None


#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import bcrypt
import snowflake.connector
import requests
import time
from streamlit_lottie import st_lottie
import json
import streamlit.components.v1 as components
import base64

TOGETHER_API_KEY = ['YOUR TOGETHER_API_KEY']

# Set page configuration with wide layout
st.set_page_config(
    page_title="Wander Wise",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI with pastel colors
def load_css():
    st.markdown("""
    <style>
        /* Main theme colors - pastel palette */
        :root {
            --pastel-blue: #ABDEE6;
            --pastel-pink: #CBAACB;
            --pastel-yellow: #FFFFB5;
            --pastel-green: #CCE2CB;
            --pastel-orange: #FFCCB6;
            --background: #F8F9FD;
            --text-color: #3E4A61;
        }
        
        /* Base styling */
        body {
            background-color: var(--background);
            color: var(--text-color);
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        h1, h2, h3 {
            font-weight: 600 !important;
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(to right, var(--pastel-blue), var(--pastel-pink));
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .main-header h1 {
            font-size: 3rem !important;
            letter-spacing: 1px;
        }
        
        .subheader {
            font-size: 1.4rem !important;
            opacity: 0.9;
            margin-top: -5px;
        }
        
        /* Card styling */
        .feature-card {
            background-color: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            height: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        .feature-card h3 {
            color: var(--text-color);
            margin-bottom: 1rem;
        }
        
        .feature-card p {
            color: #6B7A99;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 25px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            border: none;
            transition: all 0.3s ease;
        }
        
        .primary-btn button {
            background: linear-gradient(to right, var(--pastel-blue), var(--pastel-pink)) !important;
            color: white !important;
        }
        
        .primary-btn button:hover {
            box-shadow: 0 5px 15px rgba(203, 170, 203, 0.4);
            transform: translateY(-2px);
        }
        
        /* Form styling */
        .auth-form {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            max-width: 400px;
            margin: 0 auto;
        }
        
        .stTextInput>div>div>input, .stSelectbox>div>div>input {
            border-radius: 10px;
            padding: 0.5rem 1rem;
            border: 1px solid #E5E9F2;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            background-color: #F1F3FA;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: var(--pastel-blue);
        }
        
        /* Flow chart node styling */
        .node {
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .node:hover {
            transform: scale(1.05);
            filter: brightness(1.1);
        }
        
        /* Animation for content transitions */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
        
        /* Content sections */
        .content-section {
            animation: fadeIn 0.6s ease forwards;
            padding: 1.5rem;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-top: 2rem;
        }
        
        /* Results section */
        .result-container {
            background-color: white;
            border-radius: 15px;
            padding: 1.5rem;
            border-left: 5px solid var(--pastel-green);
            margin-top: 1rem;
        }
        
        /* User profile section */
        .user-profile {
            background: linear-gradient(to right, var(--pastel-green), var(--pastel-blue));
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        /* Dataframe styling */
        .dataframe-container {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# Function to render Lottie animations
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set a background image
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,?");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to create animated flow chart
def create_flow_chart():
    # Interactive flowchart using HTML/CSS/JS
    flow_chart_html = """
    <div class="flowchart-container" style="height: 450px; margin: 20px auto; position: relative;">
        <svg width="100%" height="100%" viewBox="0 0 1200 400">
            <!-- Central node -->
            <g class="node central-node" id="start-node" onclick="selectNode('start')">
                <circle cx="600" cy="200" r="70" fill="url(#centralGradient)" stroke="#FFFFFF" stroke-width="3"/>
                <text x="600" y="190" text-anchor="middle" fill="white" font-size="18" font-weight="bold">Your</text>
                <text x="600" y="215" text-anchor="middle" fill="white" font-size="14">Travel Planner</text>
            </g>
            
            <!-- Cost Estimator node -->
            <g class="node" id="cost-node" onclick="selectNode('cost')">
                <circle cx="350" cy="110" r="60" fill="url(#costGradient)" stroke="#FFFFFF" stroke-width="2"/>
                <text x="350" y="105" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Cost</text>
                <text x="350" y="125" text-anchor="middle" fill="white" font-size="14">Estimator</text>
            </g>
            
            <!-- Recommendations node -->
            <g class="node" id="rec-node" onclick="selectNode('recommendations')">
                <circle cx="850" cy="110" r="60" fill="url(#recGradient)" stroke="#FFFFFF" stroke-width="2"/>
                <text x="850" y="105" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Travel</text>
                <text x="850" y="125" text-anchor="middle" fill="white" font-size="14">Recommendations</text>
            </g>
            
            <!-- Itinerary node -->
            <g class="node" id="it-node" onclick="selectNode('itinerary')">
                <circle cx="270" cy="320" r="60" fill="url(#itGradient)" stroke="#FFFFFF" stroke-width="2"/>
                <text x="270" y="315" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Itinerary</text>
                <text x="270" y="335" text-anchor="middle" fill="white" font-size="14">Generator</text>
            </g>
            
            <!-- Trip Summary node -->
            <g class="node" id="sum-node" onclick="selectNode('summary')">
                <circle cx="930" cy="320" r="60" fill="url(#sumGradient)" stroke="#FFFFFF" stroke-width="2"/>
                <text x="930" y="315" text-anchor="middle" fill="white" font-size="16" font-weight="bold">Trip</text>
                <text x="930" y="335" text-anchor="middle" fill="white" font-size="14">Summary</text>
            </g>
            
            <!-- Connector lines -->
            <path d="M 545 165 Q 600 130 655 165" stroke="#CBAACB" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            <path d="M 390 160 Q 500 250 510 160" stroke="#ABDEE6" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            <path d="M 690 160 Q 800 250 810 160" stroke="#ABDEE6" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            <path d="M 545 235 Q 600 270 655 235" stroke="#CBAACB" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            <path d="M 330 140 L 380 270" stroke="#CCE2CB" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            <path d="M 870 140 L 890 270" stroke="#CCE2CB" stroke-width="3" fill="none" stroke-dasharray="5,5"/>
            
            <!-- Gradients for nodes -->
            <defs>
                <linearGradient id="centralGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ABDEE6" />
                    <stop offset="100%" stop-color="#CBAACB" />
                </linearGradient>
                <linearGradient id="costGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFFFB5" />
                    <stop offset="100%" stop-color="#FFCCB6" />
                </linearGradient>
                <linearGradient id="recGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#CCE2CB" />
                    <stop offset="100%" stop-color="#ABDEE6" />
                </linearGradient>
                <linearGradient id="itGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFCCB6" />
                    <stop offset="100%" stop-color="#CBAACB" />
                </linearGradient>
                <linearGradient id="sumGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#CBAACB" />
                    <stop offset="100%" stop-color="#FFFFB5" />
                </linearGradient>
            </defs>
        </svg>
    </div>
    
    <script>
        function selectNode(nodeId) {
            // Send the selected node to Streamlit
            const data = {
                nodeId: nodeId
            };
            
            // Use the Streamlit component API to send the message
            if (window.parent.streamlitApp) {
                window.parent.streamlitApp.setComponentValue(data);
            }
        }
    </script>
    """
    
    # Create a unique key for the component
    key = "flowchart_component"
    
    # Return the selected node from the flow chart
    components.html(flow_chart_html, height=450)

    # Simulate node click using radio input (Streamlit-safe interaction)
    clicked_node = st.radio(
        "👇 Select a feature to navigate:",
        ["None", "Cost Estimator", "Travel Recommendations", "Itinerary Generator", "Trip Summary"],
        horizontal=True,
        key="node_selector"
    )

    section_map = {
        "Cost Estimator": "cost",
        "Travel Recommendations": "recommendations",
        "Itinerary Generator": "itinerary",
        "Trip Summary": "summary"
    }

    if clicked_node in section_map:
        st.session_state.active_section = section_map[clicked_node]
        st.rerun()

# Function to generate recommendations for a city
def generate_recommendations_for_city(city):
    prompt = f"""You are a local travel guide. Suggest for {city}:
    - 5 top places to visit
    - 3 good restaurants
    - 3 recommended hotels (budget, mid-range, luxury)
    Format clearly in bullet points. No links, no ads, just real places."""

    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 700,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        result = response.json()
        return result["output"]["choices"][0]["text"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to generate itinerary for a city
def generate_itinerary_for_city(destination, preferences, num_days=2):
    preference_text = ", ".join(preferences) if preferences else "no specific preferences"
    prompt = f"""You are a travel expert. Create a {num_days}-day itinerary for a trip to {destination}.
    Preferences: {preference_text}
    Format:
    Day 1:
    - Morning:
    - Afternoon:
    - Evening:
    (No links, just cultural and food recommendations.)"""

    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 700,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        result = response.json()
        return result["output"]["choices"][0]["text"].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Database connection functions
def get_snowflake_connection():
    return snowflake.connector.connect(
        user="VISHWAJYOTHI",
        password="********",
        account="LFUJDSM-DI50375",
        warehouse="COMPUTE_WH",
        database="TRIP_DB",
        schema="PUBLIC"
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(name, email, password):
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM USERS WHERE EMAIL = %s", (email,))
    if cur.fetchone():
        return False, "User already exists"
    hashed_pw = hash_password(password)
    cur.execute("INSERT INTO USERS (NAME, EMAIL, PASSWORD) VALUES (%s, %s, %s)", (name, email, hashed_pw))
    conn.commit()
    return True, "Registration successful!"

def authenticate_user(email, password):
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("SELECT USER_ID, NAME, PASSWORD FROM USERS WHERE EMAIL = %s", (email,))
    result = cur.fetchone()
    if result:
        user_id, name, hashed_pw = result
        if check_password(password, hashed_pw):
            return True, {"user_id": user_id, "name": name, "email": email}
    return False, None

def get_cost():
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("SELECT CITY, MEAL_COST, ACCOMODATION_COST, TRANSPORT_COST FROM DESTINATION")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["CITY", "MEAL_COST", "ACCOMODATION_COST", "TRANSPORT_COST"])
    return df

def estimate_cost(df, city, days):
    row = df[df['CITY'].str.lower() == city.lower()]
    if row.empty:
        return None
    row = row.iloc[0]
    meal = row['MEAL_COST'] * days
    accom = row['ACCOMODATION_COST'] * days
    travel = row['TRANSPORT_COST']
    total = meal + accom + travel
    return {
        "Meal Cost": meal,
        "Accommodation Cost": accom,
        "Travel Cost": travel,
        "Total Estimated Cost": total
    }

def log_prediction_to_db(user_id, destination_id, meal, accom, transport, total):
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO COST_PREDICTIONS (
            USER_ID, DESTINATION_ID, MEAL_COST, ACCOMODATION_COST, TRANSPORT_COST, TOTAL_COST
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, destination_id, meal, accom, transport, total))
    conn.commit()

# Initialize session state variables
if 'user' not in st.session_state:
    st.session_state.user = None
    
if 'active_section' not in st.session_state:
    st.session_state.active_section = "home"
    
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None
    
if 'selected_days' not in st.session_state:
    st.session_state.selected_days = 2
    
# Make sure required packages are installed
try:
    import streamlit_lottie
except ImportError:
    st.error("The streamlit_lottie package is missing. Please install it using 'pip install streamlit-lottie'")
    st.info("You may need to restart your application after installing the package.")
    st.stop()

# Load CSS
load_css()

# Main application logic
if st.session_state.user is None:
    # Login/Register Page
    st.markdown('<div class="main-header"><h1>✈️ Wander Wise</h1><p class="subheader">Plan your trips smarter with AI</p></div>', unsafe_allow_html=True)
    
    # Lottie animation for travel
    travel_lottie = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_UgZWvP.json")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st_lottie(travel_lottie, height=300, key="travel_animation")
        
    with col2:
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            st.markdown("<h3 style='text-align: center;'>Welcome Back!</h3>", unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                login_btn = st.button("Login", key="login_btn")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if login_btn:
                with st.spinner("Authenticating..."):
                    time.sleep(1)  # Simulate loading for better UX
                    success, user = authenticate_user(email, password)
                    if success:
                        st.success(f"Welcome back, {user['name']}!")
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
        
        with tab2:
            st.markdown("<h3 style='text-align: center;'>Create Account</h3>", unsafe_allow_html=True)
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                reg_btn = st.button("Register", key="reg_btn")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if reg_btn:
                with st.spinner("Creating your account..."):
                    time.sleep(1)  # Simulate loading for better UX
                    ok, msg = register_user(name, email, password)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Main application after login
    st.markdown(f'<div class="main-header"><h1>✈️Wander Wise</h1><p class="subheader">Plan your dream trip with us!</p></div>', unsafe_allow_html=True)
    
    df = get_cost()
    
    # User profile in sidebar
    with st.sidebar:
        st.markdown(f'<div class="user-profile"><h3>👋 Hello, {st.session_state.user["name"]}</h3></div>', unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.session_state.user = None
            st.session_state.active_section = "home"
            st.experimental_rerun()
    
    # Main content area
    if st.session_state.active_section == "home":
        # Welcome message
        st.markdown("<h2 style='text-align: center;'>Your AI-Powered Travel Assistant</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Your journey starts here — follow the flow!</p>", unsafe_allow_html=True)
        
        # Display the interactive flow chart
        component_value = create_flow_chart()
        
        # Handle node selection
        # Removed invalid HTML component check; not supported in components.html
        
        # Feature showcase
        st.markdown("<h3 style='text-align: center; margin-top: 40px;'>Our Features</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>💰 Cost Estimator</h3>
                <p>Get accurate travel cost estimates for your selected destination and trip duration.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🌍 Travel Recommendations</h3>
                <p>Discover the best places, restaurants, and hotels at your destination.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>🗓️ Itinerary Generator</h3>
                <p>Create personalized day-by-day itineraries based on your preferences.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="feature-card">
                <h3>📝 Trip Summary</h3>
                <p>View and manage your saved trip plans and cost estimates.</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.active_section == "cost":
        st.markdown("""
        <div class="content-section">
            <h2>💰 Trip Cost Estimator</h2>
            <p>Get an accurate estimate of your travel expenses based on destination and duration.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.session_state.selected_city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_cost")
            st.session_state.selected_days = st.number_input("Number of Days", min_value=1, value=st.session_state.selected_days, key="days_cost")
            
            if st.button("Calculate Estimated Cost", key="estimate_btn"):
                with st.spinner("Calculating your travel expenses..."):
                    time.sleep(1)  # Simulate loading for better UX
                    cost = estimate_cost(df, st.session_state.selected_city, st.session_state.selected_days)
                    if cost:
                        st.markdown('<div class="result-container">', unsafe_allow_html=True)
                        st.subheader(f"Estimated Trip Cost for {st.session_state.selected_city}")
                        
                        # Create a clean cost breakdown
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Meal Cost", f"${cost['Meal Cost']:.2f}")
                            st.metric("Accommodation Cost", f"${cost['Accommodation Cost']:.2f}")
                        
                        with col2:
                            st.metric("Travel Cost", f"${cost['Travel Cost']:.2f}")
                            st.metric("Total Estimated Cost", f"${cost['Total Estimated Cost']:.2f}", delta="")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Log to database
                        conn = get_snowflake_connection()
                        cur = conn.cursor()
                        cur.execute("SELECT DESTINATION_ID FROM DESTINATION WHERE CITY = %s", (st.session_state.selected_city,))
                        destination_row = cur.fetchone()
                        if destination_row:
                            destination_id = destination_row[0]
                            log_prediction_to_db(
                                user_id=st.session_state.user['user_id'],
                                destination_id=destination_id,
                                meal=cost["Meal Cost"],
                                accom=cost["Accommodation Cost"],
                                transport=cost["Travel Cost"],
                                total=cost["Total Estimated Cost"]
                            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Travel cost animation
            cost_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bhebjzpu.json")
            st_lottie(cost_lottie, height=250, key="cost_animation")
            
            
            st.markdown("""
            <div class="feature-card" style="margin-top:20px;">
                <h4>💡 Did You Know?</h4>
                <p>Setting a budget before travel can help you save up to 30% on your overall expenses.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
            if st.button("Back to Home", key="cost_home_btn"):
                st.session_state.active_section = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_section == "recommendations":
        st.markdown("""
        <div class="content-section">
            <h2>🌍 Travel Recommendations</h2>
            <p>Discover the best places, restaurants, and hotels at your destination.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_rec", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
            
            if st.button("Show Recommendations", key="rec_btn"):
                with st.spinner(f"Exploring {city} for the best places to visit..."):
                    recommendations = generate_recommendations_for_city(city)
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.subheader(f"🌟 Recommendations for {city}")
                    st.write(recommendations)
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Travel recommendations animation
            rec_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bhebjzpu.json")
            st_lottie(rec_lottie, height=250, key="rec_animation")
            
            st.markdown("""
            <div class="feature-card" style="margin-top:20px;">
                <h4>💡 Insider Tip</h4>
                <p>Local recommendations often lead to the most authentic experiences. Ask hotel staff for their favorite spots!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
            if st.button("Back to Home", key="rec_home_btn"):
                st.session_state.active_section = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_section == "itinerary":
        st.markdown("""
        <div class="content-section">
            <h2>🗓️ Itinerary Generator</h2>
            <p>Create a personalized day-by-day plan for your trip based on your preferences.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_it", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
            days = st.number_input("Number of Days", min_value=1, value=st.session_state.selected_days, key="days_it")
            
            preferences = st.multiselect(
                "Select Your Travel Preferences", 
                ["Cultural", "Adventure", "Foodie", "Relaxation", "Nature", "Shopping", "Nightlife"],
                key="preferences"
            )
            
            if st.button("Generate Itinerary", key="it_btn"):
                with st.spinner(f"Creating your personalized {days}-day itinerary for {city}..."):
                    time.sleep(1)  # Simulate loading for better UX
                    itinerary = generate_itinerary_for_city(city, preferences, days)
                    import re
                    formatted_itinerary = re.sub(r'- (Morning|Afternoon|Evening):', r'\n- \1:', itinerary)
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(f""" 
                    <div style='background-color:#f9f9f9; padding:2rem; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                    <h3 style='color:#333;'>🗺️ Your {days}-day Itinerary for <span style='color:#007ACC;'>{city}</span></h3>
                    <pre style='white-space:pre-wrap; font-size:1rem; font-family:monospace;'>{formatted_itinerary}</pre>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Itinerary animation
            it_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bhebjzpu.json")
            st_lottie(it_lottie, height=250, key="it_animation")
            
            st.markdown("""
            <div class="feature-card" style="margin-top:20px;">
                <h4>💡 Travel Nugget</h4>
                <p>Leave some free time in your itinerary for unexpected discoveries - sometimes the best experiences aren't planned!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
            if st.button("Back to Home", key="it_home_btn"):
                st.session_state.active_section = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.active_section == "summary":
        st.markdown("""
        <div class="content-section">
            <h2>📝 My Trip Summary</h2>
            <p>View and manage your saved trip plans and cost estimates.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fetch user's trip history
        conn = get_snowflake_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                cp.PREDICTION_ID,
                d.CITY AS DESTINATION,
                cp.MEAL_COST,
                cp.ACCOMODATION_COST,
                cp.TRANSPORT_COST,
                cp.TOTAL_COST,
            FROM COST_PREDICTIONS cp
            JOIN DESTINATION d ON cp.DESTINATION_ID = d.DESTINATION_ID
            WHERE cp.USER_ID = %s
            ORDER BY cp.PREDICTION_ID DESC
        """, (st.session_state.user['user_id'],))
        rows = cur.fetchall()
        
        if rows:
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            df_summary = pd.DataFrame(rows, columns=[
                "ID", "Destination", "Meal Cost", "Accommodation Cost", "Transport Cost", "Total Cost"
            ])
            
            # Format the costs as currency
            for col in ["Meal Cost", "Accommodation Cost", "Transport Cost", "Total Cost"]:
                df_summary[col] = df_summary[col].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(df_summary, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Summary statistics
            st.markdown("<h3 style='margin-top:30px;'>Trip Statistics</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Trips Planned", len(df_summary))
            
            with col2:
                destinations = df_summary["Destination"].nunique()
                st.metric("Unique Destinations", destinations)
            
            with col3:
                # Convert string back to float for calculation
                avg_cost = df_summary["Total Cost"].replace(r"[\$,]", "", regex=True).astype(float).mean()
                st.metric("Average Trip Cost", f"${avg_cost:.2f}")
        else:
            st.info("You haven't planned any trips yet. Use the Cost Estimator to get started!")
            
            # Sample destinations to explore
            st.markdown("<h3 style='margin-top:30px;'>Popular Destinations to Explore</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="feature-card">
                    <h4>Paris, France</h4>
                    <p>The city of lights offers iconic landmarks, world-class cuisine, and charming neighborhoods.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="feature-card">
                    <h4>Tokyo, Japan</h4>
                    <p>Experience the perfect blend of tradition and modern innovation in this vibrant metropolis.</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="feature-card">
                    <h4>New York City, USA</h4>
                    <p>The Big Apple offers incredible diversity, amazing food, and world-famous attractions.</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
            if st.button("Back to Home", key="sum_home_btn"):
                st.session_state.active_section = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
