---
last_updated: 2026-07-03
schema_version: 7.24
---

# Repository (RE_)

Repository tables store immutable definitions — process models, case models, decision tables, form definitions, and their deployment containers. Definitions are never modified after deployment; new deployments create new versions.

## Tables

- **[`ACT_RE_DEPLOYMENT`](#act_re_deployment)** — Deployment container
- **[`ACT_RE_PROCDEF`](#act_re_procdef)** — Process definitions (BPMN)
- **[`ACT_RE_CAMFORMDEF`](#act_re_camformdef)** — Camunda form definitions
- **[`ACT_RE_CASE_DEF`](#act_re_case_def)** — Case definitions (CMMN)
- **[`ACT_RE_DECISION_DEF`](#act_re_decision_def)** — Decision definitions (DMN)
- **[`ACT_RE_DECISION_REQ_DEF`](#act_re_decision_req_def)** — Decision requirement definitions (DRG)

---

## ACT_RE_DEPLOYMENT

**Purpose:** Immutable container grouping related artifacts (BPMN, DMN, CMMN, forms) deployed together. All definitions in a deployment share the same `DEPLOYMENT_ID_`.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Deployment identifier |
| NAME_ | VARCHAR(255) | NULL | Human-readable deployment name |
| DEPLOY_TIME_ | TIMESTAMP | NOT NULL | When deployment occurred |
| SOURCE_ | VARCHAR(255) | NULL | Deployment origin (e.g., `api`, filename) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_DEPLOYMENT_NAME`, `ACT_IDX_DEPLOYMENT_TENANT_ID`

**Referenced by:** ACT_RE_PROCDEF, ACT_RE_CAMFORMDEF, ACT_RE_CASE_DEF, ACT_RE_DECISION_DEF, ACT_RE_DECISION_REQ_DEF, ACT_GE_BYTEARRAY

**Example Queries:**

```sql
-- All deployments, newest first
SELECT ID_, NAME_, DEPLOY_TIME_, SOURCE_, TENANT_ID_
FROM ACT_RE_DEPLOYMENT
ORDER BY DEPLOY_TIME_ DESC;

-- Deployment with all its process definitions
SELECT d.ID_, d.NAME_, d.DEPLOY_TIME_,
       p.ID_ AS procdef_id, p.KEY_, p.NAME_ AS proc_name, p.VERSION_
FROM ACT_RE_DEPLOYMENT d
LEFT JOIN ACT_RE_PROCDEF p ON d.ID_ = p.DEPLOYMENT_ID_
WHERE d.ID_ = 'deployment-id'
ORDER BY p.KEY_, p.VERSION_;

-- Latest deployment per tenant
SELECT TENANT_ID_, ID_, NAME_, DEPLOY_TIME_
FROM ACT_RE_DEPLOYMENT d1
WHERE DEPLOY_TIME_ = (
  SELECT MAX(DEPLOY_TIME_) FROM ACT_RE_DEPLOYMENT d2
  WHERE d2.TENANT_ID_ = d1.TENANT_ID_
)
ORDER BY TENANT_ID_;
```

---

## ACT_RE_PROCDEF

**Purpose:** Stores BPMN process definition versions. Same `KEY_` with incrementing `VERSION_` coexist; running instances reference their definition by `ID_`. Definitions are immutable once deployed.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Internal unique ID for this version |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CATEGORY_ | VARCHAR(255) | NULL | Namespace/category |
| NAME_ | VARCHAR(255) | NULL | Display name |
| KEY_ | VARCHAR(255) | NOT NULL | Logical process key |
| VERSION_ | INTEGER | NOT NULL | Version number |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Containing deployment |
| RESOURCE_NAME_ | VARCHAR(4000) | NULL | BPMN resource filename |
| DGRM_RESOURCE_NAME_ | VARCHAR(4000) | NULL | Diagram resource filename |
| HAS_START_FORM_KEY_ | BOOLEAN | NULL | Start event has a form |
| SUSPENSION_STATE_ | INTEGER | NULL | `0`=active, `1`=suspended |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| VERSION_TAG_ | VARCHAR(64) | NULL | Optional version label |
| HISTORY_TTL_ | INTEGER | NULL | History retention in days (NULL=indefinite) |
| STARTABLE_ | BOOLEAN | NOT NULL DEFAULT TRUE | Can new instances be started |

**Indexes:** `ACT_IDX_PROCDEF_DEPLOYMENT_ID`, `ACT_IDX_PROCDEF_TENANT_ID`, `ACT_IDX_PROCDEF_VER_TAG`

**Example Queries:**

```sql
-- Latest active version of all process definitions
SELECT ID_, KEY_, NAME_, VERSION_, DEPLOYMENT_ID_
FROM ACT_RE_PROCDEF p1
WHERE SUSPENSION_STATE_ = 0
  AND (KEY_, VERSION_) IN (
    SELECT KEY_, MAX(VERSION_) FROM ACT_RE_PROCDEF
    WHERE SUSPENSION_STATE_ = 0 GROUP BY KEY_
  )
ORDER BY KEY_;

-- Version history for a process key
SELECT ID_, KEY_, VERSION_, DEPLOYMENT_ID_, VERSION_TAG_, SUSPENSION_STATE_
FROM ACT_RE_PROCDEF
WHERE KEY_ = 'invoice_approval'
ORDER BY VERSION_ DESC;

-- Count running instances per definition
SELECT p.KEY_, p.VERSION_, COUNT(e.ID_) AS running_instances
FROM ACT_RE_PROCDEF p
LEFT JOIN ACT_RU_EXECUTION e ON p.ID_ = e.PROC_DEF_ID_
  AND e.PROC_INST_ID_ = e.ID_
WHERE p.SUSPENSION_STATE_ = 0
GROUP BY p.KEY_, p.VERSION_
ORDER BY running_instances DESC;
```

---

## ACT_RE_CAMFORMDEF

**Purpose:** Form definitions for user task rendering. Forms are versioned independently by `KEY_`/`VERSION_` and linked to a deployment.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Form definition identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| KEY_ | VARCHAR(255) | NOT NULL | Form key |
| VERSION_ | INTEGER | NOT NULL | Version number |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Containing deployment |
| RESOURCE_NAME_ | VARCHAR(4000) | NULL | Form resource filename |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Example Queries:**

```sql
-- Latest version of a form
SELECT ID_, KEY_, VERSION_, DEPLOYMENT_ID_, RESOURCE_NAME_
FROM ACT_RE_CAMFORMDEF
WHERE KEY_ = 'approval_form'
ORDER BY VERSION_ DESC LIMIT 1;

-- All forms in a deployment
SELECT ID_, KEY_, VERSION_, RESOURCE_NAME_
FROM ACT_RE_CAMFORMDEF
WHERE DEPLOYMENT_ID_ = 'deployment-id'
ORDER BY KEY_, VERSION_ DESC;
```

---

## ACT_RE_CASE_DEF

**Purpose:** CMMN case definition versions. Cases support flexible, non-linear execution with stages and milestones.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Internal unique ID |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CATEGORY_ | VARCHAR(255) | NULL | Namespace/category |
| NAME_ | VARCHAR(255) | NULL | Display name |
| KEY_ | VARCHAR(255) | NOT NULL | Logical case key |
| VERSION_ | INTEGER | NOT NULL | Version number |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Containing deployment |
| RESOURCE_NAME_ | VARCHAR(4000) | NULL | CMMN resource filename |
| DGRM_RESOURCE_NAME_ | VARCHAR(4000) | NULL | Diagram resource filename |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| HISTORY_TTL_ | INTEGER | NULL | History retention in days |

**Indexes:** `ACT_IDX_CASE_DEF_TENANT_ID`

**Example Queries:**

```sql
-- All case definition versions
SELECT ID_, KEY_, NAME_, VERSION_, DEPLOYMENT_ID_
FROM ACT_RE_CASE_DEF
ORDER BY KEY_, VERSION_ DESC;
```

---

## ACT_RE_DECISION_DEF

**Purpose:** DMN decision table definition versions. Decisions are invoked from process/case activities or directly via the decision service.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Internal unique ID |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CATEGORY_ | VARCHAR(255) | NULL | Namespace/category |
| NAME_ | VARCHAR(255) | NULL | Display name |
| KEY_ | VARCHAR(255) | NOT NULL | Logical decision key |
| VERSION_ | INTEGER | NOT NULL | Version number |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Containing deployment |
| RESOURCE_NAME_ | VARCHAR(4000) | NULL | DMN resource filename |
| DGRM_RESOURCE_NAME_ | VARCHAR(4000) | NULL | Diagram resource filename |
| DEC_REQ_ID_ | VARCHAR(64) | FK → ACT_RE_DECISION_REQ_DEF | Parent DRG (NULL if standalone) |
| DEC_REQ_KEY_ | VARCHAR(255) | NULL | Parent DRG key (denormalized) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| HISTORY_TTL_ | INTEGER | NULL | History retention in days |
| VERSION_TAG_ | VARCHAR(64) | NULL | Optional version label |

**Indexes:** `ACT_IDX_DEC_DEF_TENANT_ID`, `ACT_IDX_DEC_DEF_REQ_ID`

**Example Queries:**

```sql
-- Latest version of each decision
SELECT d1.ID_, d1.KEY_, d1.NAME_, d1.VERSION_, d1.DEPLOYMENT_ID_
FROM ACT_RE_DECISION_DEF d1
WHERE d1.VERSION_ = (
  SELECT MAX(d2.VERSION_) FROM ACT_RE_DECISION_DEF d2
  WHERE d2.KEY_ = d1.KEY_ AND d2.TENANT_ID_ IS NOT DISTINCT FROM d1.TENANT_ID_
)
ORDER BY d1.KEY_;

-- Decisions within a DRG
SELECT ID_, KEY_, NAME_, VERSION_
FROM ACT_RE_DECISION_DEF
WHERE DEC_REQ_ID_ = 'drg-id'
ORDER BY KEY_;
```

---

## ACT_RE_DECISION_REQ_DEF

**Purpose:** Decision Requirement Graph (DRG) — a collection of related decisions with their dependencies. A DRG groups multiple `ACT_RE_DECISION_DEF` entries.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Internal unique ID |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CATEGORY_ | VARCHAR(255) | NULL | Namespace/category |
| NAME_ | VARCHAR(255) | NULL | Display name |
| KEY_ | VARCHAR(255) | NOT NULL | Logical DRG key |
| VERSION_ | INTEGER | NOT NULL | Version number |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Containing deployment |
| RESOURCE_NAME_ | VARCHAR(4000) | NULL | DMN resource filename |
| DGRM_RESOURCE_NAME_ | VARCHAR(4000) | NULL | Diagram resource filename |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_DEC_REQ_DEF_TENANT_ID`

**Example Queries:**

```sql
-- DRGs and their decisions
SELECT r.KEY_ AS drg_key, r.VERSION_ AS drg_version,
       d.KEY_ AS decision_key, d.VERSION_ AS decision_version
FROM ACT_RE_DECISION_REQ_DEF r
JOIN ACT_RE_DECISION_DEF d ON r.ID_ = d.DEC_REQ_ID_
ORDER BY r.KEY_, d.KEY_;
```

---

## Design Notes

- **Versioning**: Definitions are immutable; redeployment creates a new row with an incremented `VERSION_`. Running instances always reference their original `ID_`, ensuring definition stability.
- **Suspension**: `ACT_RE_PROCDEF.SUSPENSION_STATE_ = 1` prevents new instances from being started without deleting the definition.
- **HISTORY_TTL_**: Sets the default retention period for history data. The cleanup job uses this to schedule removal of historical records.
- Binary content (BPMN/DMN XML, diagrams) is stored in `ACT_GE_BYTEARRAY`, referenced via `RESOURCE_NAME_` + `DEPLOYMENT_ID_`.

---

See [Database-Specific Implementation Notes](../index.md#database-specific-implementation-notes) for type mappings.

---

**Last Updated:** 2026-07-03 | **Schema Version:** 7.24 | **Operaton Versions:** 1.0.0+
