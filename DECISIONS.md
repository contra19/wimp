# WIMP - Architectural Decisions Log
## Last Updated: Monday, March 9, 2026

This document records every significant architectural decision made during WIMP development,
including the reasoning behind each choice. Use this during interviews to speak confidently
about why the system is built the way it is.

---

## Decision 001: FastAPI over Flask
**Date:** March 2, 2026
**Decision:** Use FastAPI as the web framework

**Reasoning:**
- FastAPI is async-native using Python's `async/await` — critical for an alert ingestion
  system that may receive hundreds of concurrent alerts simultaneously
- Auto-generates Swagger UI from code with zero configuration (available at /docs)
- Pydantic integration provides automatic request validation and clear error messages
  for malformed input — no manual validation code needed
- Type hints throughout make the codebase self-documenting

**Tradeoffs:**
- Flask has a larger ecosystem and more Stack Overflow coverage
- FastAPI is newer but has strong adoption in production systems

**Interview answer:** "FastAPI's async performance and built-in Pydantic validation made
it the right choice for an alert ingestion API that needs to handle concurrent requests
without blocking."

---

## Decision 002: SQLAlchemy over raw psycopg2
**Date:** March 5, 2026
**Decision:** Use SQLAlchemy ORM for database interaction

**Reasoning:**
- Defines database tables as Python classes — keeps data model in code, not SQL strings
- Handles connection pooling automatically — important for an API handling concurrent requests
- `Base.metadata.create_all()` creates tables on startup during development
- FastAPI's `Depends()` pattern integrates cleanly with SQLAlchemy sessions
- Easier migration to Alembic for production schema management later

