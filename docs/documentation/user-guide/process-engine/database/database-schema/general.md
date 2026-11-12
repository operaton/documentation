---
last_updated: 2026-11-11
schema_version: 7.25
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
| NAME_ | VARCHAR(64) | PK NOT NULL | Property name (e.g., `next.dbid`, `historyLevel`) |
| VALUE_ | VARCHAR(300) | NULL | Property value |
| REV_ | INTEGER | NULL | Revision for optimistic locking |

**Standard Properties:**

| Name | Purpose |
|------|---------|
| `schema.version` | Legacy marker, always `fox`. It does not hold the schema version; use `ACT_GE_SCHEMA_LOG` instead |
| `schema.history` | Legacy marker (`create(fox)`) |
| `next.dbid` | Start of the next ID block handed out by the `DbIdGenerator` |
| `historyLevel` | ID of the history level the engine was first started with (`0`=none, `1`=activity, `2`=audit, `3`=full) |
| `deployment.lock` | Exclusive lock row that serializes deployments across cluster nodes |
| `history.cleanup.job.lock` | Exclusive lock row used when creating the history cleanup jobs |
| `startup.lock` | Exclusive lock row used during engine bootstrap (e.g., setting the history level) |
| `installationId.lock` | Exclusive lock row used while generating the installation ID |
| `operaton.installation.id` | Unique ID of this installation, created on first start |

**Example Queries:**

```sql
-- Configured history level
SELECT VALUE_ FROM ACT_GE_PROPERTY WHERE NAME_ = 'historyLevel';

-- All properties with revision
SELECT NAME_, VALUE_, REV_ FROM ACT_GE_PROPERTY ORDER BY NAME_;
```

---

## ACT_GE_BYTEARRAY

**Purpose:** Central repository for all binary data — BPMN/DMN/CMMN XML files, process diagrams, form definitions, serialized variable values, job and external task exception stack traces, batch configurations, task attachments, and user pictures. Deployment artifacts are linked via `DEPLOYMENT_ID_`; all other rows are referenced by ID from the owning table (e.g., `ACT_RU_VARIABLE.BYTEARRAY_ID_`).

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Unique identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| NAME_ | VARCHAR(255) | NULL | Resource filename, variable name, or an engine-assigned name (e.g., `job.exceptionByteArray`) |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → [ACT_RE_DEPLOYMENT](repository.md#act_re_deployment) | Associated deployment; NULL for runtime and history data |
| BYTES_ | BYTEA | NULL | Binary content |
| GENERATED_ | BOOLEAN | NULL | Marks resources generated during deployment rather than deployed by the user; the engine writes `false` for deployment resources and leaves it NULL for runtime and history data |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| TYPE_ | INTEGER | NULL | Resource type: `1`=repository, `2`=runtime, `3`=history |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation timestamp |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance (set for history data only; used by the history cleanup) |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Time after which the history cleanup deletes the row (history data only) |

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
- Without FK constraint: `ACT_RU_BATCH.CONFIGURATION_`, `ACT_HI_VARINST.BYTEARRAY_ID_`, `ACT_HI_DETAIL.BYTEARRAY_ID_`, `ACT_HI_DEC_IN.BYTEARRAY_ID_`, `ACT_HI_DEC_OUT.BYTEARRAY_ID_`, `ACT_HI_JOB_LOG.JOB_EXCEPTION_STACK_ID_`, `ACT_HI_EXT_TASK_LOG.ERROR_DETAILS_ID_`, `ACT_HI_ATTACHMENT.CONTENT_ID_`, and `ACT_ID_INFO.VALUE_` (user picture entry)

**Example Queries:**

```sql
-- Binary data for a deployment
SELECT ID_, NAME_, GENERATED_, CREATE_TIME_, octet_length(BYTES_) AS size_bytes
FROM ACT_GE_BYTEARRAY
WHERE DEPLOYMENT_ID_ = 'deployment-id'
ORDER BY CREATE_TIME_ DESC;

-- Number and size of entries per resource type
SELECT TYPE_, COUNT(*) AS entries, SUM(octet_length(BYTES_)) AS total_bytes
FROM ACT_GE_BYTEARRAY
GROUP BY TYPE_;

-- Data scheduled for removal
SELECT ID_, NAME_, REMOVAL_TIME_
FROM ACT_GE_BYTEARRAY
WHERE REMOVAL_TIME_ IS NOT NULL AND REMOVAL_TIME_ > CURRENT_TIMESTAMP
ORDER BY REMOVAL_TIME_;
```

---

## ACT_GE_SCHEMA_LOG

**Purpose:** Immutable log of schema migration events. Each row records the schema creation or a version upgrade with a timestamp, enabling operators to verify and audit schema history.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry identifier |
| TIMESTAMP_ | TIMESTAMP | NULL | When the schema change was applied |
| VERSION_ | VARCHAR(255) | NULL | Schema version string (e.g., `7.25.0`) |

**Example Queries:**

```sql
-- Full migration history (newest first)
SELECT ID_, TIMESTAMP_, VERSION_
FROM ACT_GE_SCHEMA_LOG
ORDER BY TIMESTAMP_ DESC;

-- Current schema version
SELECT VERSION_, TIMESTAMP_
FROM ACT_GE_SCHEMA_LOG
ORDER BY TIMESTAMP_ DESC
LIMIT 1;
```

---

## Design Notes

- The `next.dbid` property must not be modified manually — the `DbIdGenerator` uses it to hand out unique ID blocks.
- The `*.lock` properties carry no data. The engine locks these rows to serialize cluster-wide operations.
- `ACT_GE_BYTEARRAY` serves dual purposes: deployment artifacts (keyed by `DEPLOYMENT_ID_`) and runtime/history data (history rows keyed by `ROOT_PROC_INST_ID_`). Query performance is optimised via separate indexes for each use case.
- The history cleanup deletes `ACT_GE_BYTEARRAY` rows of history data once their `REMOVAL_TIME_` has passed. Do not delete rows manually.

---

See [Database-Specific Implementation Notes](index.md#database-specific-implementation-notes) for type mappings across PostgreSQL, MySQL/MariaDB, Oracle, MSSQL, H2, and DB2.

---

**Last Updated:** 2026-11-11 | **Schema Version:** 7.25 | **Operaton Versions:** 1.0.0+
