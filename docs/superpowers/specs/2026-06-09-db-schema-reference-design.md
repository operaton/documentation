# DB Schema Reference Documentation Design

**Date:** 2026-06-09  
**Status:** Approved  
**Audience:** Developers and DBAs  
**Scope:** Current schema only (version 7.24)

## Overview

This design specifies a modular, markdown-based reference documentation for the Operaton database schema. The documentation will serve developers and DBAs who need to explore the schema, write queries, understand versioning, and troubleshoot data issues.

## Approach: Modular Documentation by Functional Domain

Rather than a single comprehensive file, the schema will be documented across multiple focused markdown files organized by functional domain. Each domain module will contain:
- Tables related to that functional area
- Detailed column definitions with constraints and descriptions
- Mermaid ER diagrams showing relationships within the domain
- Database-specific notes where applicable
- Example queries

A central index file will provide:
- Schema version mapping (which Operaton versions use schema 7.24)
- Full schema ER diagram (all tables and relationships)
- Quick-reference table of all tables with one-line descriptions
- Links to detailed modules
- Common query patterns

## File Structure

```
docs/reference/
├── db-schema/
│   ├── index.md                          # Overview, schema versioning, ER diagram, quick reference
│   ├── process-management.md            # Process definitions, instances, variables
│   ├── task-management.md               # Task management tables
│   ├── deployment-management.md         # Deployments, resources, byte arrays
│   ├── history.md                       # All ACT_HI_* historical tables
│   ├── authorization.md                 # Users, groups, roles, permissions
│   ├── case-management.md               # Case-related tables
│   ├── decision-management.md           # DMN decision tables
│   └── system-properties.md             # System configuration, locks, properties
```

## Content Structure Per Module File

### Header Section
- **Domain Description:** Brief explanation of what this domain manages
- **Mermaid ER Diagram:** Entity-relationship diagram showing tables in this domain and their relationships
- **Tables Covered:** List of tables included in this module

### Per-Table Entry Format

Each table entry includes:

```markdown
## TableName (ACT_XX_YYYY)

**Purpose:** [Clear description of what this table stores and why it exists]

**Columns:**
| Column Name | Type | Constraints | Description |
|---|---|---|---|
| ID_ | VARCHAR(64) | PRIMARY KEY | [What this column represents] |
| [name] | [type] | [constraints] | [description] |

**Relationships:**
- Foreign keys: [List tables this one references]
- Referenced by: [List tables that reference this one]

**Database-Specific Notes:**
- **MySQL:** [Any MySQL-specific considerations]
- **PostgreSQL:** [Any PostgreSQL-specific considerations]
- **Oracle:** [Any Oracle-specific considerations]
- **MariaDB:** [Any MariaDB-specific considerations]
- **MSSQL:** [Any MSSQL-specific considerations]
- **DB2:** [Any DB2-specific considerations]
- **H2:** [Any H2-specific considerations]

**Example Queries:**
- [1-2 practical queries developers might use with this table]
```

## Index/Overview File Details (db-schema/index.md)

The index file serves as the entry point and quick reference:

### Sections:
1. **Schema Version Information**
   - Current schema version: 7.24
   - Mapping of Operaton versions to schema versions (e.g., 1.0.0 → 7.24, 2.1.1 → 7.24)
   - Explanation of versioning strategy

2. **Full Schema ER Diagram**
   - Mermaid diagram showing all tables and their relationships
   - Organized logically by domain
   - Shows primary and foreign key relationships

3. **Quick Reference Table**
   - Table name | Domain | Purpose (one-line description)
   - Sortable/scannable format for quick lookup
   - Links to detailed module sections

4. **Schema Domains Overview**
   - Brief description of each domain
   - Link to detailed module file
   - Key tables at a glance

5. **Common Query Patterns**
   - "Find all process instances for a deployment"
   - "Query task history for a user"
   - "Get process variables"
   - (Links to detailed examples in respective modules)

## Mermaid Diagram Strategy

### Full Schema Diagram (in index.md)
- Shows all tables across all domains
- Color-coded by domain for visual organization
- Displays cardinality on relationships
- Simplified table names for readability

### Domain-Specific Diagrams (in each module)
- Shows only tables in that domain
- More detailed view of internal relationships
- Highlights key relationships to other domains
- Includes column names for primary/foreign keys

## Database-Specific Notes Handling

For each table, differences across supported databases will be documented:
- **Column Type Variations:** VARCHAR vs VARCHAR2, VARCHAR(max) vs TEXT, etc.
- **SQL Dialect Differences:** Constraint syntax, default values, sequences vs auto-increment
- **Indexing:** Database-specific index strategies or recommendations
- **Naming Conventions:** Any DB-specific naming rules applied
- **Null Handling:** Any database-specific NULL constraint differences

## Content Guidelines

1. **Canonical Schema:** All column types and constraints are based on the PostgreSQL schema as the baseline. Variations for other databases are documented in the "Database-Specific Notes" section.

2. **Column Descriptions:** Should be precise and explain:
   - What data is stored (e.g., "Process instance ID that owns this task")
   - Why (e.g., "Used to link task to parent process instance")
   - Any important constraints or formats (e.g., "Must be unique within deployment")

3. **Relationships:** Foreign keys should clearly show:
   - Which table is referenced
   - Cardinality (one-to-many, one-to-one, etc.)
   - Cascade delete behavior if relevant

4. **Example Queries:** Should be:
   - Practical and immediately useful to developers
   - Database-agnostic where possible (use standard SQL)
   - Include a comment explaining what the query does

## Maintenance and Evolution

- **Current Documentation:** Only documents schema version 7.24
- **When Schema Changes:** If a future schema version (7.25+) differs from 7.24:
  - Create new documentation set for that version
  - Maintain backwards compatibility notes
  - Decision on versioning approach to be made at that time

## Success Criteria

The documentation will be considered complete when:
- [ ] All tables across all domains are documented with full details
- [ ] Each domain module has its own ER diagram
- [ ] Index file provides both overview and quick-reference capabilities
- [ ] Database-specific notes are complete for all supported databases
- [ ] Example queries are provided for common use cases
- [ ] Documentation is committed to git and linked from main docs
