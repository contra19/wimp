# =============================================================================
# WIMP Scripting Practice - Day 10
# Problem: Alert Escalation Timer
#
# Given a list of open alerts with service name, severity, and timestamp,
# determine which alerts need escalation based on how long they have been
# open. Escalation thresholds by severity:
#   critical — 5 minutes
#   warning  — 15 minutes
#   normal   — 30 minutes
#   info     — 60 minutes
#
# Resolved alerts should never be escalated regardless of age.
# Return overdue alerts sorted by minutes overdue, most overdue first.
#
# Key concepts: datetime.strptime, timedelta, dictionary lookup,
#               conditional filtering, sorted with key, f-string formatting
# Real WIMP application: Escalation timer is the core of WIMP's
# notification routing — critical alerts that go unresolved for 5 minutes
# need to page someone. This logic feeds directly into the PagerDuty
# integration planned for Week 5.
# =============================================================================

'''
Expected output:

Alerts Requiring Escalation:
  a1 | payment-api  | critical | overdue by 15 minutes
  a2 | auth-service | warning  | overdue by 0 minutes
  a4 | db-primary   | critical | overdue by 3 minutes

Skipped (resolved):
  a3 | payment-api | normal

No escalation needed:
  a5 | cache | info | 25 minutes remaining
'''

from datetime import datetime

alerts = [
    {"id": "a1", "service_name": "payment-api",  "severity": "critical", "timestamp": "2026-03-16 09:00:00"},
    {"id": "a2", "service_name": "auth-service",  "severity": "warning",  "timestamp": "2026-03-16 09:05:00"},
    {"id": "a3", "service_name": "payment-api",   "severity": "normal",   "timestamp": "2026-03-16 09:10:00"},
    {"id": "a4", "service_name": "db-primary",    "severity": "critical", "timestamp": "2026-03-16 09:12:00"},
    {"id": "a5", "service_name": "cache",         "severity": "info",     "timestamp": "2026-03-16 09:15:00"},
]

resolved = {"a3"}
threshold = {"critical": 5, "warning": 15, "normal": 30, "info": 60}  
current_time = "2026-03-16 09:20:00"
td_format = "%Y-%m-%d %H:%M:%S"


# Get time diff function
def time_diff(timestamp):
    diff = datetime.strptime(current_time, td_format) - datetime.strptime(timestamp, td_format)
    diff_in_mins = int(diff.total_seconds()/60)
    return diff_in_mins


# loop through alerts and see if alert has been resolved
def get_skipped_alerts(alerts):
    resolved_alerts = []
    for alert in alerts:
        if alert['id'] in resolved:        
            resolved_alerts.append({
                "id": alert['id'], 
                "service": alert['service_name'], 
                "severity": alert['severity']
            })
    return resolved_alerts


# If alert has not been resolved, check to see if it needs to be escalated based on a map of escalation thresholds
def get_unresolved_alerts(alerts):
    needs_escalation = []
    no_escalation = []
    for alert in alerts:
        if alert['id'] in resolved:
            continue  # skip resolved here too
        mins_open = time_diff(alert['timestamp'])
        if mins_open >= threshold[alert['severity']]:
            needs_escalation.append({
                "id": alert['id'],
                "service": alert['service_name'],
                "severity": alert['severity'],
                "overdue": mins_open - threshold[alert['severity']]
            })
        else:
            no_escalation.append({
                "id": alert['id'], 
                "service": alert['service_name'],
                "severity": alert['severity'],
                "remaining": (threshold[alert['severity']] - mins_open)
            })
    
    needs_escalation = sorted(needs_escalation, key=lambda x: x['overdue'], reverse=True)
    return needs_escalation, no_escalation   


# Get alert data
skipped_alerts = get_skipped_alerts(alerts)
unresolved_alerts = get_unresolved_alerts(alerts)

# print alerts that need to be escalated and how long overdue they are
print("Alerts Requiring Escalation:")
for alert in unresolved_alerts[0]:
    print(f"{alert['id']} | {alert['service']} | {alert['severity']} | overdue by {alert['overdue']} minutes")

# print alerts that are skipped because they are in the resolved set 
print("\nSkipped (resolved):")
for alert in skipped_alerts:
    print(f"{alert['id']} | {alert['service']} | {alert['severity']}")
    
# print alerts that do not require escalation currently and how long until they need to be escalated
print("\nNo escalation needed:")
for alert in unresolved_alerts[1]: 
    print(f"{alert['id']} | {alert['service']} | {alert['severity']} | {alert['remaining']} minutes remaining")
