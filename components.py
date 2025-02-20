import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from utils import calculate_progress, get_date_range, validate_input


def render_goal_setting_form():
    """Render the goal setting form"""
    with st.form("goal_setting"):
        exercise_name = st.text_input("Exercise Name",
                                      placeholder="e.g., Push-ups")
        target_quantity = st.number_input("Target Quantity",
                                          min_value=1,
                                          value=100)
        duration_days = st.selectbox("Duration (days)",
                                     options=[30, 60, 90, 120, 180, 365],
                                     format_func=lambda x: f"{x} days")
        start_date = st.date_input("Start Date", datetime.now())

        submitted = st.form_submit_button("Set Goal")

        if submitted:
            valid, message = validate_input(exercise_name, target_quantity,
                                            duration_days)
            if valid:
                st.session_state.data_manager.add_goal(exercise_name,
                                                       target_quantity,
                                                       start_date,
                                                       duration_days)
                st.success(f"Goal set for {exercise_name}!")
                # Hide form after successful submission
                st.session_state.show_goal_form = False
                # Clear form inputs
                if "form_submitted" not in st.session_state:
                    st.session_state.form_submitted = True
                st.rerun()
            else:
                st.error(message)


def render_progress_tracking():
    """Render the progress tracking section"""
    active_goals = st.session_state.data_manager.get_active_goals()

    if active_goals.empty:
        st.info("No active goals. Set a new goal to start tracking!")
        return

    for _, goal in active_goals.iterrows():
        exercise = goal['exercise']
        target = goal['target']
        start_date = goal['start_date']
        duration_days = goal['duration_days']

        st.subheader(f"🎯 {exercise}")

        col1, col2 = st.columns(2)

        with col1:
            progress = st.session_state.data_manager.get_progress(exercise)
            total_done = progress['quantity'].sum()
            progress_pct = calculate_progress(total_done, target)

            # Custom progress bar with tick marks
            progress_html = f"""
                <div style="
                    width: 100%;
                    height: 30px;
                    background-color: #f0f2f6;
                    border-radius: 10px;
                    position: relative;
                    margin: 10px 0;
                ">
                    <div style="
                        width: {min(progress_pct, 100)}%;
                        height: 100%;
                        background-color: #FF4B4B;
                        border-radius: 10px;
                        transition: width 0.5s ease-in-out;
                    "></div>
                    {''.join([f'<div style="position: absolute; top: 50%; left: {i}%; transform: translate(-50%, -50%); color: {"white" if i <= progress_pct else "#262730"}; font-size: 14px; font-weight: bold;">|</div>' for i in range(10, 91, 10)])}
                </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

            # Progress metrics below the bar
            st.metric("Progress",
                      f"{total_done}/{target} ({progress_pct:.1f}%)")

            if progress_pct >= 100:
                celebrate_completion(exercise)

        with col2:
            today = datetime.now().date()
            quantity = st.number_input(f"Add today's {exercise}",
                                       min_value=0,
                                       value=0,
                                       key=f"input_{exercise}")

            if st.button(f"Log Progress", key=f"log_{exercise}"):
                st.session_state.data_manager.add_progress(
                    exercise, today, quantity)
                st.success("Progress logged!")
                st.rerun()


def render_progress_charts():
    """Render progress visualization charts"""
    active_goals = st.session_state.data_manager.get_active_goals()

    if active_goals.empty:
        st.info("No active goals to display statistics.")
        return

    for _, goal in active_goals.iterrows():
        exercise = goal['exercise']
        progress = st.session_state.data_manager.get_progress(exercise)

        if not progress.empty:
            # Daily progress chart
            fig_daily = px.bar(progress,
                               x='date',
                               y='quantity',
                               title=f"Daily {exercise} Progress")
            st.plotly_chart(fig_daily, use_container_width=True)

            # Cumulative progress chart
            progress['cumulative'] = progress['quantity'].cumsum()
            fig_cumulative = px.line(progress,
                                     x='date',
                                     y='cumulative',
                                     title=f"Cumulative {exercise} Progress")
            fig_cumulative.add_hline(y=goal['target'],
                                     line_dash="dash",
                                     annotation_text="Target")
            st.plotly_chart(fig_cumulative, use_container_width=True)


def celebrate_completion(exercise):
    """Display celebration message for completed goals"""
    st.balloons()
    st.success(f"🎉 Congratulations! You've achieved your {exercise} goal!")
    if st.button("Mark as Complete", key=f"complete_{exercise}"):
        st.session_state.data_manager.mark_goal_complete(exercise)
        st.rerun()
