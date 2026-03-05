# WIMP - Watchdog Intelligent Monitoring Platform

A production-grade alert management system built to demonstrate SRE best practices.

## Architecture
- **API**: FastAPI (Python) - Alert ingestion and management
- **Queue**: RabbitMQ - Async alert processing
- **Workers**: Queue processors for notifications
- **Database**: PostgreSQL - Alert storage
- **Infrastructure**: Terraform (AWS EKS, RDS, SQS)
- **Orchestration**: Kubernetes

## Local Development
### Startup Process
### Database Terminal - start the DB
``` bash
cd ~/wimp/infra/local
docker compose up -d
```
### API Terminal - start the API
``` bash
cd ~/wimp/api
source venv/bin/activate
uvicorn main:app --reload
```

### Shutdown Process
### API Terminal
CTRL+C

### Database Terminal - Stop the DB
``` bash
cd ~/wimp/infra/local
docker compose down
```

## WIMP API
WIMP has an API layer that includes the following endpoints: 

### GET /health 

Checks status of the WIMP API

### POST /alerts

Creates a new alert in the system.

**Required fields:**
- `service_name` (string) - Name of the service triggering the alert
- `message` (string) - Description of the alert condition
- `service_version` (string) - Version of the service

**Optional fields:**
- `severity` (string) - Alert severity, defaults to "normal"

**Auto-generated:**
- `alert_id` (UUID) - Unique identifier
- `timestamp` (datetime) - Server-side timestamp

**Example request:**
```json
{
"service_name": "payment-api",
"severity": "critical",
"message": "Database connection failed",
"service_version": "v2.1"
}
```

you can browse to **/docs** for self-generated docs explaining all of the endpoints above.

## Status
🚧 Under active development
