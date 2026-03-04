# =============================================================================
# WIMP Scripting Practice - Day 03
# Problem: Group by Key, Calculate Percentages
#
# Given a list of alerts, calculate the percentage breakdown of alerts
# by severity across the entire dataset.
#
# Key concepts: defaultdict, f-string formatting, percentage calculation,
# generator expressions with join
# Real WIMP application: Foundation for the severity breakdown dashboard
# endpoint - showing operators what percentage of alerts are critical vs
# warning vs info at a glance.
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

# Total alert count used as denominator for percentage calculation
# In production WIMP this will be a database COUNT() query instead of len(alerts)
for service, severity in alert_counts.items():
    counts = " | ".join(f"{level}: {count}/{len(alerts)} ({count/len(alerts)*100:.2f}%)" for level, count in severity.items()) 
    print(f"service: {service} -alerts-> {counts}")
