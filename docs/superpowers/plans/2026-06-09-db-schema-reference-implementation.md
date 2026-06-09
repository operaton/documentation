# DB Schema Reference Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create comprehensive, modular markdown reference documentation for the Operaton database schema (version 7.24), organized by functional domain with Mermaid ER diagrams and database-specific notes.

**Architecture:** Extract table definitions from canonical PostgreSQL schema, cross-reference against other supported databases (MySQL, Oracle, MariaDB, MSSQL, DB2, H2) for variations, organize into 8 functional domain modules plus an index file, and verify completeness.

**Tech Stack:** Markdown, Mermaid diagrams, SQL schema files (PostgreSQL baseline), bash for schema analysis

---

## File Structure

```
docs/reference/
└── db-schema/
    ├── index.md                    # Schema overview, versioning, full ER diagram, quick reference
    ├── process-management.md       # Process definitions, instances, executions, variables
    ├── task-management.md          # Tasks, task variables, assignments
    ├── deployment-management.md    # Deployments, resources, byte arrays
    ├── history.md                  # All historical data tables (ACT_HI_*)
    ├── authorization.md            # Authorization rules, users, groups, tenants
    ├── case-management.md          # Case definitions, instances, activities
    ├── decision-management.md      # DMN decision definitions and evaluations
    └── system-properties.md        # System configuration, properties, locks
```

## Table Domain Mapping Reference

**Process Management:**
- ACT_RE_PROCDEF (Process Definition)
- ACT_RU_PROCESS_INSTANCE (Process Instance)
- ACT_RU_EXECUTION (Execution)
- ACT_RE_DECISION_DEF (old, now in decision-management)

**Task Management:**
- ACT_RU_TASK (Task)
- ACT_RU_VARIABLE (Runtime Variable)
- ACT_RU_TASK_METER_LOG (Task Meter Log)

**Deployment Management:**
- ACT_RE_DEPLOYMENT (Deployment)
- ACT_RE_DEPLOYMENT_RESOURCE (Deployment Resource)
- ACT_GE_BYTEARRAY (Byte Array - resource storage)

**History:**
- ACT_HI_PROC_INST (Historic Process Instance)
- ACT_HI_ACT_INST (Historic Activity Instance)
- ACT_HI_TASK_INST (Historic Task Instance)
- ACT_HI_VARINST (Historic Variable Instance)
- ACT_HI_INCIDENT (Historic Incident)
- ACT_HI_JOB_LOG (Historic Job Log)
- ACT_HI_DETAIL (Historic Detail)
- ACT_HI_OP_LOG (Historic Operation Log)

**Authorization:**
- ACT_RU_AUTHORIZATION (Authorization Rule)
- ACT_ID_USER (User)
- ACT_ID_GROUP (Group)
- ACT_ID_TENANT (Tenant)
- ACT_ID_MEMBERSHIP (Membership)
- ACT_ID_USER_ACCOUNT (User Account)
- ACT_ID_GROUP_ACCOUNT (Group Account)
- ACT_ID_TENANT_MEMBER (Tenant Member)

**Case Management:**
- ACT_CAS_DEF (Case Definition)
- ACT_CAS_CASE_DEF_PROP (Case Definition Property)
- ACT_CAS_INSTANCE (Case Instance)
- ACT_CAS_ACT_INST (Case Activity Instance)

**Decision Management:**
- ACT_RE_DECISION_DEF (Decision Definition)
- ACT_RE_DECISION_REQ_DEF (Decision Requirement Definition)
- ACT_HI_DECISION_INST (Historic Decision Instance)
- ACT_DMN_DECISION_INSTANCE (DMN Decision Instance)
- ACT_DMN_REQUIREMENT_DEFINITION (DMN Requirement Definition)

**System Properties:**
- ACT_GE_PROPERTY (Property)
- ACT_GE_SCHEMA_LOG (Schema Log)
- ACT_RU_JOB (Job)
- ACT_RU_JOBDEF (Job Definition)
- ACT_RU_INCIDENT (Incident)
- ACT_RU_BATCH (Batch)
- ACT_RU_EXT_TASK (External Task)
- ACT_RU_EVENT_SUBSCR (Event Subscription)

