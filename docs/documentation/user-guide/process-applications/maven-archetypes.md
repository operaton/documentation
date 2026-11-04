---

title: 'Project Templates (Operaton Starter)'
sidebar_position: 40

menu:
  main:
    identifier: "user-guide-process-application-archetypes"
    parent: "user-guide-process-applications"

---

[Operaton Starter](https://start.operaton.org) generates ready-to-build projects for Operaton, similar to Spring Initializr.
Every generated project compiles and starts on first run and targets the current stable Operaton release.

The source code is available at [github.com/operaton/operaton-starter](https://github.com/operaton/operaton-starter).

## Project Types

| Project Type | Description |
|---|---|
| Process Application | Spring Boot application embedding the Operaton engine, with a skeleton BPMN process and a Java delegate stub |
| Process Archive | Engine-agnostic WAR/JAR for deployment to a standalone engine or Apache Tomcat |

The following build systems are supported: Maven, Gradle (Groovy DSL) and Gradle (Kotlin DSL).

## Usage

### Web UI

Open [start.operaton.org](https://start.operaton.org), choose a project type and build system, enter your Group ID and Artifact ID and download the generated archive.
The web UI also contains a gallery of runnable Operaton examples.

### Command Line

```bash
npx operaton-starter \
  --groupId com.example \
  --artifactId my-process \
  --projectName "My Process" \
  --projectType PROCESS_APPLICATION \
  --buildSystem MAVEN \
  > my-process.zip
```

### REST API

```bash
curl -X POST https://start.operaton.org/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"projectType":"PROCESS_APPLICATION","buildSystem":"MAVEN","groupId":"com.example","artifactId":"my-process","projectName":"My Process","javaVersion":17}' \
  -o my-process.zip
```

See the [Operaton Starter README](https://github.com/operaton/operaton-starter#readme) for further options, such as self-hosting your own instance.
