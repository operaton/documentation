---

title: "Spring Framework Integration"
sidebar_position: 50

---

The operaton-engine Spring Framework integration is located inside a maven module and can be added to apache maven-based projects through the following dependency:

:::note
  Please import the [Operaton BOM](../../../get-started/apache-maven/) to ensure correct versions for every Operaton project.
:::

* `operaton-engine-spring` maven module for Spring Framework 5

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-spring</artifactId>
</dependency>
```

* `operaton-engine-spring-6` maven module for Spring Framework 6.

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-spring-6</artifactId>
</dependency>
```

The process engine Spring artifact should be added as a library to the process application.
The following minimal set of Spring dependencies must be added in the desired version:

```xml
<properties>
  <spring.version>X.Y.Z.RELEASE</spring.version>
</properties>

<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-framework-bom</artifactId>
      <version>${spring.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-jdbc</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-tx</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-orm</artifactId>
  </dependency>
</dependencies>
```