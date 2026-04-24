---

title: "2.1"
sidebar_position: 21

---

# About release 2.1

## New and Noteworthy

### Session Cookie Path Isolation for Spring Boot

When running Operaton alongside other authentication providers (e.g. Keycloak) in the same
Spring Boot application, the Operaton web app and the backend previously shared the same session
cookie (`JSESSIONID`). Concurrent requests from a frontend could overwrite the session cookie,
causing session conflicts and unexpected logouts.

Operaton 2.1 introduces a new property to enforce a scoped `Path` attribute on the Operaton
session cookie, isolating it from cookies set by the rest of the application:

```properties
operaton.bpm.webapp.session-cookie-path-enforcement=true
```

When enabled, the `SessionCookiePathFilter` rewrites the `Path` attribute of the Operaton session
cookie to `/operaton` (or to the configured `operaton.bpm.webapp.application-path`), so the
cookie is only sent for requests under that path.

**Default behaviour:** The property defaults to `false` — existing deployments are not affected.

**Example — enabling isolation in `application.yaml`:**

```yaml
operaton:
  bpm:
    webapp:
      session-cookie-path-enforcement: true
      # application-path: /operaton   # defaults to /operaton
```

**Interaction with a custom session cookie name:**

If the session cookie has been renamed via Spring's `server.servlet.session.cookie.name`
property, the `SessionCookiePathFilter` automatically picks up that name and applies the path
restriction to the renamed cookie:

```properties
server.servlet.session.cookie.name=OPERATON_SESSION
operaton.bpm.webapp.session-cookie-path-enforcement=true
```

