# =============================================================================
# WIMP Scripting Practice - Day 08
# Problem: Parse and Summarize Kubernetes-style Event Data
#
# Given a list of K8s-style event dictionaries, extract and summarize:
# - Count events by type (Normal vs Warning)
# - List unique reasons per namespace
# - Find the most recent event per namespace
#
# Key concepts: nested dict access, datetime parsing, defaultdict,
#               set for unique values, max() with key
# Real WIMP application: Processing K8s events as alert sources —
# Warning events from K8s could feed directly into WIMP as alerts
# =============================================================================

from collections import defaultdict
from datetime import datetime

events = [
    {"namespace": "wimp-dev", "type": "Warning", "reason": "BackOff", "message": "Back-off restarting failed container", "timestamp": "2026-03-12T08:15:00"},
    {"namespace": "wimp-dev", "type": "Normal",  "reason": "Pulled",  "message": "Successfully pulled image", "timestamp": "2026-03-12T08:10:00"},
    {"namespace": "kube-system", "type": "Warning", "reason": "NodeNotReady", "message": "Node controlplane not ready", "timestamp": "2026-03-12T07:55:00"},
    {"namespace": "kube-system", "type": "Normal",  "reason": "NodeReady", "message": "Node controlplane is ready", "timestamp": "2026-03-12T08:00:00"},
    {"namespace": "wimp-dev", "type": "Warning", "reason": "OOMKilled", "message": "Container exceeded memory limit", "timestamp": "2026-03-12T08:20:00"},
    {"namespace": "kube-system", "type": "Warning", "reason": "BackOff", "message": "Back-off restarting failed container", "timestamp": "2026-03-12T08:05:00"},
    {"namespace": "default", "type": "Normal", "reason": "Scheduled", "message": "Successfully assigned pod to node", "timestamp": "2026-03-12T08:12:00"},
    {"namespace": "default", "type": "Warning", "reason": "FailedMount", "message": "Unable to attach volume", "timestamp": "2026-03-12T08:18:00"},
]

'''
Expected output:

Event counts by type:
  Warning: 5
  Normal: 3

Unique reasons per namespace:
  default: FailedMount, Scheduled
  kube-system: BackOff, NodeNotReady, NodeReady
  wimp-dev: BackOff, OOMKilled, Pulled

Most recent event per namespace:
  default: FailedMount at 2026-03-12T08:18:00
  kube-system: BackOff at 2026-03-12T08:05:00
  wimp-dev: OOMKilled at 2026-03-12T08:20:00
'''

# Group events by type and count the number of each event_type
def count_events_by_type(events):
    event_counts = defaultdict(int)
    for event in events:
        event_counts[event["type"]] += 1
    return dict(event_counts)


# Group unique reasons by namespace
def unique_reasons_by_namespace(events):
    reasons_by_namespace = defaultdict(set)
    for event in events:
        reasons_by_namespace[event["namespace"]].add(event["reason"])
    return {ns: sorted(reasons) for ns, reasons in sorted(reasons_by_namespace.items())}


# Find the most recent event per namespace
def most_recent_event_by_namespace(events):
    recent_events = {}
    for event in events:
        ns = event["namespace"]
        timestamp = datetime.fromisoformat(event["timestamp"])
        if ns not in recent_events or timestamp > recent_events[ns][1]:
            recent_events[ns] = (event["reason"], timestamp)
    return {ns: (reason, ts.isoformat()) for ns, (reason, ts) in sorted(recent_events.items())}


# print the results in the expected format
event_counts = count_events_by_type(events)
print("Event counts by type:")
for event_type, count in event_counts.items():
    print(f"  {event_type}: {count}")

reasons_by_namespace = unique_reasons_by_namespace(events)
print("\nUnique reasons per namespace:")
for ns, reasons in reasons_by_namespace.items():
    print(f"  {ns}: {', '.join(reasons)}")

recent_events = most_recent_event_by_namespace(events)
print("\nMost recent event per namespace:")
for ns, (reason, timestamp) in recent_events.items():
    print(f"  {ns}: {reason} at {timestamp}")
