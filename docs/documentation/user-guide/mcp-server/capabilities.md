---

title: "Capabilities and Examples"
sidebar_position: 20

---
# Capabilities and Examples

The Operaton MCP server groups its tools by resource. The following sections describe each group. Which tools the assistant actually sees depends on the configured [access control guards](configuration.md#access-control-guards).

## Process Definitions

Browse, inspect, suspend and delete deployed BPMN process definitions.

- List and count process definitions, filtered by key, name, version or tenant.
- Get a process definition by ID, or the latest version by key.
- Get the BPMN 2.0 XML of a process definition.
- Get process-level and activity-level statistics of running instances.
- Suspend or activate a process definition by key.
- Delete a process definition by ID or key, optionally with its instances and history.
- Restart historic process instances, synchronously or asynchronously.
- Set the history time to live of a process definition.
- List the process definitions called statically by a process definition.

## Deployments

Deploy and manage BPMN, DMN, CMMN and form resources.

- Create a deployment from uploaded resources.
- List and count deployments.
- Get a deployment by ID and list its resources.
- Redeploy the resources of an existing deployment.
- Delete a deployment.

## Process Instances

Start process instances and manage their lifecycle.

- Start a process instance by definition ID or key, with an optional business key and variables.
- List and count process instances.
- Get a process instance and its activity instance tree.
- Suspend or activate a process instance, or all instances of a process definition, key or tenant.
- Delete a process instance.
- Read and write process variables.

## Tasks

Query and work on user tasks.

- List and count tasks with the task query filters.
- Get a task by ID.
- Claim, unclaim, delegate, resolve and complete tasks; complete with output variables.
- Set or change the assignee.
- Create a standalone task or update task properties.
- Read and write task variables.
- Throw a BPMN error from a task.

## Jobs and Job Definitions

Inspect and control asynchronous jobs such as timers and asynchronous continuations.

- List and count jobs; get a job by ID.
- Execute a job immediately.
- Suspend or activate a job.
- Set the retries of a failed job.
- Get the exception stack trace of a failed job.
- List job definitions, get a job definition, and suspend or activate job definitions of a process definition.

## Incidents

Query and resolve incidents, for example failed jobs or failed external tasks.

- List and count open incidents.
- Get an incident by ID.
- Resolve an incident.

## Users and Groups

Manage users, groups and group memberships.

- List users, get a user profile, create and delete users.
- Update a user's profile or password.
- Unlock a user locked after too many failed login attempts.
- List, create and delete groups.
- Add users to groups and remove them.

## History

Query the history of process data.

- Historic process instances, activity instances and task instances.
- Historic variable instances and incidents.
- Historic job logs.
- User operation log entries, i.e. the audit log of operations such as claiming or completing tasks.

## Decisions

Inspect and evaluate DMN decisions.

- List decision definitions and get a decision definition by key.
- Get the DMN XML of a decision definition.
- Evaluate a decision with input variables.
- List decision requirements definitions.

## Migration

Plan, execute, monitor and audit the [migration of process instances](../process-engine/process-instance-migration.md) between versions of a process definition.

| Tool | Purpose |
|---|---|
| `processInstance_listMigratable` | List active instances that can be migrated, including conditions that block migration, such as call activities |
| `processDefinition_getMigrationCandidates` | Compare source and target activities: activities that can be mapped automatically, unmapped source activities and new target activities |
| `migration_generatePlan` | Generate a migration plan with automatically mapped instructions and a list of activities that need explicit mapping |
| `migration_validatePlan` | Validate a migration plan against a set of instances |
| `migration_executeBatch` | Execute a migration plan as a batch, split into chunks automatically; supports a dry run |
| `migration_awaitBatch` | Wait for batches to complete or time out, and report progress |
| `migration_getBatchStatus` | Get job counts and suspension state of a batch |
| `migration_suspendBatch`, `migration_resumeBatch`, `migration_deleteBatch` | Suspend, resume or cancel batches |
| `migration_listBatches` | List active migration batches |
| `migration_getBatchFailures` | Get failure details per instance, including error messages and stack traces |
| `migration_retryFailedJobs` | Reset the retries of all failed migration jobs of a batch |
| `migration_getBatchSummary` | Summarize submitted, succeeded and failed instances and the duration |
| `migration_listAuditEntries` | Query the user operation log for migration entries |
| `migration_listHistoricBatches` | Query completed migration batches |

A typical migration with the assistant follows these steps:

1. Find migratable instances (`processInstance_listMigratable`).
2. Generate a plan (`migration_generatePlan`) and resolve unmapped activities.
3. Validate the plan (`migration_validatePlan`).
4. Execute the batch, first as a dry run (`migration_executeBatch`).
5. Wait for completion (`migration_awaitBatch`) and check the result (`migration_getBatchSummary`, `migration_getBatchFailures`).

## Example Prompts

The following prompts show what an assistant can do with the MCP server. The assistant chooses the tools itself.

### Deployments and Process Definitions

- "Deploy this BPMN file to Operaton and name the deployment `loan-approval-v3`."
- "List all deployed versions of the `invoice-approval` process."
- "Show me the BPMN XML of the latest version of the `onboarding` process."

### Process Instances

- "Start the `invoice-approval` process with business key `INV-2024-001` and set the variable `amount` to 15000."
- "List all active instances of the `loan-approval` process."
- "Which variables are set on process instance `abc-123`?"

### User Tasks

- "Show me all unassigned tasks of the `approvers` group."
- "Claim task `task-456` for user `john.doe`."
- "Complete the approval task for invoice `INV-2024-001` and set `approved` to `true`."

### Operations and Incidents

- "Are there failed jobs without retries left?"
- "Set the retries of job `job-789` to 3 and execute it immediately."
- "List all open incidents of the `payment-processing` process."

### History and Audit

- "Show me all `invoice-approval` instances completed last week."
- "Who completed the approval task for business key `INV-2024-001`, and when?"

### Decisions

- "Deploy this DMN decision table for the loan eligibility check."
- "Evaluate the `credit-check` decision with `income` = 50000 and `creditScore` = 720."

### Migration

- "Which instances of `invoice-approval` version 3 can be migrated to version 4?"
- "Create a migration plan from version 3 to version 4 of `invoice-approval`, validate it and run a dry run."
