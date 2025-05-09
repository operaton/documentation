---

title: "Web applications"
sidebar_position: 40

menu:
  main:
    name: "Web Applications"
    identifier: "user-guide-spring-boot-webapps"
    parent: "user-guide-spring-boot-integration"

---

To enable the [Web Applications](/webapps/index.md) you can use the following starter in your `pom.xml`:

```xml
<dependency>
  <groupId>org.operaton.bpm.springboot</groupId>
  <artifactId>operaton-bpm-spring-boot-starter-webapp</artifactId>
  <version>{project-version}</version>
</dependency>
```

By default the application path is `/camunda`, so without any further configuration you can access
the Webapps under [http://localhost:8080/operaton/app/](http://localhost:8080/operaton/app/).

## Configurations

You can change the application path with the following configuration property in your `application.yaml` file:
```properties
camunda.bpm.webapp.application-path=/my/application/path
```

By default, the starter registers a controller to redirect `/` to Operaton's bundled `index.html`.
To disable this, you have to add to your application properties:
```properties
camunda.bpm.webapp.index-redirect-enabled=false
```

## Error Pages

The default error handling coming with the Spring Boot ('whitelabel' error page) is enabled in the starter. To switch to the Operaton error pages (`webjar/META-INF/resources/webjars/operaton/error-XYZ-page.html`), please put them to the application folder structure under `/src/main/resources/public/error/XYZ.html`.

## Building Custom REST APIs

The Operaton Web Applications use a `CSRF Prevention Filter` that expects a `CSRF Token` on any
modifying request for paths beginning with `/operaton/api/` or `/operaton/app/`. Any modifying requests
mapped to these paths will fail, and the current session will be ended if no CSRF Token is present.
You can avoid this by registering your resources on different paths or add your resources to the
CSRF Prevention Filter Whitelist (via the configuration property `camunda.bpm.webapp.csrf.entry-points`).