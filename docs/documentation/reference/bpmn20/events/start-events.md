---

title: 'Start Events'
sidebar_position: 10

menu:
  main:
    identifier: "bpmn-ref-events-start-event"
    parent: "bpmn-ref-events"
    description: "Start Events define where a Process or Sub Process starts."
---


Start events define where a Process or Sub Process starts.

The process engine supports different types of start events:

* [Blank](../reference/bpmn20/events/none-events.md)
* [Timer](../reference/bpmn20/events/timer-events.md)
* [Message](../reference/bpmn20/events/message-events.md)
* [Signal](../reference/bpmn20/events/signal-events.md)
* [Conditional](../reference/bpmn20/events/conditional-events.md)

The engine requires at least one start event to instantiate a process. There can be a maximum of one blank or timer start event per process definition. There can be multiple message or signal start events.


# Asynchronous Instantiation

A start event may be declared as asynchronous with `operaton:asyncBefore="true"`

```xml
<startEvent id="startEvent" operaton:asyncBefore="true" />
```

This will ensure that the process engine creates a process instance when the process is instantiated, but the execution of the initial activities is not done synchronously. Instead, a job is created and asynchronously processed by the [job executor](../user-guide/process-engine/the-job-executor.md). See the [Asynchronous Continuations](../user-guide/process-engine/transactions-in-processes.md#asynchronous-continuations) section of the [User Guide](../user-guide/index.md) for some background information.


# Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formhandlerclass">operaton:formHandlerClass</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formkey">operaton:formKey</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formref">operaton:formRef</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formrefbinding">operaton:formRefBinding</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formrefversion">operaton:formRefVersion</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#initiator">operaton:initiator</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>
    </td>
  </tr>
  <tr>
    <th>Extension Elements</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#failedjobretrytimecycle">operaton:failedJobRetryTimeCycle</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#formdata">operaton:formData</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#formproperty">operaton:formProperty</a>,
    </td>
  </tr>
  <tr>
    <th>Constraints</th>
    <td>
      The <code>operaton:exclusive</code> attribute is only evaluated if the attribute
      <code>operaton:asyncBefore</code> or <code>operaton:asyncAfter</code> is set to <code>true</code>
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attributes <code>operaton:asyncBefore</code> and <code>operaton:initiator</code> are only available for start events of a Process
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      Only one <code>operaton:formData</code> extension element is allowed
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attributes <code>operaton:formHandlerClass</code> and <code>operaton:formKey</code>
      are only available for the intital start event of a Process
    </td>
  </tr>
</table>
