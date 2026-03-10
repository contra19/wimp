# WIMP - Session Context
## Last Updated: Monday, March 9, 2026

---

## Current Status
**Week 2 of 8 — Day 1 Complete**

GET /alerts is fully implemented with pagination, severity Enum validation, optional
service_name filtering, and date range support. The API now has a complete read/write
cycle: POST alerts in, GET alerts out with filtering and pagination. All committed and
pushed to GitHub.

---

## What Is Currently Working
- FastAPI running on `http://localhost:8000`
- GET /health → returns `{"status": "healthy", "service": "wimp-api"}`
- POST /alerts → validates input, checks for duplicates, stores all alerts in PostgreSQL
- Duplicate detection: same service_name + message within 5 minute window
- All alerts recorded (duplicates flagged with is_duplicate=True, not suppressed)
- GET /alerts → paginated alert retrieval with the following parameters:
  - `severity` — filter by SeverityLevel Enum (info/normal/warning/critical)
  - `service_name` — filter by service name
  - `start_date` / `end_date` — explicit date range (both required if either provided)
  - `page` — page number, default 1
  - `page_size` — results per page, default 10
  - Default behavior: last 15 minutes, page 1, page_size 10
- SeverityLevel Enum centralizes valid severity values across the codebase
- AlertResponse model controls API output shape (separate from DB model)
- AlertListResponse wraps paginated results with total, page, size, total_pages metadata
- HTTPException returns clean 400 errors for invalid date range inputs
- PostgreSQL running in Docker container via Docker Compose
- Swagger UI available at `http://localhost:8000/docs`

---

## How To Start The System

**Terminal 1 — Database:**
```bash
cd ~/wimp/infra/local
docker compose up -d
```

**Terminal 2 — API:**
```bash
cd ~/wimp/api
source venv/bin/activate
uvicorn main:app --reload
```

## How To Stop The System

**Terminal 2 — API:**
```
CTRL+C
```

**Terminal 1 — Database:**
```bash
cd ~/wimp/infra/local
docker compose down
```

---

## Project Structure
```
/wimp
  /api
    main.py          # FastAPI app, endpoints, Pydantic models, dedup logic
    database.py      # SQLAlchemy engine, session, Alert model, get_db
    venv/            # Python virtual environment (not committed)
  /worker            # Queue processor (not yet implemented)
  /infra
    /aws             # Terraform for AWS (not yet implemented)
    /local
      docker-compose.yml  # PostgreSQL local container
      .env               # DB credentials (not committed - gitignored)
      .env.example       # Template showing required variables (TODO)
  /k8s               # Kubernetes manifests (not yet implemented)
  /docs
    /scripting       # Daily scripting practice files
      day01.py       # Count alerts by category (defaultdict)
      day02.py       # Alert deduplication with time windows
      day03.py       # Group by key, calculate percentages
      day04.py       # Find duplicates within time window
      day05.py       # Calculate error rates from log entries (defaultdict, lambda, sorting)
  TRACKER.md         # Progress checklist
  CONTEXT.md         # This file
  DECISIONS.md       # Architectural decisions log
  README.md          # Project documentation
```

---

## Current Data Model

### AlertCreate (Pydantic - API input validation)
```python
service_name: str           # Required
message: str                # Required
service_version: str        # Required
severity: SeverityLevel     # Enum: info/normal/warning/critical, defaults to "normal"
timestamp: datetime         # Auto-generated server-side
alert_id: UUID              # Auto-generated server-side
is_duplicate: bool = False  # Set to True by dedup logic if duplicate detected
```

### AlertResponse (Pydantic - API output)
```python
service_name: str
severity: SeverityLevel
message: str
service_version: str
timestamp: datetime
is_duplicate: bool
```

### AlertListResponse (Pydantic - paginated GET /alerts response)
```python
total: int          # Total records matching the query
page: int           # Current page number
size: int           # Page size used
total_pages: int    # Total pages available
alerts: list[AlertResponse]
```

### Alert (SQLAlchemy - Database model)
```python
alert_id: UUID (PK)         # UUID primary key
service_name: String        # Indexed
severity: String
message: String
service_version: String
timestamp: DateTime
is_duplicate: Boolean       # False for new alerts, True for duplicates
```

---

