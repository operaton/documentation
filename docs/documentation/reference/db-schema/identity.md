---
last_updated: 2026-07-03
schema_version: 7.24
---

# Identity (ID_)

Identity tables manage users, groups, and tenants for the built-in identity provider. These tables are optional — Operaton supports pluggable identity providers (LDAP, Kerberos, custom) that do not use this schema. When a pluggable provider is configured, `ACT_ID_*` tables may be empty or absent.

## Tables

- **[`ACT_ID_USER`](#act_id_user)** — User accounts
- **[`ACT_ID_GROUP`](#act_id_group)** — Groups/roles
- **[`ACT_ID_MEMBERSHIP`](#act_id_membership)** — User↔Group membership
- **[`ACT_ID_INFO`](#act_id_info)** — Extended user information
- **[`ACT_ID_TENANT`](#act_id_tenant)** — Tenants
- **[`ACT_ID_TENANT_MEMBER`](#act_id_tenant_member)** — User/Group↔Tenant membership

---

## ACT_ID_USER

**Purpose:** Stores user accounts for the built-in identity provider, including credentials and account lockout state.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | User identifier (e.g., `john.doe`) |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| FIRST_ | VARCHAR(255) | NULL | First name |
| LAST_ | VARCHAR(255) | NULL | Last name |
| EMAIL_ | VARCHAR(255) | NULL | Email address |
| PWD_ | VARCHAR(255) | NULL | Hashed password |
| SALT_ | VARCHAR(255) | NULL | Password salt |
| LOCK_EXP_TIME_ | TIMESTAMP | NULL | Account lock expiry (NULL = not locked) |
| ATTEMPTS_ | INTEGER | NULL | Failed login attempts since last success |
| PICTURE_ID_ | VARCHAR(64) | NULL | Reference to user picture in ACT_GE_BYTEARRAY |

**Example Queries:**

```sql
-- Find locked accounts
SELECT ID_, FIRST_, LAST_, EMAIL_, LOCK_EXP_TIME_, ATTEMPTS_
FROM ACT_ID_USER
WHERE LOCK_EXP_TIME_ IS NOT NULL AND LOCK_EXP_TIME_ > CURRENT_TIMESTAMP
ORDER BY LOCK_EXP_TIME_;

-- Search by email
SELECT ID_, FIRST_, LAST_, EMAIL_
FROM ACT_ID_USER
WHERE EMAIL_ LIKE '%@example.com'
ORDER BY LAST_, FIRST_;
```

---

## ACT_ID_GROUP

**Purpose:** Groups bundle users for authorization and task candidate assignment.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Group identifier (e.g., `managers`, `approvers`) |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| NAME_ | VARCHAR(255) | NULL | Display name |
| TYPE_ | VARCHAR(255) | NULL | Group type (e.g., `WORKFLOW`, `SYSTEM`) |

**Example Queries:**

```sql
-- All groups
SELECT ID_, NAME_, TYPE_ FROM ACT_ID_GROUP ORDER BY TYPE_, NAME_;

-- Groups a user belongs to
SELECT g.ID_, g.NAME_, g.TYPE_
FROM ACT_ID_GROUP g
JOIN ACT_ID_MEMBERSHIP m ON g.ID_ = m.GROUP_ID_
WHERE m.USER_ID_ = 'john.doe'
ORDER BY g.NAME_;
```

---

## ACT_ID_MEMBERSHIP

**Purpose:** Junction table linking users to groups. Composite primary key `(USER_ID_, GROUP_ID_)` enforces unique membership.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| USER_ID_ | VARCHAR(64) | PK, FK → ACT_ID_USER | User member |
| GROUP_ID_ | VARCHAR(64) | PK, FK → ACT_ID_GROUP | Group being joined |

**Indexes:** `ACT_IDX_MEMB_GROUP` on GROUP_ID_, `ACT_IDX_MEMB_USER` on USER_ID_

**Example Queries:**

```sql
-- All members of a group
SELECT USER_ID_ FROM ACT_ID_MEMBERSHIP
WHERE GROUP_ID_ = 'approvers'
ORDER BY USER_ID_;

-- Groups a user belongs to (IDs only)
SELECT GROUP_ID_ FROM ACT_ID_MEMBERSHIP
WHERE USER_ID_ = 'john.doe';
```

---

## ACT_ID_INFO

**Purpose:** Extensible key-value store for additional user attributes (e.g., department, phone, external account credentials). Supports hierarchical entries via `PARENT_ID_`.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Entry identifier |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| USER_ID_ | VARCHAR(64) | NULL | Owning user |
| TYPE_ | VARCHAR(64) | NULL | Entry type (e.g., `userinfo`, `account`) |
| KEY_ | VARCHAR(255) | NULL | Attribute key |
| VALUE_ | VARCHAR(255) | NULL | Attribute value (plain text) |
| PASSWORD_ | BYTEA | NULL | Encrypted value (for sensitive attributes like account passwords) |
| PARENT_ID_ | VARCHAR(255) | NULL | Parent entry ID for hierarchical grouping |

**Example Queries:**

```sql
-- All info entries for a user
SELECT TYPE_, KEY_, VALUE_
FROM ACT_ID_INFO
WHERE USER_ID_ = 'john.doe' AND TYPE_ = 'userinfo'
ORDER BY KEY_;
```

---

## ACT_ID_TENANT

**Purpose:** Defines tenants for multi-tenancy isolation. Tenants allow independent data partitioning within a single Operaton installation.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Tenant identifier (e.g., `acme-corp`) |
| REV_ | INTEGER | NULL | Revision for optimistic locking |
| NAME_ | VARCHAR(255) | NULL | Display name |

**Example Queries:**

```sql
SELECT ID_, NAME_ FROM ACT_ID_TENANT ORDER BY NAME_;
```

---

## ACT_ID_TENANT_MEMBER

**Purpose:** Associates users or groups with tenants. A member may be a user OR a group (not both simultaneously). Unique constraints prevent duplicate membership per combination.

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ID_ | VARCHAR(64) | PK NOT NULL | Member entry identifier |
| TENANT_ID_ | VARCHAR(64) | FK → ACT_ID_TENANT, NOT NULL | Tenant |
| USER_ID_ | VARCHAR(64) | FK → ACT_ID_USER, NULL | User member (NULL if group) |
| GROUP_ID_ | VARCHAR(64) | FK → ACT_ID_GROUP, NULL | Group member (NULL if user) |

**Unique Constraints:**
- `ACT_UNIQ_TENANT_MEMB_USER` on `(TENANT_ID_, USER_ID_)`
- `ACT_UNIQ_TENANT_MEMB_GROUP` on `(TENANT_ID_, GROUP_ID_)`

**Indexes:** `ACT_IDX_TENANT_MEMB`, `ACT_IDX_TENANT_MEMB_USER`, `ACT_IDX_TENANT_MEMB_GROUP`

**Example Queries:**

```sql
-- All members of a tenant
SELECT COALESCE(USER_ID_, GROUP_ID_) AS member,
       CASE WHEN USER_ID_ IS NOT NULL THEN 'user' ELSE 'group' END AS member_type
FROM ACT_ID_TENANT_MEMBER
WHERE TENANT_ID_ = 'acme-corp'
ORDER BY member_type, member;

-- Tenants a user belongs to
SELECT TENANT_ID_ FROM ACT_ID_TENANT_MEMBER
WHERE USER_ID_ = 'john.doe';
```

---

## Design Notes

- `ACT_ID_*` tables are only populated when using the **built-in identity provider**.
- `ACT_RU_AUTHORIZATION.USER_ID_` and `GROUP_ID_` are string references — there are no foreign keys to `ACT_ID_USER`/`ACT_ID_GROUP`. Authorization works with any identity source.
- Account locking: `LOCK_EXP_TIME_` + `ATTEMPTS_` in `ACT_ID_USER` implement brute-force protection. Unlock by setting `LOCK_EXP_TIME_ = NULL` and `ATTEMPTS_ = 0`.
- `ACT_ID_INFO.PASSWORD_` stores encrypted bytes (not plain text); use the Operaton API to manage account credentials.

---

See [Database-Specific Implementation Notes](index.md#database-specific-implementation-notes) for type mappings.

---

**Last Updated:** 2026-07-03 | **Schema Version:** 7.24 | **Operaton Versions:** 1.0.0+
