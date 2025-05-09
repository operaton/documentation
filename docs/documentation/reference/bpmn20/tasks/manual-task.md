---

title: 'Manual Task'
sidebar_position: 70

menu:
  main:
    identifier: "bpmn-ref-tasks-manual-task"
    parent: "bpmn-ref-tasks"
    description: "A task which is performed externally."

---

A Manual Task defines a task that is external to the BPM engine. It is used to model work that is done by somebody who the engine does not need to know of and that has no known system or UI interface. For the engine, a manual task is handled as a pass-through activity, automatically continuing the process when the process execution arrives at it.

```xml
<manualTask id="myManualTask" name="Manual Task" />
```


# Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>
    </td>
  </tr>
  <tr>
    <th>Extension Elements</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#failedjobretrytimecycle">operaton:failedJobRetryTimeCycle</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#inputoutput">operaton:inputOutput</a>
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
