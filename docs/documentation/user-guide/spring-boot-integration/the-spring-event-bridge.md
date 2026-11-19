---

title: 'Spring Eventing Bridge'
sidebar_position: 60

menu:
  main:
    identifier: "user-guide-spring-event-bridge"
    parent: "user-guide-spring-boot-integration"

---


The process engine can be hooked up to the Spring event bus. We call this the "Spring Eventing Bridge". This lets us be notified of process events using standard Spring eventing mechanisms. By default, Spring eventing is enabled by an engine plugin. Eventing is controlled by four `operaton.bpm.eventing` properties:

```
operaton.bpm.eventing.execution=true
operaton.bpm.eventing.history=true
operaton.bpm.eventing.task=true
operaton.bpm.eventing.skippable=true
```

The first three properties control the event streams for execution, task, and history events, respectively. The last property, `operaton.bpm.eventing.skippable`, controls
the registration of event listeners. If its value is `true`, listener execution can be skipped via API or in Operaton Cockpit by activating the "skip listeners" flag. Otherwise, the listeners are registered as built-in listeners and are executed unconditionally.

Listeners can subscribe to streams of mutable or immutable event objects. The latter are particularly useful
in asynchronous listener scenarios, e.g. when using `TransactionalEventListener`.
The mutable event stream objects can be modified multiple times between the creation and the reception
of the event the listener has asynchronously subscribed to. Immutable event objects reflect the data
at the creation time of the event, regardless of the time they are finally received by the listener.

On the execution event stream, `DelegateExecution`s (mutable) and `ExecutionEvent`s (immutable) can be received.
The task event stream offers `DelegateTask`s (mutable) and `TaskEvent`s (immutable).
On the history event stream, only `HistoryEvent`s (mutable) are published.

The following example gives an overview of how process events can be received in Spring beans. This way, you can implement task and delegate listeners by
providing Spring beans with annotated methods instead of implementing the `TaskListener` and `ExecutionListener` interfaces.

```java
import org.operaton.bpm.engine.delegate.DelegateExecution;
import org.operaton.bpm.engine.delegate.DelegateTask;
import org.operaton.bpm.engine.impl.history.event.HistoryEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;


@Component
class MyListener {

  @EventListener
  public void onTaskEvent(DelegateTask taskDelegate) {
    // handle mutable task event
  }

  @EventListener
  public void onTaskEvent(TaskEvent taskEvent) {
    // handle immutable task event
  }

  @EventListener
  public void onExecutionEvent(DelegateExecution executionDelegate) {
    // handle mutable execution event
  }

  @EventListener
  public void onExecutionEvent(ExecutionEvent executionEvent) {
    // handle immutable execution event
  }

  @EventListener
  public void onHistoryEvent(HistoryEvent historyEvent) {
    // handle history event
  }

}
```

:::note
  If the method, annotated with `EventListener` returns a non-`void` result, Spring will
  throw it as a new event on the Spring event bus. This lets you build event handler chains
  for processing. For more information on eventing, please consult the Spring manual.
:::

## Specifying event type

Spring lets you specify the event delivered to the listener by providing a SpEL condition in the
`@EventListener` annotation. For example, you could register a listener for a task event fired by
creating a user task with a specific task definition key. Here is the code example:

```java
@Component
class MyTaskListener {

  @EventListener(condition="#taskDelegate.eventName=='create' && #taskDelegate.taskDefinitionKey=='task_confirm'")
  public void onTaskEvent(DelegateTask taskDelegate) {
  // handle task event fired by create of task_confirm task
  }
}
```

## Ordering event listeners

Event listeners for the same event type can be executed in a specified order. To do so, provide an `Order` annotation
to the event listener:

```java
@Component
class MyTaskListener {

  @Order(1)
  @EventListener
  public void firstListener(DelegateTask taskDelegate) {
  // handle task event
  }

  @Order(2)
  @EventListener
  public void secondListener(DelegateTask taskDelegate) {
  // handle task event
  }

}
```
