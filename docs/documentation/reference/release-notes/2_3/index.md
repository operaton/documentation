---
title: "2.3 (DRAFT)"
sidebar_position: 23
---

# About release 2.3

## New and Noteworthy

### Null Safety: JSpecify Nullability Declarations

Operaton 2.3 continues the work started in 2.2 to make the nullability contract of the engine explicit using
[JSpecify](https://jspecify.dev/) annotations. This work implements the
[ADR "Null Safety Strategy for Operaton"](https://github.com/operaton/operaton/blob/main/docs/decisions/0001-null-safety-strategy-for-operaton.md),
which chose JSpecify for all public APIs and lets engine internals adopt the annotations step by step. Progress is
tracked in [issue #2353](https://github.com/operaton/operaton/issues/2353).

Classes and packages are marked with `@NullMarked`. Inside that scope, every type is non-null by default, and only the
places where `null` is really allowed or returned carry `@Nullable`. IDEs (IntelliJ IDEA, Eclipse) and static analyzers
such as NullAway can then check these contracts while you code, instead of relying on Javadoc or reading the
implementation.

```java
@NullMarked
public interface BusinessCalendar {

  // duedateDescription must not be null; startDate is optional;
  // the result can be null, e.g. when a repeating cycle has no further occurrence
  @Nullable Date resolveDuedate(String duedateDescription, @Nullable Date startDate);
}
```

#### What changed in 2.3

The number of engine classes covered by `@NullMarked` has roughly doubled, from **27%** in 2.2 to **50%** of the
`operaton-engine` module (about 1,070 of 2,150 classes). Areas annotated in this release include:

- **Persistence entities**: `ExecutionEntity`, `TaskEntity`, job, incident, variable and history entities, along with
  the DB entity manager and its operations
- **Process Virtual Machine (PVM)**: process definitions, activities, runtime operations and the delegate interfaces
- **History**: history events, event producers, handlers, parsers and transformers
- **CMMN**: behaviors, commands, handlers, model and execution
- **Core and variables**: variable scopes, variable events and mappings, serializers, typed variable values
- **Engine configuration**: `ProcessEngineConfigurationImpl`
- **Metrics, migration and deployment**: the metrics reporter, migration validators, the deployment cache, process
  application deployment and the container (JMX, Tomcat, EJB) services
- **Integrations**: the Spring integration (`engine-spring`) and Spring Boot starter events
- **Multi-tenancy**: `tenantId` parameters and `getTenantId()` methods are now consistently `@Nullable`, because
  `null` means "no tenant"

You can measure coverage per module with the script used during development:

```shell
python3 .devenv/scripts/tools/nullmarked-coverage.py
```

#### Impact for users

- **No runtime change.** JSpecify annotations are compile-time metadata only. They do not add runtime checks, and the
  engine throws the same exceptions as before. Avoiding externally visible behavior changes is an explicit goal of the
  ADR.
- **Java users** see more accurate nullability warnings in their IDE and in static analysis when they call or extend
  annotated classes. Custom subclasses of engine classes (for example, a custom `ProcessEngineConfigurationImpl`, a
  `BusinessCalendar` or an identity provider) may get new warnings if an override contradicts the declared contract.
- **Kotlin users** should take note: since Kotlin 2.1, the compiler treats JSpecify annotations strictly by default.
  Types that used to appear as platform types (`String!`) now show up as `String` or `String?`. Kotlin code that
  calls annotated Operaton APIs can therefore get new compile errors or warnings, for example when it passes a
  nullable value where the API declares non-null, or dereferences a `@Nullable` result without a null check. During
  migration, the strictness can be lowered with the compiler option `-Xjspecify-annotations=warn`.
- **Classes in `.impl.` packages** remain internal API. Their nullability declarations describe the current
  implementation and may be refined in later releases.

#### Next steps

The work continues with the remaining engine internals and, as defined in the ADR, the complete public API, including
Javadoc that describes the nullability semantics. CI checks that report nullability violations on public APIs will
follow once coverage is complete. For background, see the forum announcement
["Introducing declaration of nullability in the API"](https://forum.operaton.org/t/introducing-declaration-of-nullability-in-the-api/445).

This implements [PR #3712](https://github.com/operaton/operaton/pull/3712),
[PR #3747](https://github.com/operaton/operaton/pull/3747),
[PR #3765](https://github.com/operaton/operaton/pull/3765),
[PR #3769](https://github.com/operaton/operaton/pull/3769),
[PR #3778](https://github.com/operaton/operaton/pull/3778),
[PR #3832](https://github.com/operaton/operaton/pull/3832),
[PR #3840](https://github.com/operaton/operaton/pull/3840),
[PR #3881](https://github.com/operaton/operaton/pull/3881).

---

## API

### Database Schema

_TBD_

### REST API

_TBD_

### New APIs

_TBD_

### Removed & Changed APIs

_TBD_

### Usage of deprecated APIs

It is **strongly recommended** to avoid using deprecated methods which are marked with the `@Deprecated(forRemoval = true)`
annotation in the Java API.

Deprecated methods within packages containing the segment `.impl.` are considered internal and should not be used by clients.
**These methods are subject to removal without prior notice.**

## Versions & Compatibility

_TBD_
