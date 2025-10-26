---

title: "Quarkus Integration"
sidebar_position: 70

---

The Operaton Engine can be used in a Quarkus application by using the provided Quarkus Extension. Quarkus Extensions add 
behavior to your Quarkus application by adding dependencies to the classpath.

The Operaton Engine Quarkus Extension will pre-configure the Operaton process engine, so it can be easily used in a 
Quarkus application.

If you are not familiar with [Quarkus](https://quarkus.io/), have a look at the [getting started](https://quarkus.io/get-started/) guide.

To enable Operaton Engine autoconfiguration, add the following dependency to your `pom.xml`:

```xml
<dependency>
  <groupId>org.operaton.bpm.quarkus</groupId>
  <artifactId>operaton-bpm-quarkus-engine</artifactId>
  <version>1.0.0-rc-1</version>
</dependency>
```

This will add the Operaton engine v1.0.0.-rc-1 to your dependencies.

## Supported deployment scenarios

Operaton supports the following deployment scenario:

* executable JAR with one embedded process engine.

There are other possible variations that might also work, but are not tested by Operaton at the moment.