# Continuum — Module Development Guide

This document explains **how to design, implement, and integrate modules** within the Continuum platform.

A *module* is an optional, removable subsystem that consumes Continuum’s core capabilities to provide domain‑specific functionality (e.g. Kanban boards, contract management, billing).

This guide is intentionally strict. Following it preserves:

* architectural integrity
* research credibility
* long‑term maintainability
* safe open‑source collaboration

---

## 1. What a Module Is (and Is Not)

### 1.1 A Module **Is**

* a consumer of core APIs and events
* independently deployable
* responsible for its own data
* optional at runtime

### 1.2 A Module **Is Not**

* a modification of core behaviour
* a shared library for core logic
* allowed to access core databases
* allowed to bypass permissions

> **Rule:** If Continuum breaks when a module is removed, the module is incorrectly designed.

---

## 2. Module Placement & Structure

All modules live under:

```
backend-microservices/modules/
```

### 2.1 Recommended Module Layout

```
modules/<module-name>/
├── backend-python/
│   ├── domain/
│   ├── handlers/
│   ├── projections/
│   ├── api/
│   └── Dockerfile
├── backend-go/
│   ├── realtime/
│   ├── gateway/
│   └── Dockerfile
├── db/
│   ├── migrations/
│   └── README.md
└── README.md
```

### 2.2 Why This Structure

* **Python**: domain logic, orchestration, semantics
* **Go**: high‑throughput, real‑time, gateway concerns
* **db/**: module‑owned schema only

No module may write migrations for core tables.

---

## 3. Allowed Integration Mechanisms

Modules may integrate with Continuum **only** via the mechanisms below.

### 3.1 Core APIs

Modules may call **public, stable core APIs** such as:

* `GET /projects`
* `GET /artefacts/{id}`
* `GET /users/{id}`

Modules must not rely on undocumented endpoints.

---

### 3.2 Event Subscription (Preferred)

Modules should react to platform activity by subscribing to events.

Examples:

* `ProjectCreated`
* `ArtefactCreated`
* `UsageRecorded`

Events are immutable and replayable.

---

### 3.3 Event Emission

Modules may emit **module‑scoped events** (namespaced by module):

* `Kanban.BoardUpdated`
* `Billing.InvoiceGenerated`

Modules must **not** emit core events.

---

## 4. Data Ownership & Persistence

### 4.1 Ownership Rules

| Data          | Owner  |
| ------------- | ------ |
| Projects      | Core   |
| Artefacts     | Core   |
| Users & Roles | Core   |
| Module Tables | Module |

Modules must never:

* write to core tables
* assume core schema internals

---

### 4.2 Referential Linking

Modules may reference core entities **by ID only**:

* `project_id`
* `artefact_id`
* `user_id`

Foreign keys across ownership boundaries are discouraged; soft references are preferred.

---

## 5. Permissions & Security

### 5.1 Identity

Modules must rely on **core identity**.

No module‑specific authentication systems are allowed.

---

### 5.2 Authorisation

Modules may define **capabilities**, but enforcement is delegated to the core.

Example:

> `kanban:edit` on project X

The core resolves role → capability → decision.

---

## 6. Event Handling Pattern

### 6.1 Event Consumption Flow

```
Core Event Stream
        ↓
Module Event Handler
        ↓
Domain Logic
        ↓
State Projection (module DB)
```

Handlers must be:

* idempotent
* retry‑safe
* order‑aware where necessary

---

### 6.2 Failure Handling

If a module fails to process an event:

* the core must continue
* the event remains replayable

Modules are responsible for catch‑up and reconciliation.

---

## 7. Semantic Intelligence Usage

Modules may:

* request embeddings for module artefacts
* query semantic search via core APIs

Modules must not:

* embed data directly into Qdrant
* bypass embedding versioning

This preserves explainability and provenance.

---

## 8. Observability Requirements

Every module must expose:

* health checks
* structured logs
* minimal metrics

Modules participate in, but do not control, the platform observability stack.

---

## 9. Example Modules

### 9.1 Kanban Module

**Consumes:**

* `ProjectCreated`
* `ArtefactLinked`

**Emits:**

* `Kanban.BoardUpdated`

**Owns:**

* boards
* columns
* cards

---

### 9.2 Contract Module

**Consumes:**

* `RepoLinked`
* `ArtefactVersioned`

**Emits:**

* `Contract.VersionAdded`

**Owns:**

* contracts
* clauses

---

### 9.3 Billing Module

**Consumes:**

* `UsageRecorded`

**Emits:**

* `Billing.InvoiceGenerated`

**Owns:**

* invoices
* pricing rules

---

## 10. Versioning & Compatibility

Modules must declare:

* compatible core versions
* supported event versions

Breaking changes require a major version bump.

---

## 11. Testing Expectations

Modules should include:

* unit tests for domain logic
* contract tests for core APIs
* replay tests for event handling

---

## 12. Summary

Modules extend Continuum without redefining it.

If in doubt:

* prefer events over calls
* prefer soft coupling over shared state
* prefer clarity over convenience

A good module can be removed without regret.
