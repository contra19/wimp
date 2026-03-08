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

## Cert Strategy
**Terraform first, CKA second.** Terraform is the easier cert and gets something on the
resume sooner. CKA benefits from the full 8 weeks of hands-on K8s work through WIMP.

**Rule: Terraform course every afternoon without exception until April 4.**
25.5 hours over 26 days = ~1 hour minimum per day, target 2 hours.

| Cert | Target | Exam |
|------|--------|------|
| Terraform Associate | April 4, 2026 | Zeal Vora course + 2 practice tests |
| CKA | May 1, 2026 | CKA Udemy course + Killercoda labs |

---

## What's Next — Week 2 (March 9-13)

### Monday March 9
- Killercoda: CKA Section 4 - Logging & Monitoring (kubectl logs, describe)
- WIMP: Add severity levels (critical, warning, info) with validation
- WIMP: GET /alerts endpoint with filtering by severity
- **Terraform course: Start - Providers, Resources, State (afternoon)**
- Scripting: Day 05 - Calculate error rates from log entries
- Job search: 2-3 applications

### Tuesday March 10
- Killercoda: CKA Section 5 - Application Lifecycle (rolling updates, rollbacks)
- WIMP: Dockerfile for API
- WIMP: Push image to ghcr.io (GitHub Container Registry)
- **Terraform course: Continue (afternoon)**
- Scripting: Day 06 - Parse timestamps, calculate duration
- Job search: 2-3 applications

### Wednesday March 11
- Killercoda: K8s Networking basics
- WIMP: Terraform VPC configuration (write and plan only - no apply)
- **Terraform course: Variables and outputs (afternoon)**
- Scripting: Day 07 - Aggregate metrics by service name
- Job search: 2-3 applications

### Thursday March 12
- Killercoda: K8s Namespaces
- WIMP: Terraform subnets and internet gateway
- **Terraform course: Modules (afternoon)**
- Scripting: Day 08
- Job search: 2-3 applications

### Friday March 13
- Killercoda: Review and practice
- WIMP: Week 2 cleanup and commit
- **Terraform course: Continue (afternoon)**
- Scripting: Day 09
- Job search: Weekly review

---

## Known Issues / Open Items
- Architecture diagram (Excalidraw) not yet created
- .env.example files not yet created
- No GET /alerts endpoint yet - Week 2 Monday priority
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
