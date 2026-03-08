# WIMP Project Tracker
## 8-Week Certification + Build Plan
**Start Date:** March 2, 2026
**Target End Date:** April 24, 2026

---

## Certifications
| Cert | Target Date | Status |
|------|-------------|--------|
| Terraform Associate | April 4, 2026 | 🔲 In Progress |
| CKA (Kubernetes Admin) | April 10, 2026 | 🔲 In Progress |
| AWS SAA | Post-employment | ⏸ Deferred |

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
- [x] Cert target dates updated (Terraform: April 4, CKA: April 10)

---

## Week 2: K8s Logging + Terraform Basics
### March 9 - 13, 2026
- [ ] Killercoda: CKA Section 4 - Logging & Monitoring
- [ ] Killercoda: CKA Section 5 - Application Lifecycle
- [ ] Terraform course: Providers, Resources, State (start)
- [ ] Terraform course: Variables, outputs, modules
- [ ] WIMP: Severity levels with validation
- [ ] WIMP: GET /alerts endpoint with filtering
- [ ] WIMP: Dockerfile for API
- [ ] WIMP: Push image to ghcr.io
- [ ] WIMP: Terraform VPC configuration (plan only)
- [ ] WIMP: Terraform subnets and internet gateway
- [ ] Scripting: Days 05-09
- [ ] Job search: 10+ applications

---

## Week 3: Terraform Deep Dive + K8s Networking
### March 16 - 20, 2026
- [ ] Terraform course: Complete remaining content
- [ ] Terraform course: Practice tests x2
- [ ] Terraform: EKS cluster configuration
- [ ] WIMP: RabbitMQ via Docker Compose
- [ ] WIMP: Basic worker service
- [ ] K8s: Networking (CNI, DNS, Ingress)

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
- [ ] **Terraform Associate Exam - April 4**

---

## Week 6: CKA Prep + Observability
### April 6 - 10, 2026
- [ ] CKA: Full exam prep and practice
- [ ] WIMP: Prometheus metrics
- [ ] WIMP: Grafana dashboards
- [ ] WIMP: Health probes (liveness, readiness)
- [ ] **CKA Exam - April 10**

---

## Week 7: Hardening + AWS Validation
### April 13 - 17, 2026
- [ ] WIMP: Error handling and circuit breakers
- [ ] WIMP: Resource limits and HPA
- [ ] WIMP: Runbooks
- [ ] **AWS Validation Day - April 16**

---

## Week 8: Polish + Portfolio
### April 20 - 24, 2026
- [ ] WIMP: Comprehensive README
- [ ] WIMP: Architecture decision record
- [ ] WIMP: Demo script
- [ ] WIMP: v1.0 release tag
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
- [ ] GET /alerts with filtering
- [ ] Severity validation (critical/warning/info/normal)
- [ ] Severity prioritization
- [ ] Slack integration
- [ ] PagerDuty integration
- [ ] Alert throttling
- [ ] Dependency grouping
- [ ] Error handling and circuit breakers

### Infrastructure
- [x] Docker Compose for local PostgreSQL
- [x] SQLAlchemy models (Alert table with is_duplicate)
- [x] FastAPI connected to PostgreSQL
- [ ] RabbitMQ via Docker Compose
- [ ] Worker services
- [ ] Dockerfile for API
- [ ] Terraform VPC, EKS, RDS, SQS modules
- [ ] Kubernetes manifests
- [ ] GitHub Actions CI/CD
- [ ] Prometheus + Grafana (local)
- [ ] Resource limits and HPA
- [ ] Health probes

### Documentation
- [x] README with architecture overview
- [x] API contract documented
- [x] Startup/shutdown procedures
- [x] TRACKER.md
- [x] CONTEXT.md
- [x] DECISIONS.md
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
- [ ] Day 05: Calculate error rates from log entries
- [ ] Day 06+: Ongoing daily practice

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
