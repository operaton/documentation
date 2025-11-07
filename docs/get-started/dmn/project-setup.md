---

title: 'Setup a Java Project for DMN'
sidebar_position: 20

menu:
  main:
    name: "Project Setup"
    parent: "get-started-dmn"
    identifier: "get-started-dmn-setup"
    description: "Set up an Apache Maven-based process application inside Eclipse."

aliases: [/dmn/project-setup/]
---

Now you are ready to set up your first process application project in the IDE of your choice, the following description uses Eclipse.

:::note[Terminology - Process vs. Decisions]
DMN is a modeling language for *decisions*, whereas BPMN is a language for *processes*. This tutorial is about decisions. However, due to Operaton's BPMN-focused heritage, the Java project contains classes and files with names like `ProcessApplication` and `processes.xml`. These are in fact generally applicable and can be used with both processes and decisions.
:::

## Create a new Maven Project

:::note[Fancy to save work and use a project template instead?]

You don't have to setup the project manually but can also use a Maven Archetype (which is like a project template), see [Maven Archetypes](/docs/documentation/user-guide/process-applications/maven-archetypes/) for details. The archetype will create a project according to our best practices.

:::

In Eclipse, go to `File / New / Other ...`. This opens the *New Project Wizard*. In the *New Project Wizard* select `Maven / Maven Project`. Click Next.

![Example image](./img/eclipse-new-project.png)

On the first page of the *New Maven Project Wizard* select *Create a simple project (skip archetype selection)*. Click Next.

On the second page (see screenshot), configure the Maven coordinates for the project. Since we are setting up a WAR Project, make sure to select `Packaging: war`.

When you are done, click Finish. Eclipse sets up a new Maven project. The project appears in the *Project Explorer* View.

## Add Operaton Maven Dependencies

The next step consists of setting up the Maven dependencies for your new process application. Add the following dependencies to the `pom.xml` file of your project:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">

  <modelVersion>4.0.0</modelVersion>
  <groupId>org.operaton.bpm.getstarted</groupId>
  <artifactId>dinner-dmn</artifactId>
  <version>0.1.0-SNAPSHOT</version>
  <packaging>war</packaging>

  <properties>
    <operaton.version>1.0.0</operaton.version>
    <maven.compiler.release>11</maven.compiler.release>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.operaton.bpm</groupId>
        <artifactId>operaton-bom</artifactId>
        <version>${operaton.version}</version>
        <scope>import</scope>
        <type>pom</type>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.operaton.bpm</groupId>
      <artifactId>operaton-engine</artifactId>
      <scope>provided</scope>
    </dependency>

    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
      <version>3.0.1</version>
      <scope>provided</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-war-plugin</artifactId>
        <version>3.3.2</version>
        <configuration>
          <failOnMissingWebXml>false</failOnMissingWebXml>
        </configuration>
      </plugin>
    </plugins>
  </build>

</project>
```

Now you can perform the first build. Select the `pom.xml` in the Package Explorer, perform a right-click and select `Run As / Maven Install`.

## Add a Process Application Class

Next, you need to create a package, e.g., `org.operaton.bpm.getstarted.dmn` and add a Process Application class to it. The Process Application class constitutes the interface between your application and the process engine.

```java
package org.operaton.bpm.getstarted.dmn;

import org.operaton.bpm.application.ProcessApplication;
import org.operaton.bpm.application.impl.ServletProcessApplication;

@ProcessApplication("Dinner App DMN")
public class DinnerApplication extends ServletProcessApplication
{
  //empty implementation
}
```


## Add a META-INF/processes.xml Deployment Descriptor

The last step to set up the process application is to add the `META-INF/processes.xml` deployment descriptor file. This file allows us to provide a declarative configuration of the deployment(s) this process application makes to the process engine.

This file needs to be added to the `src/main/resources/META-INF` folder of the Maven project.

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<process-application
    xmlns="http://www.operaton.org/schema/1.0/ProcessApplication"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <process-archive name="dinner-dmn">

    <process-engine>default</process-engine>
    <properties>
      <property name="isDeleteUponUndeploy">false</property>
      <property name="isScanForProcessDefinitions">true</property>
    </properties>
  </process-archive>

</process-application>
```

At this point you have successfully set up the process application and you can start modeling your first decision table.
