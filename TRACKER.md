# WIMP Project Tracker
## 8-Week Certification + Build Plan
**Start Date:** March 2, 2026
**Target End Date:** April 24, 2026

---

## Certifications
| Cert | Target Date | Status |
|------|-------------|--------|
| Terraform Associate | April 4, 2026 | 🔲 In Progress |
| CKA (Kubernetes Admin) | May 1, 2026 | 🔲 In Progress |
| AWS SAA | Post-employment | ⏸ Deferred |

---

## Terraform Course Progress (Zeal Vora - 25.5 hours)
| Section | Title | Duration | Status |
|---------|-------|----------|--------|
| 1 | Introduction | 53min | ✅ Complete |
| 2 | Getting Started & Setting Up Labs | 53min | ✅ Complete |
| 3 | Deploying Infrastructure with Terraform | 2hr 5min | ✅ Complete |
| 4 | Read, Generate, Modify Configurations | 10hr 9min | 🔲 In Progress |
| 5 | Terraform Provisioners | 56min | 🔲 Not Started |
| 6 | Terraform Modules & Workspaces | 2hr 17min | 🔲 Not Started |
| 7 | Remote State Management | 2hr 4min | 🔲 Not Started |
| 8 | Security Primer | 1hr 6min | 🔲 Not Started |
| 9 | Terraform Cloud & Enterprise Capabilities | 1hr 58min | 🔲 Not Started |
| 10 | Terraform Challenges | 1hr 34min | 🔲 Not Started |
| 11 | Exam Preparation Section | 1hr 33min | 🔲 Not Started |

---

## Week 1: Foundation + K8s Core Concepts ✅ COMPLETE
### March 2 - 8, 2026

#### Pre-Work / Setup
- [x] WSL2 installed and configured
- [x] Docker Desktop installed with WSL2 backend
- [x] kubectl installed (v1.35.2)
- [x] Kind installed (v0.22.0)
- [x] Terraform installed (v1.14.6)
- [x] GitHub repo created (contra19/wimp)
- [x] Killercoda account created
- [x] AWS account created
- [x] VS Code configured with WSL, Python, Docker, Kubernetes extensions
- [x] SSH key configured for GitHub
- [x] Kubernetes beginner course completed (Udemy)
- [x] Zeal Vora Terraform Associate course enrolled (25.5 hours)

#### Monday March 2 - Day 1
- [x] Kind cluster created (wimp-control-plane)
- [x] WIMP project structure created
- [x] FastAPI skeleton with /health endpoint
- [x] GitHub repo initialized with README
- [x] Scripting: Count alerts by category (defaultdict pattern)

#### Tuesday March 3 - Day 2 (Missed - caught up Wednesday)
- [x] Killercoda: Create pod imperatively and declaratively
- [x] Killercoda: Deployments, replicas, scaling
- [x] Killercoda: Rolling updates and rollbacks (including failed rollout recovery)
- [x] Killercoda: Services and ClusterIP
- [x] Scripting: Alert deduplication with time windows

#### Wednesday March 4 - Day 3
- [x] Killercoda: Expose deployment with service
- [x] Killercoda: Port-forward and service routing verification
- [x] WIMP: POST /alerts endpoint with Pydantic validation
- [x] WIMP: AlertCreate model with UUID and auto-timestamp
- [x] README: API contract documented
- [x] Scripting: Group by key, calculate percentages

#### Thursday March 5 - Day 4
- [x] Killercoda: Labels and selectors
- [x] Killercoda: nodeSelector scheduling
- [x] Killercoda: Taints and tolerations (including case-sensitive bug)
- [x] WIMP: Docker Compose for local PostgreSQL
- [x] WIMP: SQLAlchemy models (Alert table with UUID PK)
- [x] WIMP: database.py - engine, session, Base, get_db
- [x] WIMP: FastAPI wired to PostgreSQL - alerts storing in DB
- [x] README: Startup/shutdown procedures documented
- [x] Scripting: Find duplicates within time window

#### Friday March 6 - Day 5 (Missed - illness, completed Sunday)
- [x] WIMP: Alert deduplication logic in API
- [x] WIMP: Check same service+message within 5 min window
- [x] WIMP: All alerts recorded with is_duplicate flag
- [x] TRACKER.md, CONTEXT.md, DECISIONS.md created

#### Saturday/Sunday March 7-8
- [x] Kubernetes beginner course completed
- [x] Zeal Vora Terraform Associate course enrolled
- [x] Project tracking docs created and committed
- [x] Cert target dates updated (Terraform: April 4, CKA: May 1)
- [x] Terraform course Section 1 completed

---

## Week 2: K8s Logging + Terraform Basics
### March 9 - 13, 2026

