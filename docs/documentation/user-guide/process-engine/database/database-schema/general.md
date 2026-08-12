---
last_updated: 2026-07-03
schema_version: 7.24
---

# General (GE_)

General tables provide shared infrastructure: binary storage, system properties, and schema version tracking. All other domains depend on these tables.

## Tables

- **[`ACT_GE_PROPERTY`](#act_ge_property)** — System configuration key-value store
- **[`ACT_GE_BYTEARRAY`](#act_ge_bytearray)** — Binary object storage (BLOBs)
- **[`ACT_GE_SCHEMA_LOG`](#act_ge_schema_log)** — Schema migration history

---

## ACT_GE_PROPERTY

**Purpose:** Key-value store for engine configuration, distributed locks, and ID generation state. Uses optimistic locking (`REV_`) to safely handle concurrent updates across engine nodes.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| NAME_ | VARCHAR(64) | PK NOT NULL | Property name (e.g., `schema.version`, `id.next.value`) |
| VALUE_ | VARCHAR(300) | NULL | Property value |
| REV_ | INTEGER | NOT NULL DEFAULT 0 | Revision for optimistic locking |

**Standard Properties:**

| Name | Purpose |
|------|---------|
| `schema.version` | Current schema version (e.g., `7.24.0`) |
| `schema.history` | Migration history log |
| `id.next.value` | Engine-wide ID counter |
| `deployment.lock` | Distributed lock for deployments |
| `execution.lock` | Distributed lock for process execution |

**Example Queries:**

```sql
-- Current schema version
SELECT VALUE_ FROM ACT_GE_PROPERTY WHERE NAME_ = 'schema.version';

-- All properties with revision
SELECT NAME_, VALUE_, REV_ FROM ACT_GE_PROPERTY ORDER BY NAME_;

-- Safe update pattern (optimistic locking)
UPDATE ACT_GE_PROPERTY
SET VALUE_ = '7.25.0', REV_ = REV_ + 1
WHERE NAME_ = 'schema.version' AND REV_ = <expected_rev>;
```

---

## ACT_GE_BYTEARRAY

**Purpose:** Central repository for all binary data — BPMN/DMN/CMMN XML files, process diagrams, form definitions, serialized variable values, and job exception stack traces. Data is linked to a deployment (for artifacts) or a process instance (for runtime data).

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Unique identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| NAME_ | VARCHAR(255) | NULL | Name/description (filename or variable name) |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | Associated deployment; NULL for runtime data |
| BYTES_ | BYTEA | NULL | Binary content |
| GENERATED_ | BOOLEAN | NULL | `true` = system-generated (diagram); `false` = user-provided |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| TYPE_ | INTEGER | NULL | Type classifier (reserved) |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation timestamp |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance (for runtime variable/error data) |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled removal time (soft-delete marker) |

**Indexes:**

| Index | Columns | Purpose |
|-------|---------|---------|
| ACT_IDX_BYTEAR_DEPL | DEPLOYMENT_ID_ | Resources per deployment |
| ACT_IDX_BYTEARRAY_ROOT_PI | ROOT_PROC_INST_ID_ | Data per process instance |
| ACT_IDX_BYTEARRAY_RM_TIME | REMOVAL_TIME_ | History cleanup |
| ACT_IDX_BYTEARRAY_NAME | NAME_ | Search by name |

**Referenced by:**

- `ACT_RU_VARIABLE.BYTEARRAY_ID_` — binary variable values
- `ACT_RU_JOB.EXCEPTION_STACK_ID_` — job exception stack traces
- `ACT_RU_EXT_TASK.ERROR_DETAILS_ID_` — external task error details

**Example Queries:**

```sql
-- Binary data for a deployment
SELECT ID_, NAME_, GENERATED_, CREATE_TIME_, octet_length(BYTES_) AS size_bytes
FROM ACT_GE_BYTEARRAY
WHERE DEPLOYMENT_ID_ = 'deployment-id'
ORDER BY CREATE_TIME_ DESC;

-- Orphaned entries (no deployment and no process instance)
SELECT ID_, NAME_, CREATE_TIME_
FROM ACT_GE_BYTEARRAY
WHERE DEPLOYMENT_ID_ IS NULL AND ROOT_PROC_INST_ID_ IS NULL;

-- Data scheduled for removal
SELECT ID_, NAME_, REMOVAL_TIME_
FROM ACT_GE_BYTEARRAY
WHERE REMOVAL_TIME_ IS NOT NULL AND REMOVAL_TIME_ > CURRENT_TIMESTAMP
ORDER BY REMOVAL_TIME_;
```

---

## ACT_GE_SCHEMA_LOG

**Purpose:** Immutable log of schema migration events. Each row records a version upgrade with a timestamp, enabling operators to verify and audit schema history.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry identifier |
| TIMESTAMP_ | TIMESTAMP | NOT NULL | When the schema change was applied |
| VERSION_ | VARCHAR(255) | NOT NULL | Schema version string (e.g., `7.24.0`) |

**Example Queries:**

```sql
-- Full migration history (newest first)
SELECT ID_, TIMESTAMP_, VERSION_
FROM ACT_GE_SCHEMA_LOG
ORDER BY TIMESTAMP_ DESC;

-- When the current version was applied
SELECT TIMESTAMP_, VERSION_
FROM ACT_GE_SCHEMA_LOG
WHERE VERSION_ = '7.24.0'
ORDER BY TIMESTAMP_ DESC
LIMIT 1;
```

---

## Design Notes

- `ACT_GE_PROPERTY.id.next.value` must not be modified manually — the engine uses it as a global counter.
- `ACT_GE_BYTEARRAY` serves dual purposes: deployment artifacts (keyed by `DEPLOYMENT_ID_`) and runtime data (keyed by `ROOT_PROC_INST_ID_`). Query performance is optimised via separate indexes for each use case.
- Periodic cleanup of `ACT_GE_BYTEARRAY` rows where `REMOVAL_TIME_ < CURRENT_TIMESTAMP` reduces table bloat.

---

See [Database-Specific Implementation Notes](../index.md#database-specific-implementation-notes) for type mappings across PostgreSQL, MySQL/MariaDB, Oracle, MSSQL, H2, and DB2.

---

**Last Updated:** 2026-07-03 | **Schema Version:** 7.24 | **Operaton Versions:** 1.0.0+
