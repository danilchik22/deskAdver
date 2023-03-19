from datetime import datetime, timedelta


def time_over():
    return datetime.utcnow + timedelta(days=30)
