---

title: "Web applications"
sidebar_position: 40

menu:
  main:
    name: "Web Applications"
    identifier: "user-guide-spring-boot-webapps"
    parent: "user-guide-spring-boot-integration"

---

To enable the [Web Applications](../../webapps/index.md), you can use the following starter in your `pom.xml`:

```xml
<dependency>
  <groupId>org.operaton.bpm.springboot</groupId>
  <artifactId>operaton-bpm-spring-boot-starter-webapp</artifactId>
  <version>{project-version}</version>
</dependency>
```

By default, the application path is `/operaton`, so without any further configuration you can access
the web apps at [http://localhost:8080/operaton/app/](http://localhost:8080/operaton/app/).

## Configurations

You can change the application path with the following configuration property in your `application.yaml` file:
```properties
operaton.bpm.webapp.application-path=/my/application/path
```

By default, the starter registers a controller to redirect `/` to Operaton's bundled `index.html`.
To disable this, add the following to your application properties:
```properties
operaton.bpm.webapp.index-redirect-enabled=false
```

## Error Pages

The default error handling provided by Spring Boot ('whitelabel' error page) is enabled in the starter. To switch to the Operaton error pages (`webjar/META-INF/resources/webjars/operaton/error-XYZ-page.html`), put them into the application folder structure under `/src/main/resources/public/error/XYZ.html`.

## Building Custom REST APIs

The Operaton Web Applications use a `CSRF Prevention Filter` that expects a `CSRF token` on any
modifying request for paths beginning with `/operaton/api/` or `/operaton/app/`. Any modifying requests
mapped to these paths will fail, and the current session will end if no CSRF token is present.
You can avoid this by registering your resources on different paths or by adding your resources to the
CSRF Prevention Filter whitelist (via the configuration property `operaton.bpm.webapp.csrf.entry-points`).
