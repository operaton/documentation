---

title: 'JTA Transaction Integration'
sidebar_position: 20

menu:
  main:
    identifier: "user-guide-cdi-transactions"
    parent: "user-guide-cdi"

---

## Embedded Process Engine

The process engine transaction management can integrate with JTA and Jakarta Transactions.
To use transaction manager integration, you need to use the

* `org.operaton.bpm.engine.impl.cfg.JtaProcessEngineConfiguration` for JTA integration only.
* `org.operaton.bpm.engine.impl.cfg.JakartaTransactionProcessEngineConfiguration` for Jakarta Transactions integration only.
* `org.operaton.bpm.engine.cdi.CdiJtaProcessEngineConfiguration` for additional CDI expression resolution support.

The process engine requires access to an implementation of `javax.transaction.TransactionManager` or `jakarta.transaction.TransactionManager` respectively.
Not all application servers provide such an implementation. Most notably, IBM WebSphere and Oracle WebLogic historically did not provide this  implementation.
To achieve JTA transaction integration on these containers, users should use the Spring Framework Abstraction and configure the process engine using the
[SpringProcessEngineConfiguration](../../user-guide/spring-framework-integration/index.md).

:::warning[]
  When you configure a transaction manager, make sure that it actually manages the data source that
  you have configured for the process engine. If that is not the case, the data source works in auto-commit mode.
  This can lead to inconsistencies in the database, because transaction commits and rollbacks are no longer performed.
:::

## Shared Process Engine

The shared process engine distributions for Java EE and Jakarta EE Application Servers (Wildfly, JBoss EAP, IBM WebSphere Application Server, Oracle WebLogic Application Server)
provide JTA or Jakarta Transactions integration out of the box.

## Example

The following example shows how to integrate your custom business logic into a transaction of the process engine:

```java
@Named
@Dependent
public class MyBean {

  @Inject
  public RuntimeService runtimeService;

  @Transactional
  public void doSomethingTransactional() {
    // Here you can do transactional stuff in your domain model and it will be
    // combined in the same transaction as the the following RuntimeService API
    // call to start a process instance:
    runtimeService.startProcessInstanceByKey("my-process");
  }

}
```

## Using JTA transaction integration with WebSphere Liberty

Operaton allows to mark a transaction as "rollback only" by calling `UserTransaction#setRollbackOnly()`.
If this code is executed within a Operaton Job, the Job is marked as failed, and can be retried.

WebSphere Liberty doesn't support this behavior of Operaton. When calling `UserTransaction#setRollbackOnly()`
in WebSphere Liberty, the transaction is rolled back silently, and the Operaton process engine is unable to unlock the
job and decrease the job retry count.

As a workaround, you can throw a `RuntimeException` after invoking the `UserTransaction#setRollbackOnly()`. The Operaton
process engine will catch this `Exception` and handle the transaction rollback inside a job correctly.