---

## Phase 1: Schema Analysis

### Task 1: Create Table Inventory from SQL Files

**Files:**
- Create: `docs/reference/db-schema/_schema-analysis.txt` (temporary working file)
- Source: `/Users/kthoms/Development/git/operaton/operaton/engine/src/main/resources/org/operaton/bpm/engine/db/create/`

- [ ] **Step 1: Extract tables from canonical PostgreSQL schema**

Run:
```bash
cat /Users/kthoms/Development/git/operaton/operaton/engine/src/main/resources/org/operaton/bpm/engine/db/create/activiti.postgres.create.engine.sql | grep "^create table" | sed 's/create table //' | sed 's/ (.*//' | sort
```

Expected output: List of all table names (ACT_*)

- [ ] **Step 2: Extract column info for each table from PostgreSQL schema**

For each table (start with ACT_RE_PROCDEF), run:
```bash
grep -A 50 "create table ACT_RE_PROCDEF" /Users/kthoms/Development/git/operaton/operaton/engine/src/main/resources/org/operaton/bpm/engine/db/create/activiti.postgres.create.engine.sql
```

Expected output: CREATE TABLE statement with all columns, types, constraints

- [ ] **Step 3: Document findings in temporary analysis file**

Create `docs/reference/db-schema/_schema-analysis.txt` with:
- List of all tables
- Column definitions extracted from PostgreSQL
- Column descriptions (sourced from code comments in SQL files or inferred from naming)
- Primary keys and constraints

Format example:
```
TABLE: ACT_RE_PROCDEF (Process Definition)
  ID_ VARCHAR(64) PRIMARY KEY - Unique process definition ID
  KEY_ VARCHAR(255) NOT NULL - Process key (namespace)
  NAME_ VARCHAR(255) - Process name
  CATEGORY_ VARCHAR(255) - Category for grouping
  DEPLOYMENT_ID_ VARCHAR(64) FK -> ACT_RE_DEPLOYMENT
  ... (continue for all columns)
```

- [ ] **Step 4: Identify relationships and foreign keys**

Extract all foreign key constraints from the PostgreSQL create script:
```bash
grep -i "foreign key\|constraint" /Users/kthoms/Development/git/operaton/operaton/engine/src/main/resources/org/operaton/bpm/engine/db/create/activiti.postgres.create.engine.sql
```

Expected output: All foreign key definitions for relationship mapping

- [ ] **Step 5: Commit working file**

```bash
git add docs/reference/db-schema/_schema-analysis.txt
git commit -m "chore: add schema analysis working file for reference"
```

### Task 2: Document Database-Specific Variations

**Files:**
- Modify: `docs/reference/db-schema/_schema-analysis.txt`
- Source databases:
  - H2: `/Users/kthoms/Development/git/operaton/operaton/engine/src/main/resources/org/operaton/bpm/engine/db/create/activiti.h2.create.engine.sql`
  - MySQL: `activiti.mysql.create.engine.sql`
  - Oracle: `activiti.oracle.create.engine.sql`
  - MariaDB: `activiti.mariadb.create.engine.sql`
  - MSSQL: `activiti.mssql.create.engine.sql`
  - DB2: `activiti.db2.create.engine.sql`

- [ ] **Step 1: Compare column types across databases**

For each major table (ACT_RE_PROCDEF, ACT_RU_TASK, ACT_HI_PROC_INST, etc.), extract column definitions from each database SQL file and document differences.

Example comparison:
```
Column: ID_
  PostgreSQL:  VARCHAR(64)
  MySQL:       varchar(64)
  Oracle:      VARCHAR2(64)
  MSSQL:       varchar(64)
  DB2:         VARCHAR(64)
  H2:          varchar(64)
  MariaDB:     varchar(64)
```

- [ ] **Step 2: Document constraint differences**

