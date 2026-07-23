---
title: "2.2 (DRAFT)"
sidebar_position: 22
---

# About release 2.2

## New and Noteworthy

### Spring Boot 4.1 Upgrade

Operaton 2.2 upgrades the Spring Boot baseline from **4.0.x** to **Spring Boot 4.1**. This
upgrade brings in the latest Spring Framework improvements, updated dependency baselines, and
continued alignment with the Spring ecosystem's active release line.

Existing Spring Boot applications built on Operaton 2.1 should migrate smoothly. Refer to the
[Spring Boot 4.1 migration guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.1-Release-Notes)
for any application-level adjustments.

This implements [PR #2844](https://github.com/operaton/operaton/pull/2844).

---

### WildFly 40 Upgrade & CDI 4.1 Compatibility

Operaton 2.2 upgrades the WildFly distribution to **WildFly 40** and adapts the CDI integration
to the **Jakarta CDI 4.1** standard API.

Key improvements:

- **`BeanManager` lookup via CDI 4.1 standard API**: The `BeanManager` is now resolved through
  the Jakarta CDI 4.1 standard API (`CDI.current().getBeanManager()`), which works correctly
  inside the WildFly module classloader. The previous approach relying on JNDI lookup could fail
  in certain module isolation scenarios.

- **Null-safe `CdiResolver`**: `CdiResolver` is now null-safe to prevent breaking the EL
  resolver chain when CDI is not fully initialised or unavailable in a given context.

- **Optional module dependencies**: The module descriptor now declares
  `jakarta.faces.api` and `jakarta.enterprise.concurrent.api` as **optional** module
  dependencies, so process application WARs that do not use JSF or Concurrent Utilities are not
  forced to depend on those modules.

- **No `jboss-deployment-structure.xml` required**: As a direct consequence of the CDI lookup
  and optional-dependency changes, process application WARs no longer need a
  `jboss-deployment-structure.xml` to control module visibility. Standard WAR packaging works
  out of the box on WildFly 39+.

This implements [PR #2781](https://github.com/operaton/operaton/pull/2781),  [PR #3153](https://github.com/operaton/operaton/pull/3153).

---

### Root Process Instance ID Added to MDC

The **root process instance ID** is now included in the MDC (Mapped Diagnostic Context) under
the key `rootProcessInstanceId`. This makes it straightforward to correlate log output across
call hierarchies that span multiple sub-process instances or called processes back to the
top-level root instance, improving distributed tracing and log aggregation.

This implements [PR #3114](https://github.com/operaton/operaton/pull/3114).

---

### Deadlock Detection for GraalJS Script Tasks

Operaton 2.2 improves the robustness of the `DbSqlSession` concurrency handling by detecting
deadlock conditions more reliably. The fix specifically addresses a scenario where GraalJS script
task execution could trigger a deadlock that was previously not recognized as a concurrent
modification exception, preventing proper retry handling.

---

### Task Authorization Query Performance

Task list and task count queries that use authorization checks now use an `EXISTS` subquery
instead of joining `ACT_RU_AUTHORIZATION` into the main result set.

Under high load or with large authorization tables, the previous join approach could inflate the
intermediate result set, causing slow task queries. The new `EXISTS` path short-circuits the
authorization check as soon as a matching row is found.

This resolves [PR #3152](https://github.com/operaton/operaton/pull/3152).

---

### MDC Logging: Process Definition Key from Stored Execution Property

When the MDC logging context requires the process definition key, the engine now reads it from
the already stored `ExecutionEntity#getProcessDefinitionKey()` property instead of resolving the
full process definition via a database lookup, avoiding unnecessary database round-trips during
logging.

This resolves [PR #3109](https://github.com/operaton/operaton/pull/3109).

---

### Date Form Values Accepted Correctly

A bug in the deprecated `DateFormType.convertFormValueToModelValue(Object)` path caused an error
when a date entered in one task was reused as the default value of another task's form field: the
converter received an already-converted `Date` object instead of a `String`, and rejected it.
The converter now accepts `Date` values directly in addition to `String` values.

This resolves [PR #3089](https://github.com/operaton/operaton/pull/3089).

---

### Attachment Delete Null Pointer Exception Fixed

A `NullPointerException` that could occur when deleting a task attachment without an associated
content byte array has been fixed.

This resolves [PR #3088](https://github.com/operaton/operaton/pull/3088).

---

### FEEL Engine Switched to the Unshaded Artifact

Operaton 2.2 replaces the shaded `feel-engine` classifier from `org.camunda.feel` with the
plain, unshaded artifact, and manages its real dependency tree (Scala, fastparse, geny,
sourcecode, jackson-module-scala) explicitly instead.

The shaded jar relocated Scala and fastparse to `camundajar.impl.*`, but bundled Jackson and
paranamer without relocation. This caused duplicate-class conflicts with applications' own
Jackson dependency (flagged by Maven Enforcer's `banDuplicateClasses`), and classpath-order
dependent version mixing when the bundled Jackson classes clashed with a differing
`jackson-annotations` version on the classpath. With the unshaded artifact, FEEL deterministically
uses the platform's Jackson, governed by the shared `jackson-bom` import.

Applications embedding the engine no longer need to work around these conflicts; the WildFly and
Tomcat distributions now ship proper modules/libraries for the additional third-party jars this
change pulls in.

This implements [PR #3342](https://github.com/operaton/operaton/pull/3342).

## API

### Database Schema

Operaton 2.2 does not introduce changes to the database schema.

### REST API

No REST API contract changes in this milestone release.

### New APIs

No new public APIs in this milestone release.

### Removed & Changed APIs

No removed or changed public APIs in this milestone release.

### Usage of deprecated APIs

It is **strongly recommended** to avoid using deprecated methods which are marked with the `@Deprecated(forRemoval = true)`
annotation in the Java API.

Deprecated methods within packages containing the segment `.impl.` are considered internal and should not be used by clients.
**These methods are subject to removal without prior notice.**

## Versions & Compatibility

### Java

Operaton requires **Java 17** as the minimum version.

Operaton is tested and supported on **Java 17**, **Java 21**, and **Java 25**.

### Camunda 7 Compatibility

This release is feature complete and API-compatible with [**Camunda 7 CE 7.24**](https://docs.camunda.org/manual/7.24/).

### Spring

Operaton is based on:

- **Spring Boot 4.1.0**
- **Spring Framework 7.0.7**

### Quarkus Extension

The Operaton Quarkus extension is based on **Quarkus 3.33.1 LTS**.

### Distributions

The Tomcat distribution is based on **Tomcat 11.0.22**.

The WildFly distribution is based on **WildFly 40.0.0.Final**.

### Database Compatibility

| Database   | Minimum version | Notes                             |
|------------|-----------------|-----------------------------------|
| PostgreSQL | 14              | PostgreSQL 13 EOL November 2025   |
| MariaDB    | 10.11           | 10.11 is the current LTS branch   |
| MySQL      | 8.4             | 8.4 is the current LTS branch     |

Oracle (21), SQL Server 2022, and DB2 support is unchanged.

### Standards Compliance

Operaton is compliant with the following standards:

- Jakarta EE 11
- BPMN 2.0
- DMN 1.3
- CMMN 1.1

### Scripting Languages

Operaton supports the following scripting languages:

| Language   | Engine             | Version  |
|------------|--------------------|----------|
| JavaScript | GraalVM JavaScript | 25.0.3   |
| Groovy     | Groovy             | 5.0.6    |
| Python     | Jython             | 2.7.4    |
| Ruby       | GraalVM Ruby       | 9.1.17.0 |

### Dependency Upgrades

The following non-test dependencies have been upgraded since Operaton 2.1:

| Dependency               | 2.1            | 2.2            |
|--------------------------|----------------|----------------|
| Spring Boot              | 4.0.6          | 4.1.0          |
| Apache Tomcat            | 11.0.21        | 11.0.22        |
| WildFly                  | 38.0.1.Final   | 40.0.0.Final   |
| Jackson                  | 2.21.2         | 2.21.4         |
| Groovy                   | 5.0.5          | 5.0.6          |
