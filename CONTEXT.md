# WIMP - Session Context
## Last Updated: Saturday, March 21, 2026

---

## Current Status
**Week 3 of 8 — Complete**

Terraform course complete — all 11 sections done. Practice tests in progress.
Scores so far: 100%, 75% (rushed), 81%, 83%. Target 80%+ consistently before scheduling exam.
CKA Udemy course started — Section 1 complete (intro), Section 2 in progress.

Monday March 23 double-header:
- 11am — US Cold Storage SRE Manager, Tony (internal TA)
- 1pm — TherapyNotes Database SRE, Penny Verrecchio
Interview prep Sunday March 22.

---

## Daily Schedule

**Monday / Wednesday / Friday mornings:**
- CKA Udemy course — work through sections sequentially
- Killercoda labs alongside relevant CKA sections
- HackerRank — 1 intermediate Python problem, 20-30 min, no intellisense

**Tuesday / Thursday mornings:**
- WIMP application work — API features, worker service
- HackerRank — 1 intermediate Python problem, 20-30 min, no intellisense

**Afternoons until Terraform exam:**
- Terraform practice tests + review
- CKA course continues after Terraform exam

**Post Terraform exam:**
- CKA full focus, 2+ hours daily
- WIMP application work on WIMP days

**HackerRank filter:** Medium difficulty, subdomains: Strings, Collections,
Date and Time, Regex and Parsing, Built-ins

**Completed HackerRank problems:**
- Time Delta (Medium, Date and Time) — 22 minutes
- The Minion Game (Medium, Strings) — 45 minutes
- Validating Credit Card Numbers (Medium, Regex) — 40 minutes

**Remaining HackerRank problems:**
- Merge the Tools!
- Athlete Sort
- ginortS

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
- RabbitMQ running in Docker container via Docker Compose
  - AMQP port: 5672 (API and worker connections)
  - Management UI: http://localhost:15672 (wimp_user credentials)
- Swagger UI available at `http://localhost:8000/docs`
- Docker image: ghcr.io/contra19/wimp-api:latest (private, make public Week 8)
- Terraform VPC plan: 9 resources ready to apply (Week 7)

---

## How To Start The System

**Terminal 1 — Database + RabbitMQ:**
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

**Terminal 1 — Database + RabbitMQ:**
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
      main.tf        # VPC, Internet Gateway, public/private subnets, routing tables
      variables.tf   # region, project, environment, CIDR variables
      outputs.tf     # (empty — to be populated Week 7)
    /local
      docker-compose.yml  # PostgreSQL + RabbitMQ local containers
      .env               # DB + RabbitMQ credentials (not committed - gitignored)
      .env.example       # Template showing required variables (TODO)
  /k8s               # Kubernetes manifests (not yet implemented)
  /docs
    /scripting       # Daily scripting practice files
      day01.py through day10.py
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
total: int
page: int
size: int
total_pages: int
alerts: list[AlertResponse]
```

### Alert (SQLAlchemy - Database model)
```python
alert_id: UUID (PK)
service_name: String        # Indexed
severity: String
message: String
service_version: String
timestamp: DateTime
is_duplicate: Boolean
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
    └── Public Route Table + subnet associations ✅