## Cert Strategy
**Terraform first, CKA second.**

**Terraform course:** Zeal Vora Terraform Associate (25.5 hours, 11 sections)
- Section 1: Introduction ✅ Complete
- Section 2: Getting Started & Setting Up Labs — starting today
- Sections 3-11: In progress over Weeks 2-4
- Target exam date: April 4, 2026
- Rule: Terraform course every afternoon without exception until April 4
  Target 2 hours per day minimum

**CKA:** Mumshad Udemy course + Killercoda labs
- Target exam date: May 1, 2026
- Benefits from full 8 weeks of hands-on K8s work through WIMP

| Cert | Target | Resource |
|------|--------|----------|
| Terraform Associate | April 4, 2026 | Zeal Vora course + 2 practice tests |
| CKA | May 1, 2026 | CKA Udemy course + Killercoda labs |

---

## What's Next — Week 2 (March 9-13)

### Monday March 9 ✅ COMPLETE
- ✅ Killercoda: CKA Section 4 - Logging & Monitoring (kubectl logs, describe, --previous, --follow, -c)
- ✅ WIMP: SeverityLevel Enum with info/normal/warning/critical
- ✅ WIMP: GET /alerts with pagination, date range filtering, severity and service_name filters
- ✅ Scripting: Day 05 - Error rates from log entries (defaultdict, lambda, side effects)
- Terraform course: Section 2 - Getting Started & Setting Up Labs (afternoon — deferred to Tuesday)
- Job search: 2-3 applications (carry forward to Tuesday)

### Tuesday March 10
- Killercoda: CKA Section 5 - Application Lifecycle (rolling updates, rollbacks)
- WIMP: Dockerfile for API
- WIMP: Push image to ghcr.io (GitHub Container Registry)
- **Terraform course: Section 2 + start Section 3 (afternoon — priority)**
- Scripting: Day 06 - Parse timestamps, calculate duration
- Job search: 2-3 applications

### Wednesday March 11
- Killercoda: K8s Networking basics
- WIMP: Terraform VPC configuration (write and plan only - no apply)
- **Terraform course: Section 3 + start Section 4 (afternoon)**
- Scripting: Day 07 - Aggregate metrics by service name
- Job search: 2-3 applications

### Thursday March 12
- Killercoda: K8s Namespaces
- WIMP: Terraform subnets and internet gateway
- **Terraform course: Section 4 continues (afternoon)**
- Scripting: Day 08
- Job search: 2-3 applications

### Friday March 13
- Killercoda: Review and practice
- WIMP: Week 2 cleanup and commit
- **Terraform course: Section 4 continues (afternoon)**
- Scripting: Day 09
- Job search: Weekly review

---

## Known Issues / Open Items
- Architecture diagram (Excalidraw) not yet created
- .env.example files not yet created
- GET /alerts/summary endpoint — planned Week 5-6 (see Decision 012)
- alert_id in AlertCreate Pydantic model could be removed since DB handles generation
  (low priority - current approach works fine)

---

## Environment Details
- OS: Windows 11 with WSL2 (Ubuntu)
- Python: 3.12
- FastAPI + Uvicorn
- SQLAlchemy + psycopg2-binary + python-dotenv
- PostgreSQL 15 (Docker)
- Kind cluster: wimp-control-plane (v1.29.2)
- kubectl: v1.35.2
- Terraform: v1.14.6

---

## K8s Concepts Covered
- Pods (imperative and declarative)
- Deployments, ReplicaSets, scaling
- Rolling updates and rollbacks
- Services (ClusterIP)
- Labels and selectors
- nodeSelector
- Taints and tolerations
- kubeadm cluster bootstrap (beginner course)
- Calico CNI installation
- Logging: kubectl logs, --follow, --tail, --previous, -c for multi-container pods
- Describe: reading Events section for crash diagnosis
- kubectl top (concept — metrics-server not installed in Killercoda env)

## K8s Concepts Still To Cover
- Namespaces
- ConfigMaps and Secrets
- Persistent Volumes
- Ingress
- RBAC
- NetworkPolicy
- Resource limits and HPA
- Liveness/readiness probes
- kubeadm upgrade
- etcd backup and restore
- Application Lifecycle (Section 5)
- K8s Networking (CNI, DNS)
