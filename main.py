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
if 'show_goal_form' not in st.session_state:
    st.session_state.show_goal_form = False

# Main title
st.title("🏃 Exercise Goal Tracker")

# Check if there are active goals
active_goals = st.session_state.data_manager.get_active_goals()
has_active_goals = not active_goals.empty

# Main content area
if not has_active_goals:
    st.info("Welcome! Start by setting your first exercise goal.")
    render_goal_setting_form()
else:
    # Add button to show/hide goal form
    if st.button("➕ Add New Goal"):
        st.session_state.show_goal_form = not st.session_state.show_goal_form

    # Show goal form if requested
    if st.session_state.show_goal_form:
        with st.expander("Set New Goal", expanded=True):
            render_goal_setting_form()
            if st.button("Close"):
                st.session_state.show_goal_form = False

    # Tabs for tracking and stats
    tab1, tab2 = st.tabs(["Track Progress", "View Statistics"])

    with tab1:
        render_progress_tracking()

    with tab2:
        render_progress_charts()

# Update data
st.session_state.data_manager.save_data()