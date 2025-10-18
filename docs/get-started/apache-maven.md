---

title: 'Apache Maven Coordinates'

menu:
  main:
    name: "Maven Coordinates"
    identifier: "get-started-maven"
    description: "The most commonly used Apache Maven Coordinates for Operaton."

---

This page lists the most commonly used Apache Maven Coordinates for Operaton.

Most Operaton artifacts are pushed to [maven central](https://central.sonatype.com/).


# Operaton BOM (Bill of Materials)

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.operaton.bpm</groupId>
      <artifactId>operaton-bom</artifactId>
      <version>v1.0.0-beta-3</version>
      <scope>import</scope>
      <type>pom</type>
    </dependency>
  </dependencies>
</dependencyManagement>
```

:::note[Use the BOM!]
  Please import the Operaton BOM if you use multiple Operaton projects. The BOM defines versions for all Operaton projects. This way it is ensured that no incompatible versions are imported.
:::

# Operaton Engine

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine</artifactId>
</dependency>
```


# Operaton Engine Spring Integration

The `operaton-engine` Spring integration for Spring Framework 5:

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-spring</artifactId>
</dependency>
```

The `operaton-engine` Spring integration for Spring Framework 6:

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-spring-6</artifactId>
</dependency>
```

# Operaton Engine CDI Integration

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-cdi</artifactId>
</dependency>
```

# Operaton DMN Engine BOM (Bill of Materials)
This BOM allows to use the DMN engine standalone without the BPMN engine and the rest of the Operaton Platform.

```xml
<dependencyManagement>
  <dependency>
    <groupId>org.operaton.bpm.dmn</groupId>
    <artifactId>operaton-engine-dmn-bom</artifactId>
    <version>v1.0.0-beta-3</version>
    <type>pom</type>
    <scope>import</scope>
  </dependency>
</dependencyManagement>
```

# Operaton DMN
This dependency allows to use DMN engine standalone without the BPMN engine and the rest of the Operaton Platform.
It is not needed when using `operaton-engine` because that already contains the DMN engine.

```xml
<dependency>
  <groupId>org.operaton.bpm.dmn</groupId>
  <artifactId>operaton-engine-dmn</artifactId>
</dependency>
```

# Process Application EJB Client

```xml
<dependency>
  <groupId>org.operaton.bpm.javaee</groupId>
  <artifactId>operaton-ejb-client</artifactId>
</dependency>
```

# Other Operaton Modules:

* [DMN Engine](../documentation/user-guide/dmn-engine/embed.md#maven-coordinates)
* [Operaton Spin](../documentation/reference/spin/index.md)
* [Operaton Connect](../documentation/reference/connect/index.md#maven-coordinates)
* [Templating Engines](../documentation/user-guide/process-engine/templating.md#install-a-template-engine-for-an-embedded-process-engine)
* [Spring Boot Integration](../documentation/user-guide/spring-boot-integration/index.md)