Compare PRIMARY KEY, UNIQUE, NOT NULL, and other constraints across databases. Note if any constraints are dialect-specific.

- [ ] **Step 3: Document indexing variations**

Extract CREATE INDEX statements from each database schema file and note any database-specific indexes.

- [ ] **Step 4: Update analysis file with variations**

Append a "Database Variations" section to `_schema-analysis.txt`:

```
DATABASE VARIATIONS:

H2:
  - Uses AUTO_INCREMENT for sequences
  - Column type note: TEXT used for large strings
  
MySQL:
  - Uses AUTO_INCREMENT for ID generation
  - VARCHAR(max) not available, uses TEXT
  
Oracle:
  - Uses VARCHAR2 instead of VARCHAR
  - Sequences used for ID generation
  
(etc. for each database)
```

- [ ] **Step 5: Commit**

```bash
git add docs/reference/db-schema/_schema-analysis.txt
git commit -m "chore: add database-specific variations to schema analysis"
```

---

## Phase 2: Index File Creation

### Task 3: Create Index File with Schema Version and Quick Reference

**Files:**
- Create: `docs/reference/db-schema/index.md`

- [ ] **Step 1: Write header with schema version info**

```markdown
# Database Schema Reference

**Current Schema Version:** 7.24

## Schema Version Mapping

The following Operaton versions use schema version 7.24:
- Operaton 1.0.0 through 2.1.1

## Overview

This documentation provides a comprehensive reference for the Operaton database schema. The schema is organized by functional domain to make it easier to understand relationships and dependencies.

### Domains

- [Process Management](#process-management) - Process definitions and instances
- [Task Management](#task-management) - Task execution and management
- [Deployment Management](#deployment-management) - Process and decision deployments
- [History](#history) - Historical data and audit trails
- [Authorization](#authorization) - Users, groups, permissions, and tenants
- [Case Management](#case-management) - Case definitions and instances
- [Decision Management](#decision-management) - Decision definitions and evaluations
- [System Properties](#system-properties) - System configuration and internal state
```

- [ ] **Step 2: Create quick reference table of all tables**

After the header, add:

```markdown
## Quick Reference: All Tables

| Table Name | Domain | Purpose |
|---|---|---|
| ACT_RE_PROCDEF | Process Management | Defines a process and its structure |
| ACT_RU_PROCESS_INSTANCE | Process Management | Runtime instance of a process |
| ACT_RU_EXECUTION | Process Management | Represents a scope of execution within a process |
| ACT_RU_TASK | Task Management | A task to be completed by a user or system |
| ACT_RU_VARIABLE | Task Management | Variable value at runtime |
| ... (complete table for all 40+ tables) |
```

Use the table inventory from Task 1 to populate this. Keep descriptions to one line.

- [ ] **Step 3: Add common query patterns section**

```markdown
## Common Query Patterns

### Find all process instances for a deployment
See [Process Management - ACT_RU_PROCESS_INSTANCE](process-management.md#act_ru_process_instance)

### Query task history for a user
See [History - ACT_HI_TASK_INST](history.md#act_hi_task_inst)

### Get all variables for a process instance
See [Task Management - ACT_RU_VARIABLE](task-management.md#act_ru_variable)

(etc. for 5-7 common patterns, each linking to detailed module)
```

- [ ] **Step 4: Add domain overviews section**

```markdown
## Domain Descriptions

### Process Management
Manages process definitions, instances, and execution flow.
[View detailed documentation →](process-management.md)

### Task Management
Handles user tasks, system tasks, and task variables.
[View detailed documentation →](task-management.md)

(etc. for all 8 domains)
```

- [ ] **Step 5: Commit**

```bash
git add docs/reference/db-schema/index.md
git commit -m "docs: create schema index with version info and quick reference"
```

### Task 4: Create Full Schema ER Diagram

**Files:**
- Modify: `docs/reference/db-schema/index.md`

- [ ] **Step 1: Create Mermaid ER diagram showing all tables and relationships**

Add this to index.md after the domain descriptions:

