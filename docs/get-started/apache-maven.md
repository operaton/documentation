---

title: 'Apache Maven Coordinates'

menu:
  main:
    name: "Maven Coordinates"
    identifier: "get-started-maven"
    description: "The most commonly used Apache Maven Coordinates for Operaton."

---

This page lists the most commonly used Apache Maven Coordinates for Operaton.

Most Operaton artifacts are pushed to [maven central](https://central.sonatype.com/search?q=org.operaton.bpm).


## Operaton BOM (Bill of Materials)

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.operaton.bpm</groupId>
      <artifactId>operaton-bom</artifactId>
      <version>1.0.0</version>
      <scope>import</scope>
      <type>pom</type>
    </dependency>
  </dependencies>
</dependencyManagement>
```

:::note[Use the BOM!]
  Please import the Operaton BOM if you use multiple Operaton projects. The BOM defines versions for all Operaton projects. This way it is ensured that no incompatible versions are imported.
:::

## Operaton Engine

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine</artifactId>
</dependency>
```


## Operaton Engine Spring Integration

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

## Operaton Engine CDI Integration

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-cdi</artifactId>
</dependency>
```

## Operaton DMN Engine BOM (Bill of Materials)
This BOM allows to use the DMN engine standalone without the BPMN engine and the rest of the Operaton Platform.

```xml
<dependencyManagement>
  <dependency>
    <groupId>org.operaton.bpm.dmn</groupId>
    <artifactId>operaton-engine-dmn-bom</artifactId>
    <version>1.0.0</version>
    <type>pom</type>
    <scope>import</scope>
  </dependency>
</dependencyManagement>
```

## Operaton DMN
This dependency allows to use DMN engine standalone without the BPMN engine and the rest of the Operaton Platform.
It is not needed when using `operaton-engine` because that already contains the DMN engine.

```xml
<dependency>
  <groupId>org.operaton.bpm.dmn</groupId>
  <artifactId>operaton-engine-dmn</artifactId>
</dependency>
```

## Process Application EJB Client

```xml
<dependency>
  <groupId>org.operaton.bpm.javaee</groupId>
  <artifactId>operaton-ejb-client</artifactId>
</dependency>
```

## Other Operaton Modules:

* [DMN Engine](/docs/documentation/user-guide/dmn-engine/embed/#maven-coordinates)
* [Operaton Spin](/docs/documentation/reference/spin)
* [Operaton Connect](/docs/documentation/reference/connect/#maven-coordinates)
* [Templating Engines](/docs/documentation/user-guide/process-engine/templating/#install-a-template-engine-for-an-embedded-process-engine)
* [Spring Boot Integration](/docs/documentation/user-guide/spring-boot-integration/)
