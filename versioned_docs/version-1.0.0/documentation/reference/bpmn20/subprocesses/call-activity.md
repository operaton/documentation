---

title: 'Call Activity'
sidebar_position: 20

menu:
  main:
    identifier: "bpmn-subprocess-call-activity"
    parent: "bpmn-subprocess"
    description: "Call a process from another process."

---

BPMN 2.0 makes a distinction between an embedded subprocess and a call activity. From a conceptual point of view, both will call a subprocess when process execution arrives at the activity.

The difference is that the call activity references a process that is external to the process definition, whereas the subprocess is embedded within the original process definition. The main use case for the call activity is to have a reusable process definition that can be called from multiple other process definitions. Although not yet part of the BPMN specification, it is also possible to call a CMMN case definition.

When process execution arrives at the call activity, a new process instance is created, which is used to execute the subprocess, potentially creating parallel child executions as within a regular process. The main process instance waits until the subprocess is completely ended, and continues the original process afterwards.

<div data-bpmn-diagram="./bpmn/call-activity"></div>

A call activity is visualized the same way as a collapsed embedded subprocess, however with a thick border. Depending on the modeling tool, a call activity can also be expanded, but the default visualization is the collapsed representation.

A call activity is a regular activity that requires a calledElement which references a process definition by its key. In practice, this means that the id of the process is used in the calledElement:

```xml
<callActivity id="callCheckCreditProcess" name="Check credit" calledElement="checkCreditProcess" />
```

Note that the process definition of the subprocess is resolved at runtime. This means that the subprocess can be deployed independently from the calling process, if needed.


## CalledElement Binding

In a call activity the `calledElement` attribute contains the process definition key as reference to the subprocess. This means that the latest process definition version of the subprocess is always called.
To call another version of the subprocess it is possible to define the attributes `calledElementBinding`, `calledElementVersion`, and `calledElementVersionTag` in the call activity. These attributes are optional.

CalledElementBinding has four different values:

