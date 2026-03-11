# =============================================================================
# WIMP Scripting Practice - Day 07
# Problem: Aggregate Metrics by Service Name
#
# Given a list of metric readings with service name, response time (ms),
# and status code, calculate per-service averages and error counts.
# Output sorted by average response time descending.
#
# Key concepts: defaultdict, running totals, integer division, sorted()
# Real WIMP application: Foundation for the /alerts/summary endpoint —
# aggregating per-service health metrics is exactly what a dashboard
# needs to show which services are degraded at a glance.
# =============================================================================

from collections import defaultdict

metrics = [
    {"service": "payment-api", "response_ms": 245, "status": 200},
    {"service": "payment-api", "response_ms": 8750, "status": 500},
    {"service": "payment-api", "response_ms": 312, "status": 200},
    {"service": "auth-service", "response_ms": 95, "status": 200},
    {"service": "auth-service", "response_ms": 102, "status": 200},
    {"service": "auth-service", "response_ms": 4500, "status": 503},
    {"service": "notification", "response_ms": 1200, "status": 200},
    {"service": "notification", "response_ms": 1350, "status": 200},
    {"service": "notification", "response_ms": 1100, "status": 200},
    {"service": "inventory",    "response_ms": 3200, "status": 500},
    {"service": "inventory",    "response_ms": 4100, "status": 500},
    {"service": "inventory",    "response_ms": 2900, "status": 200},
]
'''
Expected output:

payment-api  | avg: 3102ms | errors: 1/3
inventory    | avg: 3400ms | errors: 2/3
notification | avg: 1217ms | errors: 0/3
auth-service | avg: 1566ms | errors: 1/3
'''

# Function to aggregate metrics by service
def aggregate_metrics(metrics):
    # Use defaultdict to accumulate total response time, count, and error count per service
    service_data = defaultdict(lambda: {'total_response':0, 'count':0, 'errors':0})

    # Process each metric entry to update totals and counts
    for metric in metrics:
        service = metric['service']
        service_data[service]['total_response'] += metric['response_ms']
        service_data[service]['count'] += 1
        if metric['status'] >= 400:
            service_data[service]['errors'] += 1

    # Calculate average response time and prepare aggregated list
    aggregated = []
    for service, data in service_data.items():
        avg_response = data['total_response'] / data['count'] if data['count'] > 0 else 0
        aggregated.append((service, avg_response, data['errors'], data['count']))
    # Sort by average response time descending
    aggregated.sort(key=lambda x: x[1], reverse=True)
    return aggregated

# Run aggregation
aggregated_metrics = aggregate_metrics(metrics)

# Print results in formatted table
for service, avg_response, errors, total in aggregated_metrics:
    print(f"{service} | avg: {avg_response:.0f}ms | errors: {errors}/{total}")