---

title: "Camunda to Operaton Migration"
sidebar_position: 10

---

# Migration Guide from Camunda 7 CE to Operaton

Operaton is a fork of the Camunda 7 platform. It is API-compatible and
schema-compatible with **Camunda 7.24**: the database schema and the REST API have
been adopted from Camunda 7.24 and are kept in sync. As a result, migrating an
existing Camunda 7 CE application to Operaton requires no data conversion — you
update your code dependencies and run Operaton against your existing database.

A migration consists of two independent parts:

1. **[Runtime data](#runtime-data)** — your engine database. No schema migration
   is needed; you point Operaton at the database you already have.
2. **[Application code](#application-code)** — your Java sources and build files.
   An [OpenRewrite](https://docs.openrewrite.org/) recipe automates this.

## Prerequisites

- **Upgrade your existing application to Camunda 7.24 first**, then migrate to
  Operaton. Operaton tracks Camunda 7.24, so this keeps the schema and API at the
  expected level and makes the switch a one-step change. Follow the
  [Camunda 7 update guide](https://docs.camunda.org/manual/7.24/update/) to reach
  7.24.
- **Java 17 or later.** Operaton requires Java 17 as a minimum and is tested on
  Java 17, 21, and 25.

## Runtime data

Because the Operaton schema is identical to the Camunda 7.24 schema, there is
**no database migration to perform**:

- Database tables keep the `ACT_` prefix — no tables are renamed.
- Once your application runs on Camunda 7.24, its database is already at the
  schema level Operaton expects.
- Already-deployed BPMN, DMN, and CMMN models continue to work. The engine
  accepts both the `operaton:` and the legacy `camunda:` extension namespaces, so
  process definitions deployed under Camunda remain valid.

:::warning[Back up your database first]
Always create a backup of your database before switching the runtime, so you can
roll back if needed.
:::

To switch the runtime:

1. Stop the Camunda application.
2. Start Operaton configured against the **same datasource**. No schema upgrade
   scripts need to be run as part of the Camunda-to-Operaton switch.

## Application code

Use the [Operaton migration recipe](https://github.com/operaton/migrate-from-camunda-recipe),
an OpenRewrite recipe that rewrites your sources and build files. The meta recipe
`org.operaton.rewrite.MigrateFromCamunda` applies all migration steps:

- Replaces Camunda Maven/Gradle dependencies with their Operaton equivalents.
- Renames Camunda packages, types, constants, and methods to their Operaton
  counterparts (for example `getCamundaExpression()` → `getOperatonExpression()`).
- Updates XML namespace declarations in deployment descriptors.
- Renames `META-INF/services` ServiceLoader files and resolves deprecated APIs.

:::note[Recipe version]
The examples below use recipe version `1.0.1` and plugin versions current at the
time of writing. Check
[Maven Central](https://central.sonatype.com/artifact/org.operaton/migrate-camunda-recipe)
for the latest recipe version and the
[recipe README](https://github.com/operaton/migrate-from-camunda-recipe) for the
matching OpenRewrite plugin versions.
:::

The recipe can be run without modifying your build files.

### Maven

```bash
mvn org.openrewrite.maven:rewrite-maven-plugin:6.28.1:run \
  -Drewrite.recipeArtifactCoordinates=org.operaton:migrate-camunda-recipe:1.0.1 \
  -Drewrite.activeRecipes=org.operaton.rewrite.MigrateFromCamunda
```

For Spring Boot applications use `org.operaton.rewrite.spring.MigrateSpringBootApplication`,
for Quarkus use `org.operaton.rewrite.quarkus.MigrateQuarkusApplication`.

### Gradle

Create an `init.gradle` file in your project directory:

```groovy
initscript {
  repositories {
    maven { url "https://plugins.gradle.org/m2" }
  }
  dependencies {
    classpath("org.openrewrite:plugin:7.25.0")
  }
}

rootProject {
  plugins.apply(org.openrewrite.gradle.RewritePlugin)
  dependencies {
    rewrite("org.operaton:migrate-camunda-recipe:1.0.1")
  }

  afterEvaluate {
    if (repositories.isEmpty()) {
      repositories {
        mavenLocal()
        mavenCentral()
      }
    } else {
      repositories {
        mavenLocal()
      }
    }
  }
}
```

Then run:

```bash
./gradlew --init-script init.gradle rewriteRun \
  -Drewrite.activeRecipe=org.operaton.rewrite.MigrateFromCamunda
```

### Review the changes

The recipe modifies source and build files in place. After running it:

1. Review the diff and run your build and test suite.
2. Commit the changes.

## Known issues

**ServiceLoader file contents.** When a renamed `META-INF/services` file
references a class that is itself relocated from a `camunda` to an `operaton`
package, the file is renamed but its content may not be updated. Check the
recipe output for warnings such as:

```text
[WARNING]     org.operaton.rewrite.RenameServiceLoader
[WARNING]         org.openrewrite.RenameFile: {fileMatcher=**/META-INF/services/org.camunda.spin.spi.DataFormatProvider, fileName=org.operaton.spin.spi.DataFormatProvider}
```

If ServiceLoader files were renamed, verify their contents and make sure the
referenced classes are available.

## Reference

- [Operaton migration recipe](https://github.com/operaton/migrate-from-camunda-recipe)
  — full recipe documentation, individual recipes, and command-line usage.
- [Camunda to Operaton artifact mapping](https://github.com/operaton/migrate-from-camunda-recipe/blob/main/camunda-to-operaton-mapping.md)
  — the complete mapping of Camunda artifacts, packages, types, and constants to
  their Operaton equivalents.
