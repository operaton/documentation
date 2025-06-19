---

title: 'Supported Environments'
sidebar_position: 40

menu:
  main:
    identifier: "user-guide-introduction-supported-environments"
    parent: "user-guide-introduction"

---


Run Operaton in every Java-runnable environment. Operaton is supported with our QA infrastructure in the following environments. Here you can find more information about our [enterprise support](http://camunda.com/platform-7/editions/).

:::note[Supported Environments]
  Please note that the environments listed in this section depend on the version of Operaton. Please select the corresponding version of this documentation to see the environment that fits to your version of Operaton. e.g., [supported environments for version 7.15](http://docs.camunda.org/7.15/guides/user-guide/#introduction-supported-environments)
:::


# Container/Application Server for Runtime Components

## Application-Embedded Process Engine

* All Java application servers
* Operaton Spring Boot Starter: Embedded Tomcat
  * [Supported versions](../user-guide/spring-boot-integration/version-compatibility.md)
  * [Deployment scenarios](../user-guide/spring-boot-integration/index.md#supported-deployment-scenarios)
* Operaton Engine Quarkus Extension
  * [Supported versions](../user-guide/quarkus-integration/version-compatibility.md)
  * [Deployment scenarios](../user-guide/quarkus-integration/index.md#supported-deployment-scenarios)

## Container-Managed Process Engine and Operaton Cockpit, Tasklist, Admin

* Apache Tomcat 9.0 / 10.1
* JBoss EAP 7.4 / 8.0
* WildFly Application Server 23.0 / 26.0 / 33.0
  see [Installation guide](../installation/full/was/index.md))

# Databases

## Supported Database Products

* MySQL  8.0
* Oracle 19c / 23ai
* IBM DB2 11.5 (excluding IBM z/OS for all versions)
* PostgreSQL 14 / 15 / 16
* Amazon Aurora PostgreSQL compatible with PostgreSQL 14 / 15
* Microsoft SQL Server 2017 / 2019 / 2022 (see [Configuration Note](../user-guide/process-engine/database/mssql-configuration.md))
* Microsoft Azure SQL with Operaton-supported SQL Server compatibility levels
  (see [Configuration Note](../user-guide/process-engine/database/mssql-configuration.md#azure-sql-compatibility-levels-supported-by-camunda)):
  * SQL Server on Azure Virtual Machines
  * Azure SQL Managed Instance
  * Azure SQL Database
* H2 2.3 (not recommended for [Cluster Mode](./architecture.md#clustering-model) - see [Deployment Note](../user-guide/process-engine/deployments.md))

## Database Clustering & Replication

Clustered or replicated databases are supported given the following conditions. The communication between Operaton and the database cluster has to match with the corresponding non-clustered / non-replicated configuration. It is especially important that the configuration of the database cluster guarantees the equivalent behavior of READ-COMMITTED isolation level.


# Web Browser

* Google Chrome latest
* Mozilla Firefox latest
* Microsoft Edge latest


# Java

* Java 11 / 17 / 21 (if supported by your application server/container)


# Java Runtime

* Oracle JDK 11 / 17 / 21
* OpenJDK 11 / 17 / 21, including builds of the following products:
  * Oracle OpenJDK
  * Eclipse Temurin JDK
  * Amazon Corretto
  * Azul Zulu

# Camunda Modeler

[Supported environments](https://docs.camunda.io/docs/reference/supported-environments/#camunda-modeler) for Camunda Modeler have moved to [docs.camunda.io](https://docs.camunda.io/).

# Maintenance Policy

## Adding Environments

Whenever a new version of one of the following environments is released, we target support of that new version with the next minor release of Operaton. A new released environment has to be available three months before the next Operaton minor release to be considered.

* Java Language (LTS)
* Spring Boot
* Wildfly Application Server
* PostgreSQL

The exact release in which we support a new environment depends on factors such as the release date of the environment and the required implementation effort.

Version support for other environments is decided case by case, much of which is based on the demand in our user base.

## Removing Environments

Whenever a new version of one of the following environments is supported, we usually discontinue support of the oldest version with the same release:

* Wildfly Application Server

Note that we may decide to deviate from this policy on a case-by-case basis.
