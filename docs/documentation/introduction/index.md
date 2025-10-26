---

sidebar_position: 1

---
# Introduction

Welcome to the Operaton Manual! Operaton is a Java-based framework supporting BPMN for workflow and process automation, CMMN for Case Management and DMN for Business Decision Management. Also see: [Implemented Standards](./implemented-standards.md).

Operaton inherited its source code from the legacy of Camunda, Activiti and their predecessors. Camunda 7 was an important contribution to the open-source BPMN community. Building on this legacy, we aim to create a thriving future for a truly free and open-source BPMN engine.

:::info
We are in the process of forming a legal foundation, specifically a German eingetragener Verein (Registered Association), that will own the project and its trademark.
:::

This document contains information about the features provided by Operaton.

To give you an overview of Operaton, the following illustration shows the most important components along with some typical user roles.

![Operaton Components and Roles](./img/architecture-overview.png)


## Process Engine & Infrastructure

* [Process Engine](../user-guide/process-engine/index.md) The process engine is a Java library responsible for executing BPMN 2.0 processes, CMMN 1.1 cases and DMN 1.3 decisions. It has a lightweight POJO core and uses a relational database for persistence. ORM mapping is provided by the MyBatis mapping framework.
* [Spring Framework Integration](../user-guide/spring-framework-integration/index.md)
* [CDI/Java EE Integration](../user-guide/cdi-java-ee-integration/index.md)
* [Runtime Container Integration](../user-guide/runtime-container-integration/index.md) (Integration with application server infrastructure.)

## Modeler

* [Camunda Modeler](../modeling-bpmn/index.md): Modeling tool for BPMN 2.0 and CMMN 1.1 diagrams as well as DMN 1.3 decision tables.
* [bpmn.io](http://bpmn.io/): Open-source project for the modeling framework and toolkits.

## Web Applications

* [REST API](../reference/rest/index.md) The REST API allows you to use the process engine from a remote application or a JavaScript application. (Note: The documentation of the REST API is factored out into own documents.)
* [Operaton Tasklist](../webapps/tasklist/index.md) A web application for human workflow management and user tasks that allows process participants to inspect their workflow tasks and navigate to task forms in order to work on the tasks and provide data input.
* [Operaton Cockpit](../webapps/cockpit/index.md) A web application for process monitoring and operations that allows you to search for process instances, inspect their state and repair broken instances.
* [Operaton Admin](../webapps/admin/index.md) A web application that allows you to manage users, groups and authorizations.
