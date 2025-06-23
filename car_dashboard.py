import os
import streamlit as st
import pandas as pd
import plotly.express as px
import psutil

# =============================
# Handle dynamic PORT for AWS App Runner
# =============================
def run_streamlit_on_port():
    import streamlit.web.bootstrap as bootstrap
    from streamlit.web.server import Server
    port = int(os.environ.get("PORT", 8501))
    if not Server._singleton:
        bootstrap.run(
            "car_dashboard.py",
            "",
            None,
            [],
            {},
            port=port,
        )

if __name__ == "__main__" and os.getenv("AWS_EXECUTION_ENV"):
    run_streamlit_on_port()

# =============================
# Streamlit UI Starts Here
# =============================

st.set_page_config(page_title="Car Dashboard", layout="wide")
st.title("🚗 Car Fuel Efficiency Dashboard (MPG)")
st.markdown("Built with **Streamlit** | Includes Performance Monitoring")

# Load car MPG dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
    df = pd.read_csv(url)
    df.dropna(inplace=True)
    return df

df = load_data()

# Sidebar filters
origin_options = df['origin'].unique()
selected_origin = st.sidebar.multiselect("🌍 Choose Origin", origin_options, default=origin_options)

cylinder_options = sorted(df['cylinders'].unique())
selected_cylinders = st.sidebar.multiselect("🔧 Choose Cylinders", cylinder_options, default=cylinder_options)

# Filtered dataset
df_filtered = df[(df['origin'].isin(selected_origin)) & (df['cylinders'].isin(selected_cylinders))]

# Show raw filtered data
with st.expander("📋 Show Filtered Data"):
    st.dataframe(df_filtered)

# KPI Metrics
st.subheader("📌 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg MPG", f"{df_filtered['mpg'].mean():.2f}")
col2.metric("Max Horsepower", f"{df_filtered['horsepower'].max():.0f}")
col3.metric("Total Cars", len(df_filtered))

# Data Visualizations
st.subheader("📊 Car Data Visualizations")
col4, col5 = st.columns(2)

with col4:
    fig1 = px.histogram(df_filtered, x='mpg', nbins=20, color='origin', title="MPG Distribution")
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    fig2 = px.scatter(
        df_filtered, x='horsepower', y='mpg',
        size='weight', color='origin',
        hover_name='name', title="Horsepower vs MPG (Bubble = Weight)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# Real-time system performance
st.subheader("🖥️ System Performance Monitor")
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory()
st.write(f"**CPU Usage:** {cpu}%")
st.write(f"**Memory Usage:** {mem.percent}%")

# Live CPU trend chart
st.line_chart([psutil.cpu_percent(interval=0.3) for _ in range(20)])
