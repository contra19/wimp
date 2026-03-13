# =============================================================================
# WIMP Scripting Practice - Day 09
# Problem: Analyze Service Retry Patterns
#
# Given a list of API call attempts with service name, attempt number,
# response time, and success status, identify:
# - Total attempts and success rate per service
# - Average response time for successful vs failed attempts per service
# - Services exceeding a failure threshold (>30% failure rate)
#
# Key concepts: defaultdict with nested dict, conditional accumulation,
#               percentage calculation, filtering with list comprehension
# Real WIMP application: Retry pattern analysis feeds directly into
# alert throttling logic — services with high failure rates should
# trigger escalating alerts, not repeated identical ones.
# =============================================================================

from collections import defaultdict

attempts = [
    {"service": "payment-api", "attempt": 1, "response_ms": 245, "success": True},
    {"service": "payment-api", "attempt": 2, "response_ms": 8750, "success": False},
    {"service": "payment-api", "attempt": 3, "response_ms": 312, "success": True},
    {"service": "payment-api", "attempt": 4, "response_ms": 9100, "success": False},
    {"service": "payment-api", "attempt": 5, "response_ms": 289, "success": True},
    {"service": "auth-service", "attempt": 1, "response_ms": 95, "success": True},
    {"service": "auth-service", "attempt": 2, "response_ms": 102, "success": True},
    {"service": "auth-service", "attempt": 3, "response_ms": 98, "success": True},
    {"service": "auth-service", "attempt": 4, "response_ms": 110, "success": True},
    {"service": "inventory",    "attempt": 1, "response_ms": 3200, "success": False},
    {"service": "inventory",    "attempt": 2, "response_ms": 4100, "success": False},
    {"service": "inventory",    "attempt": 3, "response_ms": 3800, "success": False},
    {"service": "inventory",    "attempt": 4, "response_ms": 2900, "success": True},
    {"service": "inventory",    "attempt": 5, "response_ms": 3100, "success": False},
]
'''
Expected output:

Service Summary:
  auth-service  | attempts: 4  | success rate: 100.0% | failed: 0
  inventory     | attempts: 5  | success rate: 20.0%  | failed: 4
  payment-api   | attempts: 5  | success rate: 60.0%  | failed: 2

Average Response Times:
  auth-service  | success: 101ms  | failed: N/A
  inventory     | success: 2900ms | failed: 3775ms
  payment-api   | success: 282ms  | failed: 8925ms

Services exceeding 30% failure threshold:
  inventory     | failure rate: 80.0%
  payment-api   | failure rate: 40.0%
'''

# Step 1: Aggregate data per service
# Using defaultdict to create a nested structure for attempts, successes, and response times
def aggregate_service_data(attempts):
    service_data = defaultdict(lambda: {"attempts": 0, "successes": 0, "response_times": {"success": [], "failed": []}})
    for attempt in attempts:
        service = attempt["service"]
        success = attempt["success"]
        response_time = attempt["response_ms"]
        # Update counts and response times
        service_data[service]["attempts"] += 1
        if success:
            service_data[service]["successes"] += 1
            service_data[service]["response_times"]["success"].append(response_time)
        else:
            service_data[service]["response_times"]["failed"].append(response_time)
    return service_data


# Step 2: Calculate success rates and average response times
# Create a summary dictionary to hold the calculated metrics for each service
def calculate_service_summary(service_data):
    service_summary = {}
    for service, data in service_data.items():
        attempts = data["attempts"]
        successes = data["successes"]
        success_rate = (successes / attempts) * 100 if attempts > 0 else 0
        failure_rate = 100 - success_rate
        avg_success_time = sum(data["response_times"]["success"]) / len(data["response_times"]["success"]) if data["response_times"]["success"] else None
        avg_failed_time = sum(data["response_times"]["failed"]) / len(data["response_times"]["failed"]) if data["response_times"]["failed"] else None

        # Store the calculated metrics in the service_summary dictionary
        service_summary[service] = {
            "attempts": attempts,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "avg_success_time": avg_success_time,
            "avg_failed_time": avg_failed_time,
            "failed_attempts": attempts - successes
        }
    return service_summary

# Step 3: Identify services exceeding failure threshold
def identify_high_failure_services(service_summary, threshold=30):
    high_failure_services = {}
    for service, summary in service_summary.items():
        if summary["failure_rate"] >= threshold:
            high_failure_services[service] = summary["failure_rate"]
    return high_failure_services


# Main execution
service_data = aggregate_service_data(attempts)
service_summary = calculate_service_summary(service_data)
high_failure_services = identify_high_failure_services(service_summary)

# Output results
print("Service Summary:")
for service, summary in service_summary.items():
    print(f"  {service} | attempts: {summary['attempts']}  | success rate: {summary['success_rate']:.1f}% | failed: {summary['failed_attempts']}")

print("\nAverage Response Times:")
for service, summary in service_summary.items():
    success_time = f"{summary['avg_success_time']:.0f}ms" if summary['avg_success_time'] is not None else "N/A"
    failed_time = f"{summary['avg_failed_time']:.0f}ms" if summary['avg_failed_time'] is not None else "N/A"
    print(f"  {service} | success: {success_time}  | failed: {failed_time}")

print("\nServices exceeding 30% failure threshold:")
for service, failure_rate in high_failure_services.items():
    print(f"  {service} | failure rate: {failure_rate:.1f}%")