* latest: always call the latest process definition version (which is also the default behaviour if the attribute isn't defined)
* deployment: if called process definition is part of the same deployment as the calling process definition, use the version from deployment
* version: call a fixed version of the process definition, in this case `calledElementVersion` is required. The version number can either be specified in the BPMN XML or returned by an expression (see [custom extensions](../custom-extensions/extension-attributes.md#calledelementversion))
* versionTag: call a fixed version tag of the process definition, in this case `calledElementVersionTag` is required. The version tag can either be specified in the BPMN XML or returned by an expression (see [custom extensions](../custom-extensions/extension-attributes.md#calledelementversiontag))

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess"
  operaton:calledElementBinding="latest|deployment|version"
  operaton:calledElementVersion="17">
</callActivity>
```
or
```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess"
  operaton:calledElementBinding="versionTag"
  operaton:calledElementVersionTag="ver-tag-1.0.1">
</callActivity>
```

## CalledElement Tenant Id

When the call activity resolves the process definition to be called it must take multi tenancy into account.

### Default Tenant Resolution
By default, the tenant id of the calling process definition is used to resolve the called process definition.
That is, if the calling process definition has no tenant id, then the call activity resolves a process definition using the provided key, binding and without a tenant id (tenant id = null).
If the calling process definition has a tenant id, a process definition with the provided key and the same tenant id is resolved.

Note that the tenant id of the calling process instance is not taken into account in the default behavior.

### Explicit Tenant Resolution

In some situations it may be useful to override this default behavior and specify the tenant id explicitly.

The `operaton:calledElementTenantId` attribute allows to explicitly specify a tenant id:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess"
  operaton:calledElementTenantId="TENANT_1">
</callActivity>
```

If the tenant id is not known at design time, an expression can be used as well:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess"
  operaton:calledElementTenantId="${ myBean.calculateTenantId(variable) }">
</callActivity>
```

An expression also allows using the tenant id of the calling process instance instead of the calling process definition:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess"
  operaton:calledElementTenantId="${ execution.tenantId }">
</callActivity>
```


## Passing Variables

You can pass process variables to the subprocess and vice versa. The data is copied into the subprocess when it is started and copied back into the main process when it ends.

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <operaton:in source="someVariableInMainProcess" target="nameOfVariableInSubProcess" />
    <operaton:out source="someVariableInSubProcss" target="nameOfVariableInMainProcess" />
  </extensionElements>
</callActivity>
```

By default, variables declared in `out` elements are set in the highest possible variable scope.

Furthermore, you can configure the call activity so that all process variables are passed to the subprocess and vice versa. The process variables have the same name in the main process as in the subprocess.

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <operaton:in variables="all" />
    <operaton:out variables="all" />
  </extensionElements>
</callActivity>
```

It is possible to use expressions here as well:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <operaton:in sourceExpression="${x+5}" target="y" />
    <operaton:out sourceExpression="${y+5}" target="z" />
  </extensionElements>
</callActivity>
```

So in the end `z = y+5 = x+5+5` holds.

Source expressions are evaluated in the context of the called process instance. That means, in cases where calling and called process definitions belong to different process applications, context like Java classes, Spring or CDI beans is resolved from the process application the called process definition belongs to.

### Variable Output on BPMN Error Event

When a BPMN error event from a called process instance is caught in the calling process instance, the output variable mappings are executed as well. Depending on the BPMN models, this requires output parameters to tolerate `null` values for variables that do not exist in the called instance when the error is propagated.

### Combination with Input/Output parameters

Call activities can be combined with [Input/Output parameters](../../../user-guide/process-engine/variables.md#inputoutput-variable-mapping) as well. This allows for an even more flexible mapping of variables into the called process. In order to only map variables that are declared in the `inputOutput` mapping, the attribute `local` can be used. Consider the following XML:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <!-- Input/Output parameters -->
    <operaton:inputOutput>
      <operaton:inputParameter name="var1">
        <operaton:script scriptFormat="groovy">
          <![CDATA[
            sum = a + b + c
          ]]>
        </operaton:script>
      </operaton:inputParameter>
      <operaton:inputParameter name="var2"></operaton:inputParameter>
    </operaton:inputOutput>

    <!-- Mapping to called instance -->
    <operaton:in variables="all" local="true" />
  </extensionElements>
</callActivity>
```

Setting `local="true"` means that all local variables of the execution executing the call activity are mapped into the called process instance. These are exactly the variables that are declared as input parameters.

The same can be done with output parameters:

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <!-- Input/Output parameters -->
    <operaton:inputOutput>
      <operaton:outputParameter name="var1">
        <operaton:script scriptFormat="groovy">
          <![CDATA[
            sum = a + b + c
          ]]>
        </operaton:script>
      </operaton:outputParameter>
      <operaton:outputParameter name="var2"></operaton:outputParameter>
    </operaton:inputOutput>

    <!-- Mapping from called instance -->
    <operaton:out variables="all" local="true" />
  </extensionElements>
</callActivity>
```

When the called process instance ends, due to `local="true"` in the `operaton:out` parameter all variables are mapped to local variables of the execution executing the call activity. These variables can be mapped to process instance variables by using an output mapping. Any variable that is not declared by a `operaton:outputParameter` element will not be available anymore after the call activity ends.


### Delegation of Variable Mapping

The mapping of input and output variables can also be delegated. This means the passing of input or/and output variables can be done in Java code.
For this the [Delegate Variable Mapping](../../../user-guide/process-engine/delegation-code.md#delegate-variable-mapping) interface must be implemented.

There are two possible ways to use delegation for variable mapping.

### Delegate Variable Mapping via Reference

The first one is to set the Operaton extension property `variableMappingClass` and reference the implementation of the `DelegateVariableMapping` interface via the whole class name.


```xml
 <process id="callSimpleSubProcess">

    <startEvent id="theStart" />

    <sequenceFlow id="flow1" sourceRef="theStart" targetRef="callSubProcess" />

    <callActivity id="callSubProcess" calledElement="simpleSubProcess" operaton:variableMappingClass="org.operaton.bpm.example.bpm.callactivity.DelegatedVarMapping"/>

    <sequenceFlow id="flow3" sourceRef="callSubProcess" targetRef="taskAfterSubProcess" />

    <userTask id="taskAfterSubProcess" name="Task after subprocess" />

    <sequenceFlow id="flow4" sourceRef="taskAfterSubProcess" targetRef="theEnd" />

    <endEvent id="theEnd" />

  </process>
```

### Delegate Variable Mapping via Expression

The second one is to set the Operaton extension property `variableMappingDelegateExpression` with an expression.
This allows to specify an expression that resolves to an object implementing the `DelegateVariableMapping` interface.

```xml
  <process id="callSimpleSubProcess">

    <startEvent id="theStart" />

    <sequenceFlow id="flow1" sourceRef="theStart" targetRef="callSubProcess" />

    <callActivity id="callSubProcess" calledElement="simpleSubProcess" operaton:variableMappingDelegateExpression="${expr}"/>

    <sequenceFlow id="flow3" sourceRef="callSubProcess" targetRef="taskAfterSubProcess" />

    <userTask id="taskAfterSubProcess" name="Task after subprocess" />

    <sequenceFlow id="flow4" sourceRef="taskAfterSubProcess" targetRef="theEnd" />

    <endEvent id="theEnd" />

  </process>
```
See [Delegate Variable Mapping](../../../user-guide/process-engine/delegation-code.md#delegate-variable-mapping) for further information of implementing the interface.

## Passing Business Key

You can pass the business key to the subprocess. The data is copied into the subprocess when it is started. You can not give back the business key to the parent process because the business key is not changeable.

```xml
<callActivity id="callSubProcess" calledElement="checkCreditProcess" >
  <extensionElements>
    <operaton:in businessKey="#{execution.processBusinessKey}" />
  </extensionElements>
</callActivity>
```


## Example

The following process diagram shows a simple handling of an order. Since, for example, the billing could be common to many other processes, it is modeled as a call activity.

<div data-bpmn-diagram="./bpmn/call-activity"></div>

The XML looks as follows:

```xml
<startEvent id="theStart" />
<sequenceFlow id="flow1" sourceRef="theStart" targetRef="shipping" />

<callActivity id="shipping" name="Shipping" calledElement="shippingProcess" />
<sequenceFlow id="flow2" sourceRef="shipping" targetRef="billing" />

<callActivity id="billing" name="Billing" calledElement="billingProcess" />
<sequenceFlow id="flow3" sourceRef="billing" targetRef="end" />

<endEvent id="end" />
```

There is nothing special about the process definition of the subprocess. It could also be used without being called from another process.

## Create a Case Instance

A call activity can also be used to create a new CMMN case instance as a subordinate of the corresponding process instance. The call activity completes as soon as the created case instance reaches the state `COMPLETED` for the first time. In contrast to calling a BPMN process, the attribute `caseRef` instead of the attribute `calledElement` must be used to reference a case definition by its key. This means that the latest case definition version is always called.

### Case Binding

To call another version of a case definition it is possible to define the attributes `caseBinding` and `caseVersion` in the call activity. Both attributes are optional.

CaseBinding has three different values:

*   latest: always call the latest case definition version (which is also the default behaviour if the attribute isn't defined)
*   deployment: if called case  definition is part of the same deployment as the calling process definition, use the version from deployment
*   version: call a fixed version of the case definition, in this case `caseVersion` is required

```xml
<callActivity id="callSubProcess" operaton:caseRef="checkCreditCase"
  operaton:caseBinding="latest|deployment|version"
  operaton:caseVersion="17">
</callActivity>
```

### Case Tenant Id

The call activity must take multi tenancy into account when resolving the case definition to be called.

The [default behavior](#default-tenant-resolution) is the same as when resolving BPMN Process Definitions (i.e., the tenant id of the calling process definition is used to resolve the called case definition.)

In order to override the default behavior, the tenant id for resolving the called case definition can be specified explicitly using the `operaton:caseTenantId` attribute:

```xml
<callActivity id="callSubProcess" operaton:caseRef="checkCreditCase"
  operaton:caseTenantId="TENANT_1">
</callActivity>
```

If the tenant id is not known at design time, an expression can be used as well:

```xml
<callActivity id="callSubProcess" operaton:caseRef="checkCreditCase"
  operaton:caseTenantId="${ myBean.calculateTenantId(variable) }">
</callActivity>
```

An expression also allows using the tenant id of the calling process instance instead of the calling process definition:

```xml
<callActivity id="callSubProcess" operaton:caseRef="checkCreditCase"
  operaton:caseTenantId="${ execution.tenantId }">
</callActivity>
```

## Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementbinding">operaton:calledElementBinding</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementversion">operaton:calledElementVersion</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementversiontag">operaton:calledElementVersionTag</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementtenantid">operaton:calledElementTenantId</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#casebinding">operaton:caseBinding</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#caseref">operaton:caseRef</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#caseversion">operaton:caseVersion</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#casetenantid">operaton:caseTenantId</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#variablemappingclass">operaton:variableMappingClass</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#variablemappingdelegateexpression">operaton:variableMappingDelegateExpression</a>
    </td>
  </tr>
  <tr>
    <th>Extension Elements</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#in">operaton:in</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#out">operaton:out</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#inputoutput">operaton:inputOutput</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#failedjobretrytimecycle">operaton:failedJobRetryTimeCycle</a>
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
      The attribute <code>operaton:calledElementVersion</code> should only be set if
      the attribute <code>operaton:calledElementBinding</code> equals <code>version</code>
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>calledElement</code> cannot be used in combination
      with the attribute <code>operaton:caseRef</code> and vice versa.
    </td>
  </tr>
  <tr>
    <td></td>
    <td>
      The attribute <code>operaton:caseVersion</code> should only be set if
      the attribute <code>operaton:caseBinding</code> equals <code>version</code>
    </td>
  </tr>
</table>

## Additional Resources

*   [Call Activity](http://operaton.org/bpmn/reference.html#activities-call-activity) in the [BPMN 2.0 Modeling Reference](http://operaton.org/bpmn/reference.html)
