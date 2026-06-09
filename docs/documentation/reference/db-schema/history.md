---
last_updated: 2026-07-03
schema_version: 7.24
---

# History (HI_)

History tables store immutable audit records of completed processes, tasks, activities, variables, decisions, and operations. They are physically separate from runtime tables for query isolation and independent cleanup. History data is written as events occur and retained according to the `HISTORY_TTL_` configured on each definition.

## Tables

| Table | Purpose |
|-------|---------|
| [ACT_HI_PROCINST](#act_hi_procinst) | Historic process instances |
| [ACT_HI_ACTINST](#act_hi_actinst) | Historic activity instances |
| [ACT_HI_TASKINST](#act_hi_taskinst) | Historic task instances |
| [ACT_HI_VARINST](#act_hi_varinst) | Historic variable values |
| [ACT_HI_DETAIL](#act_hi_detail) | Historic variable change events |
| [ACT_HI_IDENTITYLINK](#act_hi_identitylink) | Historic identity link events |
| [ACT_HI_COMMENT](#act_hi_comment) | Task/process comments |
| [ACT_HI_ATTACHMENT](#act_hi_attachment) | Task/process attachments |
| [ACT_HI_OP_LOG](#act_hi_op_log) | Operator audit log |
| [ACT_HI_INCIDENT](#act_hi_incident) | Historic incidents |
| [ACT_HI_JOB_LOG](#act_hi_job_log) | Job execution log |
| [ACT_HI_BATCH](#act_hi_batch) | Historic batch operations |
| [ACT_HI_EXT_TASK_LOG](#act_hi_ext_task_log) | External task execution log |
| [ACT_HI_CASEINST](#act_hi_caseinst) | Historic case instances (CMMN) |
| [ACT_HI_CASEACTINST](#act_hi_caseactinst) | Historic case activity instances (CMMN) |
| [ACT_HI_DECINST](#act_hi_decinst) | Historic decision evaluations (DMN) |
| [ACT_HI_DEC_IN](#act_hi_dec_in) | Historic decision inputs (DMN) |
| [ACT_HI_DEC_OUT](#act_hi_dec_out) | Historic decision outputs (DMN) |

---

## ACT_HI_PROCINST

**Purpose:** Complete lifecycle record of a process instance from start to finish. Written at process completion or deletion. Includes timing metrics for SLA analysis.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | History record ID |
| PROC_INST_ID_ | VARCHAR(64) | NOT NULL UNIQUE | Runtime process instance ID |
| BUSINESS_KEY_ | VARCHAR(255) | NULL | External correlation key |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NOT NULL | Process definition ID |
| START_TIME_ | TIMESTAMP | NOT NULL | Start time |
| END_TIME_ | TIMESTAMP | NULL | End time (NULL = still active) |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| DURATION_ | BIGINT | NULL | Duration in milliseconds |
| START_USER_ID_ | VARCHAR(255) | NULL | User who started the instance |
| START_ACT_ID_ | VARCHAR(255) | NULL | Start event activity ID |
| END_ACT_ID_ | VARCHAR(255) | NULL | End event activity ID |
| SUPER_PROCESS_INSTANCE_ID_ | VARCHAR(64) | NULL | Parent process instance (call activity) |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root of nested subprocess hierarchy |
| SUPER_CASE_INSTANCE_ID_ | VARCHAR(64) | NULL | Parent case instance |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Associated case instance |
| DELETE_REASON_ | VARCHAR(4000) | NULL | Reason when deleted/cancelled |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| STATE_ | VARCHAR(255) | NULL | `COMPLETED`, `EXTERNALLY_TERMINATED`, `INTERNALLY_TERMINATED`, `ACTIVE` |
| RESTARTED_PROC_INST_ID_ | VARCHAR(64) | NULL | Original instance if this is a restart |

**Indexes:** `ACT_IDX_HI_PRO_INST_END`, `ACT_IDX_HI_PRO_I_BUSKEY`, `ACT_IDX_HI_PRO_INST_TENANT_ID`, `ACT_IDX_HI_PRO_INST_PROC_DEF_KEY`, `ACT_IDX_HI_PRO_INST_PROC_TIME`, `ACT_IDX_HI_PRO_INST_ROOT_PI`, `ACT_IDX_HI_PRO_INST_RM_TIME`

**Example Queries:**

```sql
-- SLA report: completed instances last 30 days
SELECT PROC_DEF_KEY_, COUNT(*) AS count,
       AVG(DURATION_) AS avg_ms,
       MAX(DURATION_) AS max_ms
FROM ACT_HI_PROCINST
WHERE STATE_ = 'COMPLETED'
  AND START_TIME_ >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY PROC_DEF_KEY_
ORDER BY avg_ms DESC;

-- Instances pending cleanup
SELECT ID_, PROC_DEF_KEY_, END_TIME_, REMOVAL_TIME_
FROM ACT_HI_PROCINST
WHERE REMOVAL_TIME_ < CURRENT_TIMESTAMP
ORDER BY REMOVAL_TIME_;
```

---

## ACT_HI_ACTINST

**Purpose:** History record for each individual activity execution (task, gateway, event, subprocess). Created when an activity starts; END_TIME_ set on completion.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Activity instance history ID |
| PARENT_ACT_INST_ID_ | VARCHAR(64) | NULL | Parent activity instance |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NOT NULL | Process definition ID |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NOT NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NOT NULL | Execution scope |
| ACT_ID_ | VARCHAR(255) | NOT NULL | Activity element ID |
| TASK_ID_ | VARCHAR(64) | NULL | Associated task ID |
| CALL_PROC_INST_ID_ | VARCHAR(64) | NULL | Called process instance (call activity) |
| CALL_CASE_INST_ID_ | VARCHAR(64) | NULL | Called case instance |
| ACT_NAME_ | VARCHAR(255) | NULL | Activity display name |
| ACT_TYPE_ | VARCHAR(255) | NOT NULL | Activity type (userTask, serviceTask, …) |
| ASSIGNEE_ | VARCHAR(255) | NULL | Assignee (for task activities) |
| START_TIME_ | TIMESTAMP | NOT NULL | Activity start time |
| END_TIME_ | TIMESTAMP | NULL | Activity end time |
| DURATION_ | BIGINT | NULL | Duration in milliseconds |
| ACT_INST_STATE_ | INTEGER | NULL | State: `0`=active, `1`=completed, `2`=cancelled |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Ordering counter |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_ACTINST_ROOT_PI`, `ACT_IDX_HI_ACT_INST_START_END`, `ACT_IDX_HI_ACT_INST_END`, `ACT_IDX_HI_ACT_INST_PROCINST`, `ACT_IDX_HI_ACT_INST_COMP`, `ACT_IDX_HI_ACT_INST_STATS`, `ACT_IDX_HI_ACT_INST_TENANT_ID`, `ACT_IDX_HI_ACT_INST_RM_TIME`

**Example Queries:**

```sql
-- Activity execution stats for a process definition
SELECT ACT_ID_, ACT_TYPE_, COUNT(*) AS executions,
       AVG(DURATION_) AS avg_ms, MAX(DURATION_) AS max_ms
FROM ACT_HI_ACTINST
WHERE PROC_DEF_KEY_ = 'invoice_approval'
  AND END_TIME_ IS NOT NULL
  AND START_TIME_ >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY ACT_ID_, ACT_TYPE_
ORDER BY avg_ms DESC;
```

---

## ACT_HI_TASKINST

**Purpose:** Historical record of each task instance. Captures full task lifecycle including assignment, delegation, priority, dates, and completion state.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Task history ID |
| TASK_DEF_KEY_ | VARCHAR(255) | NULL | Task definition key |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition ID |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution scope |
| CASE_DEF_KEY_ | VARCHAR(255) | NULL | Case definition key (CMMN) |
| CASE_DEF_ID_ | VARCHAR(64) | NULL | Case definition ID |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Case instance |
| CASE_EXECUTION_ID_ | VARCHAR(64) | NULL | Case execution |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance reference |
| NAME_ | VARCHAR(255) | NULL | Task name |
| PARENT_TASK_ID_ | VARCHAR(64) | NULL | Parent task |
| DESCRIPTION_ | VARCHAR(4000) | NULL | Task description |
| OWNER_ | VARCHAR(255) | NULL | Task owner |
| ASSIGNEE_ | VARCHAR(255) | NULL | Assignee |
| START_TIME_ | TIMESTAMP | NOT NULL | Task creation time |
| END_TIME_ | TIMESTAMP | NULL | Task completion time |
| DURATION_ | BIGINT | NULL | Duration in milliseconds |
| DELETE_REASON_ | VARCHAR(4000) | NULL | Reason when deleted |
| PRIORITY_ | INTEGER | NULL | Task priority |
| DUE_DATE_ | TIMESTAMP | NULL | Due date |
| FOLLOW_UP_DATE_ | TIMESTAMP | NULL | Follow-up date |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| TASK_STATE_ | VARCHAR(64) | NULL | Extended task state |

**Indexes:** `ACT_IDX_HI_TASKINST_ROOT_PI`, `ACT_IDX_HI_TASK_INST_TENANT_ID`, `ACT_IDX_HI_TASK_INST_PROC_DEF_KEY`, `ACT_IDX_HI_TASKINST_PROCINST`, `ACT_IDX_HI_TASK_INST_RM_TIME`, `ACT_IDX_HI_TASK_INST_START`, `ACT_IDX_HI_TASK_INST_END`

**Example Queries:**

```sql
-- Average task duration by definition
SELECT TASK_DEF_KEY_, COUNT(*) AS completions,
       AVG(DURATION_) AS avg_ms
FROM ACT_HI_TASKINST
WHERE END_TIME_ IS NOT NULL
  AND START_TIME_ >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY TASK_DEF_KEY_
ORDER BY avg_ms DESC;

-- Tasks completed by a specific user
SELECT ID_, NAME_, PROC_INST_ID_, START_TIME_, END_TIME_, DURATION_
FROM ACT_HI_TASKINST
WHERE ASSIGNEE_ = 'john.doe' AND END_TIME_ IS NOT NULL
ORDER BY END_TIME_ DESC
LIMIT 50;
```

---

## ACT_HI_VARINST

**Purpose:** Snapshot of each variable's current value. Updated when the variable changes; represents the latest known value when history level includes variables.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Variable history ID |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition ID |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution scope |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance |
| CASE_DEF_KEY_ | VARCHAR(255) | NULL | Case definition key |
| CASE_DEF_ID_ | VARCHAR(64) | NULL | Case definition ID |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Case instance |
| CASE_EXECUTION_ID_ | VARCHAR(64) | NULL | Case execution |
| TASK_ID_ | VARCHAR(64) | NULL | Task scope |
| NAME_ | VARCHAR(255) | NOT NULL | Variable name |
| VAR_TYPE_ | VARCHAR(100) | NULL | Variable type |
| CREATE_TIME_ | TIMESTAMP | NULL | When variable was first set |
| REV_ | INTEGER | NULL | Revision |
| BYTEARRAY_ID_ | VARCHAR(64) | NULL | Binary value reference |
| DOUBLE_ | DOUBLE PRECISION | NULL | Float value |
| LONG_ | BIGINT | NULL | Integer/long value |
| TEXT_ | VARCHAR(4000) | NULL | String value |
| TEXT2_ | VARCHAR(4000) | NULL | String continuation |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| STATE_ | VARCHAR(20) | NULL | Variable state (`CREATED`, `DELETED`) |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_VARINST_ROOT_PI`, `ACT_IDX_HI_PROCVAR_PROC_INST`, `ACT_IDX_HI_PROCVAR_NAME_TYPE`, `ACT_IDX_HI_VAR_INST_TENANT_ID`, `ACT_IDX_HI_VARINST_BYTEAR`, `ACT_IDX_HI_VARINST_RM_TIME`, `ACT_IDX_HI_VAR_PI_NAME_TYPE`, `ACT_IDX_HI_VARINST_NAME`, `ACT_IDX_HI_VARINST_ACT_INST_ID`

---

## ACT_HI_DETAIL

**Purpose:** Fine-grained variable change events. Each row is a single variable update event (name, type, old/new value). Enables full variable audit trail when `HISTORY_LEVEL=FULL`.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Detail event ID |
| TYPE_ | VARCHAR(255) | NOT NULL | Event type: `VariableUpdate`, `FormProperty` |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition ID |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution scope |
| CASE_DEF_KEY_ | VARCHAR(255) | NULL | Case definition key |
| CASE_DEF_ID_ | VARCHAR(64) | NULL | Case definition ID |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Case instance |
| CASE_EXECUTION_ID_ | VARCHAR(64) | NULL | Case execution |
| TASK_ID_ | VARCHAR(64) | NULL | Task scope |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance |
| VAR_INST_ID_ | VARCHAR(64) | NULL | Variable instance reference |
| NAME_ | VARCHAR(255) | NOT NULL | Variable/property name |
| VAR_TYPE_ | VARCHAR(64) | NULL | Variable type |
| REV_ | INTEGER | NULL | Revision |
| TIME_ | TIMESTAMP | NOT NULL | Event timestamp |
| BYTEARRAY_ID_ | VARCHAR(64) | NULL | Binary value reference |
| DOUBLE_ | DOUBLE PRECISION | NULL | Float value |
| LONG_ | BIGINT | NULL | Integer/long value |
| TEXT_ | VARCHAR(4000) | NULL | String value |
| TEXT2_ | VARCHAR(4000) | NULL | String continuation |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Ordering counter |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| OPERATION_ID_ | VARCHAR(64) | NULL | Linked operation log entry |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| INITIAL_ | BOOLEAN | NULL | Whether this is the initial value |

**Indexes:** `ACT_IDX_HI_DETAIL_ROOT_PI`, `ACT_IDX_HI_DETAIL_PROC_INST`, `ACT_IDX_HI_DETAIL_ACT_INST`, `ACT_IDX_HI_DETAIL_TIME`, `ACT_IDX_HI_DETAIL_NAME`, `ACT_IDX_HI_DETAIL_TASK_ID`, `ACT_IDX_HI_DETAIL_RM_TIME`, `ACT_IDX_HI_DETAIL_BYTEAR`, `ACT_IDX_HI_DETAIL_VAR_INST_ID`

---

## ACT_HI_IDENTITYLINK

**Purpose:** Audit log of identity link add/remove events (task assignment, candidate group changes). Each row is a timestamped event, not current state.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Event ID |
| TIMESTAMP_ | TIMESTAMP | NOT NULL | Event time |
| TYPE_ | VARCHAR(255) | NULL | Link type |
| USER_ID_ | VARCHAR(255) | NULL | User |
| GROUP_ID_ | VARCHAR(255) | NULL | Group |
| TASK_ID_ | VARCHAR(64) | NULL | Associated task |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition |
| OPERATION_TYPE_ | VARCHAR(64) | NULL | `ADD` or `DELETE` |
| ASSIGNER_ID_ | VARCHAR(64) | NULL | User who made the change |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_IDENT_LNK_ROOT_PI`, `ACT_IDX_HI_IDENT_LNK_USER`, `ACT_IDX_HI_IDENT_LNK_GROUP`, `ACT_IDX_HI_IDENT_LNK_TENANT_ID`, `ACT_IDX_HI_IDENT_LINK_TASK`, `ACT_IDX_HI_IDENT_LINK_RM_TIME`, `ACT_IDX_HI_IDENT_LNK_TIMESTAMP`

---

## ACT_HI_COMMENT

**Purpose:** User and system comments on tasks and process instances. `FULL_MSG_` stores the full comment text as binary when it exceeds the `MESSAGE_` column limit.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Comment ID |
| TYPE_ | VARCHAR(255) | NULL | `comment` or `event` |
| TIME_ | TIMESTAMP | NOT NULL | Comment timestamp |
| USER_ID_ | VARCHAR(255) | NULL | Author user ID |
| TASK_ID_ | VARCHAR(64) | NULL | Associated task |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| ACTION_ | VARCHAR(255) | NULL | Action type (for event entries) |
| MESSAGE_ | VARCHAR(4000) | NULL | Comment text (truncated) |
| FULL_MSG_ | BYTEA | NULL | Full comment text (binary) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| REV_ | INTEGER | NOT NULL DEFAULT 1 | Revision |

**Indexes:** `ACT_IDX_HI_COMMENT_TASK`, `ACT_IDX_HI_COMMENT_ROOT_PI`, `ACT_IDX_HI_COMMENT_PROCINST`, `ACT_IDX_HI_COMMENT_RM_TIME`

---

## ACT_HI_ATTACHMENT

**Purpose:** Attachments (files, URLs) associated with tasks or process instances.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Attachment ID |
| REV_ | INTEGER | NULL | Revision |
| USER_ID_ | VARCHAR(255) | NULL | Uploading user |
| NAME_ | VARCHAR(255) | NULL | Attachment name |
| DESCRIPTION_ | VARCHAR(4000) | NULL | Description |
| TYPE_ | VARCHAR(255) | NULL | MIME type or category |
| TASK_ID_ | VARCHAR(64) | NULL | Associated task |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| URL_ | VARCHAR(4000) | NULL | External URL |
| CONTENT_ID_ | VARCHAR(64) | NULL | Reference to content in ACT_GE_BYTEARRAY |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_TIME_ | TIMESTAMP | NULL | Upload time |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_ATTACHMENT_CONTENT`, `ACT_IDX_HI_ATTACHMENT_ROOT_PI`, `ACT_IDX_HI_ATTACHMENT_PROCINST`, `ACT_IDX_HI_ATTACHMENT_TASK`, `ACT_IDX_HI_ATTACHMENT_RM_TIME`

---

## ACT_HI_OP_LOG

**Purpose:** Operator audit log. Records administrative operations (suspend/activate, delete, migrate, reassign) performed by users or the engine itself. Essential for compliance and forensics.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry ID |
| DEPLOYMENT_ID_ | VARCHAR(64) | NULL | Associated deployment |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution |
| CASE_DEF_ID_ | VARCHAR(64) | NULL | Case definition |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Case instance |
| CASE_EXECUTION_ID_ | VARCHAR(64) | NULL | Case execution |
| TASK_ID_ | VARCHAR(64) | NULL | Task |
| JOB_ID_ | VARCHAR(64) | NULL | Job |
| JOB_DEF_ID_ | VARCHAR(64) | NULL | Job definition |
| BATCH_ID_ | VARCHAR(64) | NULL | Batch |
| USER_ID_ | VARCHAR(255) | NULL | User who performed the operation |
| TIMESTAMP_ | TIMESTAMP | NOT NULL | When the operation occurred |
| OPERATION_TYPE_ | VARCHAR(64) | NULL | Operation (e.g., `Suspend`, `Delete`, `Assign`) |
| OPERATION_ID_ | VARCHAR(64) | NULL | Groups related changes in one operation |
| ENTITY_TYPE_ | VARCHAR(30) | NULL | Entity class (e.g., `ProcessInstance`, `Task`) |
| PROPERTY_ | VARCHAR(64) | NULL | Property changed |
| ORG_VALUE_ | VARCHAR(4000) | NULL | Old value |
| NEW_VALUE_ | VARCHAR(4000) | NULL | New value |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| CATEGORY_ | VARCHAR(64) | NULL | Operation category |
| EXTERNAL_TASK_ID_ | VARCHAR(64) | NULL | External task |
| ANNOTATION_ | VARCHAR(4000) | NULL | Operator notes |

**Indexes:** `ACT_IDX_HI_OP_LOG_ROOT_PI`, `ACT_IDX_HI_OP_LOG_PROCINST`, `ACT_IDX_HI_OP_LOG_PROCDEF`, `ACT_IDX_HI_OP_LOG_TASK`, `ACT_IDX_HI_OP_LOG_RM_TIME`, `ACT_IDX_HI_OP_LOG_TIMESTAMP`, `ACT_IDX_HI_OP_LOG_USER_ID`, `ACT_IDX_HI_OP_LOG_OP_TYPE`, `ACT_IDX_HI_OP_LOG_ENTITY_TYPE`

**Example Queries:**

```sql
-- All operations on a process instance
SELECT TIMESTAMP_, USER_ID_, OPERATION_TYPE_, ENTITY_TYPE_,
       PROPERTY_, ORG_VALUE_, NEW_VALUE_, ANNOTATION_
FROM ACT_HI_OP_LOG
WHERE PROC_INST_ID_ = 'pi-id'
ORDER BY TIMESTAMP_;

-- Recent admin operations by user
SELECT TIMESTAMP_, OPERATION_TYPE_, ENTITY_TYPE_, PROC_INST_ID_, TASK_ID_
FROM ACT_HI_OP_LOG
WHERE USER_ID_ = 'admin' AND TIMESTAMP_ >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY TIMESTAMP_ DESC;
```

---

## ACT_HI_INCIDENT

**Purpose:** Historical record of incidents (resolved and open). Captures the full lifecycle including resolution time and configuration history.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Incident history ID |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition ID |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution |
| CREATE_TIME_ | TIMESTAMP | NOT NULL | Incident creation time |
| END_TIME_ | TIMESTAMP | NULL | Resolution/deletion time |
| INCIDENT_MSG_ | VARCHAR(4000) | NULL | Error message |
| INCIDENT_TYPE_ | VARCHAR(255) | NOT NULL | Incident type |
| ACTIVITY_ID_ | VARCHAR(255) | NULL | Activity where incident occurred |
| FAILED_ACTIVITY_ID_ | VARCHAR(255) | NULL | Failed activity |
| CAUSE_INCIDENT_ID_ | VARCHAR(64) | NULL | Cause incident |
| ROOT_CAUSE_INCIDENT_ID_ | VARCHAR(64) | NULL | Root cause incident |
| CONFIGURATION_ | VARCHAR(255) | NULL | Configuration (e.g., job ID) |
| HISTORY_CONFIGURATION_ | VARCHAR(255) | NULL | Historic configuration |
| INCIDENT_STATE_ | INTEGER | NULL | `0`=open, `1`=resolved, `2`=deleted |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| JOB_DEF_ID_ | VARCHAR(64) | NULL | Job definition |
| ANNOTATION_ | VARCHAR(4000) | NULL | Operator notes |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_INCIDENT_TENANT_ID`, `ACT_IDX_HI_INCIDENT_PROC_DEF_KEY`, `ACT_IDX_HI_INCIDENT_ROOT_PI`, `ACT_IDX_HI_INCIDENT_PROCINST`, `ACT_IDX_HI_INCIDENT_RM_TIME`, `ACT_IDX_HI_INCIDENT_CREATE_TIME`, `ACT_IDX_HI_INCIDENT_END_TIME`

---

## ACT_HI_JOB_LOG

**Purpose:** Execution log for background jobs — creation, lock acquisition, execution success/failure, and retry events. Essential for debugging asynchronous failures.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry ID |
| TIMESTAMP_ | TIMESTAMP | NOT NULL | Event timestamp |
| JOB_ID_ | VARCHAR(64) | NOT NULL | Job that was logged |
| JOB_DUEDATE_ | TIMESTAMP | NULL | Job due time at event |
| JOB_RETRIES_ | INTEGER | NULL | Retry count at event |
| JOB_PRIORITY_ | BIGINT | NOT NULL DEFAULT 0 | Job priority at event |
| JOB_EXCEPTION_MSG_ | VARCHAR(4000) | NULL | Exception message |
| JOB_EXCEPTION_STACK_ID_ | VARCHAR(64) | NULL | Stack trace reference |
| JOB_STATE_ | INTEGER | NULL | `0`=created, `1`=fired, `2`=succeeded, `3`=failed, `4`=deleted |
| JOB_DEF_ID_ | VARCHAR(64) | NULL | Job definition |
| JOB_DEF_TYPE_ | VARCHAR(255) | NULL | Job type |
| JOB_DEF_CONFIGURATION_ | VARCHAR(255) | NULL | Job configuration |
| ACT_ID_ | VARCHAR(255) | NULL | Activity ID |
| FAILED_ACT_ID_ | VARCHAR(255) | NULL | Failed activity ID |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROCESS_INSTANCE_ID_ | VARCHAR(64) | NULL | Process instance |
| PROCESS_DEF_ID_ | VARCHAR(64) | NULL | Process definition ID |
| PROCESS_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| DEPLOYMENT_ID_ | VARCHAR(64) | NULL | Deployment |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Ordering counter |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| HOSTNAME_ | VARCHAR(255) | NULL | Engine node hostname |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| BATCH_ID_ | VARCHAR(64) | NULL | Associated batch |

**Indexes:** `ACT_IDX_HI_JOB_LOG_ROOT_PI`, `ACT_IDX_HI_JOB_LOG_PROCINST`, `ACT_IDX_HI_JOB_LOG_PROCDEF`, `ACT_IDX_HI_JOB_LOG_TENANT_ID`, `ACT_IDX_HI_JOB_LOG_JOB_DEF_ID`, `ACT_IDX_HI_JOB_LOG_EX_STACK`, `ACT_IDX_HI_JOB_LOG_RM_TIME`, `ACT_IDX_HI_JOB_LOG_JOB_CONF`

**Example Queries:**

```sql
-- All log entries for a job
SELECT TIMESTAMP_, JOB_STATE_, JOB_RETRIES_, JOB_EXCEPTION_MSG_, HOSTNAME_
FROM ACT_HI_JOB_LOG
WHERE JOB_ID_ = 'job-id'
ORDER BY TIMESTAMP_;

-- Frequently failing jobs
SELECT PROCESS_DEF_KEY_, ACT_ID_, COUNT(*) AS failures
FROM ACT_HI_JOB_LOG
WHERE JOB_STATE_ = 3  -- failed
  AND TIMESTAMP_ >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY PROCESS_DEF_KEY_, ACT_ID_
ORDER BY failures DESC;
```

---

## ACT_HI_BATCH

**Purpose:** Historical record of completed batch operations.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Batch history ID |
| TYPE_ | VARCHAR(255) | NULL | Batch type |
| TOTAL_JOBS_ | INTEGER | NULL | Total jobs |
| JOBS_PER_SEED_ | INTEGER | NULL | Jobs per seed |
| INVOCATIONS_PER_JOB_ | INTEGER | NULL | Invocations per job |
| SEED_JOB_DEF_ID_ | VARCHAR(64) | NULL | Seed job definition |
| MONITOR_JOB_DEF_ID_ | VARCHAR(64) | NULL | Monitor job definition |
| BATCH_JOB_DEF_ID_ | VARCHAR(64) | NULL | Batch job definition |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_USER_ID_ | VARCHAR(255) | NULL | User who started the batch |
| START_TIME_ | TIMESTAMP | NOT NULL | Start time |
| END_TIME_ | TIMESTAMP | NULL | End time |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| EXEC_START_TIME_ | TIMESTAMP | NULL | Execution phase start |

**Indexes:** `ACT_HI_BAT_RM_TIME`

---

## ACT_HI_EXT_TASK_LOG

**Purpose:** Execution log for external tasks — fetch, lock, complete, fail events. Mirrors `ACT_HI_JOB_LOG` for the external task pattern.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry ID |
| TIMESTAMP_ | TIMESTAMP | NOT NULL | Event timestamp |
| EXT_TASK_ID_ | VARCHAR(64) | NOT NULL | External task |
| RETRIES_ | INTEGER | NULL | Retry count at event |
| TOPIC_NAME_ | VARCHAR(255) | NULL | Worker topic |
| WORKER_ID_ | VARCHAR(255) | NULL | Worker ID |
| PRIORITY_ | BIGINT | NOT NULL DEFAULT 0 | Priority at event |
| ERROR_MSG_ | VARCHAR(4000) | NULL | Error message |
| ERROR_DETAILS_ID_ | VARCHAR(64) | NULL | Error detail reference |
| ACT_ID_ | VARCHAR(255) | NULL | Activity ID |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Execution |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| STATE_ | INTEGER | NULL | `0`=created, `1`=locked, `2`=succeeded, `3`=failed, `4`=deleted |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_HI_EXT_TASK_LOG_ROOT_PI`, `ACT_HI_EXT_TASK_LOG_PROCINST`, `ACT_HI_EXT_TASK_LOG_PROCDEF`, `ACT_HI_EXT_TASK_LOG_PROC_DEF_KEY`, `ACT_HI_EXT_TASK_LOG_TENANT_ID`, `ACT_IDX_HI_EXTTASKLOG_ERRORDET`, `ACT_HI_EXT_TASK_LOG_RM_TIME`

---

## ACT_HI_CASEINST

**Purpose:** Historical record of a CMMN case instance lifecycle.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | History record ID |
| CASE_INST_ID_ | VARCHAR(64) | NOT NULL UNIQUE | Runtime case instance ID |
| BUSINESS_KEY_ | VARCHAR(255) | NULL | External correlation key |
| CASE_DEF_ID_ | VARCHAR(64) | NOT NULL | Case definition ID |
| CREATE_TIME_ | TIMESTAMP | NOT NULL | Case creation time |
| CLOSE_TIME_ | TIMESTAMP | NULL | Case close time |
| DURATION_ | BIGINT | NULL | Duration in milliseconds |
| STATE_ | INTEGER | NULL | Case state |
| CREATE_USER_ID_ | VARCHAR(255) | NULL | User who created the case |
| SUPER_CASE_INSTANCE_ID_ | VARCHAR(64) | NULL | Parent case instance |
| SUPER_PROCESS_INSTANCE_ID_ | VARCHAR(64) | NULL | Parent process instance |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_HI_CAS_I_CLOSE`, `ACT_IDX_HI_CAS_I_BUSKEY`, `ACT_IDX_HI_CAS_I_TENANT_ID`

---

## ACT_HI_CASEACTINST

**Purpose:** Historical record of each activity (stage, milestone, task) executed within a case.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | History record ID |
| PARENT_ACT_INST_ID_ | VARCHAR(64) | NULL | Parent activity instance |
| CASE_DEF_ID_ | VARCHAR(64) | NOT NULL | Case definition ID |
| CASE_INST_ID_ | VARCHAR(64) | NOT NULL | Case instance |
| CASE_ACT_ID_ | VARCHAR(255) | NOT NULL | CMMN activity element ID |
| TASK_ID_ | VARCHAR(64) | NULL | Associated task |
| CALL_PROC_INST_ID_ | VARCHAR(64) | NULL | Called process instance |
| CALL_CASE_INST_ID_ | VARCHAR(64) | NULL | Called case instance |
| CASE_ACT_NAME_ | VARCHAR(255) | NULL | Activity display name |
| CASE_ACT_TYPE_ | VARCHAR(255) | NULL | Activity type (stage, milestone, …) |
| CREATE_TIME_ | TIMESTAMP | NOT NULL | Activity start time |
| END_TIME_ | TIMESTAMP | NULL | Activity end time |
| DURATION_ | BIGINT | NULL | Duration in milliseconds |
| STATE_ | INTEGER | NULL | State |
| REQUIRED_ | BOOLEAN | NULL | Required for case completion |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_HI_CAS_A_I_CREATE`, `ACT_IDX_HI_CAS_A_I_END`, `ACT_IDX_HI_CAS_A_I_COMP`, `ACT_IDX_HI_CAS_A_I_TENANT_ID`

---

## ACT_HI_DECINST

**Purpose:** Records each DMN decision evaluation — which decision was evaluated, when, with what context (process/case/standalone).

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Decision evaluation ID |
| DEC_DEF_ID_ | VARCHAR(64) | NOT NULL | Decision definition ID |
| DEC_DEF_KEY_ | VARCHAR(255) | NOT NULL | Decision key |
| DEC_DEF_NAME_ | VARCHAR(255) | NULL | Decision name |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Calling process key |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Calling process definition |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Calling process instance |
| CASE_DEF_KEY_ | VARCHAR(255) | NULL | Calling case key |
| CASE_DEF_ID_ | VARCHAR(64) | NULL | Calling case definition |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Calling case instance |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance that triggered evaluation |
| ACT_ID_ | VARCHAR(255) | NULL | Activity ID |
| EVAL_TIME_ | TIMESTAMP | NOT NULL | Evaluation timestamp |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |
| COLLECT_VALUE_ | DOUBLE PRECISION | NULL | Aggregated collect value (for collect hit policy) |
| USER_ID_ | VARCHAR(255) | NULL | User who triggered evaluation |
| ROOT_DEC_INST_ID_ | VARCHAR(64) | NULL | Root decision instance (for chained evaluations) |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| DEC_REQ_ID_ | VARCHAR(64) | NULL | Decision requirement definition |
| DEC_REQ_KEY_ | VARCHAR(255) | NULL | Decision requirement key |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_HI_DEC_INST_ID`, `ACT_IDX_HI_DEC_INST_KEY`, `ACT_IDX_HI_DEC_INST_PI`, `ACT_IDX_HI_DEC_INST_TIME`, `ACT_IDX_HI_DEC_INST_TENANT_ID`, `ACT_IDX_HI_DEC_INST_ROOT_PI`, `ACT_IDX_HI_DEC_INST_REQ_ID`, `ACT_IDX_HI_DEC_INST_RM_TIME`

**Example Queries:**

```sql
-- Decision evaluation frequency
SELECT DEC_DEF_KEY_, COUNT(*) AS evaluations,
       AVG(COLLECT_VALUE_) AS avg_collect
FROM ACT_HI_DECINST
WHERE EVAL_TIME_ >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY DEC_DEF_KEY_
ORDER BY evaluations DESC;
```

---

## ACT_HI_DEC_IN

**Purpose:** Input clause values used in a specific decision evaluation. One row per input clause per evaluation.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Input record ID |
| DEC_INST_ID_ | VARCHAR(64) | FK → ACT_HI_DECINST, NOT NULL | Parent decision evaluation |
| CLAUSE_ID_ | VARCHAR(64) | NULL | Input clause element ID |
| CLAUSE_NAME_ | VARCHAR(255) | NULL | Input clause name |
| VAR_TYPE_ | VARCHAR(100) | NULL | Variable type |
| BYTEARRAY_ID_ | VARCHAR(64) | NULL | Binary value reference |
| DOUBLE_ | DOUBLE PRECISION | NULL | Float value |
| LONG_ | BIGINT | NULL | Integer/long value |
| TEXT_ | VARCHAR(4000) | NULL | String value |
| TEXT2_ | VARCHAR(4000) | NULL | String continuation |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation time |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_DEC_IN_INST`, `ACT_IDX_HI_DEC_IN_CLAUSE`, `ACT_IDX_HI_DEC_IN_ROOT_PI`, `ACT_IDX_HI_DEC_IN_RM_TIME`

---

## ACT_HI_DEC_OUT

**Purpose:** Output clause values produced by a decision evaluation. One row per output clause per matched rule per evaluation.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Output record ID |
| DEC_INST_ID_ | VARCHAR(64) | FK → ACT_HI_DECINST, NOT NULL | Parent decision evaluation |
| CLAUSE_ID_ | VARCHAR(64) | NULL | Output clause element ID |
| CLAUSE_NAME_ | VARCHAR(255) | NULL | Output clause name |
| RULE_ID_ | VARCHAR(64) | NULL | Matched rule ID |
| RULE_ORDER_ | INTEGER | NULL | Rule position in the table |
| VAR_NAME_ | VARCHAR(255) | NULL | Output variable name |
| VAR_TYPE_ | VARCHAR(100) | NULL | Variable type |
| BYTEARRAY_ID_ | VARCHAR(64) | NULL | Binary value reference |
| DOUBLE_ | DOUBLE PRECISION | NULL | Float value |
| LONG_ | BIGINT | NULL | Integer/long value |
| TEXT_ | VARCHAR(4000) | NULL | String value |
| TEXT2_ | VARCHAR(4000) | NULL | String continuation |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation time |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Scheduled cleanup time |

**Indexes:** `ACT_IDX_HI_DEC_OUT_INST`, `ACT_IDX_HI_DEC_OUT_RULE`, `ACT_IDX_HI_DEC_OUT_ROOT_PI`, `ACT_IDX_HI_DEC_OUT_RM_TIME`

---

## Design Notes

- **History levels**: The amount of data written to history tables is controlled by the engine's history level: `NONE`, `ACTIVITY`, `AUDIT`, `FULL`. `FULL` writes `ACT_HI_DETAIL` for every variable change.
- **REMOVAL_TIME_**: Set by the history cleanup job based on `HISTORY_TTL_` from the definition. Cleanup runs in batches; set `historyCleanupEnabled=true` in the engine config.
- **Immutability**: History records are never updated after creation (except `REMOVAL_TIME_` during cleanup scheduling). Treat them as append-only audit events.
- **ACT_HI_PROCINST vs ACT_HI_ACTINST**: `PROCINST` is one row per process instance; `ACTINST` is many rows — one per activity execution within that instance.

---

See [Database-Specific Implementation Notes](index.md#database-specific-implementation-notes) for type mappings.

---

**Last Updated:** 2026-07-03 | **Schema Version:** 7.24 | **Operaton Versions:** 1.0.0+
