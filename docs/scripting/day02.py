from datetime import datetime, timedelta

alerts = [
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 0, 0)},
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 3, 0)},
    {"service_name": "auth-service", "message": "High latency", "timestamp": datetime(2026, 3, 4, 10, 4, 0)},
    {"service_name": "payment-api", "message": "DB connection failed", "timestamp": datetime(2026, 3, 4, 10, 6, 0)},
    {"service_name": "auth-service", "message": "High latency", "timestamp": datetime(2026, 3, 4, 10, 8, 0)},
]



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


group_alerts(alerts)
for alert in alerts:
    print(f"{alert['timestamp']} | {alert['service_name']} | {alert['message']} | {alert['disposition']}")