```markdown
## Full Schema ER Diagram

\`\`\`mermaid
erDiagram
    ACT_RE_PROCDEF ||--o{ ACT_RU_PROCESS_INSTANCE : "defines"
    ACT_RE_PROCDEF ||--o{ ACT_RE_DECISION_DEF : "can invoke"
    ACT_RU_PROCESS_INSTANCE ||--o{ ACT_RU_EXECUTION : "contains"
    ACT_RU_PROCESS_INSTANCE ||--o{ ACT_RU_TASK : "creates"
    ACT_RU_PROCESS_INSTANCE ||--o{ ACT_RU_VARIABLE : "has"
    ACT_RU_EXECUTION ||--o{ ACT_RU_VARIABLE : "has"
    ACT_RU_TASK ||--o{ ACT_RU_VARIABLE : "has"
    ACT_RE_DEPLOYMENT ||--o{ ACT_RE_PROCDEF : "contains"
    ACT_RE_DEPLOYMENT ||--o{ ACT_RE_DEPLOYMENT_RESOURCE : "has"
    ACT_RE_DEPLOYMENT_RESOURCE ||--o{ ACT_GE_BYTEARRAY : "references"
    ACT_RU_PROCESS_INSTANCE ||--o{ ACT_HI_PROC_INST : "generates"
    ACT_RU_EXECUTION ||--o{ ACT_HI_ACT_INST : "generates"
    ACT_RU_TASK ||--o{ ACT_HI_TASK_INST : "generates"
    ACT_RU_VARIABLE ||--o{ ACT_HI_VARINST : "generates"
    ACT_RU_INCIDENT ||--o{ ACT_HI_INCIDENT : "generates"
    ACT_ID_USER ||--o{ ACT_RU_AUTHORIZATION : "has"
    ACT_ID_GROUP ||--o{ ACT_RU_AUTHORIZATION : "has"
    ACT_ID_TENANT ||--o{ ACT_RU_AUTHORIZATION : "scopes"
    ACT_CAS_DEF ||--o{ ACT_CAS_INSTANCE : "defines"
    ACT_CAS_INSTANCE ||--o{ ACT_CAS_ACT_INST : "contains"
    ACT_RE_DECISION_DEF ||--o{ ACT_HI_DECISION_INST : "evaluated by"
\`\`\`

This diagram shows the relationships between major table groups. See individual domain modules for detailed diagrams.
```

- [ ] **Step 2: Verify Mermaid syntax is correct**

Run (if you have mermaid-cli installed):
```bash
mmdc -i docs/reference/db-schema/index.md -o /tmp/test-diagram.svg 2>&1 | head -20
```

Or test by viewing the markdown in a Mermaid-capable editor (GitHub markdown, VS Code with Markdown Preview Mermaid Support).

- [ ] **Step 3: Commit**

```bash
git add docs/reference/db-schema/index.md
git commit -m "docs: add full schema ER diagram to index"
```

---

## Phase 3: Domain Module Documentation

Each domain module follows the same structure. Create each module as a single task. Modules are standalone but can reference other modules.

### Task 5: Document Process Management Module

**Files:**
- Create: `docs/reference/db-schema/process-management.md`
- Reference: `docs/reference/db-schema/_schema-analysis.txt`

- [ ] **Step 1: Create module header with domain description**

```markdown
# Process Management

Process Management tables handle the definition, deployment, and execution of business processes. This domain covers process definitions, active process instances, execution scopes, and process variables.

## Tables in This Domain

- ACT_RE_PROCDEF - Process Definition
- ACT_RU_PROCESS_INSTANCE - Process Instance
- ACT_RU_EXECUTION - Execution (scope)

## Domain ER Diagram

\`\`\`mermaid
erDiagram
    ACT_RE_PROCDEF ||--o{ ACT_RU_PROCESS_INSTANCE : "defines"
    ACT_RU_PROCESS_INSTANCE ||--o{ ACT_RU_EXECUTION : "contains"
    ACT_RE_DEPLOYMENT ||--o{ ACT_RE_PROCDEF : "contains"
\`\`\`
```

