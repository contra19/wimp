from collections import defaultdict

alerts = [
    {"service": "payment-api", "severity": "critical"},
    {"service": "auth-service", "severity": "warning"},
    {"service": "payment-api", "severity": "critical"},
    {"service": "inventory", "severity": "info"},
    {"service": "auth-service", "severity": "critical"},
    {"service": "payment-api", "severity": "warning"},
    {"service": "inventory", "severity": "warning"},
    {"service": "auth-service", "severity": "warning"},
]

alert_counts = defaultdict(lambda: defaultdict(int))
for alert in alerts:
    service = alert['service'] 
    severity = alert['severity']
    alert_counts[service][severity] += 1

for service, severity in alert_counts.items():
    counts = " | ".join(f"{level}: {count}" for level, count in severity.items()) 
    print(f"service: {service} -alerts-> {counts}")
