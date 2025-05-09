---

title: "Resource Deployments"
sidebar_position: 20

menu:
  main:
    name: "Resource Deployments"
    identifier: "user-guide-quarkus-deployments"
    parent: "user-guide-quarkus-integration"

---

This section documents how to perform process engine deployments with a Quarkus application containing an embedded
process engine. The documentation assumes some familiarity with [Quarkus CDI support][quarkus-cdi] and the Operaton
<a class="javadocref" href="org/operaton/bpm/engine/repository/DeploymentBuilder.html">DeploymentBuilder API</a>.

The Operaton Engine Quarkus Extension only supports programmatic deployments. A user can observe for the
`OperatonEngineStartupEvent` CDI event. The `OperatonEngineStartupEvent` signals that a process engine has been
successfully bootstrapped, and a deployment can be performed.

The following example shows how a single process engine deployment can be performed in a Quarkus application:

```java
@ApplicationScoped
public class MyConfig {

  @Inject
  RepositoryService repositoryService;

  public void createDeployment(@Observes OperatonEngineStartupEvent event) {
    repositoryService.createDeployment()
        .addClasspathResource("resources/bpmn/simpleProcess.bpmn")
        .deploy();
  }

}
```

However, a Quarkus application doesn't have to be limited to a single process engine deployment. You can observe for
the `OperatonEngineStartupEvent` in multiple methods, and perform multiple deployments with a finer-grained control
over the deployed resources.

```java
@ApplicationScoped
public class MyConfig {

  @Inject
  RepositoryService repositoryService;

  public void createDeployment1(@Observes OperatonEngineStartupEvent event) {
    repositoryService.createDeployment()
        .name("deployment-1")
        .addClasspathResource("resources/bpmn/one/simpleProcess1.bpmn")
        .deploy();
  }

  public void createDeployment2(@Observes OperatonEngineStartupEvent event) {
    repositoryService.createDeployment()
        .name("deployment-2")
        .addClasspathResource("resources/bpmn/two/simpleProcess2.bpmn")
        .deploy();
  }

}
```

[quarkus-cdi]: https://quarkus.io/guides/cdi-reference