---

title: 'Maven Project Templates (Archetypes)'
sidebar_position: 40

menu:
  main:
    identifier: "user-guide-process-application-archetypes"
    parent: "user-guide-process-applications"

---

Maven Archetypes are project templates that can generate a ready-to-use Maven project.

:::caution[Current Availability]
Operaton does not currently publish public Maven archetype artifacts or an archetype catalog. Older documentation pointed to artifact and template repositories that are not available for Operaton and should not be used.
:::

## Recommended Project Setup

Use the manual project setup guides instead. They show the current Maven dependencies and project structure directly:

| Use case | Setup guide |
| --- | --- |
| BPMN process application on Tomcat | [Java process application project setup](/docs/get-started/archive/java-process-app/project-setup/) |
| Java EE process application on WildFly | [Java EE project setup](/docs/get-started/archive/javaee7/project-setup/) |
| DMN project | [DMN project setup](/docs/get-started/dmn/project-setup/) |
| Spring Boot application | [Spring Boot project setup](/docs/get-started/spring-boot/project-setup/) |
| Dependency versions | [Apache Maven and the Operaton BOM](/docs/get-started/apache-maven/) |

## Historical Archetype Names

Some older Operaton or Camunda 7 material may mention these archetype artifact IDs:

| Artifact ID | Intended use |
| --- | --- |
| `operaton-archetype-cockpit-plugin` | Cockpit plugin project |
| `operaton-archetype-ejb-war` | Java EE process application packaged as WAR |
| `operaton-archetype-servlet-war` | Servlet process application packaged as WAR |
| `operaton-archetype-spring-boot` | Spring Boot process application |
| `operaton-archetype-spring-boot-demo` | Spring Boot process application with demo users |
| `operaton-archetype-engine-plugin` | Process engine plugin project |

Treat these names as historical until Operaton publishes a public archetype catalog again. For new applications, start from the setup guides above and import the Operaton BOM from Maven Central.
