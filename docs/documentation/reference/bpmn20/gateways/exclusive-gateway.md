---

title: 'Data-based Exclusive Gateway (XOR)'
sidebar_position: 10

menu:
  main:
    identifier: "bpmn-ref-gateways-xor"
    parent: "bpmn-ref-gateways"
    description: "Model decisions based on data."

---


An exclusive gateway (also called the XOR gateway or, in more technical terms, the exclusive data-based gateway), is used to model a decision in the process. When the execution arrives at this gateway, all outgoing sequence flows are evaluated in the order in which they have been defined. The sequence flow which condition evaluates to 'true' (or which doesn't have a condition set, conceptually having a 'true' value defined on the sequence flow) is selected for continuing the process.

Note that only one sequence flow is selected when using the exclusive gateway. In case multiple sequence flow have a condition that evaluates to 'true', the first one defined in the XML is exclusively selected for continuing the process.

If no sequence flow can be selected (no condition evaluates to 'true') this will result in a runtime exception, unless you have a default flow defined. One default flow can be set on the gateway itself in case no other condition matches - like an 'else' in programming languages.


<div data-bpmn-diagram="../bpmn/exclusive-gateway"></div>


Note that a gateway without an icon inside it defaults to an exclusive gateway, even if we recommend to use the X within the gateway if your BPMN tool gives you that option.

The XML representation of an exclusive gateway is straightforward: one line defining the gateway and condition expressions defined on the outgoing sequence flow. The default flow (optional) is set as attribute on the gateway itself. Note that the name of the flow (used in the diagram, meant for the human being) might be different than the formal expression (used in the engine).


```xml
<exclusiveGateway id="exclusiveGw" name="Exclusive Gateway" default="flow4" />

<sequenceFlow id="flow2" sourceRef="exclusiveGw" targetRef="theTask1" name="${x==1}">
  <conditionExpression xsi:type="tFormalExpression">${x == 1}</conditionExpression>
</sequenceFlow>

<sequenceFlow id="flow3" sourceRef="exclusiveGw" targetRef="theTask2" name="${x==2}">
  <conditionExpression xsi:type="tFormalExpression">${x == 2}</conditionExpression>
</sequenceFlow>

<sequenceFlow id="flow4" sourceRef="exclusiveGw" targetRef="theTask3" name="else">
</sequenceFlow>
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
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#executionlistener">operaton:executionListener</a>
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


# Additional Resources

*   [Conditional and Default Sequence Flows](../gateways/sequence-flow.md)
*   [Exclusive Gateways](http://operaton.org/bpmn/reference.html#gateways-data-based-exclusive-gateways) in the [BPMN 2.0 Modeling Reference](http://operaton.org/bpmn/reference.html)