#### Monday March 9 ✅ COMPLETE
- [x] Killercoda: CKA Section 4 - Logging & Monitoring
  - kubectl logs, --follow, --tail, --previous
  - -c flag for multi-container pods
  - kubectl describe — reading Events section
  - kubectl top (concept covered, metrics-server not available in env)
- [x] WIMP: SeverityLevel Enum (info/normal/warning/critical)
- [x] WIMP: GET /alerts endpoint with pagination
  - page / page_size parameters
  - severity and service_name filters
  - start_date / end_date date range with validation
  - AlertResponse and AlertListResponse models
  - HTTPException for clean 400 error responses
- [x] Scripting: Day 05 - Error rates from log entries
  - defaultdict with lambda, sorting with key, side effects concept
- [x] Job search: 2 applications

#### Tuesday March 10 ✅ COMPLETE
- [x] Killercoda: CKA Section 5 - Application Lifecycle
  - Rolling updates with kubectl set image
  - Rollout status, history, undo
  - --to-revision for specific rollback
  - kubectl scale and kubectl edit
  - ReplicaSet behavior during updates vs scaling
  - Annotations with kubernetes.io/change-cause
- [x] WIMP: Dockerfile for API
- [x] WIMP: database.py updated for container env var support
- [x] WIMP: Docker image built and tested locally
- [x] WIMP: Image pushed to ghcr.io/contra19/wimp-api:latest
- [x] Terraform course: Sections 2 and 3 complete
- [x] Scripting: Day 06 - Parse timestamps, calculate duration
- [x] Job search: 2 applications

#### Wednesday March 11 ✅ COMPLETE
- [x] Killercoda: K8s Networking
  - ClusterIP, NodePort service types
  - kubectl expose shorthand
  - DNS resolution — same namespace vs cross-namespace
  - Full DNS format: service.namespace.svc.cluster.local
  - NetworkPolicy — deny-all, podSelector, namespaceSelector
  - AND vs OR logic in NetworkPolicy (indentation matters)
- [x] WIMP: Terraform VPC configuration
  - main.tf — VPC, Internet Gateway, public/private subnets
  - variables.tf — region, project, environment, CIDRs
  - terraform init — AWS provider v5.100.0
  - terraform plan — 6 resources, 0 errors, plan clean
- [x] Scripting: Day 07 - Aggregate metrics by service name
- [x] Job search: 2 applications (nothing new)

#### Thursday March 12
- [ ] Killercoda: K8s Namespaces
- [x] WIMP: Terraform routing tables — public route table + subnet associations (plan: 9 resources clean)
- [ ] **Terraform course: Section 4 (afternoon — priority)**
- [ ] Scripting: Day 08
- [ ] Job search: 2-3 applications

#### Friday March 13
- [ ] Killercoda: Review and practice
- [ ] WIMP: Week 2 cleanup and commit
- [ ] **Terraform course: Section 4 continues (afternoon)**
- [ ] Scripting: Day 09
- [ ] Job search: Weekly review

---

## Week 3: Terraform Deep Dive + K8s Networking
### March 16 - 20, 2026
- [ ] Terraform course: Complete Section 4 (10hr 9min — likely spans Weeks 2-3)
- [ ] Terraform course: Sections 5-7
- [ ] Terraform: EKS cluster configuration
- [ ] WIMP: RabbitMQ via Docker Compose
- [ ] WIMP: Basic worker service
- [ ] K8s: Storage, ConfigMaps, Secrets
- [ ] TherapyNotes phone screen — Tuesday March 17 at 10am EST

---

## Week 4: K8s Storage + Advanced Config
### March 23 - 27, 2026
- [ ] CKA: Storage (PV, PVC, StorageClass)
- [ ] CKA: ConfigMaps and Secrets
- [ ] WIMP: K8s manifests for API deployment
- [ ] WIMP: ConfigMaps and Secrets in K8s
- [ ] WIMP: Ingress configuration

---

## Week 5: Security + Integrations
### March 30 - April 3, 2026
- [ ] CKA: Security (RBAC, ServiceAccounts, NetworkPolicy)
- [ ] WIMP: Slack integration
- [ ] WIMP: PagerDuty integration
- [ ] WIMP: Alert throttling
- [ ] Terraform course: Sections 8-11 + practice tests
- [ ] **Terraform Associate Exam - April 4**

---

## Week 6: CKA Prep + Observability
### April 6 - 10, 2026
- [ ] CKA: Full exam prep and practice
- [ ] WIMP: Prometheus metrics
- [ ] WIMP: Grafana dashboards
- [ ] WIMP: GET /alerts/summary endpoint
- [ ] WIMP: Health probes (liveness, readiness)
- [ ] **CKA Exam - May 1**

---

