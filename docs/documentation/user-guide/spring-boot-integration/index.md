---

title: "Spring Boot Integration"
sidebar_position: 60

---

The Operaton Engine can be used in a Spring Boot application by using provided Spring Boot starters.
Spring boot starters allow to enable behavior of your spring-boot application by adding dependencies to the classpath.

These starters will pre-configure the Operaton process engine, REST API and Web applications, so they can easily be used in a standalone process application.

If you are not familiar with [Spring Boot](http://projects.spring.io/spring-boot/), read the [getting started](http://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#getting-started) guide.

To enable Operaton auto configuration, add the following dependency to your ```pom.xml```:

```xml
<dependency>
  <groupId>org.operaton.bpm.springboot</groupId>
  <artifactId>operaton-bpm-spring-boot-starter</artifactId>
  <version>1.0.0-rc-1</version>
</dependency>
```

This will add the Operaton engine v1.0.0-rc-1 to your dependencies.

Other starters that can be used are: 

* [`Operaton-bpm-spring-boot-starter-rest`](rest-api)
* [`Operaton-bpm-spring-boot-starter-webapp`](webapps)
* [`Operaton-bpm-spring-boot-starter-external-task-client`](../../user-guide/ext-client/spring-boot-starter.md)


## Requirements

Operaton Spring Boot Starter requires Java 17.

## Supported deployment scenarios

Following deployment scenario is supported by Operaton:

* executable JAR with embedded Tomcat and one embedded process engine (plus Webapps when needed)

There are other possible variations that might also work, but are not tested by Operaton at the moment.