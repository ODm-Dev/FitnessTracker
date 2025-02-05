import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models import Goal, Progress, get_db
from typing import Iterator

class DataManager:
    def __init__(self):
        """Initialize DataManager with database connection"""
        self.db: Iterator[Session] = get_db()
        self.session = next(self.db)

    def add_goal(self, exercise: str, target: int, start_date: datetime.date, duration_days: int) -> None:
        """Add a new exercise goal"""
        new_goal = Goal(
            exercise=exercise,
            target=target,
            start_date=start_date,
            duration_days=duration_days,
            completed=False
        )
        self.session.add(new_goal)
        self.session.commit()

    def add_progress(self, exercise: str, date: datetime.date, quantity: int) -> None:
        """Add progress entry for an exercise"""
        new_progress = Progress(
            exercise=exercise,
            date=date,
            quantity=quantity
        )
        self.session.add(new_progress)
        self.session.commit()

    def get_goal(self, exercise: str) -> Goal:
        """Get goal details for an exercise"""
        return self.session.query(Goal).filter(Goal.exercise == exercise).first()

    def get_progress(self, exercise: str) -> pd.DataFrame:
        """Get progress for an exercise"""
        progress = self.session.query(Progress).filter(Progress.exercise == exercise).all()
        if not progress:
            return pd.DataFrame(columns=['exercise', 'date', 'quantity'])

        return pd.DataFrame([
            {'exercise': p.exercise, 'date': p.date, 'quantity': p.quantity}
            for p in progress
        ])

    def get_active_goals(self) -> pd.DataFrame:
        """Get list of active goals"""
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

    def mark_goal_complete(self, exercise: str) -> None:
        """Mark a goal as completed"""
        goal = self.session.query(Goal).filter(Goal.exercise == exercise).first()
        if goal:
            goal.completed = True
            self.session.commit()

    def save_data(self) -> None:
        """Commit any pending changes to the database"""
        self.session.commit()