## Week 7: Hardening + AWS Validation
### April 13 - 17, 2026
- [ ] WIMP: Error handling and circuit breakers
- [ ] WIMP: Resource limits and HPA
- [ ] WIMP: Runbooks
- [ ] WIMP: Terraform remote state (S3 + DynamoDB)
- [ ] WIMP: GitHub Actions CI/CD pipeline (test → build → push → terraform plan)
- [ ] GitHub Actions course (start when pipeline is ready to build)
- [ ] **AWS Validation Day - April 16**

---

## Week 8: Polish + Portfolio
### April 20 - 24, 2026
- [ ] WIMP: Comprehensive README
- [ ] WIMP: Architecture decision record
- [ ] WIMP: Demo script
- [ ] WIMP: v1.0 release tag
- [ ] WIMP: Make ghcr.io package public
- [ ] Resume updated with certs + WIMP
- [ ] LinkedIn updated

---

## WIMP Feature Checklist
### API
- [x] Health check endpoint (GET /health)
- [x] Alert ingestion endpoint (POST /alerts)
- [x] Pydantic validation with AlertCreate model
- [x] UUID primary keys
- [x] Auto-generated timestamps
- [x] Alert deduplication logic (5 minute window)
- [x] All alerts recorded with is_duplicate flag
- [x] SeverityLevel Enum (info/normal/warning/critical)
- [x] GET /alerts with pagination (page/page_size)
- [x] GET /alerts severity filtering
- [x] GET /alerts service_name filtering
- [x] GET /alerts date range filtering (start_date/end_date)
- [x] AlertResponse model (separate from DB model)
- [x] AlertListResponse with total/page/size/total_pages metadata
- [x] HTTPException for clean error responses
- [ ] GET /alerts/summary (aggregated counts for dashboards) — Week 6
- [ ] Slack integration
- [ ] PagerDuty integration
- [ ] Alert throttling
- [ ] Dependency grouping
- [ ] Error handling and circuit breakers

### Infrastructure
- [x] Docker Compose for local PostgreSQL
- [x] SQLAlchemy models (Alert table with is_duplicate)
- [x] FastAPI connected to PostgreSQL
- [x] Dockerfile for API
- [x] Docker image pushed to ghcr.io/contra19/wimp-api:latest
- [x] Terraform VPC — main.tf, variables.tf, terraform plan clean (9 resources)
- [x] Terraform routing tables — public route table + subnet associations
- [x] Terraform routing tables — public route table + subnet associations
- [ ] Terraform outputs.tf
- [ ] Terraform routing tables
- [ ] Terraform EKS, RDS, SQS modules
- [ ] Terraform remote state (S3 + DynamoDB)
- [ ] RabbitMQ via Docker Compose
- [ ] Worker services
- [ ] Kubernetes manifests
- [ ] GitHub Actions CI/CD pipeline (test → build → push → terraform plan) — Week 7
- [ ] Prometheus + Grafana (local)
- [ ] Resource limits and HPA
- [ ] Health probes

### Documentation
- [x] README with architecture overview
- [x] API contract documented
- [x] Startup/shutdown procedures
- [x] TRACKER.md
- [x] CONTEXT.md
- [x] DECISIONS.md (Decisions 001-012)
- [ ] .env.example files
- [ ] Runbooks
- [ ] Architecture diagram (Excalidraw)
- [ ] Architecture decision record (ADR)
- [ ] Demo script

### Scripting Practice
- [x] Day 01: Count alerts by category (defaultdict)
- [x] Day 02: Alert deduplication with time windows
- [x] Day 03: Group by key, calculate percentages
- [x] Day 04: Find duplicates within time window
- [x] Day 05: Calculate error rates (defaultdict, lambda, sorting, side effects)
- [x] Day 06: Parse timestamps, calculate duration (datetime.strptime, divmod, max with key)
- [x] Day 07: Aggregate metrics by service name (defaultdict, running totals, sorted)
- [ ] Day 08+: Ongoing daily practice

---

## Job Search
- [x] Resume overhauled (20+ years framing)
- [x] LinkedIn updated with open-to-work
- [x] Recruiter outreach drafted
- [ ] 80+ applications target
- [ ] Terraform cert added to resume
- [ ] CKA cert added to resume
- [ ] WIMP added to portfolio/resume

**Applications sent Week 1:**
- Centene (Staff/Senior SRE)
- Inhabit (Senior DevOps)
- Robert Half position
- McGraw Hill
- SRE Manager (greenfield program)
- 1 LinkedIn job

**Applications sent Week 2:**
- 2 applications Monday March 9
- 2 applications Tuesday March 10
- 2 applications Wednesday March 11 (nothing new in market)

**Active Pipeline:**
- TherapyNotes — Database SRE — Phone screen Tuesday March 17 10am EST with Rochelle Hall
- Brittany (recruiter) — Datadog position — intro call Tuesday March 10 (details pending)
