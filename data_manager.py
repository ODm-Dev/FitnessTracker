import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import os

class DataManager:
    def __init__(self):
        """Initialize DataManager with goals and progress DataFrames"""
        if 'goals_df' not in st.session_state:
            st.session_state.goals_df = pd.DataFrame(
                columns=['exercise', 'target', 'start_date', 'duration_days', 'completed']
            )
        if 'progress_df' not in st.session_state:
            st.session_state.progress_df = pd.DataFrame(
                columns=['exercise', 'date', 'quantity']
            )
        
    def add_goal(self, exercise, target, start_date, duration_days):
        """Add a new exercise goal"""
        new_goal = pd.DataFrame({
            'exercise': [exercise],
            'target': [target],
            'start_date': [start_date],
            'duration_days': [duration_days],
            'completed': [False]
        })
        st.session_state.goals_df = pd.concat([st.session_state.goals_df, new_goal], ignore_index=True)

    def add_progress(self, exercise, date, quantity):
        """Add progress entry for an exercise"""
        new_progress = pd.DataFrame({
            'exercise': [exercise],
            'date': [date],
            'quantity': [quantity]
        })
        st.session_state.progress_df = pd.concat([st.session_state.progress_df, new_progress], ignore_index=True)

    def get_goal(self, exercise):
        """Get goal details for an exercise"""
        goal = st.session_state.goals_df[st.session_state.goals_df['exercise'] == exercise]
        return goal.iloc[0] if not goal.empty else None

    def get_progress(self, exercise):
        """Get progress for an exercise"""
        return st.session_state.progress_df[st.session_state.progress_df['exercise'] == exercise]

    def get_active_goals(self):
        """Get list of active goals"""
        return st.session_state.goals_df[~st.session_state.goals_df['completed']]

    def mark_goal_complete(self, exercise):
        """Mark a goal as completed"""
        idx = st.session_state.goals_df.index[st.session_state.goals_df['exercise'] == exercise]
        st.session_state.goals_df.loc[idx, 'completed'] = True

    def save_data(self):
        """Save data to session state"""
        # Data is automatically saved in session state
        pass
