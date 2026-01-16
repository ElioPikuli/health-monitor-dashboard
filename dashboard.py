import streamlit as st
import sqlite3
import pandas as pd
import time
import os

# Configuration
DB_NAME = os.getenv("DB_FILE", "health_monitor.db")
st.set_page_config(page_title="Home Lab Health Monitor", layout="wide")

def load_data():
    """Load data from SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        # Read the last 2000 records
        df = pd.read_sql_query("SELECT * FROM uptracking ORDER BY timestamp DESC LIMIT 2000", conn)
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

# Title
st.title("🛡️ Home Lab Health Monitor")
st.write("Real-time monitoring of website uptime and latency.")

# Refresh Button
if st.button("Refresh Now"):
    st.rerun()

# Load Data
df = load_data()

if df.empty:
    st.warning("No data available yet. Please run monitor.py first.")
else:
    # --- KPI Section ---
    st.subheader("Key Performance Indicators (KPIs)")
    
    # Filter for valid latency measurements
    valid_pings = df[df['latency_ms'].notna()]
    
    # 1. Slowest Site
    if not valid_pings.empty:
        # Group by URL and calculate mean latency
        avg_latencies = valid_pings.groupby('url')['latency_ms'].mean()
        slowest_site_url = avg_latencies.idxmax()
        slowest_site_val = avg_latencies.max()
        slowest_site_formatted = f"{slowest_site_url} ({slowest_site_val:.1f}ms)"
    else:
        slowest_site_formatted = "N/A"

    # 2. Avg Latency (Global)
    if not valid_pings.empty:
        global_avg = valid_pings['latency_ms'].mean()
        avg_latency_formatted = f"{global_avg:.1f} ms"
    else:
        avg_latency_formatted = "0 ms"

    # 3. Total Pings
    total_pings = len(df)
    
    # Display Metrics in Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Slowest Site (Avg)", value=slowest_site_formatted)
        
    with col2:
        st.metric(label="Global Avg Latency", value=avg_latency_formatted)
        
    with col3:
        st.metric(label="Total Pings Logged", value=total_pings)
        
    st.markdown("---") # Divider

    # --- Visualization Section ---
    st.subheader("Latency Over Time")
    
    if not valid_pings.empty:
        st.line_chart(
            valid_pings,
            x='timestamp',
            y='latency_ms',
            color='url'
        )
    else:
        st.info("No latency data to display.")
    
    st.markdown("---") # Divider

    # --- Current Status Section ---
    st.subheader("Latest Status by Site")
    latest_time = df['timestamp'].max()
    latest_df = df[df['timestamp'] == latest_time]
    
    cols = st.columns(len(latest_df))
    for idx, (index, row) in enumerate(latest_df.iterrows()):
        # Handle cases where there might be more rows than columns
        if idx < len(cols): 
            with cols[idx]:
                status_color = "green" if row['status_code'] == 200 else "red"
                st.markdown(f"**{row['url']}**")
                if row['error']:
                    st.markdown(f":red[DOWN] ({row['error']})")
                else:
                    st.metric(label="Latency", value=f"{row['latency_ms']:.0f} ms", delta=None)
                    st.markdown(f":{status_color}[Status: {row['status_code']}]")

    st.subheader("Recent Raw Data")
    st.dataframe(df.head(50), use_container_width=True)
