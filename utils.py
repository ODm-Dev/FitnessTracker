from datetime import datetime, timedelta

def calculate_progress(current, target):
    """Calculate progress percentage"""
    if target == 0:
        return 0
    return min(100, (current / target) * 100)

def format_date(date_str):
    """Format date string to datetime object"""
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def get_date_range(start_date, duration_days):
    """Generate date range for goal period"""
    end_date = start_date + timedelta(days=duration_days)
    return start_date, end_date

def validate_input(exercise_name, target_quantity, duration_days):
    """Validate user input for goal setting"""
    if not exercise_name:
        return False, "Exercise name cannot be empty"
    if target_quantity <= 0:
        return False, "Target quantity must be greater than 0"
    if duration_days <= 0:
        return False, "Duration must be greater than 0"
    return True, ""
