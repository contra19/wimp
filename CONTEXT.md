# WIMP - Session Context
## Last Updated: Tuesday, March 24, 2026

---

## Current Status
**Week 4 of 8 — Day 2**

Terraform course complete. Practice tests in progress — scores 100%, 75%(rushed), 81%, 83%.
Tests 5-7 and HashiCorp official sample questions pending.
CKA Udemy course started — Section 1 complete, Section 2 (Core Concepts, 3hr 39min) in progress.

Monday March 23 interviews completed:
- 11am US Cold Storage SRE Manager — Tony (internal TA), Teams video call
- 1pm TherapyNotes Database SRE — Penny Verrecchio, phone screen

---

## Daily Schedule

**Monday / Wednesday / Friday mornings:**
- CKA Udemy course — work through sections sequentially
- Killercoda labs alongside relevant CKA sections
- HackerRank — 1 intermediate Python problem, 20-30 min, no intellisense

**Tuesday / Thursday mornings:**
- WIMP application work — API features, worker service
- HackerRank — 1 intermediate Python problem, 20-30 min, no intellisense

**Afternoons:**
- Terraform practice tests + review until exam scheduled
- CKA course after Terraform exam

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
  TRACKER.md
  CONTEXT.md
  DECISIONS.md
  README.md
```

---

## Current Data Model

### AlertCreate (Pydantic - API input validation)
```python
service_name: str
message: str
service_version: str
severity: SeverityLevel     # Enum: info/normal/warning/critical
timestamp: datetime         # Auto-generated
alert_id: UUID              # Auto-generated
is_duplicate: bool = False
```

### AlertResponse / AlertListResponse / Alert (SQLAlchemy)
See DECISIONS.md for full model details.

---

## Terraform VPC Design
```
AWS VPC (10.0.0.0/16) — wimp-dev-vpc
├── Public Subnets (10.0.1.0/24, 10.0.2.0/24)
├── Private Subnets (10.0.10.0/24, 10.0.11.0/24)
└── Internet Gateway + Public Route Table ✅
```

---

## Cert Strategy

**Terraform Associate:**
- Course: ✅ Complete (all 11 sections)
- Practice tests: 100%, 75%(rushed), 81%, 83% — tests 5-7 + HashiCorp official pending
- Schedule exam when: consistently 80%+ on fresh tests with context switching
- Target exam date: this week if scores warrant
- Cost: $70.50, online proctored via Certiverse

**Key Terraform concepts to know cold:**
- sensitive = true — redacts CLI output only, value still in tfstate plain text
- terraform state mv — rename resource without destroy/recreate
- moved {} block — declarative alternative (Terraform 1.1+)
- terraform workspace new — creates AND switches automatically
- terraform workspace select — switches to existing workspace
- .terraform/providers/ — plugin location (0.13+, NOT .terraform/plugins)
- dynamic block — nested configuration blocks programmatically
- locals {} — define repeated expressions once
- terraform state list — list all resources in state file
- Error budget = allowable failure margin from SLO (99.9% = 8.7 hrs/year)
- Terraform Public Registry: public GitHub repo, terraform-provider-name format, semver tag required
- terraform apply -replace — force rebuild non-tainted resource

**CKA:** Mumshad Udemy course + Killercoda labs
- Section 1: ✅ Complete
- Section 2: Core Concepts (3hr 39min) — in progress
- Target exam: May 1, 2026
- Total remaining: ~26 hours

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

### This Week (March 24-28)
- Terraform practice tests 5, 6, 7 + HashiCorp official sample questions
- Schedule Terraform exam if 80%+ consistently
- CKA Section 2 — finish Core Concepts
- HackerRank daily
- WIMP: RabbitMQ publisher in API (next feature)
- Job applications: resume daily volume 2-3/day
- Follow up with interview outcomes as they come in

---

## Active Recruiters / Pipeline
- US Cold Storage — SRE Manager — interviewed Monday March 23, awaiting feedback
- TherapyNotes — Database SRE — interviewed Monday March 23, awaiting feedback
- Alex Dickinson / Jobot — US Cold Storage referral
- Dan Christenson / Robert Half — searching pipeline
- Diamarie Schoombie / Calyptus — call to schedule, Web3 focus
- Rochelle Hall / TherapyNotes — returns from leave, may reschedule original screen

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
- WSL2 host IP: 172.31.19.95

---

## K8s Concepts Covered
- Pods, Deployments, ReplicaSets, scaling
- Rolling updates and rollbacks
- Services (ClusterIP, NodePort)
- Labels, selectors, nodeSelector
- Taints and tolerations
- kubeadm cluster bootstrap, Calico CNI
- Logging: kubectl logs, --follow, --tail, --previous, -c
- Application Lifecycle: set image, rollout, undo, scale, edit
- Networking: ClusterIP, NodePort, DNS, cross-namespace DNS
- NetworkPolicy: deny-all, podSelector, namespaceSelector
- Namespaces: create, switch context, -n flag, --all-namespaces/-A

## K8s Concepts Still To Cover
- Core Concepts deep dive (Section 2 in progress)
- Scheduling, ConfigMaps, Secrets
- Persistent Volumes, Ingress, RBAC
- Resource limits, HPA, probes
- kubeadm upgrade, etcd backup/restore
- Helm, Kustomize, Troubleshooting
