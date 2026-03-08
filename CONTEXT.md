# WIMP - Session Context
## Last Updated: Sunday, March 8, 2026

---

## Current Status
**Week 1 of 8 — COMPLETE**

The core API is functional end-to-end: FastAPI receives alerts, validates them via Pydantic,
checks for duplicates against PostgreSQL, stores all alerts with is_duplicate flag, and returns
appropriate status. Local development environment fully operational via Docker Compose.

---

## What Is Currently Working
- FastAPI running on `http://localhost:8000`
- GET /health → returns `{"status": "healthy", "service": "wimp-api"}`
- POST /alerts → validates input, checks for duplicates, stores all alerts in PostgreSQL
- Duplicate detection: same service_name + message within 5 minute window
- All alerts recorded (duplicates flagged with is_duplicate=True, not suppressed)
- PostgreSQL running in Docker container via Docker Compose
- Alerts table with UUID primary key and is_duplicate boolean flag
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
severity: str = "normal"    # Optional, defaults to "normal"
timestamp: datetime         # Auto-generated server-side
alert_id: UUID              # Auto-generated server-side
is_duplicate: bool = False  # Set to True by dedup logic if duplicate detected
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

## What's Next — Week 2 (March 9-13)

### Monday March 9
- Killercoda: CKA Section 4 - Logging & Monitoring (kubectl logs, describe)
- WIMP: Add severity levels (critical, warning, info) with validation
- WIMP: GET /alerts endpoint with filtering by severity
- Scripting: Day 05 - Calculate error rates from log entries
- Start Zeal Vora Terraform Associate course (25.5 hours)

### Tuesday March 10
- Killercoda: CKA Section 5 - Application Lifecycle (rolling updates, rollbacks)
- WIMP: Dockerfile for API
- WIMP: Push image to ghcr.io (GitHub Container Registry)
- Scripting: Day 06 - Parse timestamps, calculate duration

### Wednesday March 11
- Terraform course: Providers, Resources, State
- WIMP: Terraform VPC configuration (write, plan only - no apply)
- Scripting: Day 07 - Aggregate metrics by service name

### Thursday March 12
- Terraform course: Variables, outputs
- WIMP: Terraform subnets and internet gateway
- Scripting: Day 08

### Friday March 13
- Terraform course: Modules
- WIMP: Week 2 review and cleanup
- Scripting: Day 09

---

## Known Issues / Open Items
- Architecture diagram (Excalidraw) not yet created
- .env.example files not yet created
- No GET /alerts endpoint yet - Week 2 priority
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

## K8s Concepts Still To Cover
- Namespaces
- ConfigMaps and Secrets
- Persistent Volumes
- Ingress
- RBAC
- NetworkPolicy
- Resource limits and HPA
- Liveness/readiness probes
- kubeadm cluster setup and upgrade
- etcd backup and restore