```

Still to add: NAT gateway, EKS, RDS, SQS (Weeks 5-7)

---

## Cert Strategy

**Terraform Associate:**
- Course: ✅ Complete (all 11 sections)
- Practice tests: In progress — scores 100%, 75%(rushed), 81%, 83%
- Tests remaining: 5, 6, 7 + HashiCorp official sample questions
- Schedule exam when: consistently 80%+ on fresh tests with context switching
- Target exam date: late week of March 23 or early week of March 30
- Cost: $70.50, online proctored via Certiverse

**Key Terraform concepts to know cold:**
- `sensitive = true` — redacts CLI output only, value still in tfstate in plain text
- `terraform state mv` — rename resource without destroy/recreate
- `moved {}` block — declarative alternative to state mv (Terraform 1.1+)
- `terraform workspace new` — creates AND switches automatically
- `terraform workspace select` — switches to existing workspace
- `.terraform/providers/` — provider plugin location (Terraform 0.13+, NOT .terraform/plugins)
- `dynamic` block — constructs nested configuration blocks programmatically
- `locals {}` — define repeated expressions once, reference as local.name
- `terraform state list` — list all resources in state file
- Remote backend log streaming — Terraform Cloud streams plan/apply logs to terminal
- tfstate always in plain text — use encrypted S3 + strict IAM, never git
- Terraform Public Registry requirements: public GitHub repo, terraform-provider-name format,
  semantic version tag — security scan is NOT a requirement
- Implicit dependency — resource referencing another resource's attribute auto-creates dependency
- `terraform apply -replace` — force rebuild of non-tainted resource (replaces deprecated taint)

**CKA:** Mumshad Udemy course + Killercoda labs
- Section 1: ✅ Complete (intro, 13min)
- Section 2: Core Concepts (3hr 39min) — in progress, spans Monday-Tuesday
- Target exam date: May 1, 2026
- Total course remaining: ~26 hours

**CKA Course Breakdown:**
| Section | Title | Duration | Status |
|---------|-------|----------|--------|
| 1 | Introduction | 13min | ✅ Complete |
| 2 | Core Concepts | 3hr 39min | 🔲 In Progress |
| 3 | Scheduling | 3hr 2min | 🔲 Not Started |
| 4 | Logging & Monitoring | 14min | 🔲 Not Started |
| 5 | Application Lifecycle Management | 2hr 22min | 🔲 Not Started |
| 6 | Cluster Maintenance | 46min | 🔲 Not Started |
| 7 | Security | 4hr 4min | 🔲 Not Started |
| 8 | Storage | 1hr 5min | 🔲 Not Started |
| 9 | Networking | 3hr 21min | 🔲 Not Started |
| 10 | Design and Install a K8s Cluster | 32min | 🔲 Not Started |
| 11 | Install K8s the kubeadm way | 44min | 🔲 Not Started |
| 12 | Helm Basics (2025) | 50min | 🔲 Not Started |
| 13 | Kustomize Basics (2025) | 1hr 30min | 🔲 Not Started |
| 14 | Troubleshooting | 1hr 5min | 🔲 Not Started |
| 15 | Other Topics | 12min | 🔲 Not Started |
| 16 | Lightning Labs | 1min | 🔲 Not Started |
| 17 | Mock Exams | 2hr 5min | 🔲 Not Started |
| 18 | Bonus Section | 15min | 🔲 Not Started |

---

## What's Next

### Sunday March 22
- Interview prep — US Cold Storage SRE Manager
- Interview prep — TherapyNotes Database SRE

### Monday March 23
- CKA Section 2 — as much as possible before 11am
- **11am — US Cold Storage SRE Manager, Tony**
- **1pm — TherapyNotes Database SRE, Penny Verrecchio**
- Terraform practice test 5 — evening
- Follow up with Dan Christenson/Robert Half if no response

### Tuesday March 24
- Finish CKA Section 2
- Terraform practice tests 6, 7
- HashiCorp official sample questions
- If 80%+ consistently — schedule Terraform exam
- TherapyNotes — Rochelle Hall returns, may reschedule original screen

### Week of March 23 ongoing
- Terraform exam — late this week or early next if scores warrant
- CKA course continues daily
- WIMP: RabbitMQ publisher in API (next WIMP feature)
- Job applications: resume daily volume

---

## Active Recruiters
- **Tony / US Cold Storage** — SRE Manager, Monday March 23 11am
- **Penny Verrecchio / TherapyNotes** — Database SRE, Monday March 23 1pm
- **Alex Dickinson / Jobot** — US Cold Storage referral
- **Dan Christenson / Robert Half** — searching pipeline, follow up Monday
- **Diamarie Schoombie / Calyptus** — call to schedule, Web3 focus

---

## Known Issues / Open Items
- Architecture diagram (Excalidraw) not yet created
- .env.example files not yet created
- GET /alerts/summary endpoint — planned Week 6
- Terraform outputs.tf empty — populate Week 7
- GitHub Actions CI/CD pipeline — planned Week 7
- RabbitMQ publisher in API — next WIMP feature
- Worker service — pending

---

## Environment Details
- OS: Windows 11 with WSL2 (Ubuntu 24.04)
- Python: 3.12
- FastAPI + Uvicorn
- SQLAlchemy + psycopg2-binary + python-dotenv
- PostgreSQL 15 (Docker)
- RabbitMQ 3 with management plugin (Docker)
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
- Namespaces: create, switch context, -n flag, --all-namespaces/-A, isolation, delete cascade

## K8s Concepts Still To Cover (via CKA Udemy course)
- Core Concepts (Section 2 — in progress)
- Scheduling
- ConfigMaps and Secrets
- Persistent Volumes
- Ingress
- RBAC
- Resource limits and HPA
- Liveness/readiness probes
- kubeadm upgrade
- etcd backup and restore
- Helm, Kustomize
- Troubleshooting
