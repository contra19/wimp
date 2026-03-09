# =============================================================================
# WIMP Scripting Practice - Day 05
# Problem: Calculate Error Rates from Log Entries
#
# Given a list of log entry dicts with service name and status (success/error),
# calculate the error rate percentage for each service, sorted by highest
# error rate first.
#
# Key concepts: defaultdict, sorting with sorted(), lambda, f-string formatting
# Real WIMP application: Foundation for service health scoring — knowing which
# services are throwing the most errors drives alert severity prioritization
# in later weeks.
# =============================================================================

from collections import defaultdict

logs = [
    {"service": "payment-api", "status": "error"},
    {"service": "payment-api", "status": "success"},
    {"service": "payment-api", "status": "error"},
    {"service": "payment-api", "status": "success"},
    {"service": "payment-api", "status": "error"},
    {"service": "auth-service", "status": "success"},
    {"service": "auth-service", "status": "success"},
    {"service": "auth-service", "status": "error"},
    {"service": "notification", "status": "error"},
    {"service": "notification", "status": "error"},
    {"service": "notification", "status": "success"},
    {"service": "notification", "status": "error"},
]    


def calculate_error_rates(logs):
    service_stats = defaultdict(lambda: {"success": 0, "error": 0})
    for log in logs:
        service_stats[log['service']][log['status']] += 1

    error_rates = []
    for service, stats in service_stats.items():
        total = stats['success'] + stats['error']
        error_rate = (stats['error']/total) * 100 if total > 0 else 0
        error_rates.append((service, error_rate))

    error_rates.sort(key=lambda x: x[1], reverse=True)
    return error_rates


error_rates = calculate_error_rates(logs)
error_rate_info = " | ".join([f"{service}: {rate:.2f}%" for service, rate in error_rates])
print(f"Service Error Rates: {error_rate_info}")
