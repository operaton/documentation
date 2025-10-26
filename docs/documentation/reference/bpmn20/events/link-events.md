---

title: 'Link Events'
sidebar_position: 80

menu:
  main:
    identifier: "bpmn-ref-events-link-events"
    parent: "bpmn-ref-events"
    description: "Bridge very long sequence flows."

---

Link events are a special case - it has no special execution semantics but serves as a "GoTo" to another point
in the same process model (to be precise: in the same sub process). Hence you can use two matching links as an
alternative to a sequence flow as shown in the following example.

<div data-bpmn-diagram="../bpmn/event-link"></div>

Note that you might have the same event source (throwing intermediate link event with the same event definition name) multiple times, but the event target (catching intermediate link event) has to be unique according to the BPMN 2.0 specification.


## Link Event Definition

The name of the link is set by a LinkEventDefinition within the XML. Please note that this should always correspond to the name
of the intermediate event, otherwise this gets really confusing to everybody looking at the diagram (however, the engine just
gives a warning as it is valid BPMN 2.0).

```xml
<process id="someProcess">
  <!-- ... -->
  <intermediateThrowEvent id="IntermediateThrowEvent_1" name="LinkA">
    <linkEventDefinition id="LinkEventDefinition_1" name="LinkA"/>
  </intermediateThrowEvent>
  <intermediateCatchEvent id="IntermediateCatchEvent_1" name="LinkA">
    <linkEventDefinition id="LinkEventDefinition_2" name="LinkA"/>
  </intermediateCatchEvent>
  <!-- ... -->
</process>
```


## Operaton Extensions

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
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#inputoutput">operaton:inputOutput</a>
    </td>
  </tr>
  <tr>
    <th>Constraints</th>
    <td>&ndash;</td>
  </tr>
</table>