- [ ] **Step 2: Document each table in the domain**

For ACT_RE_PROCDEF, add:

```markdown
## ACT_RE_PROCDEF (Process Definition)

**Purpose:** 
Stores the definition of a process. Each row represents a unique process definition version. Multiple versions of the same process (different key) can coexist.

**Columns:**

| Column Name | Type | Constraints | Description |
|---|---|---|---|
| ID_ | VARCHAR(64) | PRIMARY KEY | Unique identifier for this process definition |
| KEY_ | VARCHAR(255) | NOT NULL | The process key (unique within a deployment) - used to identify the process logically |
| NAME_ | VARCHAR(255) | | User-friendly name of the process |
| CATEGORY_ | VARCHAR(255) | | Category for organizing processes |
| DEPLOYMENT_ID_ | VARCHAR(64) | FK → ACT_RE_DEPLOYMENT | References the deployment that contains this definition |
| VERSION_ | INT | NOT NULL | Version number - increments for each new version of the same key |
| RESOURCE_NAME_ | VARCHAR(255) | | Name of the BPMN XML resource file |
| DGRM_RESOURCE_NAME_ | VARCHAR(255) | | Name of the diagram resource file (if generated) |
| HAS_START_FORM_KEY_ | BOOLEAN | | Whether this process has a start form |
| HAS_GRAPHICAL_NOTATION_ | BOOLEAN | | Whether graphical notation is available |
| SUSPENSION_STATE_ | INT | | 0 = active, 1 = suspended |
| TENANT_ID_ | VARCHAR(64) | | Tenant ID (if multi-tenancy enabled) |
| VERSION_TAG_ | VARCHAR(64) | | Optional version tag for the process definition |

**Relationships:**
- Referenced by: ACT_RU_PROCESS_INSTANCE, ACT_RU_EXECUTION, ACT_RE_DECISION_DEF
- References: ACT_RE_DEPLOYMENT

**Database-Specific Notes:**

- **MySQL/MariaDB:** VARCHAR(255) is used for NAME_, CATEGORY_, RESOURCE_NAME_; consider VARCHAR(max) if names exceed 255 characters
- **Oracle:** Uses VARCHAR2 instead of VARCHAR
- **MSSQL:** BOOLEAN values stored as 0/1; SUSPENSION_STATE_ is INT (0 or 1)
- **DB2:** Column names must respect DB2's identifier limits; consider alias if exceeded
- **PostgreSQL:** BOOLEAN type available; uses true/false or 0/1
- **H2:** Full BOOLEAN type support

**Example Queries:**

Get the latest version of all active processes:
\`\`\`sql
SELECT p1.* FROM ACT_RE_PROCDEF p1
WHERE SUSPENSION_STATE_ = 0
AND (p1.KEY_, p1.VERSION_) IN (
  SELECT KEY_, MAX(VERSION_) FROM ACT_RE_PROCDEF GROUP BY KEY_
)
ORDER BY p1.KEY_;
\`\`\`

Find all process definitions in a specific deployment:
\`\`\`sql
SELECT * FROM ACT_RE_PROCDEF WHERE DEPLOYMENT_ID_ = ?;
\`\`\`
```

Repeat this structure for ACT_RU_PROCESS_INSTANCE and ACT_RU_EXECUTION.

- [ ] **Step 3: Add module summary at top**

At the very beginning, add:
```markdown
---
last_updated: 2026-06-09
schema_version: 7.24
---
```

- [ ] **Step 4: Commit**

```bash
git add docs/reference/db-schema/process-management.md
git commit -m "docs: add process management domain documentation"
```

### Task 6: Document Task Management Module

**Files:**
- Create: `docs/reference/db-schema/task-management.md`

- [ ] **Step 1: Create module with tables: ACT_RU_TASK, ACT_RU_VARIABLE, ACT_RU_TASK_METER_LOG**

Follow the same structure as Task 5:
1. Module header with domain description and domain ER diagram
2. Per-table entries with columns, relationships, DB-specific notes, example queries
3. Metadata header

