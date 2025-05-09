---

title: 'Send Task'
sidebar_position: 20

menu:
  main:
    identifier: "bpmn-ref-tasks-send-task"
    parent: "bpmn-ref-tasks"
    description: "Send a message."

---

A Send Task is used to send a message. In Operaton this is done by calling Java code.

The Send Task has the same behavior as a Service Task.

```xml
<sendTask id="sendTask" operaton:class="org.operaton.bpm.MySendTaskDelegate" />
```


# Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#class">operaton:class</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#delegateexpression">operaton:delegateExpression</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#expression">operaton:expression</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resultvariable">operaton:resultVariable</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#topic">operaton:topic</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#type">operaton:type</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#taskpriority">operaton:taskPriority</a>
    </td>
  </tr>
  <tr>
    <th>Extension Elements</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#failedjobretrytimecycle">operaton:failedJobRetryTimeCycle</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#field">operaton:field</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#connector">operaton:connector</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#inputoutput">operaton:inputOutput</a>
    </td>
  </tr>
  <tr>
    <th>Constraints</th>
    <td>
      One of the attributes <code>operaton:class</code>, <code>operaton:delegateExpression</code>,
      <code>operaton:type</code> or <code>operaton:expression</code> is mandatory
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>operaton:resultVariable</code> can only be used in combination with the
      <code>operaton:expression</code> attribute
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The <code>operaton:exclusive</code> attribute is only evaluated if the attribute
      <code>operaton:asyncBefore</code> or <code>operaton:asyncAfter</code> is set to <code>true</code>
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>operaton:topic</code> can only be used when the <code>operaton:type</code> attribute is set to <code>external</code>.
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>operaton:taskPriority</code> can only be used when the <code>operaton:type</code> attribute is set to <code>external</code>.
    </td>
  </tr>
</table>
