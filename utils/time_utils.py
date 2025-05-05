# Time utilities - placeholder for future implementation

from datetime import datetime, timedelta

def get_time_until(target_time):
    """Calculate and format the time until a target time"""
    now = datetime.now()
    
    if isinstance(target_time, str):
        # Convert string to datetime if needed
        try:
            target_time = datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Invalid time format"
    
    if target_time < now:
        return "Past"
    
    diff = target_time - now
    
    # Format the difference
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"
