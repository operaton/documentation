---

title: 'Receive Task'
sidebar_position: 60

menu:
  main:
    identifier: "bpmn-ref-tasks-receive-task"
    parent: "bpmn-ref-tasks"
    description: "Wait for a message to arrive."

---

A Receive Task is a simple task that waits for the arrival of a certain message. When the process execution arrives at a Receive Task, the process state is committed to the persistence storage. This means that the process will stay in this wait state until a specific message is received by the engine, which triggers continuation of the process beyond the Receive Task.

A Receive Task with a message reference can be triggered like an ordinary event:

```xml
<definitions ...>
  <message id="newInvoice" name="newInvoiceMessage"/>
  <process ...>
    <receiveTask id="waitState" name="wait" messageRef="newInvoice">
  ...
```

You can then either correlate the message:

```java
// correlate the message
runtimeService.createMessageCorrelation(subscription.getEventName())
  .processInstanceBusinessKey("AB-123")
  .correlate();
```

Or explicitly query for the subscription and trigger it:

```java
ProcessInstance pi = runtimeService.startProcessInstanceByKey("processWaitingInReceiveTask");

EventSubscription subscription = runtimeService.createEventSubscriptionQuery()
  .processInstanceId(pi.getId()).eventType("message").singleResult();

runtimeService.messageEventReceived(subscription.getEventName(), subscription.getExecutionId());
```

:::note
Correlation of a parallel multi instance isn't possible because the subscription can't be identified unambiguously.
:::

To continue a process instance that is currently waiting at a Receive Task without a message reference, the `runtimeService.signal(executionId)` can be called, using the id of the execution that arrived in the Receive Task.

```xml
<receiveTask id="waitState" name="wait" />
```

The following code snippet shows how this works in practice:

```java
ProcessInstance pi = runtimeService.startProcessInstanceByKey("receiveTask");
Execution execution = runtimeService.createExecutionQuery()
  .processInstanceId(pi.getId()).activityId("waitState").singleResult();

runtimeService.signal(execution.getId());
```


## Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-attributes#asyncbefore">operaton:asyncBefore</a>,
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-attributes#asyncafter">operaton:asyncAfter</a>,
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-attributes#exclusive">operaton:exclusive</a>,
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-attributes#jobpriority">operaton:jobPriority</a>
    </td>
  </tr>
  <tr>
    <th>Extension Elements</th>
    <td>
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-elements#failedjobretrytimecycle">operaton:failedJobRetryTimeCycle</a>,
      <a href="/docs/documentation/reference/bpmn20/custom-extensions/extension-elements#inputoutput">operaton:inputOutput</a>
    </td>
  </tr>
  <tr>
    <th>Constraints</th>
    <td>
      The <code>operaton:exclusive</code> attribute is only evaluated if the attribute
      <code>operaton:asyncBefore</code> or <code>operaton:asyncAfter</code> is set to <code>true</code>
    </td>
  </tr>
</table>


## Additional Resources

* [Tasks](http://operaton.org/bpmn/reference.html#activities-task) in the [BPMN 2.0 Modeling Reference](http://operaton.org/bpmn/reference.html)
* [Message Receive Events](../events/message-events.md)
