# Continuum — Core API Specification

This document defines the **stable, public APIs exposed by the Continuum core**.

These APIs are the **only supported integration surface** for:

* modules (Kanban, Contracts, Billing, etc.)
* external services
* research experiments and tooling

They are intentionally conservative, explicit, and boring.

---

## 1. Design Goals

The Core API is designed to:

* expose authoritative system state
* preserve strict ownership boundaries
* support event‑driven and request‑driven integration
* remain stable across module evolution

The Core API **does not**:

* embed business workflows
* provide UI‑specific endpoints
* expose internal persistence models

---

## 2. API Stability Contract

### 2.1 Stability Levels

| Level            | Meaning                          |
| ---------------- | -------------------------------- |
| **Stable**       | Backwards‑compatible, long‑lived |
| **Experimental** | May change without notice        |

Only **Stable** endpoints may be used by modules.

---

### 2.2 Versioning

* Versioned via URL prefix: `/api/v1/`
* Breaking changes require a new major version

---

## 3. Authentication & Identity

All Core APIs require authentication.

### 3.1 Identity Model

* Users are globally unique
* Identity resolution is handled by the core
* Modules must not implement custom auth

### 3.2 Request Context

Every request is executed with:

* `user_id`
* `roles`
* `capabilities`

Capabilities are evaluated centrally.

---

## 4. Projects API (Stable)

### 4.1 List Projects

```
GET /api/v1/projects
```

Returns projects visible to the caller.

**Response (example):**

```json
[
  {
    "id": "uuid",
    "name": "Continuum",
    "created_at": "2025-01-01T12:00:00Z"
  }
]
```

---

### 4.2 Get Project

```
GET /api/v1/projects/{project_id}
```

Returns authoritative project metadata.

---

## 5. Artefacts API (Stable)

Artefacts are immutable, versioned entities.

### 5.1 Create Artefact

```
POST /api/v1/artefacts
```

**Request:**

```json
{
  "project_id": "uuid",
  "type": "diagram",
  "metadata": {
    "name": "System Architecture"
  }
}
```

---

### 5.2 Get Artefact

```
GET /api/v1/artefacts/{artefact_id}
```

Returns artefact metadata and current version.

---

### 5.3 Add Artefact Version

```
POST /api/v1/artefacts/{artefact_id}/versions
```

Creates a new immutable version.

---

## 6. Git Integration API (Stable)

### 6.1 Link Repository

```
POST /api/v1/projects/{project_id}/repos
```

Links a Git repository to a project.

---

### 6.2 List Linked Repositories

```
GET /api/v1/projects/{project_id}/repos
```

---

## 7. Semantic Intelligence API (Stable)

### 7.1 Request Semantic Indexing

```
POST /api/v1/semantic/index
```

Requests embedding generation for an artefact version.

**Request:**

```json
{
  "artefact_id": "uuid",
  "version_id": "uuid"
}
```

---

### 7.2 Semantic Search

```
POST /api/v1/semantic/search
```

**Request:**

```json
{
  "query": "authentication flow",
  "filters": {
    "artefact_type": "diagram"
  }
}
```

**Response:**

```json
{
  "results": [
    {
      "artefact_id": "uuid",
      "score": 0.91,
      "explanation": {
        "model": "embedding-v1",
        "matched_chunks": ["chunk-3"]
      }
    }
  ]
}
```

---

## 8. Events API (Stable)

Modules and external systems consume events via this API.

### 8.1 List Events

```
GET /api/v1/events
```

Supports filtering by:

* event type
* time range
* entity ID

---

### 8.2 Event Replay

```
GET /api/v1/events/replay
```

Allows consumers to replay historical events.

---

## 9. Permissions API (Stable)

### 9.1 Check Capability

```
POST /api/v1/permissions/check
```

**Request:**

```json
{
  "capability": "kanban:edit",
  "project_id": "uuid"
}
```

**Response:**

```json
{ "allowed": true }
```

---

## 10. Audit & Observability API (Stable)

### 10.1 Audit Log

```
GET /api/v1/audit
```

Returns structured, immutable audit events.

---

### 10.2 Metrics (Read‑Only)

```
GET /api/v1/metrics
```

Exposes system metrics for observability.

---

## 11. Experimental APIs

Experimental APIs are prefixed with:

```
/api/v1/experimental/
```

Modules must not depend on these endpoints.

---

## 12. What the Core API Will Never Do

The Core API will not:

* execute business workflows
* expose module data
* accept free‑form LLM prompts
* mutate state without emitting events

---

## 13. Summary

The Core API defines **what is knowable and authoritative** in Continuum.

If an integration cannot be expressed via these APIs or the event stream, it does not belong in the core.
