import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="sportsradar"
    )

def query_df(sql):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

# Set up Streamlit page
st.set_page_config(layout="wide")
st.title("🎾 Tennis Rankings Dashboard")

# --- Overview Section ---
st.subheader("📊 Overview")
col1, col2, col3, col4 = st.columns(4)

# Metrics
with col1:
    total_comp = query_df("SELECT COUNT(*) AS total FROM Competitors")
    st.metric("Total Competitors", int(total_comp.iloc[0]['total']))

with col2:
    total_competitions = query_df("SELECT COUNT(DISTINCT competition_name) AS total FROM competitions;")
    st.metric("Total Competitions", int(total_competitions.iloc[0]['total']))

with col3:
    countries = query_df("SELECT COUNT(DISTINCT country) AS countries FROM Competitors")
    st.metric("Countries Represented", int(countries.iloc[0]['countries']))

with col4:
    top_score = query_df("SELECT MAX(points) AS max_points FROM Rankings")
    st.metric("Highest Points", int(top_score.iloc[0]['max_points']))

# --- 2. Filter/Search Panel ---
st.sidebar.header("🔍 Filter Competitors")
name_filter = st.sidebar.text_input("Search by name")
country_filter = st.sidebar.selectbox("Select Country", ["All"] + query_df("SELECT DISTINCT country FROM Competitors ORDER BY country ASC")['country'].tolist())
rank_range = st.sidebar.slider("Rank Range", 1, 100, (1, 10))
min_points = st.sidebar.slider("Minimum Points", 0, 10000, 1000)

query = f"""
SELECT c.name, c.country, r.rank, r.points, r.movement, r.competitions_played
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
WHERE r.rank BETWEEN {rank_range[0]} AND {rank_range[1]} AND r.points >= {min_points}
"""
if name_filter:
    query += f" AND c.name LIKE '%{name_filter}%'"
if country_filter != "All":
    query += f" AND c.country = '{country_filter}'"

st.subheader("📋 Filtered Competitors")
st.dataframe(query_df(query))

# --- 3. Venues by Country ---
st.subheader("🏟️ Venues by Country")
col_input, col_clear = st.columns([4, 1])

if "venue_input" not in st.session_state:
    st.session_state.venue_input = ""

# Define a function to clear the input
def clear_venue_input():
    st.session_state.venue_input = ""

# Input field
with col_input:
    venue_country = st.text_input(
        "Enter a country name to see its venues (e.g., Chile)", 
        key="venue_input"
    )

# Clear button uses callback
with col_clear:
    st.button("❌", on_click=clear_venue_input)

# Query and display if there's input
if st.session_state.venue_input:
    venue_df = query_df(f"""
        SELECT venue_name, timezone, country_name FROM venues
        WHERE country_name = '{st.session_state.venue_input}'
    """)
    if not venue_df.empty:
        st.dataframe(venue_df)
    else:
        st.warning("No venues found for the given country.")

# --- 4. Country Analysis ---
st.subheader("🌍 Country Analysis")
country_stats = query_df("""
SELECT c.country, COUNT(*) AS competitors, AVG(r.points) AS avg_points
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY competitors DESC
""")

# Country Analysis Bar Plots
bar1, bar2 = st.columns(2)

with bar1:
    fig1 = px.bar(country_stats, x='country', y='competitors', title='Competitors per Country')
    st.plotly_chart(fig1, use_container_width=True)

with bar2:
    fig2 = px.bar(country_stats, x='country', y='avg_points', title='Average Points per Country')
    st.plotly_chart(fig2, use_container_width=True)

# --- 5. Leaderboards ---
st.subheader("🏆 Leaderboards")
lead_tab = st.tabs(["Top Rank", "Top Points", "Top Movement"])

with lead_tab[0]:
    top_ranked = query_df("""
    SELECT c.name, r.rank, r.points, r.movement
    FROM Competitors c
    JOIN Rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.rank ASC
    LIMIT 10;
    """)
    st.dataframe(top_ranked)

with lead_tab[1]:
    top_points = query_df("""
    SELECT c.name, r.rank, r.points, r.movement
    FROM Competitors c
    JOIN Rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.points DESC
    LIMIT 10;
    """)
    st.dataframe(top_points)

with lead_tab[2]:
    top_movement = query_df("""
    SELECT c.name, r.rank, r.points, r.movement
    FROM Competitors c
    JOIN Rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.movement DESC
    LIMIT 10;
    """)
    st.dataframe(top_movement)

# --- 6. Dynamic Sorting for Leaderboards ---
sort_by = st.selectbox("Sort Leaderboards by", ["Rank", "Points", "Movement"])
query_leaderboard = f"""
SELECT c.name, r.rank, r.points, r.movement
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
ORDER BY r.{sort_by} DESC
LIMIT 10;
"""
leaderboard_df = query_df(query_leaderboard)
st.subheader(f"🏆 Top 10 by {sort_by}")
st.dataframe(leaderboard_df)

