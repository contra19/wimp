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
Coming soon.

## Status
🚧 Under active development
