# WIMP - Session Context
## Last Updated: Wednesday, March 11, 2026

---

## Current Status
**Week 2 of 8 — Day 3 Complete**

Terraform VPC configuration is written and planned clean — 6 resources, 0 errors.
Docker image is built, tested, and pushed to ghcr.io. API is fully functional with
pagination, severity Enum, and date range filtering. K8s networking concepts covered
through NetworkPolicy.

---

## Daily Practice Routine
- **Morning:** HackerRank — 1 intermediate Python problem, 20-30 min max, no intellisense
  - Domains: string manipulation, collections, datetime, log parsing, data aggregation
  - Skip: binary trees, dynamic programming, graph traversal
- **Morning:** Killercoda CKA lab
- **Morning:** WIMP scripting problem (domain-relevant, builds portfolio narrative)
- **Afternoon:** Terraform course — 2 hours minimum, non-negotiable until April 4

---

## What Is Currently Working
- FastAPI running on `http://localhost:8000`
- GET /health → returns `{"status": "healthy", "service": "wimp-api"}`
- POST /alerts → validates input, checks for duplicates, stores all alerts in PostgreSQL
- Duplicate detection: same service_name + message within 5 minute window
- All alerts recorded (duplicates flagged with is_duplicate=True, not suppressed)
- GET /alerts → paginated alert retrieval with:
  - severity filter (SeverityLevel Enum: info/normal/warning/critical)
  - service_name filter
  - start_date / end_date date range with validation
  - page / page_size pagination
  - Default: last 15 minutes, page 1, page_size 10
- AlertResponse and AlertListResponse models (separate from DB model)
- HTTPException for clean 400 error responses
- PostgreSQL running in Docker container via Docker Compose
- Swagger UI available at `http://localhost:8000/docs`
- Docker image: ghcr.io/contra19/wimp-api:latest (private, make public Week 8)
- Terraform VPC plan: 9 resources ready to apply (Week 7)

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

**Run containerized API (for testing Docker image):**
```bash
WIMP_HOST_IP=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://wimp_user:$(grep POSTGRES_PASSWORD ~/wimp/infra/local/.env | cut -d= -f2)@${WIMP_HOST_IP}:5432/wimp" \
  wimp-api:latest
```

Note: Use WSL2 host IP directly — host.docker.internal does not reliably resolve in WSL2.

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
    Dockerfile       # Container definition for wimp-api
    requirements.txt # Python dependencies
    venv/            # Python virtual environment (not committed)
  /worker            # Queue processor (not yet implemented)
  /infra
    /aws
      main.tf        # VPC, Internet Gateway, public/private subnets
      variables.tf   # region, project, environment, CIDR variables
      outputs.tf     # (empty — to be populated Week 7)
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
      day05.py       # Calculate error rates (defaultdict, lambda, side effects)
      day06.py       # Parse timestamps, calculate duration (strptime, divmod)
      day07.py       # Aggregate metrics by service name (running totals, sorted)
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

## Terraform VPC Design
```
AWS VPC (10.0.0.0/16) — wimp-dev-vpc
├── Public Subnets
│   ├── wimp-dev-public-1 (10.0.1.0/24) — us-east-1a
│   └── wimp-dev-public-2 (10.0.2.0/24) — us-east-1b
├── Private Subnets
│   ├── wimp-dev-private-1 (10.0.10.0/24) — us-east-1a
│   └── wimp-dev-private-2 (10.0.11.0/24) — us-east-1b
└── Internet Gateway — wimp-dev-igw
```

Still to add: NAT gateway, EKS, RDS, SQS (Weeks 3-4)

---

## Cert Strategy
**Terraform first, CKA second.**

**Terraform course:** Zeal Vora Terraform Associate (25.5 hours, 11 sections)
- Sections 1-3: ✅ Complete
- Section 4: In progress (10hr 9min — the big one)
- Sections 5-11: Upcoming
- Target exam date: April 4, 2026
- Rule: Terraform course every afternoon without exception until April 4
  Target 2 hours per day minimum

**CKA:** Mumshad Udemy course + Killercoda labs
- Target exam date: May 1, 2026

| Cert | Target | Resource |
|------|--------|----------|
| Terraform Associate | April 4, 2026 | Zeal Vora course + 2 practice tests |
| CKA | May 1, 2026 | CKA Udemy course + Killercoda labs |

---

## What's Next — Week 2 Remaining (March 12-13)

### Thursday March 12
- Killercoda: K8s Namespaces
- WIMP: Terraform routing tables (public route table + associations)
- **Terraform course: Section 4 — priority, start today**
- Scripting: Day 08
- Job search: 2-3 applications

### Friday March 13
- Killercoda: Review and practice
- WIMP: Week 2 cleanup and commit
- **Terraform course: Section 4 continues**
- Scripting: Day 09
- Job search: Weekly review

## Week 3 Preview (March 16-20)
- TherapyNotes phone screen — Tuesday March 17 at 10am EST (Rochelle Hall)
  - Prep: Monday afternoon or Tuesday morning
  - Role: Database SRE — PostgreSQL focus, Datadog observability, Python automation
  - Salary anchored at $175K
- Terraform Section 4 continues — likely spans into Week 3
- K8s: Storage, ConfigMaps, Secrets

---

## Known Issues / Open Items
- Architecture diagram (Excalidraw) not yet created
- .env.example files not yet created
- GET /alerts/summary endpoint — planned Week 6
- Terraform outputs.tf empty — populate Week 7
- Terraform routing tables ✅ complete — public route table + subnet associations
- GitHub Actions CI/CD pipeline — planned Week 7 (start course when ready to build)
- host.docker.internal unreliable in WSL2 — use eth0 IP for container testing

---

## Environment Details
- OS: Windows 11 with WSL2 (Ubuntu 24.04)
- Python: 3.12
- FastAPI + Uvicorn
- SQLAlchemy + psycopg2-binary + python-dotenv
- PostgreSQL 15 (Docker)
- Kind cluster: wimp-control-plane (v1.29.2)
- kubectl: v1.35.2
- Terraform: v1.14.6
- WSL2 host IP: 172.31.19.95 (use for container-to-host PostgreSQL connections)

---

## K8s Concepts Covered
- Pods (imperative and declarative)
- Deployments, ReplicaSets, scaling
- Rolling updates and rollbacks
- Services (ClusterIP, NodePort)
- Labels and selectors
- nodeSelector
- Taints and tolerations
- kubeadm cluster bootstrap
- Calico CNI installation
- Logging: kubectl logs, --follow, --tail, --previous, -c
- Describe: reading Events section
- kubectl top (concept — metrics-server required)
- Application Lifecycle: set image, rollout, undo, --to-revision, scale, edit
- Networking: ClusterIP, NodePort, DNS resolution, cross-namespace DNS
- NetworkPolicy: deny-all, podSelector, namespaceSelector, AND vs OR logic

## K8s Concepts Still To Cover
- Namespaces (deep dive)
- ConfigMaps and Secrets
- Persistent Volumes
- Ingress
- RBAC
- Resource limits and HPA
- Liveness/readiness probes
- kubeadm upgrade
- etcd backup and restore
