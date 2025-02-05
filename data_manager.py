import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models import Goal, Progress, get_db
from typing import Iterator, Optional
import streamlit as st

class DataManager:
    def __init__(self):
        """Initialize DataManager with database connection"""
        try:
            self.db: Iterator[Session] = get_db()
            self.session = next(self.db)
        except Exception as e:
            st.error(f"Failed to connect to database: {str(e)}")
            raise

    def add_goal(self, exercise: str, target: int, start_date: datetime.date, duration_days: int) -> None:
        """Add a new exercise goal"""
        try:
            new_goal = Goal(
                exercise=exercise,
                target=target,
                start_date=start_date,
                duration_days=duration_days,
                completed=False
            )
            self.session.add(new_goal)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add goal: {str(e)}")

    def add_progress(self, exercise: str, date: datetime.date, quantity: int) -> None:
        """Add progress entry for an exercise"""
        try:
            new_progress = Progress(
                exercise=exercise,
                date=date,
                quantity=quantity
            )
            self.session.add(new_progress)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to add progress: {str(e)}")

    def get_goal(self, exercise: str) -> Optional[Goal]:
        """Get goal details for an exercise"""
        try:
            return self.session.query(Goal).filter(Goal.exercise == exercise).first()
        except Exception as e:
            st.error(f"Failed to get goal: {str(e)}")
            return None

    def get_progress(self, exercise: str) -> pd.DataFrame:
        """Get progress for an exercise"""
        try:
            progress = self.session.query(Progress).filter(Progress.exercise == exercise).all()
            if not progress:
                return pd.DataFrame(columns=['exercise', 'date', 'quantity'])

            return pd.DataFrame([
                {'exercise': p.exercise, 'date': p.date, 'quantity': p.quantity}
                for p in progress
            ])
        except Exception as e:
            st.error(f"Failed to get progress: {str(e)}")
            return pd.DataFrame(columns=['exercise', 'date', 'quantity'])

    def get_active_goals(self) -> pd.DataFrame:
        """Get list of active goals"""
        try:
            goals = self.session.query(Goal).filter(Goal.completed == False).all()
            if not goals:
                return pd.DataFrame(columns=['exercise', 'target', 'start_date', 'duration_days', 'completed'])

            return pd.DataFrame([
                {
                    'exercise': g.exercise,
                    'target': g.target,
                    'start_date': g.start_date,
                    'duration_days': g.duration_days,
                    'completed': g.completed
                }
                for g in goals
            ])
        except Exception as e:
            st.error(f"Failed to get active goals: {str(e)}")
            return pd.DataFrame(columns=['exercise', 'target', 'start_date', 'duration_days', 'completed'])

    def mark_goal_complete(self, exercise: str) -> None:
        """Mark a goal as completed"""
        try:
            goal = self.session.query(Goal).filter(Goal.exercise == exercise).first()
            if goal:
                goal.completed = True
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to mark goal as complete: {str(e)}")

    def save_data(self) -> None:
        """Commit any pending changes to the database"""
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to save data: {str(e)}")