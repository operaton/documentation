---

title: 'Business Rule Task'
sidebar_position: 40

menu:
  main:
    identifier: "bpmn-ref-tasks-business-rule-task"
    parent: "bpmn-ref-tasks"
    description: "Execute an automated business decision."

---

A Business Rule Task is used to synchronously execute one or more rules. It is also possible to call Java code or providing a work item for an external worker to complete asynchronously or invoking a logic which is implemented in form of webservices.

# Using Operaton DMN Engine

You can use the Operaton DMN engine integration to evaluate a DMN decision. You have
to specify the decision key to evaluate as the `operaton:decisionRef` attribute. Additionally,
the `operaton:decisionRefBinding` specifies which version of the decision should be evaluated.
Valid values are:

* `deployment`, which evaluates the decision version which was deployed with the process
version,
* `latest` which will always evaluate the latest decision version,
* `version` which allows you to specify a specific version to execute with the `operaton:decisionRefVersion` attribute, and
* `versionTag` which allows you to specify a specific version tag to execute with the `operaton:decisionRefVersionTag` attribute.

```xml
<businessRuleTask id="businessRuleTask"
    operaton:decisionRef="myDecision"
    operaton:decisionRefBinding="version"
    operaton:decisionRefVersion="12" />
```

The `operaton:decisionRefBinding` attribute defaults to `latest`.

```xml
<businessRuleTask id="businessRuleTask"
    operaton:decisionRef="myDecision" />
```

The attributes `operaton:decisionRef`, `operaton:decisionRefVersion`, and `operaton:decisionRefVersionTag` can be specified as
an expression which will be evaluated on execution of the task.

```xml
<businessRuleTask id="businessRuleTask"
    operaton:decisionRef="${decisionKey}"
    operaton:decisionRefBinding="version"
    operaton:decisionRefVersion="${decisionVersion}" />
```

The output of the decision, also called decision result, is not saved as process variable automatically. It has to pass into a process variable by using a [predefined](../user-guide/process-engine/decisions/bpmn-cmmn.md#predefined-mapping-of-the-decision-result) or a [custom](../user-guide/process-engine/decisions/bpmn-cmmn.md#custom-mapping-into-process-variables) mapping of the decision result.

In case of a predefined mapping, the `operaton:mapDecisionResult` attribute references the mapper to use. The result of the mapping is saved in the variable which is specified by the `operaton:resultVariable` attribute. If no predefined mapper is set then the `resultList` mapper is used by default.

```xml
<businessRuleTask id="businessRuleTask"
    operaton:decisionRef="myDecision"
    operaton:mapDecisionResult="singleEntry"
    operaton:resultVariable="result" />
```

See the [User Guide](../user-guide/process-engine/decisions/bpmn-cmmn.md#the-decision-result) for details about the mapping.

:::warning[Name of the Result Variable]
The result variable should not have the name `decisionResult`, as the decision result itself is saved in a variable with this name. Otherwise, an exception is thrown while saving the result variable.
:::

# DecisionRef Tenant Id

When the Business Rule Task resolves the decision definition to be evaluated it must take multi tenancy into account.

## Default Tenant Resolution
By default, the tenant id of the calling process definition is used to evaluate the decision definition.
That is, if the calling process definition has no tenant id, then the Business Rule Task evaluates a decision definition using the provided key, binding and without a tenant id (tenant id = null).
If the calling process definition has a tenant id, a decision definition with the provided key and the same tenant id is evaluated.

Note that the tenant id of the calling process instance is not taken into account in the default behavior.

## Explicit Tenant Resolution

In some situations it may be useful to override this default behavior and specify the tenant id explicitly.

The `operaton:decisionRefTenantId` attribute allows to explicitly specify a tenant id:

```xml
<businessRuleTask id="businessRuleTask" decisionRef="myDecision"
  operaton:decisionRefTenantId="TENANT_1">
</businessRuleTask>
```

If the tenant id is not known at design time, an expression can be used as well:

```xml
<businessRuleTask id="businessRuleTask" decisionRef="myDecision"
  operaton:decisionRefTenantId="${ myBean.calculateTenantId(variable) }">
</businessRuleTask>
```

An expression also allows using the tenant id of the calling process instance instead of the calling process definition:

```xml
<businessRuleTask id="businessRuleTask" decisionRef="myDecision"
  operaton:decisionRefTenantId="${ execution.tenantId }">
</businessRuleTask>
```

# Using a Custom Rule Engine

You can integrate with other rule engines. To do so, you have to plug in your
implementation of the rule task the same way as in a Service Task.

```xml
<businessRuleTask id="businessRuleTask"
    operaton:delegateExpression="${MyRuleServiceDelegate}" />
```


# Using Delegate Code

Alternatively, a Business Rule Task can be implemented using Java Delegation just as a Service Task. For more
information on this please see the [Service Tasks](service-task.md) documentation.


# Implementing as an External Task

In addition to the above, a Business Rule Task can be implemented via the [External Task](../user-guide/process-engine/external-tasks.md) mechanism where an external system polls the process engine for work to do. See the section on [Service Tasks](service-task.md#external-tasks) for more information about how to configure an external task.


# Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#class">operaton:class</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionref">operaton:decisionRef</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefbinding">operaton:decisionRefBinding</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionreftenantid">operaton:decisionRefTenantId</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefversion">operaton:decisionRefVersion</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefversiontag">operaton:decisionRefVersionTag</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#delegateexpression">operaton:delegateExpression</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#expression">operaton:expression</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#mapdecisionresult">operaton:mapDecisionResult</a>,
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
      One of the attributes <code>operaton:class</code>, <code>operaton:delegateExpression</code>, <code>operaton:decisionRef</code>,
      <code>operaton:type</code> or <code>operaton:expression</code> is mandatory
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>operaton:resultVariable</code> can only be used in combination with the
      <code>operaton:decisionRef</code> or <code>operaton:expression</code> attribute
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


# Additional Resources

* [Decisions](../user-guide/process-engine/decisions/index.md)
* [Service Tasks](../reference/bpmn20/tasks/service-task.md)
* [Tasks](http://operaton.org/bpmn/reference.html#activities-task) in the [BPMN 2.0 Modeling Reference](http://operaton.org/bpmn/reference.html)
* [Demo using Drools on the Business Rule Task](https://github.com/operaton/operaton-consulting/tree/master/one-time-examples/order-confirmation-rules)
