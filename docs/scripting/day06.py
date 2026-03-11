# =============================================================================
# WIMP Scripting Practice - Day 06
# Problem: Parse Timestamps and Calculate Duration
#
# Given a list of alert events with start and end timestamps, calculate the
# duration of each alert in minutes and seconds, and identify which alert
# had the longest duration.
#
# Key concepts: datetime.strptime, timedelta, string formatting, max() with key
# Real WIMP application: Alert duration tracking — knowing how long a service
# was in a degraded state is critical for SLA reporting and post-incident
# review. Foundation for future alert resolution tracking in WIMP.
# =============================================================================

events = [
    {"service": "payment-api", "start": "2026-03-09 08:12:34", "end": "2026-03-09 08:45:11"},
    {"service": "auth-service", "start": "2026-03-09 09:03:22", "end": "2026-03-09 09:07:55"},
    {"service": "notification", "start": "2026-03-09 11:30:00", "end": "2026-03-09 12:15:45"},
    {"service": "inventory",    "start": "2026-03-09 14:22:10", "end": "2026-03-09 14:29:58"},
]
'''
Expected output:
payment-api: 32 minutes, 37 seconds
auth-service: 4 minutes, 33 seconds
notification: 45 minutes, 45 seconds
inventory: 7 minutes, 48 seconds

Longest outage: notification (45 minutes, 45 seconds)
'''
from datetime import datetime, timedelta

# Function to calculate durations of alerts
def calculate_durations(events):
    # Parse timestamps and calculate duration for each event
    dt_format = "%Y-%m-%d %H:%M:%S"
    durations = []
    for event in events:
        start_time = datetime.strptime(event["start"], dt_format)
        end_time = datetime.strptime(event["end"], dt_format)
        duration = end_time - start_time
        minutes, seconds = divmod(duration.total_seconds(), 60)
        durations.append((event["service"], int(minutes), int(seconds), duration.total_seconds()))
    return durations

# Function to find the longest outage
def get_longest_outage(durations):
    return max(durations, key=lambda x: x[3])

# Calculate durations and print results
print("Alert Durations:")
durations = calculate_durations(events)
# Print each service's duration
for service, minutes, seconds, _ in durations:
    print(f"{service}: {minutes} minutes, {seconds} seconds")
longest_service, longest_minutes, longest_seconds, _ = get_longest_outage(durations)
# Print longest outage information
print(f"\nLongest outage: {longest_service} ({longest_minutes} minutes, {longest_seconds} seconds)")