Key tables:
- **ACT_RU_TASK:** User or system tasks that need to be completed
- **ACT_RU_VARIABLE:** Variable values (string, integer, JSON, file reference, etc.)
- **ACT_RU_TASK_METER_LOG:** Metrics for task execution

Example column details for ACT_RU_TASK:
- ID_, CREATED_, SUSPENDED_, PRIORITY_, ASSIGNEE_, OWNER_
- TASK_DEF_KEY_, PROC_INST_ID_, EXECUTION_ID_, CASE_EXECUTION_ID_
- DUE_DATE_, FOLLOW_UP_DATE_, DELEGATION_STATE_

Example column details for ACT_RU_VARIABLE:
- ID_, NAME_, TYPE_, VALUE_, PROC_INST_ID_, EXECUTION_ID_, TASK_ID_
- CASE_EXECUTION_ID_, CASE_INST_ID_

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/task-management.md
git commit -m "docs: add task management domain documentation"
```

### Task 7: Document Deployment Management Module

**Files:**
- Create: `docs/reference/db-schema/deployment-management.md`

- [ ] **Step 1: Create module with tables: ACT_RE_DEPLOYMENT, ACT_RE_DEPLOYMENT_RESOURCE, ACT_GE_BYTEARRAY**

Key information:
- **ACT_RE_DEPLOYMENT:** Groups related resources (process definitions, decision definitions, etc.) deployed together
- **ACT_RE_DEPLOYMENT_RESOURCE:** References resources within a deployment
- **ACT_GE_BYTEARRAY:** Stores binary data (BPMN XML files, images, etc.)

Important columns:
- Deployment: DEPLOY_TIME_, SOURCE_, TENANT_ID_
- Resource: RESOURCE_NAME_, DEPLOYMENT_ID_
- ByteArray: NAME_, BYTES_, DEPLOYMENT_ID_, PROC_DEF_ID_

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/deployment-management.md
git commit -m "docs: add deployment management domain documentation"
```

### Task 8: Document History Module

**Files:**
- Create: `docs/reference/db-schema/history.md`

- [ ] **Step 1: Create module with all ACT_HI_* tables**

Tables to include:
- ACT_HI_PROC_INST - Historic process instance data
- ACT_HI_ACT_INST - Historic activity execution
- ACT_HI_TASK_INST - Historic task execution
- ACT_HI_VARINST - Historic variable values
- ACT_HI_INCIDENT - Historic incidents (failures/errors)
- ACT_HI_JOB_LOG - Historic job execution
- ACT_HI_OP_LOG - Historic operations
- ACT_HI_DETAIL - Historic variable changes/updates

Key design note: History tables mirror runtime tables but include additional temporal columns:
- START_TIME_, END_TIME_, DURATION_
- STATE_ (COMPLETED, DELETED, ACTIVE, etc.)

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/history.md
git commit -m "docs: add history domain documentation"
```

### Task 9: Document Authorization Module

**Files:**
- Create: `docs/reference/db-schema/authorization.md`

- [ ] **Step 1: Create module with identity and authorization tables**

Tables:
- ACT_RU_AUTHORIZATION - Permission rules
- ACT_ID_USER - Users
- ACT_ID_GROUP - Groups
- ACT_ID_TENANT - Tenants (for multi-tenancy)
- ACT_ID_MEMBERSHIP - User-group memberships
- ACT_ID_USER_ACCOUNT - External account mappings for users
- ACT_ID_GROUP_ACCOUNT - External account mappings for groups
- ACT_ID_TENANT_MEMBER - Tenant members

Key columns for ACT_RU_AUTHORIZATION:
- TYPE_ (0=ALLOW, 1=REVOKE)
- PERMISSION_ (different values per resource type)
- USER_ID_, GROUP_ID_, RESOURCE_ID_, RESOURCE_TYPE_

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/authorization.md
git commit -m "docs: add authorization domain documentation"
```

### Task 10: Document Case Management Module

**Files:**
- Create: `docs/reference/db-schema/case-management.md`

