import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

from utils import calculate_progress, format_date
from data_manager import DataManager
from components import (
    render_goal_setting_form,
    render_progress_tracking,
    render_progress_charts,
    celebrate_completion
)

# Page config
st.set_page_config(
    page_title="Exercise Goal Tracker",
    page_icon="🏃",
    layout="wide"
)

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

# Main title
st.title("🏃 Exercise Goal Tracker")

# Sidebar for adding new goals
with st.sidebar:
    st.header("Set New Goal")
    render_goal_setting_form()

# Main content area
tab1, tab2 = st.tabs(["Track Progress", "View Statistics"])

with tab1:
    render_progress_tracking()

with tab2:
    render_progress_charts()

# Update data
st.session_state.data_manager.save_data()
