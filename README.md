# Wander Wise 🌍✈️
**A Smart AI-Powered Travel Planner**  
Built with Streamlit, Snowflake, and Together AI API.

## Features
- 💰 Cost Estimator
- 🌍 Travel Recommendations (AI-powered)
- 🗓️ Itinerary Generator (AI-powered)
- 📝 Trip Summary & History
- 🔐 Secure Login/Register

## Tech Stack
- Frontend: Python + Streamlit
- Backend: Snowflake Cloud Database
- AI: Together API (Mistral-7B-Instruct)
- Authentication: bcrypt

## Raw Content
- `Travel_Cost-3.csv`: Contains city-wise cost estimates for meals, accommodation, and transport.

## Database
- `db_schema.sql`: Snowflake table schema for USERS, DESTINATION, and COST_PREDICTIONS.

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run TRAVEL.py
```
