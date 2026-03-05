# =============================================================================
# WIMP Scripting Practice - Day 04
# Problem: Find Duplicates Within a Time Window
#
# Given a stream of alerts, find all groups of duplicate alerts where
# the same service_name and message occur within a 10 minute window.
# Return only the duplicates, not the originals.
#
# Key concepts: timedelta, dict tracking, list comprehension
# Real WIMP application: Duplicate detection reporting - showing operators
# which alerts are firing repeatedly and need investigation.
# =============================================================================
from datetime import datetime, timedelta

alerts = [
    {"service_name": "payment-api", "message": "timeout", "timestamp": datetime(2026, 3, 5, 9, 0, 0)},
    {"service_name": "payment-api", "message": "timeout", "timestamp": datetime(2026, 3, 5, 9, 5, 0)},
    {"service_name": "payment-api", "message": "timeout", "timestamp": datetime(2026, 3, 5, 9, 12, 0)},
    {"service_name": "auth-service", "message": "login failed", "timestamp": datetime(2026, 3, 5, 9, 1, 0)},
    {"service_name": "auth-service", "message": "login failed", "timestamp": datetime(2026, 3, 5, 9, 8, 0)},
    {"service_name": "auth-service", "message": "login failed", "timestamp": datetime(2026, 3, 5, 9, 20, 0)},
]

# Group alerts by service_name + message key, tagging each as 'new' or 'duplicate'
# Uses a seen dict to track the last timestamp per service/message combo
# Window resets when gap exceeds 5 minutes - alert becomes 'new' again
duplicate_alerts = []

def find_duplicate_alerts(alerts):
    seen = {}
    for alert in alerts:
        key = (alert['service_name'], alert['message'])
        if key in seen:
            if alert['timestamp'] - seen[key] < timedelta(minutes=10):
                duplicate_alerts.append(alert)
        else:
            seen[key] = alert['timestamp']

# Run the grouping function and print results
find_duplicate_alerts(alerts)
print("Duplicate alerts:")
for alert in duplicate_alerts:
    print(f"{alert['timestamp']} | {alert['service_name']} | {alert['message']}")
