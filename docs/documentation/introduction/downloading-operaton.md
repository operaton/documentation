---

title: 'Download'
sidebar_position: 10

menu:
  main:
    identifier: "user-guide-introduction-downloading-operaton"
    parent: "user-guide-introduction"

---


## Prerequisites

Before downloading Operaton, make sure you have a JRE (Java Runtime Environment), or better, a JDK
(Java Development Kit) installed. Please check the supported [Java versions](./supported-environments.md#java).

[Download JDK][get-jdk]


## Download the Runtime

Operaton is a flexible framework which can be used in different contexts. See [Architecture Overview](./architecture.md) for more details. Based on how you want
to use Operaton, you can choose a different distribution.


### Spring Boot and Docker

It is also possible to run Operaton with [Spring Boot][run-with-spring-boot] and [Docker][run-with-docker].


### Full Distribution

Download the full distribution if you want to use a [shared process engine][shared-engine] or if you
want to get to know Operaton quickly, without any additional setup or installation steps required.

The full distribution bundles

* Process Engine configured as [shared process engine][shared-engine],
* Runtime Web Applications (Tasklist, Cockpit, Admin),
* REST API,
* the application server for the pre-packaged Tomcat and WildFly archives.

:::note[Server/Container]
  Operaton publishes pre-packaged Tomcat and WildFly distributions as release assets.
  Those archives include the application server and the Operaton binaries (process engine and web apps)
  pre-installed in the container.
:::

:::note[WildFly Application Server]
  WildFly Application Server is provided as part of the archives as a convenience. For a copy of the source code, the full set of attribution notices, and other relevant information please see https://github.com/wildfly/wildfly. We will also provide you with a copy of the source code if you [contact our Open-Source Compliance Team](./licenses.md#contact) at any time within three years of you downloading an archive (for which we may charge a nominal sum). WildFly Application Server is copyright © JBoss, Home of Professional Open Source, 2010, Red Hat Middleware LLC [..and contributors].
:::

Download stable distribution assets from the [latest Operaton release][operaton-releases-latest].
Snapshot distribution assets are published in the [Operaton GitHub releases][operaton-releases]
as prereleases with tags such as `2.2.0-SNAPSHOT`.

See the [Installation Guide][installation-guide-full] for additional details.


## Download Operaton Modeler

Operaton Modeler supports BPMN 2.0, DMN 1.3, CMMN 1.1, and Operaton Forms. You can find installation
instructions in the [Operaton Modeler installation guide][operaton-modeler-install].



[get-jdk]: https://www.oracle.com/java/technologies/downloads/
[operaton-modeler-install]: ../installation/operaton-modeler.md
[operaton-releases]: https://github.com/operaton/operaton/releases
[operaton-releases-latest]: https://github.com/operaton/operaton/releases/latest
[shared-engine]: ./architecture.md#shared-container-managed-process-engine
[installation-guide-full]: ../installation/index.md
[run-with-spring-boot]: ../user-guide/spring-boot-integration/index.md
[run-with-docker]: ../installation/docker.md
