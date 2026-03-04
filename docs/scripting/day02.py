# =============================================================================
# WIMP Scripting Practice - Day 02
# Problem: Alert Deduplication with Time Windows
#
# Given a list of alerts, tag each as 'new' or 'duplicate' where duplicate
# means the same service_name and message appeared within a 5 minute window.
#
# Key concepts: timedelta comparison, tuple keys, dict as seen-tracker,
# in-place dict mutation
# Real WIMP application: This logic becomes the database deduplication check
# in POST /alerts when PostgreSQL is wired up on Thursday.
# =============================================================================
# Imports
from datetime import datetime, timedelta

# Sample alert data
alerts = [
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 0, 0)},
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 3, 0)},
    {"service_name": "auth-service", "message": "High latency", "timestamp": datetime(2026, 3, 4, 10, 4, 0)},
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 6, 0)},
    {"service_name": "auth-service", "message": "High latency", "timestamp": datetime(2026, 3, 4, 10, 8, 0)},
]

# Group alerts by service_name + message key, tagging each as 'new' or 'duplicate'
# Uses a seen dict to track the last timestamp per service/message combo
# Window resets when gap exceeds 5 minutes - alert becomes 'new' again
def group_alerts(alerts):
    new_alerts = []
    duplicate_alerts = []
    seen = {}
    for alert in alerts:
        key = (alert['service_name'], alert['message'])
        if key in seen:
            if alert['timestamp'] - seen[key] < timedelta(minutes=5):
                alert["disposition"] = "duplicate"
                duplicate_alerts.append(alert)
            else:
                if alert['timestamp'] - seen[key] >= timedelta(minutes=5):
                    alert["disposition"] = "new"
                    new_alerts.append(alert)
                    seen[key] = alert['timestamp']
        else:
            alert["disposition"] = "new"
            new_alerts.append(alert)
            seen[key] = alert['timestamp']

# Run the grouping function and print results
group_alerts(alerts)
for alert in alerts:
    print(f"{alert['timestamp']} | {alert['service_name']} | {alert['message']} | {alert['disposition']}")
