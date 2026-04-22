# Design Document

## Clinical Care Plan Generation System (v1)

---

# 1. Overview

### 1.1 Background

Specialty pharmacy pharmacists currently spend **20–40 minutes per patient** manually generating care plans required for:

- Medicare compliance
- Pharma reimbursement

Due to staffing shortages, this process is a **critical bottleneck**.

---

### 1.2 Goal

Build an internal web-based system that:

> **automatically generates compliant care plans from structured + unstructured patient data**

while ensuring:

- Data integrity
- Duplicate prevention
- Safe clinical workflow
- Export for reporting

---

### 1.3 Non-Goals (v1)

- Full EHR integration
- Autonomous clinical decision-making
- Multi-agent orchestration
- Real-time provider system sync

---

# 2. Users & Workflow

### 2.1 Users

- Medical Assistants (data entry)
- Pharmacists (review + finalize)

Patients do **NOT** interact with system

---

### 2.2 Workflow

```text
1. Medical assistant inputs patient + order info
2. System validates all fields
3. System checks duplicates
   → ERROR → block
   → WARNING → user confirm
4. System calls LLM to generate care plan
5. Pharmacist reviews (optional edit)
6. Export / download care plan
7. Data stored for reporting
```

---

# 3. Functional Requirements

---

## 3.1 Input Form

### Required Fields

| Field                | Type              |
| -------------------- | ----------------- |
| First Name           | string            |
| Last Name            | string            |
| DOB                  | date              |
| MRN                  | string (unique)   |
| Provider Name        | string            |
| Provider NPI         | string (10-digit) |
| Primary Diagnosis    | ICD-10            |
| Additional Diagnoses | list              |
| Medication Name      | string            |
| Medication History   | list              |
| Patient Records      | text OR PDF       |

---

## 3.2 Validation Layer (Hard Requirement)

### Field Validation

| Field                              | Rule                                     |
| ---------------------------------- | ---------------------------------------- |
| MRN（Medical Record Number）       | unique, fixed length (TBD: 6 vs 8 digit) |
| NPI (National Provider Identifier) | 10-digit numeric                         |
| ICD-10                             | valid format                             |
| Medication                         | non-empty                                |
| DOB                                | valid date                               |

---

### System-Level Validation

- Provider uniqueness enforced via **NPI**
- Required fields must be present
- PDF must be valid format (if uploaded)

---

## 3.3 Duplicate Detection Engine

### Purpose

Prevent:

- duplicate orders
- duplicate patients
- inconsistent provider data

---

### Rules

#### HARD ERRORS (block submission)

1. Same patient + same medication + same day
   → definite duplicate order

2. Same NPI + different provider name
   → data inconsistency

---

#### WARNINGS (user can override)

1. Same patient + same medication + different day
   → likely refill

2. Same MRN + different name or DOB
   → possible data entry error

3. Same name + DOB + different MRN
   → possible duplicate patient

---

### Warning Handling

- Must display reason
- Requires explicit user confirmation
- Must log:
  - user_id
  - timestamp
  - override reason (optional)

---

## 3.4 Care Plan Generation (LLM)

### Input to LLM

- Patient demographics
- Diagnoses (ICD-10)
- Medication
- Medication history
- Clinical notes (text/PDF)

---

### Output Requirements

Care plan MUST include:

- Problem list / DTPs
- Goals (SMART)
- Pharmacist interventions
- Monitoring plan

---

### Output Format (recommended)

```json
{
  "problems": [],
  "goals": [],
  "interventions": [],
  "monitoring": []
}
```

👉 Enables:

- validation
- export
- testing

---

### Post-processing

- Convert JSON → formatted text/PDF
- Allow optional pharmacist editing

---

## 3.5 Export & Reporting

### Required

- Download care plan (text or PDF)
- Export data for pharma reporting

---

# 4. System Architecture

---

## 4.1 High-Level Architecture

```text
Frontend (Web Form)
    ↓
Backend API (FastAPI)
    ↓
Validation Layer
    ↓
Duplicate Detection Engine
    ↓
LLM Service
    ↓
Database (Postgres)
    ↓
Export Service
```

---

## 4.2 Components

### 1. API Layer

- Handles requests
- Input validation
- Response formatting

---

### 2. Validation Module

- Field validation
- Schema enforcement

---

### 3. Duplicate Detection Engine

- Rule-based engine
- Query existing DB
- Returns:
  - ERROR
  - WARNING

---

### 4. LLM Service

- Prompt construction
- Response parsing
- Retry / fallback logic

---

### 5. Storage Layer

PostgreSQL tables:

- patients
- providers
- orders
- care_plans
- audit_logs

---

### 6. Export Module

- PDF/text generation
- Reporting format

---

# 5. Data Model

---

## Patient

```sql
id (PK)
first_name
last_name
dob
mrn (UNIQUE)
```

---

## Provider

```sql
id (PK)
name
npi (UNIQUE)
```

---

## Order

```sql
id (PK)
patient_id
provider_id
medication_name
primary_diagnosis
created_at
```

---

## CarePlan

```sql
id (PK)
order_id (UNIQUE)
content
created_at
```

---

## Audit Log

```sql
id
user_id
action
reason
timestamp
```

---

# 6. Error Handling Strategy

---

## ERROR (blocking)

- Prevent submission
- Return clear message
- Require correction

---

## WARNING (non-blocking)

- Show reason
- Require confirmation
- Log override

---

## LLM Errors

- Retry (1–2 times)
- Fallback template (optional)
- Return safe error message

---

# 7. Edge Cases

---

### 7.1 Duplicate MRN

- Reject OR flag (TBD)

---

### 7.2 Concurrent Submissions

- Use DB constraints
- Optional optimistic locking

---

### 7.3 Multiple Providers per Patient

- Allowed (assumption, confirm)

---

### 7.4 Multi-medication scenarios

- v1: one order = one medication

---

### 7.5 LLM hallucination risk

- Restrict output format
- Avoid autonomous decisions

---

# 8. Non-Functional Requirements

---

### Reliability

- Must not crash on bad input
- Graceful error handling

---

### Security

- No PHI leakage
- Access control (internal users only)

---

### Performance

- Care plan generation < 10 seconds target

---

### Auditability

- All warnings + overrides logged

---

# 9. Testing Strategy

---

### Unit Tests

- validation rules
- duplicate detection

---

### Integration Tests

- full flow: input → care plan

---

### Edge Case Tests

- duplicate scenarios
- malformed input
- LLM failure

---

# 10. MVP Scope (Phase 1)

---

### MUST HAVE

- Web form inpu
- Validation
- Duplicate detection
- LLM generation
- Download care plan
- Provider uniqueness

---

### NICE TO HAVE (Phase 2)

- PDF parsing
- Structured output UI
- Reporting dashboard
- Fuzzy matching

---

# 11. Open Questions (for client)

---

### Data & Validation

- MRN length: 6 or 8 digits?
- ICD-10 validation depth?
- NPI verification needed?

---

### Duplicate Logic

- Definition of “same day”?
- Medication normalization needed?

---

### Workflow

- Can pharmacist edit care plan?
- Is override justification required?

---

### Input

- PDF needs parsing or just storage?

---

# 12. Key Design Insight（

> **“a safety-critical workflow system with strict data validation and duplicate detection”**