This resolves [issue #1632](https://github.com/operaton/operaton/issues/1632).

---

### SPI Configuration Factories

Operaton 2.1 introduces two new Service Provider Interface (SPI) factory interfaces that decouple
the configuration APIs from their implementation classes:

- `org.operaton.bpm.engine.spi.ProcessEngineConfigurationFactory`
- `org.operaton.bpm.dmn.engine.spi.DmnEngineConfigurationFactory`

These interfaces are discovered at runtime via Java's `ServiceLoader` mechanism and allow
frameworks or embedding tools to plug in custom configuration implementations without depending
on internal implementation classes.

**`ProcessEngineConfigurationFactory`** (module `operaton-engine`):

```java
package org.operaton.bpm.engine.spi;

public interface ProcessEngineConfigurationFactory {
  ProcessEngineConfiguration createProcessEngineConfigurationFromResourceDefault();
  ProcessEngineConfiguration createProcessEngineConfigurationFromResource(String resource);
  ProcessEngineConfiguration createProcessEngineConfigurationFromResource(String resource, String beanName);
  ProcessEngineConfiguration createProcessEngineConfigurationFromInputStream(InputStream inputStream);
  ProcessEngineConfiguration createProcessEngineConfigurationFromInputStream(InputStream inputStream, String beanName);
  ProcessEngineConfiguration createStandaloneProcessEngineConfiguration();
  ProcessEngineConfiguration createStandaloneInMemProcessEngineConfiguration();
}
```

**`DmnEngineConfigurationFactory`** (module `operaton-engine-dmn`):

```java
package org.operaton.bpm.dmn.engine.spi;

public interface DmnEngineConfigurationFactory {
  DmnEngineConfiguration createDefaultDmnEngineConfiguration();
}
```

The existing factory methods on `ProcessEngineConfiguration` and `DmnEngineConfiguration` are
unchanged and continue to work as before — they now delegate to the SPI implementation discovered
via `ServiceLoader`. The default implementations are
`ProcessEngineConfigurationFactoryImpl` and `DmnEngineConfigurationFactoryImpl`.

This change implements [PR #1804](https://github.com/operaton/operaton/pull/1804).

---

### Quarkus LTS

The Operaton Quarkus extension is now based on the **Quarkus 3.33 LTS** release (previously
3.32.0, a non-LTS release). Moving to the LTS stream means the extension benefits from a
longer support window and more stable dependency versions.

Operaton 2.x will continue to be based on the latest 3.33 LTS release line.

---

### Health SPI and `/health` Endpoint

Operaton 2.1 introduces a runtime-agnostic **Health SPI** that allows health checks to be
plugged in across different deployment runtimes (Spring Boot, Quarkus, and plain Java). The SPI
is defined in the `operaton-engine` module and consists of three public types:

**`HealthService`** — the central health check interface:

```java
package org.operaton.bpm.engine.health;

public interface HealthService {
  HealthResult check();
}
```

**`HealthResult`** — an immutable record that carries the check outcome:

```java
package org.operaton.bpm.engine.health;

public record HealthResult(String status, String timestamp, String version, Map<String, Object> details) { }
```

The `status` field is `"UP"` or `"DOWN"`. The `details` map may contain nested sub-maps for
individual health contributors (database, job executor, frontend webapp).

**`FrontendHealthContributor`** — optional SPI to include webapp availability details:

```java
package org.operaton.bpm.engine.health;

public interface FrontendHealthContributor {
  Map<String, Object> frontendDetails();
}
```

The default implementation (`DefaultHealthService`) probes the JDBC `DataSource` and the
`JobExecutor` state. An inactive or absent job executor does not affect the overall
`UP`/`DOWN` status — only a failed database connection marks the engine as `DOWN`.

#### Spring Boot integration

In Spring Boot deployments, `HealthService` is auto-configured as a `@Bean` via
`OperatonBpmHealthServiceConfiguration`. A custom bean implementing `HealthService` replaces
the default. The `ProcessEngineHealthIndicator` Spring Boot Actuator health indicator exposes
the result at the standard `/actuator/health` endpoint (enabled by default, controlled via
`management.health.operaton.enabled`):

```yaml
# application.yaml — disable the Operaton health indicator
management:
  health:
    operaton:
      enabled: false
```

#### Quarkus integration

In Quarkus deployments, `OperatonHealthCheck` implements the MicroProfile Health `@Readiness`
check and is exposed automatically at `/q/health/ready`.

#### Operaton Run — dedicated `/health` endpoint

The Operaton Run distribution exposes a lightweight, cache-disabled JSON endpoint at `/health`
that is designed for load balancers and uptime monitors. It returns HTTP 200 (`UP`) or 503
(`DOWN`), and is **disabled by default**. Enable it with:

```properties
operaton.run.health.rest-endpoint.enabled=true
```

**Example response:**

```json
{
  "status": "UP",
  "timestamp": "2026-04-01T12:00:00+02:00",
  "version": "2.1.0",
  "details": {
    "jobExecutor": { "operational": true },
    "database":    { "connected": true },
    "frontend":    { "operational": true, "path": "/operaton" }
  }
}
```

This implements [PR #2730](https://github.com/operaton/operaton/pull/2730).

---

### GraalJS Memory Leak Fix

Operaton 2.1 fixes a **progressive memory leak** that occurred when using JavaScript script tasks
(e.g. process variables transformed via Spin/JSON) under sustained load, ultimately causing
`OutOfMemoryError` and container restarts.


This resolves [issue #2768](https://github.com/operaton/operaton/issues/2768) and is tracked
against the load-test scenario documented in
[issue #2761](https://github.com/operaton/operaton/issues/2761).

---

### `HistoryLevelSetupCommand` Extracted to Interface

The `HistoryLevelSetupCommand` was previously a `final` concrete class without a parent
interface, making it impossible for engine plugins to override the history level setup behaviour.

Operaton 2.1 extracts a new **`HistoryLevelSetupCommand`** interface (package
`org.operaton.bpm.engine.impl`) that extends `Command<Void>`:

```java
package org.operaton.bpm.engine.impl;

public interface HistoryLevelSetupCommand extends Command<Void> {
}
```

The previous implementation is renamed to `DefaultHistoryLevelSetupCommand`. Engine plugins can
now supply a custom implementation via `ProcessEngineConfiguration.setHistoryLevelCommand(…)`:

```java
ProcessEngineConfiguration config = ProcessEngineConfiguration.createStandaloneProcessEngineConfiguration();
config.setHistoryLevelCommand(new MyCustomHistoryLevelSetupCommand());
```

`ProcessEngineConfiguration.getHistoryLevelCommand()` now returns the interface type. The
default value is `new DefaultHistoryLevelSetupCommand()`, so existing setups are unaffected.

A companion utility class **`HistoryLevelUtils`** has been extracted to hold shared helper
methods used by the default command and is available as a public API for custom implementations.

This implements [issue #2760](https://github.com/operaton/operaton/issues/2760) and
[PR #2767](https://github.com/operaton/operaton/pull/2767).

## API

### Database Schema

Operaton 2.1 does not introduce changes to the database schema.

The database schema remains version 7.24.

### REST API

Operaton 2.1 fixes the following OpenAPI specification issues (no changes to API behaviour):

- **`PUT /external-task/{id}/retries`**: The 400 and 404 response descriptions were semantically
  inverted — the 400 description mentioned "task does not exist" and the 404 described a
  negative-retries scenario. These have been corrected to their proper meanings.
- **`POST /external-task/{id}/lock`**: A missing `summary` field has been added to the OpenAPI
  template.

These fixes are purely documentation corrections; no HTTP contract change.
This resolves [issue #2766](https://github.com/operaton/operaton/issues/2766).

### New APIs

- Module `operaton-engine`:
    - New interface `org.operaton.bpm.engine.spi.ProcessEngineConfigurationFactory`
      (see [SPI Configuration Factories](#spi-configuration-factories))
    - New class `org.operaton.bpm.engine.impl.cfg.ProcessEngineConfigurationFactoryImpl`
      (default implementation, internal)
    - New interface `org.operaton.bpm.engine.health.HealthService`
      (see [Health SPI and `/health` Endpoint](#health-spi-and-health-endpoint))
    - New record `org.operaton.bpm.engine.health.HealthResult`
    - New interface `org.operaton.bpm.engine.health.FrontendHealthContributor`
    - New class `org.operaton.bpm.engine.impl.health.DefaultHealthService`
      (default implementation, internal)
    - New interface `org.operaton.bpm.engine.impl.HistoryLevelSetupCommand`
      (see [`HistoryLevelSetupCommand` Extracted to Interface](#historylevelsetupcommand-extracted-to-interface))
    - New class `org.operaton.bpm.engine.impl.DefaultHistoryLevelSetupCommand`
      (replaces the former concrete `HistoryLevelSetupCommand` class)
    - New class `org.operaton.bpm.engine.impl.HistoryLevelUtils`
      (shared helpers for history level setup commands)
- Module `operaton-engine-dmn`:
    - New interface `org.operaton.bpm.dmn.engine.spi.DmnEngineConfigurationFactory`
      (see [SPI Configuration Factories](#spi-configuration-factories))
    - New class `org.operaton.bpm.dmn.engine.impl.DmnEngineConfigurationFactoryImpl`
      (default implementation, internal)
- Module `operaton-spring-boot-starter`:
    - New class `org.operaton.bpm.spring.boot.starter.actuator.ProcessEngineHealthIndicator`
      (Spring Boot Actuator health indicator, registered automatically)
    - New class `org.operaton.bpm.spring.boot.starter.OperatonBpmHealthServiceConfiguration`
      (auto-configures `HealthService` bean)
- Module `operaton-spring-boot-starter-webapp`:
    - New class `org.operaton.bpm.spring.boot.starter.webapp.filter.SessionCookiePathFilter`
      (registered automatically when `operaton.bpm.webapp.session-cookie-path-enforcement=true`)
    - New class `org.operaton.bpm.spring.boot.starter.webapp.SpringWebappFrontendHealthContributor`

### Removed & Changed APIs

The following **internal** APIs have been changed. They reside in packages containing the
`.impl.` segment and should not be used by clients. See also the [usage of deprecated APIs](#usage-of-deprecated-apis) section.

- Module `operaton-engine-rest-core`:
    - `org.operaton.bpm.engine.rest.exception.ExceptionHandlerHelper`:
        - Removed field: `public static final ExceptionHandlerHelper INSTANCE`
        - Removed method: `public static ExceptionHandlerHelper getInstance()`
        - Changed method: `getResponse(Throwable)` is now `static`
        - Changed method: `fromException(Throwable)` is now `static`
        - Changed method: `provideExceptionCode(Throwable, ExceptionDto)` is now `static`
        - Changed method: `getCode(Throwable)` is now `static`

- Module `operaton-engine`:
    - `org.operaton.bpm.engine.impl.el.StartProcessVariableScope`:
        - Removed method: `public static StartProcessVariableScope getInstance()`
    - `org.operaton.bpm.engine.impl.persistence.entity.VariableInstanceEntityFactory`:
        - Removed field: `public static final VariableInstanceEntityFactory INSTANCE`
    - `org.operaton.bpm.engine.impl.core.variable.scope.SimpleVariableInstance.SimpleVariableInstanceFactory`:
        - Removed field: `public static final SimpleVariableInstanceFactory INSTANCE`
    - `org.operaton.bpm.engine.impl.HistoryLevelSetupCommand`:
        - Converted from a `final` class to an **interface** extending `Command<Void>`.
          The concrete implementation is now `DefaultHistoryLevelSetupCommand`. Code that
          directly instantiated `new HistoryLevelSetupCommand()` must be updated to
          `new DefaultHistoryLevelSetupCommand()`.
    - `org.operaton.bpm.engine.ProcessEngineConfiguration`:
        - `getHistoryLevelCommand()` now returns `HistoryLevelSetupCommand` (interface type
          instead of the former class type — compatible for callers that only invoke the method).

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

This release is feature complete and API-compatible with [**Camunda 7.24**](https://docs.camunda.org/enterprise/announcement/#camunda-platform-7-24).

### Spring

Operaton is based on:

- **Spring Boot 4.0.6**
- **Spring Framework 7.0.7**

### Quarkus Extension

<!-- /pom.xml -->
The Operaton Quarkus extension is based on **Quarkus 3.33.1 LTS**.

### Distributions

The Tomcat distribution is based on **Tomcat 11.0.21**.

The Wildfly distribution is based on **Wildfly 38.0.1**.

### Database Compatibility

Operaton 2.1 raises the **minimum supported database versions** in line with vendor LTS and
extended-support timelines:

| Database   | 2.0 minimum | 2.1 minimum | Notes                             |
|------------|-------------|-------------|-----------------------------------|
| PostgreSQL | 13          | **14**      | PostgreSQL 13 EOL November 2025   |
| MariaDB    | 10.6        | **10.11**   | 10.11 is the current LTS branch   |
| MySQL      | 8.4         | **8.4**     | 8.4 is the current LTS branch     |

Versions already at or above the new minimum are unaffected. Oracle (21), SQL Server 2022, and
DB2 support is unchanged.

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
| Groovy     | Groovy             | 5.0.5    |
| Python     | Jython             | 2.7.4    |
| Ruby       | GraalVM Ruby       | 9.1.17.0 |

### Dependency Upgrades

The following non-test dependencies have been upgraded since Operaton 2.0:

| Dependency               | 2.0            | 2.1            |
|--------------------------|----------------|----------------|
| RESTEasy                 | 6.2.15.Final   | 7.0.2.Final    |
| Quarkus                  | 3.32.0         | 3.33.1 (LTS)   |
| Spring Boot              | 4.0.4          | 4.0.6          |
| Spring Framework         | 7.0.5          | 7.0.7          |
| Apache Tomcat            | 11.0.18        | 11.0.21        |
| Jackson                  | 2.21.1         | 2.21.2         |
| Groovy                   | 5.0.4          | 5.0.5          |
| GraalVM JavaScript       | 25.0.2         | 25.0.3         |
| Scala library            | 2.13.17        | 2.13.18        |

#### RESTEasy 7

RESTEasy 7 Upgrade The upgrade of RESTEasy from **6.2.15.Final** to **7.0.2.Final** is the most significant dependency change in this release. 
RESTEasy 7 is based on **Jakarta REST 4.0** and is the current supported release line.

This upgrade is completely transparent for clients using the Operaton REST API or the WildFly distribution. 
No configuration or code changes are required on the client side.