- [ ] **Step 1: Create module with CMMN case tables**

Tables:
- ACT_CAS_DEF - Case definitions
- ACT_CAS_CASE_DEF_PROP - Case definition properties
- ACT_CAS_INSTANCE - Case instances
- ACT_CAS_ACT_INST - Case activity instances

Key note: Case management is optional feature (CMMN), similar to process management but for case workflows.

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/case-management.md
git commit -m "docs: add case management domain documentation"
```

### Task 11: Document Decision Management Module

**Files:**
- Create: `docs/reference/db-schema/decision-management.md`

- [ ] **Step 1: Create module with DMN decision tables**

Tables:
- ACT_RE_DECISION_DEF - Decision definitions (DMN decision tables)
- ACT_RE_DECISION_REQ_DEF - Decision requirements (relationships between decisions)
- ACT_HI_DECISION_INST - Historic decision evaluations
- ACT_DMN_DECISION_INSTANCE - DMN decision instances (runtime)
- ACT_DMN_REQUIREMENT_DEFINITION - DMN requirement definitions

Key note: Decisions are deployed with processes and can be invoked from process tasks.

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/decision-management.md
git commit -m "docs: add decision management domain documentation"
```

### Task 12: Document System Properties Module

**Files:**
- Create: `docs/reference/db-schema/system-properties.md`

- [ ] **Step 1: Create module with system and infrastructure tables**

Tables:
- ACT_GE_PROPERTY - System properties and locks (schema version, lock entries, IDs)
- ACT_GE_SCHEMA_LOG - Schema version history/audit trail
- ACT_RU_JOB - Background jobs (timers, async tasks, etc.)
- ACT_RU_JOBDEF - Job definitions
- ACT_RU_INCIDENT - Incident/failure tracking
- ACT_RU_BATCH - Batch operation records
- ACT_RU_EXT_TASK - External task subscriptions
- ACT_RU_EVENT_SUBSCR - Event subscriptions (message, signal, etc.)

Key table: ACT_GE_PROPERTY stores critical system state:
- schema.version - Current schema version
- deployment.lock - Lock for deployment operations
- history.cleanup.job.lock - Lock for history cleanup
- startup.lock - Lock during engine startup
- next.dbid - Next available ID

- [ ] **Step 2: Commit**

```bash
git add docs/reference/db-schema/system-properties.md
git commit -m "docs: add system properties domain documentation"
```

---

## Phase 4: Verification and Finalization

### Task 13: Verify Documentation Completeness and Cross-References

**Files:**
- Reference: All docs/reference/db-schema/*.md files
- Reference: docs/reference/db-schema/_schema-analysis.txt

- [ ] **Step 1: Verify all tables from schema are documented**

Extract all table names from analysis file:
```bash
grep "^TABLE:" docs/reference/db-schema/_schema-analysis.txt | wc -l
```

Search for each table name in all module files to ensure it's documented. Run:
```bash
for table in $(grep "^TABLE:" docs/reference/db-schema/_schema-analysis.txt | sed 's/TABLE: //' | sed 's/ .*//' | sort); do
  if ! grep -q "## $table" docs/reference/db-schema/*.md; then
    echo "MISSING: $table"
  fi
done
```

Expected: No "MISSING" output

- [ ] **Step 2: Verify all foreign key references are valid**

For each foreign key in index.md and module diagrams, verify:
1. Referenced table exists and is documented
2. Reference direction is correct
3. No orphaned references

Example check for ACT_RU_PROCESS_INSTANCE → ACT_RE_PROCDEF:
```bash
grep -A 10 "## ACT_RU_PROCESS_INSTANCE" docs/reference/db-schema/process-management.md | grep "ACT_RE_PROCDEF"
```

- [ ] **Step 3: Verify all internal cross-links work**

Check that all markdown links between files are valid:
```bash
grep -r "\[.*\](.*\.md#" docs/reference/db-schema/ | while read link; do
  file=$(echo "$link" | sed 's/.*(\([^)]*\)).*/\1/' | sed 's/#.*//')
  anchor=$(echo "$link" | sed 's/.*#//')
  if [ ! -f "docs/reference/db-schema/$file" ]; then
    echo "BROKEN FILE LINK: $link"
  fi
