---
last_updated: 2026-11-11
schema_version: 7.25
---

# Runtime (RU_)

Runtime tables hold the live state of all active process/case executions, tasks, variables, jobs, incidents, and related objects. Rows are deleted or moved to history tables when work completes.

## Tables

| Table | Purpose |
|-------|---------|
| [ACT_RU_EXECUTION](#act_ru_execution) | Active process execution scopes |
| [ACT_RU_TASK](#act_ru_task) | Active user tasks |
| [ACT_RU_VARIABLE](#act_ru_variable) | Runtime variables |
| [ACT_RU_IDENTITYLINK](#act_ru_identitylink) | Task/process user-group assignments |
| [ACT_RU_JOB](#act_ru_job) | Background jobs (timers, async work) |
| [ACT_RU_JOBDEF](#act_ru_jobdef) | Job definitions |
| [ACT_RU_INCIDENT](#act_ru_incident) | Active incidents |
| [ACT_RU_EVENT_SUBSCR](#act_ru_event_subscr) | Event subscriptions |
| [ACT_RU_EXT_TASK](#act_ru_ext_task) | External task subscriptions |
| [ACT_RU_BATCH](#act_ru_batch) | Batch operation records |
| [ACT_RU_AUTHORIZATION](#act_ru_authorization) | Permission rules |
| [ACT_RU_FILTER](#act_ru_filter) | Saved task filters |
| [ACT_RU_METER_LOG](#act_ru_meter_log) | Engine metrics |
| [ACT_RU_TASK_METER_LOG](#act_ru_task_meter_log) | Task worker (assignment) metrics |
| [ACT_RU_CASE_EXECUTION](#act_ru_case_execution) | Active case executions (CMMN) |
| [ACT_RU_CASE_SENTRY_PART](#act_ru_case_sentry_part) | Case sentry parts (CMMN) |

---

## ACT_RU_EXECUTION

**Purpose:** Represents one execution scope within a process instance. Executions form a self-referential tree: the root execution (`PROC_INST_ID_ = ID_`) represents the process instance; child executions represent parallel branches, sub-processes, or event scopes.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Execution identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Top-level process instance of the call hierarchy (same for all executions of a process instance and of the instances it calls) |
| PROC_INST_ID_ | VARCHAR(64) | FK → self | Root execution ID; equals ID_ for root |
| BUSINESS_KEY_ | VARCHAR(255) | NULL | External correlation key |
| PARENT_ID_ | VARCHAR(64) | FK → self | Parent execution (NULL for root) |
| PROC_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_PROCDEF | Process definition |
| SUPER_EXEC_ | VARCHAR(64) | FK → self | Caller execution (for call activities) |
| SUPER_CASE_EXEC_ | VARCHAR(64) | NULL | Caller case execution |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Associated case instance |
| ACT_ID_ | VARCHAR(255) | NULL | Current activity element ID |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Current activity instance ID |
| IS_ACTIVE_ | BOOLEAN | NULL | Whether execution is active |
| IS_CONCURRENT_ | BOOLEAN | NULL | Parallel branch |
| IS_SCOPE_ | BOOLEAN | NULL | Creates a new variable scope |
| IS_EVENT_SCOPE_ | BOOLEAN | NULL | Event scope execution kept after its scope completed, for compensation |
| SUSPENSION_STATE_ | INTEGER | NULL | `1`=active, `2`=suspended |
| CACHED_ENT_STATE_ | INTEGER | NULL | Bitmask of related entities present (event subscriptions, tasks, jobs, incidents, variables, sub-process/case instances, external tasks) |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Ordering counter for events of this execution (inherited by child executions) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key (denormalized) |

**Indexes:** `ACT_IDX_EXE_ROOT_PI`, `ACT_IDX_EXEC_BUSKEY`, `ACT_IDX_EXE_PROCINST`, `ACT_IDX_EXE_PARENT`, `ACT_IDX_EXE_SUPER`, `ACT_IDX_EXE_PROCDEF`, `ACT_IDX_EXEC_TENANT_ID`

**Example Queries:**

```sql
-- All scopes in a process instance
SELECT ID_, PARENT_ID_, ACT_ID_, IS_SCOPE_, IS_CONCURRENT_, SUSPENSION_STATE_
FROM ACT_RU_EXECUTION
WHERE PROC_INST_ID_ = 'pi-id'
ORDER BY SEQUENCE_COUNTER_;

-- Suspended process instances
SELECT ID_, BUSINESS_KEY_, PROC_DEF_KEY_, SUSPENSION_STATE_
FROM ACT_RU_EXECUTION
WHERE PROC_INST_ID_ = ID_ AND SUSPENSION_STATE_ = 2;

-- Execution hierarchy (PostgreSQL recursive)
WITH RECURSIVE tree AS (
  SELECT ID_, PARENT_ID_, ACT_ID_, 1 AS depth
  FROM ACT_RU_EXECUTION WHERE PARENT_ID_ IS NULL AND PROC_INST_ID_ = ID_
  UNION ALL
  SELECT e.ID_, e.PARENT_ID_, e.ACT_ID_, t.depth + 1
  FROM ACT_RU_EXECUTION e JOIN tree t ON e.PARENT_ID_ = t.ID_
)
SELECT * FROM tree ORDER BY depth, ID_;
```

---

## ACT_RU_TASK

**Purpose:** Active user task instance (BPMN user task, CMMN human task, or standalone task created via the API). Tracks assignment, delegation, priority, due dates, and suspension state. Deleted when completed or cancelled; history written to `ACT_HI_TASKINST`.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Task identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Enclosing execution scope |
| PROC_INST_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Process instance |
| PROC_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_PROCDEF | Process definition |
| CASE_EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_CASE_EXECUTION | Case execution (CMMN) |
| CASE_INST_ID_ | VARCHAR(64) | NULL | Case instance (CMMN) |
| CASE_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_CASE_DEF | Case definition (CMMN) |
| NAME_ | VARCHAR(255) | NULL | Task display name |
| PARENT_TASK_ID_ | VARCHAR(64) | NULL | Parent task for subtask hierarchies |
| DESCRIPTION_ | VARCHAR(4000) | NULL | Task description |
| TASK_DEF_KEY_ | VARCHAR(255) | NULL | Activity element ID from the BPMN definition |
| OWNER_ | VARCHAR(255) | NULL | Task owner user ID |
| ASSIGNEE_ | VARCHAR(255) | NULL | Currently assigned user ID |
| DELEGATION_ | VARCHAR(64) | NULL | Delegation state: NULL, `PENDING`, `RESOLVED` |
| PRIORITY_ | INTEGER | NULL | Priority (higher = more urgent) |
| CREATE_TIME_ | TIMESTAMP | NULL | Task creation time |
| LAST_UPDATED_ | TIMESTAMP | NULL | Last modification time |
| DUE_DATE_ | TIMESTAMP | NULL | Deadline |
| FOLLOW_UP_DATE_ | TIMESTAMP | NULL | Follow-up reminder date |
| SUSPENSION_STATE_ | INTEGER | NULL | `1`=active, `2`=suspended |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| TASK_STATE_ | VARCHAR(64) | NULL | Lifecycle state: `Init`, `Created`, `Updated`, `Completed`, `Deleted` |

**Indexes:** `ACT_IDX_TASK_CREATE`, `ACT_IDX_TASK_LAST_UPDATED`, `ACT_IDX_TASK_ASSIGNEE`, `ACT_IDX_TASK_OWNER`, `ACT_IDX_TASK_TENANT_ID`, `ACT_IDX_TASK_EXEC`, `ACT_IDX_TASK_PROCINST`, `ACT_IDX_TASK_PROCDEF`, `ACT_IDX_TASK_CASE_EXEC`, `ACT_IDX_TASK_CASE_DEF_ID`

**Example Queries:**

```sql
-- Unassigned tasks for a process instance
SELECT ID_, NAME_, PRIORITY_, CREATE_TIME_, DUE_DATE_
FROM ACT_RU_TASK
WHERE PROC_INST_ID_ = 'pi-id' AND ASSIGNEE_ IS NULL AND SUSPENSION_STATE_ = 1
ORDER BY PRIORITY_ DESC, CREATE_TIME_;

-- Overdue tasks
SELECT ID_, NAME_, ASSIGNEE_, DUE_DATE_
FROM ACT_RU_TASK
WHERE DUE_DATE_ < CURRENT_TIMESTAMP AND SUSPENSION_STATE_ = 1
ORDER BY DUE_DATE_;

-- Task load per user
SELECT ASSIGNEE_, COUNT(*) AS tasks,
       SUM(CASE WHEN DUE_DATE_ < CURRENT_TIMESTAMP THEN 1 ELSE 0 END) AS overdue
FROM ACT_RU_TASK
WHERE ASSIGNEE_ IS NOT NULL AND SUSPENSION_STATE_ = 1
GROUP BY ASSIGNEE_ ORDER BY tasks DESC;
```

---

## ACT_RU_VARIABLE

**Purpose:** Runtime variables scoped to a process instance, execution, task, case execution, or batch. Stores typed values: scalars in `LONG_`/`DOUBLE_`/`TEXT_`, complex objects via `BYTEARRAY_ID_`. Unique constraint `(VAR_SCOPE_, NAME_)` ensures one variable per name per scope.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Variable identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| TYPE_ | VARCHAR(255) | NOT NULL | Serializer name: `string`, `integer`, `long`, `short`, `double`, `boolean`, `date`, `bytes`, `file`, `null`, `serializable` (Java object), `json`, `xml`, … |
| NAME_ | VARCHAR(255) | NOT NULL | Variable name |
| EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Execution scope |
| PROC_INST_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Process instance |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition (denormalized) |
| CASE_EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_CASE_EXECUTION | Case execution scope |
| CASE_INST_ID_ | VARCHAR(64) | FK → ACT_RU_CASE_EXECUTION | Case instance scope |
| TASK_ID_ | VARCHAR(64) | NULL | Task scope |
| BATCH_ID_ | VARCHAR(64) | FK → ACT_RU_BATCH | Batch scope |
| BYTEARRAY_ID_ | VARCHAR(64) | FK → ACT_GE_BYTEARRAY | Binary value reference |
| DOUBLE_ | DOUBLE PRECISION | NULL | Float/double value |
| LONG_ | BIGINT | NULL | Integer/long/boolean/date value |
| TEXT_ | VARCHAR(4000) | NULL | String value; string form of `Short`/`Integer`/`Long`; file name for `File` |
| TEXT2_ | VARCHAR(4000) | NULL | Type-specific extra value: object type name for `Object`, MIME type and encoding for `File` |
| VAR_SCOPE_ | VARCHAR(64) | NULL | Scope key for uniqueness check |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Update version counter |
| IS_CONCURRENT_LOCAL_ | BOOLEAN | NULL | Local to a concurrent branch |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Unique Constraint:** `ACT_UNIQ_VARIABLE` on `(VAR_SCOPE_, NAME_)`

**Indexes:** `ACT_IDX_VAR_EXE`, `ACT_IDX_VAR_PROCINST`, `ACT_IDX_VAR_BYTEARRAY`, `ACT_IDX_VARIABLE_TASK_ID`, `ACT_IDX_VARIABLE_TASK_NAME_TYPE`, `ACT_IDX_BATCH_ID`, `ACT_IDX_VAR_CASE_EXE`, `ACT_IDX_VAR_CASE_INST_ID`, `ACT_IDX_VARIABLE_TENANT_ID`

**Variable Type→Column Mapping:**

| Type | Column(s) |
|------|-----------|
| String | TEXT_ (limited by the column size) |
| Boolean, Date | LONG_ |
| Short, Integer, Long | LONG_, TEXT_ (string form) |
| Double | DOUBLE_ |
| Bytes | BYTEARRAY_ID_ |
| File | BYTEARRAY_ID_ (content), TEXT_ (file name), TEXT2_ (MIME type, encoding) |
| Object | BYTEARRAY_ID_ (serialized value), TEXT2_ (object type name); serialization format is given by `TYPE_` |
| JSON, XML | BYTEARRAY_ID_ (serialized value) |
| Null | all value columns NULL |

**Example Queries:**

```sql
-- All variables for a process instance
SELECT NAME_, TYPE_, TEXT_, LONG_, DOUBLE_
FROM ACT_RU_VARIABLE
WHERE PROC_INST_ID_ = 'pi-id'
ORDER BY NAME_;

-- Find processes with variable value
SELECT DISTINCT PROC_INST_ID_
FROM ACT_RU_VARIABLE
WHERE NAME_ = 'status' AND TEXT_ = 'approved';

-- Task variables
SELECT NAME_, TYPE_, TEXT_, LONG_
FROM ACT_RU_VARIABLE WHERE TASK_ID_ = 'task-id' ORDER BY NAME_;
```

---

## ACT_RU_IDENTITYLINK

**Purpose:** Links tasks or process definitions to users/groups. Task links hold candidate users and groups (`TYPE_ = 'candidate'`) and custom link types. Process definition links hold candidate starters, also with `TYPE_ = 'candidate'`. The assignee and owner of a task are stored in `ACT_RU_TASK`, not here.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Link identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| GROUP_ID_ | VARCHAR(255) | NULL | Group identifier |
| TYPE_ | VARCHAR(255) | NULL | Link type, usually `candidate`; custom types are possible |
| USER_ID_ | VARCHAR(255) | NULL | User identifier |
| TASK_ID_ | VARCHAR(64) | FK → ACT_RU_TASK | Associated task (NULL for process-scoped) |
| PROC_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_PROCDEF | Process definition (NULL for task-scoped) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_IDENT_LNK_USER`, `ACT_IDX_IDENT_LNK_GROUP`, `ACT_IDX_TSKASS_TASK`, `ACT_IDX_ATHRZ_PROCEDEF`

**Example Queries:**

```sql
-- All tasks a user can claim (as candidate)
SELECT DISTINCT t.ID_, t.NAME_, t.PRIORITY_, t.CREATE_TIME_
FROM ACT_RU_TASK t
JOIN ACT_RU_IDENTITYLINK il ON t.ID_ = il.TASK_ID_
WHERE il.USER_ID_ = 'john.doe' AND il.TYPE_ = 'candidate'
  AND t.ASSIGNEE_ IS NULL AND t.SUSPENSION_STATE_ = 1;

-- Candidate groups for a task
SELECT GROUP_ID_ FROM ACT_RU_IDENTITYLINK
WHERE TASK_ID_ = 'task-id' AND TYPE_ = 'candidate' AND GROUP_ID_ IS NOT NULL;
```

---

## ACT_RU_JOB

**Purpose:** Background job queue: timers (`TYPE_='timer'`), asynchronous continuations and batch jobs (`TYPE_='message'`), and the history cleanup job (`TYPE_='ever-living'`). Distributed execution uses `LOCK_OWNER_`/`LOCK_EXP_TIME_` for coordination. Failed jobs decrement `RETRIES_` and create incidents.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Job identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| TYPE_ | VARCHAR(255) | NOT NULL | Job type: `message`, `timer`, `ever-living` |
| LOCK_EXP_TIME_ | TIMESTAMP | NULL | Lock expiry for distributed execution |
| LOCK_OWNER_ | VARCHAR(255) | NULL | Engine instance holding the lock |
| EXCLUSIVE_ | BOOLEAN | NULL | Exclusive execution (no parallel) |
| EXECUTION_ID_ | VARCHAR(64) | NULL | Associated execution |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance |
| PROCESS_INSTANCE_ID_ | VARCHAR(64) | NULL | Process instance |
| PROCESS_DEF_ID_ | VARCHAR(64) | NULL | Process definition |
| PROCESS_DEF_KEY_ | VARCHAR(255) | NULL | Process key (denormalized) |
| RETRIES_ | INTEGER | NULL | Remaining retry attempts |
| EXCEPTION_STACK_ID_ | VARCHAR(64) | FK → ACT_GE_BYTEARRAY | Exception stack trace |
| EXCEPTION_MSG_ | VARCHAR(4000) | NULL | Last exception message |
| FAILED_ACT_ID_ | VARCHAR(255) | NULL | Failed activity ID |
| DUEDATE_ | TIMESTAMP | NULL | Execution due time (for timers) |
| REPEAT_ | VARCHAR(255) | NULL | Cycle expression of a repeating timer (ISO 8601 `R…` or cron) |
| REPEAT_OFFSET_ | BIGINT | DEFAULT 0 | Repeat offset |
| HANDLER_TYPE_ | VARCHAR(255) | NULL | Job handler type (e.g., `async-continuation`, `timer-transition`, `batch-seed-job`) |
| HANDLER_CFG_ | VARCHAR(4000) | NULL | Handler configuration |
| DEPLOYMENT_ID_ | VARCHAR(64) | NULL | Associated deployment |
| SUSPENSION_STATE_ | INTEGER | NOT NULL DEFAULT 1 | `1`=active, `2`=suspended |
| JOB_DEF_ID_ | VARCHAR(64) | NULL | Job definition (logical reference, no FK constraint) |
| PRIORITY_ | BIGINT | NOT NULL DEFAULT 0 | Execution priority |
| SEQUENCE_COUNTER_ | BIGINT | NULL | Ordering counter |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation timestamp |
| LAST_FAILURE_LOG_ID_ | VARCHAR(64) | NULL | Last failure log reference |
| BATCH_ID_ | VARCHAR(64) | NULL | Associated batch |

**Indexes:** `ACT_IDX_JOB_EXECUTION_ID`, `ACT_IDX_JOB_HANDLER`, `ACT_IDX_JOB_PROCINST`, `ACT_IDX_JOB_ROOT_PROCINST`, `ACT_IDX_JOB_TENANT_ID`, `ACT_IDX_JOB_EXCEPTION`, `ACT_IDX_JOB_JOB_DEF_ID`, `ACT_IDX_JOB_HANDLER_TYPE`

**Example Queries:**

```sql
-- Jobs ready for execution
SELECT ID_, TYPE_, HANDLER_TYPE_, PRIORITY_, DUEDATE_, PROCESS_INSTANCE_ID_, RETRIES_
FROM ACT_RU_JOB
WHERE SUSPENSION_STATE_ = 1
  AND RETRIES_ > 0
  AND (DUEDATE_ IS NULL OR DUEDATE_ <= CURRENT_TIMESTAMP)
  AND (LOCK_OWNER_ IS NULL OR LOCK_EXP_TIME_ < CURRENT_TIMESTAMP)
ORDER BY PRIORITY_ DESC, DUEDATE_ ASC;

-- Jobs with failures
SELECT ID_, TYPE_, EXCEPTION_MSG_, RETRIES_, FAILED_ACT_ID_
FROM ACT_RU_JOB
WHERE EXCEPTION_MSG_ IS NOT NULL
ORDER BY CREATE_TIME_ DESC;

-- Jobs currently locked by job executors
SELECT LOCK_OWNER_, COUNT(*) AS locked_jobs, MIN(LOCK_EXP_TIME_) AS next_lock_expiry
FROM ACT_RU_JOB
WHERE LOCK_OWNER_ IS NOT NULL
GROUP BY LOCK_OWNER_;
```

---

## ACT_RU_JOBDEF

**Purpose:** Defines job execution characteristics for an activity (timer event, async continuation) or a batch. Stores default priority, job type, and suspension state that apply to all instances of that activity's jobs.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Job definition identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Associated process definition |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key (denormalized) |
| ACT_ID_ | VARCHAR(255) | NULL | Activity element ID |
| JOB_TYPE_ | VARCHAR(255) | NOT NULL | Job handler type (e.g., `async-continuation`, `timer-transition`, `batch-seed-job`) |
| JOB_CONFIGURATION_ | VARCHAR(255) | NULL | Handler-specific configuration (e.g., `async-before`/`async-after`, `DURATION: PT5M`, or the batch ID) |
| SUSPENSION_STATE_ | INTEGER | NULL | `1`=active, `2`=suspended |
| JOB_PRIORITY_ | BIGINT | NULL | Default priority for new jobs |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| DEPLOYMENT_ID_ | VARCHAR(64) | NULL | Associated deployment |

**Indexes:** `ACT_IDX_JOBDEF_TENANT_ID`, `ACT_IDX_JOBDEF_PROC_DEF_ID`

---

## ACT_RU_INCIDENT

**Purpose:** Tracks active failures within a process. When a job exhausts retries, an incident is created. Incidents form a chain: `CAUSE_INCIDENT_ID_` → direct cause, `ROOT_CAUSE_INCIDENT_ID_` → original root cause.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Incident identifier |
| REV_ | INTEGER | NOT NULL | Revision for optimistic locking |
| INCIDENT_TIMESTAMP_ | TIMESTAMP | NOT NULL | When the incident occurred |
| INCIDENT_MSG_ | VARCHAR(4000) | NULL | Error message |
| INCIDENT_TYPE_ | VARCHAR(255) | NOT NULL | Type: `failedJob`, `failedExternalTask`, … |
| EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Associated execution |
| ACTIVITY_ID_ | VARCHAR(255) | NULL | Activity where incident is attached |
| FAILED_ACTIVITY_ID_ | VARCHAR(255) | NULL | Activity that actually failed |
| PROC_INST_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Process instance |
| PROC_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_PROCDEF | Process definition |
| CAUSE_INCIDENT_ID_ | VARCHAR(64) | FK → self | Direct cause incident |
| ROOT_CAUSE_INCIDENT_ID_ | VARCHAR(64) | FK → self | Root cause incident |
| CONFIGURATION_ | VARCHAR(255) | NULL | Configuration (e.g., job ID) |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| JOB_DEF_ID_ | VARCHAR(64) | FK → ACT_RU_JOBDEF | Related job definition |
| ANNOTATION_ | VARCHAR(4000) | NULL | Operator notes |

**Indexes:** `ACT_IDX_INC_CONFIGURATION`, `ACT_IDX_INC_TENANT_ID`, `ACT_IDX_INC_EXID`, `ACT_IDX_INC_PROCINSTID`, `ACT_IDX_INC_PROCDEFID`, `ACT_IDX_INC_CAUSEINCID`, `ACT_IDX_INC_ROOTCAUSEINCID`, `ACT_IDX_INC_JOB_DEF`

**Example Queries:**

```sql
-- Active incidents for a process instance
SELECT ID_, INCIDENT_TYPE_, INCIDENT_MSG_, ACTIVITY_ID_, ANNOTATION_
FROM ACT_RU_INCIDENT
WHERE PROC_INST_ID_ = 'pi-id'
ORDER BY INCIDENT_TIMESTAMP_ DESC;

-- Incident cause chain
SELECT e.ID_, e.INCIDENT_TYPE_, e.INCIDENT_MSG_,
       c.ID_ AS cause_id, c.INCIDENT_TYPE_ AS cause_type
FROM ACT_RU_INCIDENT e
LEFT JOIN ACT_RU_INCIDENT c ON e.CAUSE_INCIDENT_ID_ = c.ID_
WHERE e.ROOT_CAUSE_INCIDENT_ID_ = 'root-incident-id';
```

---

## ACT_RU_EVENT_SUBSCR

**Purpose:** An active subscription to a message, signal, compensation or conditional event. Created when an execution reaches a catch event or enters a scope with boundary or event sub-process events; deleted when the event is received and execution resumes. Message, signal and conditional start events have subscriptions without an execution.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Subscription identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| EVENT_TYPE_ | VARCHAR(255) | NOT NULL | Type: `message`, `signal`, `compensate`, `conditional` |
| EVENT_NAME_ | VARCHAR(255) | NULL | Message or signal name |
| EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Awaiting execution (NULL for start event subscriptions) |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| ACTIVITY_ID_ | VARCHAR(255) | NULL | Catch element activity ID |
| CONFIGURATION_ | VARCHAR(255) | NULL | Process definition ID for start event subscriptions; event scope execution ID for `compensate` |
| CREATED_ | TIMESTAMP | NOT NULL | Creation time |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_EVENT_SUBSCR`, `ACT_IDX_EVENT_SUBSCR_CONFIG_`, `ACT_IDX_EVENT_SUBSCR_TENANT_ID`, `ACT_IDX_EVENT_SUBSCR_EVT_NAME`

**Example Queries:**

```sql
-- All message subscriptions pending correlation
SELECT ID_, EVENT_NAME_, EXECUTION_ID_, PROC_INST_ID_, CONFIGURATION_
FROM ACT_RU_EVENT_SUBSCR
WHERE EVENT_TYPE_ = 'message'
ORDER BY CREATED_ ASC;
```

---

## ACT_RU_EXT_TASK

**Purpose:** External task subscription enabling decoupled worker execution. Workers fetch tasks by `TOPIC_NAME_`, acquire a lock via `WORKER_ID_`/`LOCK_EXP_TIME_`, execute, then complete or fail the task.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | External task identifier |
| REV_ | INTEGER | NOT NULL | Revision for optimistic locking |
| WORKER_ID_ | VARCHAR(255) | NULL | Worker holding the lock |
| TOPIC_NAME_ | VARCHAR(255) | NULL | Worker routing topic |
| RETRIES_ | INTEGER | NULL | Remaining retry attempts |
| ERROR_MSG_ | VARCHAR(4000) | NULL | Last error message |
| ERROR_DETAILS_ID_ | VARCHAR(64) | FK → ACT_GE_BYTEARRAY | Detailed error (serialized) |
| LOCK_EXP_TIME_ | TIMESTAMP | NULL | Lock expiry |
| CREATE_TIME_ | TIMESTAMP | NULL | Creation time |
| SUSPENSION_STATE_ | INTEGER | NULL | `1`=active, `2`=suspended |
| EXECUTION_ID_ | VARCHAR(64) | FK → ACT_RU_EXECUTION | Associated execution |
| PROC_INST_ID_ | VARCHAR(64) | NULL | Process instance |
| PROC_DEF_ID_ | VARCHAR(64) | NULL | Process definition |
| PROC_DEF_KEY_ | VARCHAR(255) | NULL | Process key |
| ACT_ID_ | VARCHAR(255) | NULL | Activity ID |
| ACT_INST_ID_ | VARCHAR(64) | NULL | Activity instance ID |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| PRIORITY_ | BIGINT | NOT NULL DEFAULT 0 | Execution priority |
| LAST_FAILURE_LOG_ID_ | VARCHAR(64) | NULL | Last failure log reference |

**Indexes:** `ACT_IDX_EXT_TASK_TOPIC`, `ACT_IDX_EXT_TASK_TENANT_ID`, `ACT_IDX_EXT_TASK_PRIORITY`, `ACT_IDX_EXT_TASK_ERR_DETAILS`, `ACT_IDX_EXT_TASK_EXEC`

**Example Queries:**

```sql
-- Available tasks for a worker topic
SELECT ID_, TOPIC_NAME_, PRIORITY_, EXECUTION_ID_, PROC_INST_ID_
FROM ACT_RU_EXT_TASK
WHERE TOPIC_NAME_ = 'payment-processing'
  AND SUSPENSION_STATE_ = 1
  AND (RETRIES_ IS NULL OR RETRIES_ > 0)
  AND (LOCK_EXP_TIME_ IS NULL OR LOCK_EXP_TIME_ <= CURRENT_TIMESTAMP)
ORDER BY PRIORITY_ DESC, CREATE_TIME_ ASC
LIMIT 10;
```

---

## ACT_RU_BATCH

**Purpose:** Coordinates bulk operations (process migration, message correlation, etc.). A batch spawns three job types: seed jobs (create work), batch jobs (do work), and a monitor job (tracks progress).

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Batch identifier |
| REV_ | INTEGER | NOT NULL | Revision for optimistic locking |
| TYPE_ | VARCHAR(255) | NULL | Batch type (e.g., `instance-migration`, `correlate-message`) |
| TOTAL_JOBS_ | INTEGER | NULL | Total jobs to complete |
| JOBS_CREATED_ | INTEGER | NULL | Jobs created so far |
| JOBS_PER_SEED_ | INTEGER | NULL | Jobs per seed invocation |
| INVOCATIONS_PER_JOB_ | INTEGER | NULL | Work units per batch job |
| SEED_JOB_DEF_ID_ | VARCHAR(64) | FK → ACT_RU_JOBDEF | Seed job definition |
| BATCH_JOB_DEF_ID_ | VARCHAR(64) | FK → ACT_RU_JOBDEF | Batch job definition |
| MONITOR_JOB_DEF_ID_ | VARCHAR(64) | FK → ACT_RU_JOBDEF | Monitor job definition |
| SUSPENSION_STATE_ | INTEGER | NULL | `1`=active, `2`=suspended |
| CONFIGURATION_ | VARCHAR(255) | NULL | ID of the batch configuration in `ACT_GE_BYTEARRAY` |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |
| CREATE_USER_ID_ | VARCHAR(255) | NULL | User who started the batch |
| START_TIME_ | TIMESTAMP | NULL | Start time |
| EXEC_START_TIME_ | TIMESTAMP | NULL | Execution phase start time |

**Indexes:** `ACT_IDX_BATCH_SEED_JOB_DEF`, `ACT_IDX_BATCH_MONITOR_JOB_DEF`, `ACT_IDX_BATCH_JOB_DEF`

**Example Queries:**

```sql
-- Batch job creation progress (seeding)
SELECT ID_, TYPE_, TOTAL_JOBS_, JOBS_CREATED_,
       ROUND(100.0 * JOBS_CREATED_ / NULLIF(TOTAL_JOBS_, 0), 1) AS pct_jobs_created
FROM ACT_RU_BATCH WHERE SUSPENSION_STATE_ = 1;
```

---

## ACT_RU_AUTHORIZATION

**Purpose:** Fine-grained access control rules. Each row grants or revokes permission(s) to a user or group on a resource type/ID combination. `PERMS_` is a bitmask of permission flags.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Authorization rule identifier |
| REV_ | INTEGER | NOT NULL | Revision for optimistic locking |
| TYPE_ | INTEGER | NOT NULL | `0`=global, `1`=grant, `2`=revoke |
| GROUP_ID_ | VARCHAR(255) | NULL | Target group (mutually exclusive with USER_ID_) |
| USER_ID_ | VARCHAR(255) | NULL | Target user (mutually exclusive with GROUP_ID_); `*` for global authorizations |
| RESOURCE_TYPE_ | INTEGER | NOT NULL | Resource type (`0`=application, `1`=user, `2`=group, `6`=process definition, `7`=task, `8`=process instance, …) |
| RESOURCE_ID_ | VARCHAR(255) | NULL | Specific resource ID; `*` for all resources of the type |
| PERMS_ | INTEGER | NULL | Permission bitmask (READ=2, UPDATE=4, CREATE=8, DELETE=16, …); for revoke rows a cleared bit means revoked |
| REMOVAL_TIME_ | TIMESTAMP | NULL | Removal time for authorizations on history data (history cleanup) |
| ROOT_PROC_INST_ID_ | VARCHAR(64) | NULL | Root process instance reference |

**Unique Constraints:**
- `ACT_UNIQ_AUTH_USER` on `(TYPE_, USER_ID_, RESOURCE_TYPE_, RESOURCE_ID_)`
- `ACT_UNIQ_AUTH_GROUP` on `(TYPE_, GROUP_ID_, RESOURCE_TYPE_, RESOURCE_ID_)`

**Indexes:** `ACT_IDX_AUTH_GROUP_ID`, `ACT_IDX_AUTH_RESOURCE_ID`, `ACT_IDX_AUTH_ROOT_PI`, `ACT_IDX_AUTH_RM_TIME`

**Permission Flags:** `NONE=0`, `READ=2`, `UPDATE=4`, `CREATE=8`, `DELETE=16`, `ACCESS=32`, `READ_TASK=64`, `UPDATE_TASK=128`, `CREATE_INSTANCE=256`, `READ_INSTANCE=512`, `UPDATE_INSTANCE=1024`, `DELETE_INSTANCE=2048`, `READ_HISTORY=4096`, `DELETE_HISTORY=8192`, `TASK_WORK=16384`, `TASK_ASSIGN=32768`, `MIGRATE_INSTANCE=65536`; `ALL` sets every bit (`2147483647`). Resource-specific permissions (e.g. `ProcessDefinitionPermissions`) add further flags such as `SUSPEND=1048576`, and may reuse bits (`RETRY_JOB=32`).

**Resource Types:** `APPLICATION=0`, `USER=1`, `GROUP=2`, `GROUP_MEMBERSHIP=3`, `AUTHORIZATION=4`, `FILTER=5`, `PROCESS_DEFINITION=6`, `TASK=7`, `PROCESS_INSTANCE=8`, `DEPLOYMENT=9`, `DECISION_DEFINITION=10`, `TENANT=11`, `TENANT_MEMBERSHIP=12`, `BATCH=13`, `DECISION_REQUIREMENTS_DEFINITION=14`, `REPORT=15`, `DASHBOARD=16`, `OPERATION_LOG_CATEGORY=17`, `OPTIMIZE=18`, `HISTORIC_TASK=19`, `HISTORIC_PROCESS_INSTANCE=20`, `SYSTEM=21`

**Example Queries:**

```sql
-- All permissions for a user
SELECT TYPE_, RESOURCE_TYPE_, RESOURCE_ID_, PERMS_
FROM ACT_RU_AUTHORIZATION
WHERE USER_ID_ = 'john.doe'
ORDER BY RESOURCE_TYPE_, RESOURCE_ID_;

-- Grants with READ on a process definition (PostgreSQL/MySQL)
-- The engine also evaluates group, global and revoke authorizations.
SELECT ID_, TYPE_, RESOURCE_ID_, PERMS_
FROM ACT_RU_AUTHORIZATION
WHERE USER_ID_ = 'john.doe'
  AND RESOURCE_TYPE_ = 6
  AND RESOURCE_ID_ IN ('invoice_approval', '*')
  AND TYPE_ = 1
  AND (PERMS_ & 2) = 2;
```

---

## ACT_RU_FILTER

**Purpose:** Saved task filter/query definitions for the Tasklist UI. Each filter stores its query criteria (assignee, priority, process, etc.) as JSON in `QUERY_`.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Filter identifier |
| REV_ | INTEGER | NOT NULL | Revision for optimistic locking |
| RESOURCE_TYPE_ | VARCHAR(255) | NOT NULL | Resource type; currently always `Task` |
| NAME_ | VARCHAR(255) | NOT NULL | Filter display name |
| OWNER_ | VARCHAR(255) | NULL | Owning user ID |
| QUERY_ | TEXT | NOT NULL | Filter query (JSON) |
| PROPERTIES_ | TEXT | NULL | Additional metadata (JSON) |

---

## ACT_RU_METER_LOG

**Purpose:** Engine metrics such as `root-process-instance-start`, `activity-instance-start`, `job-successful` or `executed-decision-elements`. The metrics reporter writes one row per metric and reporting interval.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry identifier |
| NAME_ | VARCHAR(64) | NOT NULL | Metric name (e.g., `root-process-instance-start`) |
| REPORTER_ | VARCHAR(255) | NULL | Reporting engine instance ID |
| VALUE_ | BIGINT | NULL | Metric value |
| TIMESTAMP_ | TIMESTAMP | NULL | End of the reporting interval |
| MILLISECONDS_ | BIGINT | DEFAULT 0 | `TIMESTAMP_` as epoch milliseconds (indexed for range queries) |

**Indexes:** `ACT_IDX_METER_LOG_MS`, `ACT_IDX_METER_LOG_NAME_MS`, `ACT_IDX_METER_LOG_REPORT`, `ACT_IDX_METER_LOG_TIME`, `ACT_IDX_METER_LOG`

**Example Queries:**

```sql
-- Hourly root process instance starts (last 7 days)
SELECT date_trunc('hour', TIMESTAMP_) AS hour, SUM(VALUE_) AS starts
FROM ACT_RU_METER_LOG
WHERE NAME_ = 'root-process-instance-start'
  AND TIMESTAMP_ >= CURRENT_TIMESTAMP - INTERVAL '7 days'
GROUP BY 1 ORDER BY 1 DESC;
```

---

## ACT_RU_TASK_METER_LOG

**Purpose:** Task worker metrics. The engine writes one row each time a task is assigned, with a pseudonymized `ASSIGNEE_HASH_` instead of the user ID. Used to count unique task workers.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Log entry identifier |
| ASSIGNEE_HASH_ | BIGINT | NULL | Hash of assignee user ID |
| TIMESTAMP_ | TIMESTAMP | NULL | Time of the assignment |

**Indexes:** `ACT_IDX_TASK_METER_LOG_TIME`

---

## ACT_RU_CASE_EXECUTION

**Purpose:** Active execution scope within a CMMN case instance. Mirrors `ACT_RU_EXECUTION` for cases — root execution is the case instance, child executions are stages and tasks.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Case execution identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CASE_INST_ID_ | VARCHAR(64) | FK → self | Root case instance (equals ID_ for root) |
| SUPER_CASE_EXEC_ | VARCHAR(64) | NULL | Caller case execution |
| SUPER_EXEC_ | VARCHAR(64) | NULL | Caller process execution |
| BUSINESS_KEY_ | VARCHAR(255) | NULL | External correlation key |
| PARENT_ID_ | VARCHAR(64) | FK → self | Parent case execution |
| CASE_DEF_ID_ | VARCHAR(64) | FK → ACT_RE_CASE_DEF | Case definition |
| ACT_ID_ | VARCHAR(255) | NULL | Current CMMN activity ID |
| PREV_STATE_ | INTEGER | NULL | Previous state |
| CURRENT_STATE_ | INTEGER | NULL | Current state (`0`=new, `1`=available, `2`=enabled, `3`=disabled, `4`=active, `5`=suspended, `6`=terminated, `7`=completed, `8`=failed, `9`=closed, `10`–`14`=transient terminating/suspending states) |
| REQUIRED_ | BOOLEAN | NULL | Whether completion is required for parent |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_CASE_EXEC_BUSKEY`, `ACT_IDX_CASE_EXE_CASE_INST`, `ACT_IDX_CASE_EXE_PARENT`, `ACT_IDX_CASE_EXE_CASE_DEF`, `ACT_IDX_CASE_EXEC_TENANT_ID`

---

## ACT_RU_CASE_SENTRY_PART

**Purpose:** Tracks satisfaction state of individual sentry conditions in a CMMN case. A sentry fires when all its parts are satisfied, enabling or disabling case elements.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Sentry part identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| CASE_INST_ID_ | VARCHAR(64) | FK → ACT_RU_CASE_EXECUTION | Case instance |
| CASE_EXEC_ID_ | VARCHAR(64) | FK → ACT_RU_CASE_EXECUTION | Associated case execution |
| SENTRY_ID_ | VARCHAR(255) | NULL | Sentry element ID |
| TYPE_ | VARCHAR(255) | NULL | Part type: `planItemOnPart`, `ifPart`, `variableOnPart` |
| SOURCE_CASE_EXEC_ID_ | VARCHAR(64) | NULL | Source execution for transition conditions |
| STANDARD_EVENT_ | VARCHAR(255) | NULL | CMMN standard event |
| SOURCE_ | VARCHAR(255) | NULL | Source plan item activity ID (for planItemOnPart) |
| VARIABLE_EVENT_ | VARCHAR(255) | NULL | Variable change event (for variableOnPart) |
| VARIABLE_NAME_ | VARCHAR(255) | NULL | Observed variable name |
| SATISFIED_ | BOOLEAN | NULL | Whether this part is satisfied |
| TENANT_ID_ | VARCHAR(64) | NULL | Tenant identifier |

**Indexes:** `ACT_IDX_CASE_SENTRY_CASE_INST`, `ACT_IDX_CASE_SENTRY_CASE_EXEC`

---

## Design Notes

- **Optimistic locking**: The engine checks `REV_` on every update and raises an `OptimisticLockingException` on conflict. Change data through the engine API, not with direct SQL updates.
- **Suspension**: `SUSPENSION_STATE_` (`1`=active, `2`=suspended) is set on executions, tasks, jobs, job definitions, external tasks and batches. Suspended items cannot progress but are not deleted.
- **Incident chains**: `CAUSE_INCIDENT_ID_` and `ROOT_CAUSE_INCIDENT_ID_` in `ACT_RU_INCIDENT` enable root cause navigation for cascaded failures.
- **Job lock expiry**: Locks of crashed engine nodes need no cleanup. Once `LOCK_EXP_TIME_` has passed, any job executor can acquire the job again.
- **Multi-tenancy**: Always include `TENANT_ID_` predicates in queries on multi-tenant installations.

---

See [Database-Specific Implementation Notes](../index.md#database-specific-implementation-notes) for type mappings.

---

**Last Updated:** 2026-11-11 | **Schema Version:** 7.25 | **Operaton Versions:** 1.0.0+
