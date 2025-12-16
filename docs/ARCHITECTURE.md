# Continuum — Architecture

This document defines the **architectural principles, system boundaries, and extension model** of **Continuum**.

Continuum is designed as a **platform**, not a single application. Its primary purpose is to explore and implement:

* distributed system design
* semantic intelligence via vector embeddings
* real‑time collaborative state
* strong auditability and traceability

Business‑oriented functionality (e.g. Kanban boards, contract management, billing) exists only as **modules** that exercise the platform under realistic constraints.

---

## 1. Core Architectural Principles

### 1.1 Platform > Product

Continuum provides *capabilities*, not workflows.

* The **core** defines how systems behave.
* **Modules** demonstrate what can be built on top.

If a module is removed, the core must continue to function unchanged.

---

### 1.2 Explicit Boundaries

Every concern has an explicit boundary:

* **Core**: system primitives
* **Modules**: optional domain logic
* **Shared**: contracts and schemas only

There are **no implicit dependencies**.

---

### 1.3 Event‑Driven by Default

State changes are expressed as **events**, not side‑effects.

Events are:

* immutable
* append‑only
* replayable
* inspectable

This enables:

* auditability
* deterministic replay
* loose coupling between subsystems

---

### 1.4 AI as Representation, Not Authority

LLMs are used only to:

* encode semantic meaning (embeddings)
* summarise retrieved artefacts

They **never**:

* decide truth
* filter authoritative data
* mutate system state

---

## 2. Repository Structure (Authoritative)

```
backend-microservices/
├── core/
│   ├── backend-go/          # high‑throughput, infra‑adjacent services
│   └── backend-python/      # orchestration, semantics, storage
├── modules/                 # optional reference implementations
└── shared/                  # schemas, APIs, event definitions
```

### 2.1 Core

The core contains **non‑negotiable platform primitives**:

* artefacts (projects, diagrams, contracts)
* semantic ingestion & retrieval
* event emission
* identity & permissions
* audit logging

The core **must not** import from `modules/`.

---

### 2.2 Modules

Modules:

* depend on the core
* subscribe to events
* own their own data
* are removable at runtime

Examples:

* Kanban planning
* Contract lifecycle
* Billing

---

### 2.3 Shared

`shared/` contains **contracts**, not logic.

Allowed:

* event schemas
* OpenAPI / protobuf definitions
* canonical data formats

Forbidden:

* persistence code
* business logic
* LLM usage

---

## 3. Core System Domains

### 3.1 Artefacts

An **artefact** is any versioned, inspectable object:

* diagrams
* documents
* Git commits
* contracts

Artefacts are immutable once created; new versions form explicit graphs.

---

### 3.2 Semantic Intelligence

Artefacts may be semantically indexed via:

* deterministic chunking
* LLM‑based embeddings
* vector storage (Qdrant)

Every vector is traceable to:

* an artefact ID
* an artefact version
* an embedding model version

---

### 3.3 Real‑Time State

Shared mutable state (e.g. boards) is handled via:

* event sourcing
* deterministic reducers
* explicit conflict resolution

---

## 4. Event System

Events are the **primary integration mechanism** between the core and modules.

### 4.1 Event Characteristics

* Immutable
* Append‑only
* JSON (initially)
* Versioned

---

### 4.2 Canonical Event Envelope

```json
{
  "event_id": "uuid",
  "event_type": "ArtefactCreated",
  "event_version": 1,
  "occurred_at": "2025-01-01T12:00:00Z",
  "actor": {
    "user_id": "uuid",
    "role": "editor"
  },
  "entity": {
    "type": "diagram",
    "id": "uuid"
  },
  "payload": {},
  "metadata": {
    "source": "core",
    "correlation_id": "uuid"
  }
}
```

The envelope is stable; payloads evolve via `event_version`.

---

### 4.3 Core Event Types (Initial)

| Event             | Purpose                  |
| ----------------- | ------------------------ |
| ProjectCreated    | New project boundary     |
| ArtefactCreated   | Immutable artefact added |
| ArtefactVersioned | New version of artefact  |
| RepoLinked        | Git repository attached  |
| DiagramUpdated    | Diagram semantic change  |
| SemanticIndexed   | Embedding generated      |
| AccessGranted     | Permission change        |
| UsageRecorded     | Measurable system usage  |

---

## 5. Module Implementation Model

### 5.1 What a Module Is

A module is a **consumer of platform capabilities**.

It:

* subscribes to events
* calls core APIs
* owns its domain logic and tables

It does **not**:

* mutate core state directly
* bypass permissions
* depend on core internals

---

### 5.2 Example: Kanban Module

**Responsibilities**

* board state
* card ordering
* workflow transitions

**Integration points**

* subscribes to `ProjectCreated`
* emits `BoardUpdated`
* links cards to artefact IDs

**Data ownership**

* boards, columns, cards

---

### 5.3 Example: Billing Module

**Responsibilities**

* usage aggregation
* pricing logic
* invoice generation

**Integration points**

* subscribes to `UsageRecorded`
* queries `GET /projects`
* emits `InvoiceGenerated`

**Data ownership**

* invoices
* pricing plans

---

## 6. Data Ownership Rules

| Data      | Owner           |
| --------- | --------------- |
| Users     | Core            |
| Projects  | Core            |
| Artefacts | Core            |
| Events    | Core            |
| Boards    | Kanban module   |
| Contracts | Contract module |
| Invoices  | Billing module  |

No table is shared between owners.

---

## 7. Open‑Source Strategy

Open by default:

* core services
* semantic pipeline
* event schemas
* reference modules

Private / restricted:

* secrets
* deployment credentials
* environment‑specific config

---

## 8. Future Extensions (Explicitly Out of Scope)

* autonomous agents
* LLM‑driven decision making
* hard real‑time control
* payment processing

These may be explored as **external clients**, not core features.

---

## 9. Summary

Continuum is intentionally conservative in its core and permissive at its edges.

This architecture ensures:

* research credibility
* long‑term maintainability
* clean extensibility
* safe open‑source collaboration

Modules add value.
The core defines behaviour.