done
```

- [ ] **Step 4: Verify Mermaid diagrams render**

Open each markdown file in a Mermaid-capable viewer (GitHub, VS Code) and verify:
1. All module diagrams render without syntax errors
2. Index full schema diagram displays correctly
3. No missing entities or relationships

- [ ] **Step 5: Verify example queries syntax**

For each example query in the documentation, check basic syntax:
- Runs without SQL errors (use `postgres` or preferred DB CLI)
- Column names match documented columns
- Table names are correct and exist

Example check:
```bash
psql -h localhost -U postgres -d operaton_db -c "SELECT * FROM ACT_RE_PROCDEF WHERE 1=0;" 2>&1 | head -5
```

- [ ] **Step 6: Commit verification results**

```bash
git add docs/reference/db-schema/
git commit -m "docs: verify schema documentation completeness and cross-references"
```

### Task 14: Final Review and Cleanup

**Files:**
- Modify: All docs/reference/db-schema/*.md files
- Delete: docs/reference/db-schema/_schema-analysis.txt (temporary working file)

- [ ] **Step 1: Remove temporary analysis file**

```bash
rm docs/reference/db-schema/_schema-analysis.txt
git rm docs/reference/db-schema/_schema-analysis.txt
```

- [ ] **Step 2: Do final consistency check**

Read through index.md and verify:
1. Schema version info is correct (7.24)
2. All domains are listed and have links
3. Quick reference table is complete and accurate
4. ER diagram is comprehensive
5. Common query patterns are helpful

Read through 1-2 module files and verify:
1. Module description is clear
2. All tables in that domain are documented
3. Domain ER diagram shows key relationships
4. Database-specific notes are useful
5. Example queries are practical

- [ ] **Step 3: Update metadata in all files**

Ensure each module has metadata header:
```yaml
---
last_updated: 2026-06-09
schema_version: 7.24
---
```

Run:
```bash
for file in docs/reference/db-schema/*.md; do
  if ! head -5 "$file" | grep -q "^---$"; then
    echo "Adding metadata header to $file"
    sed -i '1i---\nlast_updated: 2026-06-09\nschema_version: 7.24\n---\n' "$file"
  fi
done
```

Then manually review and clean up any duplicates.

- [ ] **Step 4: Final commit**

```bash
git add docs/reference/db-schema/
git commit -m "docs: finalize schema reference documentation

- Remove temporary working files
- Add metadata headers to all modules
- Verify all cross-references and examples
- Schema version: 7.24
- Includes 8 domain modules with ER diagrams and DB-specific notes"
```

---

## Verification Checklist

Before marking implementation complete, verify:

- [ ] All 8 domain modules created: process-management.md, task-management.md, deployment-management.md, history.md, authorization.md, case-management.md, decision-management.md, system-properties.md
- [ ] Index file created with schema version info, quick reference table, full ER diagram, common query patterns
- [ ] All documented tables match canonical schema (extracted from SQL files)
- [ ] All foreign key relationships properly documented with bidirectional references
- [ ] Database-specific notes included for MySQL, PostgreSQL, Oracle, MariaDB, MSSQL, DB2, H2
- [ ] Example queries provided for each domain (at least 2-3 practical queries)
- [ ] All Mermaid diagrams render without syntax errors
- [ ] All internal cross-links verified as working
- [ ] No "TODO", "TBD", or placeholder content remains
- [ ] Commit messages follow conventional commits format

---

## Success Criteria

Documentation is complete when:
1. Users can find any table by searching the quick reference in index.md
2. Users can understand relationships between tables from ER diagrams
3. Users can see example queries for common use cases
4. Users understand database-specific considerations for their database platform
5. All 40+ tables are documented with column definitions, constraints, and purposes
6. Documentation is discoverable from the main docs navigation
