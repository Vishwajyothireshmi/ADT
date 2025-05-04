-- Interaction SQL Queries (used in Python code) --

"👇 Select a feature to navigate:",
cur.execute("SELECT 1 FROM USERS WHERE EMAIL = %s", (email,))
cur.execute("INSERT INTO USERS (NAME, EMAIL, PASSWORD) VALUES (%s, %s, %s)", (name, email, hashed_pw))
cur.execute("SELECT USER_ID, NAME, PASSWORD FROM USERS WHERE EMAIL = %s", (email,))
cur.execute("SELECT CITY, MEAL_COST, ACCOMODATION_COST, TRANSPORT_COST FROM DESTINATION")
INSERT INTO COST_PREDICTIONS (
st.session_state.selected_city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_cost")
cur.execute("SELECT DESTINATION_ID FROM DESTINATION WHERE CITY = %s", (st.session_state.selected_city,))
city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_rec", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
city = st.selectbox("Select Destination", df['CITY'].unique(), key="destination_it", index=df['CITY'].tolist().index(st.session_state.selected_city) if st.session_state.selected_city in df['CITY'].values else 0)
"Select Your Travel Preferences",
SELECT