**Tradeoffs:**
- Raw psycopg2 gives more control and is faster for complex queries
- SQLAlchemy adds abstraction overhead
- For simple CRUD operations (which WIMP's API primarily does) the overhead is negligible

**Interview answer:** "SQLAlchemy's connection pooling and ORM layer made sense for an API
with concurrent requests. The Pydantic + SQLAlchemy combination is the standard FastAPI
production pattern."

---

## Decision 003: UUID Primary Keys over Auto-increment Integer
**Date:** March 5, 2026
**Decision:** Use UUID as primary key for the alerts table

**Reasoning:**
- UUIDs can be generated anywhere (API, worker, external service) without coordinating
  with the database — important for distributed systems
- When WIMP scales to multiple API instances, each can generate IDs independently
  without database round-trips to get the next integer
- Standard practice for distributed alert management systems
- Prevents ID enumeration — external callers can't guess alert IDs sequentially

**Tradeoffs:**
- UUIDs are larger than integers (16 bytes vs 4 bytes) — minor storage overhead
- Slightly slower index performance at extreme scale
- Less human-readable than integers

**Interview answer:** "UUID primary keys allow any service to generate IDs without database
coordination, which is essential as WIMP scales to multiple API instances and worker services."

---

## Decision 004: Docker Compose for Local Development
**Date:** March 5, 2026
**Decision:** Use Docker Compose for local PostgreSQL, not a local install

**Reasoning:**
- Keeps the development environment isolated and reproducible
- Any developer can run `docker compose up -d` and have an identical environment
- Easy to reset — `docker compose down -v` wipes everything, `up -d` starts fresh
- Mirrors the production architecture (separate database service) rather than
  conflating local and production concerns
- Named volume (`postgres_data`) persists data across container restarts

**Tradeoffs:**
- Requires Docker Desktop running — slight overhead vs a local PostgreSQL install
- Adds one step to startup process

**Interview answer:** "Docker Compose gives us a reproducible local environment that mirrors
production architecture. Every developer gets identical behavior with a single command."

---

## Decision 005: Kind for Local Kubernetes Development
**Date:** March 2, 2026
**Decision:** Use Kind (Kubernetes in Docker) for local K8s cluster

**Reasoning:**
- Runs entirely inside Docker — no VM overhead, works on any OS with Docker
- Fast cluster creation (~2 minutes vs 10+ for Minikube with VM)
- Matches real Kubernetes behavior closely enough for manifest development and testing
- Free, no cloud costs during development
- Industry standard for CI/CD pipeline K8s testing

**Tradeoffs:**
- Single node by default — can't test true multi-node scheduling locally
- No cloud provider integrations (no real LoadBalancer, no EBS volumes)
- These limitations are acceptable for local development; EKS handles production concerns

**Interview answer:** "Kind gives us a real Kubernetes API in Docker with near-zero overhead.
We test manifests locally in Kind before promoting to EKS, keeping cloud costs near zero
during development."

---

## Decision 006: Free Development Stack with AWS Demo-Only Approach
**Date:** March 2, 2026
**Decision:** Build and test entirely locally, only deploy to AWS for validation demos

**Reasoning:**
- 8-week development period with no income — minimizing burn rate is critical
- All K8s learning can be done on Kind and Killercoda for free
- Terraform can be written and planned (`terraform plan`) without applying
- Single AWS validation day (Week 7) proves production capability for portfolio
- Estimated total AWS cost: ~$10-20 vs hundreds of dollars for continuous EKS

**Tradeoffs:**
- Can't catch AWS-specific issues until validation day
- Some EKS behaviors differ from Kind

**Interview answer:** "The stack is designed to minimize cost while maximizing learning.
Everything runs locally until the portfolio validation day, which proves we can deploy
to production AWS infrastructure on demand."

---

## Decision 007: Credentials Management via .env Files
**Date:** March 5, 2026
**Decision:** Use .env files for local credentials, gitignored from repository

**Reasoning:**
- Never commit credentials to git — even for local development this is a hard rule
- .env pattern is universally understood and works with python-dotenv
- `**/.env` in .gitignore catches .env files anywhere in the repo tree
- Sets the right habit for production secret management (Kubernetes Secrets, AWS
  Secrets Manager) — the code never has credentials baked in

**Tradeoffs:**
- Developers must create their own .env files from a template
- Will add `.env.example` with placeholder values as documentation

**Next step:** Create `.env.example` files showing required variables without values.

---

## Decision 008: Separate Pydantic and SQLAlchemy Models
**Date:** March 5, 2026
**Decision:** Maintain separate AlertCreate (Pydantic) and Alert (SQLAlchemy) models

**Reasoning:**
- Pydantic models control what the API accepts and returns (API contract)
- SQLAlchemy models control what gets stored in the database (data model)
- These concerns should be separate — the API shape and DB shape often diverge
- Standard FastAPI pattern used in production codebases
- Naming convention: `AlertCreate` (input), `AlertResponse` (output), `Alert` (DB)

**Tradeoffs:**
- More code to maintain — changes to data model require updates in both places
- Worth it for clean separation of concerns

**Interview answer:** "Separating Pydantic and SQLAlchemy models follows the standard
FastAPI pattern. The API contract and database schema evolve independently — you don't
want database implementation details leaking into your API responses."

---

## Decision 009: Record All Alerts Including Duplicates
**Date:** March 8, 2026
**Decision:** Store every alert in the database, flagging duplicates with is_duplicate=True
rather than discarding them

**Reasoning:**
- Audit trail — knowing that payment-api fired 47 times in 5 minutes is valuable data
- Pattern detection — repeated duplicates indicate a systemic problem worth investigating
- Metrics — duplicate rate per service is a useful operational metric
- Only the notification/action layer suppresses duplicates, not the storage layer

**Tradeoffs:**
- More storage used vs discarding duplicates
- At extreme scale duplicate volume could be significant — mitigated by the queue
  architecture in later weeks (workers handle action suppression, not the API)

**Interview answer:** "We record everything for audit and observability purposes.
The is_duplicate flag lets downstream systems decide how to act on alerts without
losing the raw signal. Suppressing storage would make post-incident analysis harder."

---

## Decision 010: Pagination over Arbitrary Result Limits on GET /alerts
**Date:** March 9, 2026
**Decision:** Use page/page_size pagination on GET /alerts rather than a hard row cap

**Reasoning:**
- A hard cap (e.g. 1000 rows) is arbitrary and breaks legitimate use cases — during a
  major incident, 1000 alerts could represent only 10 minutes of data for a high-traffic
  service, making the tool useless for exactly the scenarios it was built for
- Pagination puts control in the caller's hands — they stop pulling pages when they have
  what they need, without the API deciding what "enough" data is
- Returns total count and total_pages in every response so callers know upfront how much
  data exists without blind pagination
- Scales naturally — same endpoint serves dashboards (page 1, small page_size) and
  RCA investigations (paginate through all matching records)
- No unbounded queries — every response is still capped at page_size rows

**Tradeoffs:**
- Slightly more complex client logic vs a simple list response
- Multiple requests required for large result sets

**Interview answer:** "We use pagination instead of arbitrary limits because a hard cap
breaks incident investigation workflows — you don't know upfront how many alerts an
incident generated. Pagination lets the caller retrieve exactly what they need while
the API never returns an unbounded result set."

---

## Decision 011: Enum over Literal for Severity Levels
**Date:** March 9, 2026
**Decision:** Use Python Enum (SeverityLevel) instead of Literal type for severity validation

**Reasoning:**
- Severity levels are a core domain concept used across multiple layers — API validation,
  database filtering, future worker routing, and Slack/PagerDuty notification logic
- Enum centralizes the valid values in one place — adding or changing a severity level
  requires one change, not a find-and-replace across the codebase
- `SeverityLevel.critical` as a referenceable constant is cleaner than the string
  "critical" scattered across filter conditions and routing logic
- `str, Enum` inheritance ensures JSON serialization works without extra configuration —
  FastAPI and Pydantic handle it transparently

**Tradeoffs:**
- More code upfront than a one-line Literal type
- Worth it given severity is referenced in multiple layers

**Interview answer:** "I used Enum over Literal because severity levels are a domain
concept that will be referenced across API validation, filtering, and notification routing.
Centralizing them in an Enum means one place to change if requirements evolve, and
SeverityLevel.critical as a constant is more reliable than string literals scattered
throughout the codebase."

---

## Decision 012: Separate /alerts and /alerts/summary Endpoints
**Date:** March 9, 2026
**Decision:** Build two distinct endpoints for alert data — paginated raw records and
aggregated summary counts — rather than one endpoint that serves both use cases

**Reasoning:**
- Raw alert records (GET /alerts) and dashboard summary data (GET /alerts/summary) are
  fundamentally different query types with different performance profiles and response shapes
- GET /alerts returns individual records for investigation and RCA — pagination required,
  response is a list of alert objects
- GET /alerts/summary returns aggregated counts by severity and service for dashboards —
  single fast aggregation query, no pagination needed
- Mixing both into one endpoint would require complex response shaping logic and make
  neither use case work cleanly
- Mirrors how production observability platforms (e.g. Datadog) separate log search from
  dashboard metrics — same underlying data, different access patterns

**Tradeoffs:**
- Two endpoints to maintain instead of one
- Worth it for clean separation of concerns and performance predictability

**Status:** GET /alerts implemented in Week 2. GET /alerts/summary planned for Week 5-6
alongside Prometheus metrics integration.

**Interview answer:** "Dashboard consumers need aggregated counts — total critical alerts
by service in the last hour. Investigation consumers need raw paginated records. These are
different query types with different performance profiles. Serving both from one endpoint
would mean compromising both use cases. Separate endpoints keep each use case clean."
---

## Decision 013: Terraform Remote State with S3 + DynamoDB
**Date:** March 11, 2026
**Decision:** Store Terraform state in S3 with DynamoDB locking rather than local state
or git

**Reasoning:**
- tfstate contains sensitive data in plaintext (passwords, keys, resource IDs) —
  committing it to git is a security risk regardless of repo visibility
- Local state only works for solo development — the moment a second person or CI/CD
  pipeline runs terraform apply, state conflicts corrupt the infrastructure
- S3 provides encrypted, versioned state storage — accidental state corruption is
  recoverable via S3 versioning
- DynamoDB provides state locking — prevents two concurrent applies from corrupting
  state, the same problem a database transaction lock solves
- This is the AWS-standard Terraform pattern used in every production environment

**Tradeoffs:**
- Requires S3 bucket and DynamoDB table to exist before Terraform can manage state
  (chicken-and-egg — bootstrap manually or with a separate script)
- Small additional AWS cost — negligible for a single project

**Implementation:**
```hcl
terraform {
  backend "s3" {
    bucket         = "wimp-terraform-state"
    key            = "wimp/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "wimp-terraform-locks"
    encrypt        = true
  }
}
```

**Status:** Planned for Week 7 before AWS validation day. Using local state during
development to avoid AWS costs.

**Interview answer:** "Terraform state contains sensitive values in plaintext and requires
locking for concurrent access. S3 gives us encrypted versioned storage and DynamoDB gives
us atomic locking — the same guarantees a production database provides for concurrent
writes. Storing state in git is a security antipattern regardless of repo visibility."

---

## Decision 014: WSL2 Host IP over host.docker.internal for Container Networking
**Date:** March 11, 2026
**Decision:** Use the WSL2 eth0 IP address directly when connecting containers to
host services, rather than the host.docker.internal DNS alias

**Reasoning:**
- host.docker.internal resolves to the Docker Desktop VM gateway (192.168.65.254)
  in WSL2, not the WSL2 network interface where services actually run
- WSL2 has a layered network topology: Windows host → Docker Desktop VM → WSL2
  instance — host.docker.internal points to the wrong layer
- The eth0 IP (172.31.19.95) is the actual address of the WSL2 network interface
  where PostgreSQL and other local services are bound
- This is a local development concern only — in production, containers communicate
  via Kubernetes service DNS, not host IP addresses

**Tradeoffs:**
- WSL2 eth0 IP can change between WSL2 restarts — may need to update DATABASE_URL
- Acceptable for local testing; production uses K8s service DNS

**Workaround:**
```bash
WIMP_HOST_IP=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
docker run -e DATABASE_URL="postgresql://user:pass@${WIMP_HOST_IP}:5432/wimp" wimp-api:latest
```

**Interview answer:** "In WSL2, host.docker.internal resolves to the Docker Desktop VM
gateway rather than the WSL2 host. We use the eth0 IP directly for local container
testing. In production this isn't an issue since all services communicate via Kubernetes
DNS within the cluster."
