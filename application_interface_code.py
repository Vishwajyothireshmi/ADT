# --- Application Interface Code (Streamlit + UI Elements) ---

st.error(f"Failed to load Lottie from URL. Status code: {r.status_code}")
st.error(f"Exception while loading Lottie animation: {e}")
import streamlit as st
import snowflake.connector
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
st.set_page_config(
st.markdown("""
st.markdown(page_bg_img, unsafe_allow_html=True)
if (window.parent.streamlitApp) {
window.parent.streamlitApp.setComponentValue(data);
components.html(flow_chart_html, height=450)
clicked_node = st.radio(
st.session_state.active_section = section_map[clicked_node]
st.rerun()
return snowflake.connector.connect(
if 'user' not in st.session_state:
st.session_state.user = None
if 'active_section' not in st.session_state:
st.session_state.active_section = "home"
if 'selected_city' not in st.session_state:
st.session_state.selected_city = None
if 'selected_days' not in st.session_state:
st.session_state.selected_days = 2
import streamlit_lottie
st.error("The streamlit_lottie package is missing. Please install it using 'pip install streamlit-lottie'")
st.info("You may need to restart your application after installing the package.")
st.stop()
if st.session_state.user is None:
st.markdown('<div class="main-header"><h1>✈️ Wander Wise</h1><p class="subheader">Plan your trips smarter with AI</p></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
st_lottie(travel_lottie, height=300, key="travel_animation")
st.markdown('<div class="auth-form">', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
st.markdown("<h3 style='text-align: center;'>Welcome Back!</h3>", unsafe_allow_html=True)
email = st.text_input("Email", key="login_email")
password = st.text_input("Password", type="password", key="login_password")
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
login_btn = st.button("Login", key="login_btn")
st.markdown('</div>', unsafe_allow_html=True)
with st.spinner("Authenticating..."):
st.success(f"Welcome back, {user['name']}!")
st.session_state.user = user
st.rerun()
st.error("Invalid email or password")
st.markdown("<h3 style='text-align: center;'>Create Account</h3>", unsafe_allow_html=True)
name = st.text_input("Full Name", key="reg_name")
email = st.text_input("Email", key="reg_email")
password = st.text_input("Password", type="password", key="reg_pass")
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
reg_btn = st.button("Register", key="reg_btn")
st.markdown('</div>', unsafe_allow_html=True)
with st.spinner("Creating your account..."):
st.success(msg)
st.error(msg)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-header"><h1>✈️Wander Wise</h1><p class="subheader">Plan your dream trip with us!</p></div>', unsafe_allow_html=True)
with st.sidebar:
st.markdown(f'<div class="user-profile"><h3>👋 Hello, {st.session_state.user["name"]}</h3></div>', unsafe_allow_html=True)
if st.button("Logout", key="logout_btn"):
st.session_state.user = None
st.session_state.active_section = "home"
st.experimental_rerun()
if st.session_state.active_section == "home":
st.markdown("<h2 style='text-align: center;'>Your AI-Powered Travel Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Your journey starts here — follow the flow!</p>", unsafe_allow_html=True)
# Removed invalid HTML component check; not supported in components.html
st.markdown("<h3 style='text-align: center; margin-top: 40px;'>Our Features</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
st.markdown("""
st.markdown("""
st.markdown("""
st.markdown("""
elif st.session_state.active_section == "cost":
st.markdown("""
col1, col2 = st.columns([2, 1])
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
st.session_state.selected_city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_cost")
st.session_state.selected_days = st.number_input("Number of Days", min_value=1, value=st.session_state.selected_days, key="days_cost")
if st.button("Calculate Estimated Cost", key="estimate_btn"):
with st.spinner("Calculating your travel expenses..."):
cost = estimate_cost(df, st.session_state.selected_city, st.session_state.selected_days)
st.markdown('<div class="result-container">', unsafe_allow_html=True)
st.subheader(f"Estimated Trip Cost for {st.session_state.selected_city}")
col1, col2 = st.columns(2)
st.metric("Meal Cost", f"${cost['Meal Cost']:.2f}")
st.metric("Accommodation Cost", f"${cost['Accommodation Cost']:.2f}")
st.metric("Travel Cost", f"${cost['Travel Cost']:.2f}")
st.metric("Total Estimated Cost", f"${cost['Total Estimated Cost']:.2f}", delta="")
st.markdown('</div>', unsafe_allow_html=True)
cur.execute("SELECT DESTINATION_ID FROM DESTINATION WHERE CITY = %s", (st.session_state.selected_city,))
user_id=st.session_state.user['user_id'],
st.markdown('</div>', unsafe_allow_html=True)
cost_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bhebjzpu.json")
st_lottie(cost_lottie, height=250, key="cost_animation")
st.markdown("""
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
if st.button("Back to Home", key="cost_home_btn"):
st.session_state.active_section = "home"
st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.active_section == "recommendations":
st.markdown("""
col1, col2 = st.columns([2, 1])
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_rec", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
if st.button("Show Recommendations", key="rec_btn"):
with st.spinner(f"Exploring {city} for the best places to visit..."):
st.markdown('<div class="result-container">', unsafe_allow_html=True)
st.subheader(f"🌟 Recommendations for {city}")
st.write(recommendations)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st_lottie(rec_lottie, height=250, key="rec_animation")
st.markdown("""
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
if st.button("Back to Home", key="rec_home_btn"):
st.session_state.active_section = "home"
st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.active_section == "itinerary":
st.markdown("""
col1, col2 = st.columns([2, 1])
st.markdown('<div class="feature-card">', unsafe_allow_html=True)
city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_it", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
days = st.number_input("Number of Days", min_value=1, value=st.session_state.selected_days, key="days_it")
preferences = st.multiselect(
if st.button("Generate Itinerary", key="it_btn"):
with st.spinner(f"Creating your personalized {days}-day itinerary for {city}..."):
st.markdown('<div class="result-container">', unsafe_allow_html=True)
st.markdown(f"""
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st_lottie(it_lottie, height=250, key="it_animation")
st.markdown("""
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
if st.button("Back to Home", key="it_home_btn"):
st.session_state.active_section = "home"
st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.active_section == "summary":
st.markdown("""
""", (st.session_state.user['user_id'],))
st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
st.dataframe(df_summary, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:30px;'>Trip Statistics</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
st.metric("Total Trips Planned", len(df_summary))
st.metric("Unique Destinations", destinations)
st.metric("Average Trip Cost", f"${avg_cost:.2f}")
st.info("You haven't planned any trips yet. Use the Cost Estimator to get started!")
st.markdown("<h3 style='margin-top:30px;'>Popular Destinations to Explore</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
st.markdown("""
st.markdown("""
st.markdown("""
col1, col2, col3 = st.columns([1, 2, 1])
st.markdown('<div class="primary-btn" style="text-align:center; margin-top:30px;">', unsafe_allow_html=True)
if st.button("Back to Home", key="sum_home_btn"):
st.session_state.active_section = "home"
st.rerun()
st.markdown('</div>', unsafe_allow_html=True)