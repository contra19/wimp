# =============================================================================
# WIMP Scripting Practice - Day 01
# Problem: Count Alerts by Category
#
# Given a list of alert dicts, group and count alerts by service and severity.
#
# Key concepts: defaultdict, nested defaultdict, generator expressions, join
# Real WIMP application: Foundation for the alert dashboard severity breakdown
# endpoint and reporting features built in later weeks.
# =============================================================================
# Imports
from collections import defaultdict

# Sample alert data
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

# Group and count alerts by service and severity
alert_counts = defaultdict(lambda: defaultdict(int))
for alert in alerts:
    service = alert['service'] 
    severity = alert['severity']
    alert_counts[service][severity] += 1

# Print the alert counts by service and severity
for service, severity in alert_counts.items():
    counts = " | ".join(f"{level}: {count}" for level, count in severity.items()) 
    print(f"service: {service} -alerts-> {counts}")
