---

title: 'Service Task'
sidebar_position: 10

menu:
  main:
    identifier: "bpmn-ref-tasks-service-task"
    parent: "bpmn-ref-tasks"
    description: "Invoke or execute business logic."

---



A Service Task is used to invoke services. In Operaton this is done by calling Java code or providing a work item for an external worker to complete asynchronously or invoking a logic which is implemented in form of webservices.

# Calling Java Code

There are four ways of declaring how to invoke Java logic:

* Specifying a class that implements a JavaDelegate or ActivityBehavior
* Evaluating an expression that resolves to a delegation object
* Invoking a method expression
* Evaluating a value expression

To specify a class that is called during process execution, the fully qualified classname needs to be provided by the `operaton:class` attribute.

```xml
<serviceTask id="javaService"
             name="My Java Service Task"
             operaton:class="org.operaton.bpm.MyJavaDelegate" />
```

Please refer to the [Java Delegate](../user-guide/process-engine/delegation-code.md#java-delegate) section of the [User Guide](../user-guide/index.md) for details on how to implement a Java Delegate.

It is also possible to use an expression that resolves to an object. This object must follow the
same rules as objects that are created when the `operaton:class` attribute is used.

```xml
<serviceTask id="beanService"
             name="My Bean Service Task"
             operaton:delegateExpression="${myDelegateBean}" />
```

Or an expression which calls a method or resolves to a value.

```xml
<serviceTask id="expressionService"
             name="My Expression Service Task"
             operaton:expression="${myBean.doWork()}" />
```

For more information about expression language as delegation code, please see the corresponding
[section](../user-guide/process-engine/expression-language.md#use-expression-language-as-delegation-code)
of the [User Guide](../user-guide/index.md).

It is also possible to invoke logic which is implemented in form of webservices. `operaton:connector` is an extension that allows calling REST/SOAP APIs directly from the workflow. For more information about using connectors, please see the corresponding [section](../user-guide/process-engine/connectors.md#use-connectors) of the [User Guide](../user-guide/index.md)

## Generic Java Delegates & Field Injection

You can easily write generic Java Delegate classes which can be configured later on via the BPMN 2.0 XML in the Service Task. Please refer to the [Field Injection](../user-guide/process-engine/delegation-code.md#field-injection) section of the [User Guide](../user-guide/index.md) for details.


## Service Task Results

The return value of a service execution (for a Service Task exclusively using expressions) can be assigned to an already existing or to a new process variable by specifying the process variable name as a literal value for the `operaton:resultVariable` attribute of a Service Task definition. Any existing value for a specific process variable will be overwritten by the result value of the service execution. When not specifying a result variable name, the service execution result value is ignored.

```xml
<serviceTask id="aMethodExpressionServiceTask"
           operaton:expression="#{myService.doSomething()}"
           operaton:resultVariable="myVar" />
```

In the example above, the result of the service execution (the return value of the `doSomething()` method invocation on object `myService`) is set to the process variable named `myVar` after the service execution completes.

:::warning[Result variables and multi-instance]
Note that when you use <code>operaton:resultVariable</code> in a multi-instance construct, for example in a multi-instance subprocess, the result variable is overwritten every time the task completes, which may appear as random behavior. See <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resultvariable">operaton:resultVariable</a> for details.
:::

# External Tasks

In contrast to calling Java code, where the process engine synchronously invokes Java logic, it is possible to implement a Service Task outside of the process engine's boundaries in the form of an external task. When a Service Task is declared external, the process engine offers a work item to workers that independently poll the engine for work to do. This decouples the implementation of tasks from the process engine and allows to cross system and technology boundaries. See the [user guide on external tasks](../user-guide/process-engine/external-tasks.md) for details on the concept and the relevant API.

To declare a Service Task to be handled externally, the attribute `operaton:type` can be set to `external` and the attribute `operaton:topic` specifies the external task's topic. For example, the following XML snippet defines an external Service Task with topic `ShipmentProcessing`:

```xml
<serviceTask id="anExternalServiceTask"
           operaton:type="external"
           operaton:topic="ShipmentProcessing" />
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
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#erroreventdefinition">operaton:errorEventDefinition</a>,
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
  <tr>
    <td></td>
    <td>
      The element <code>operaton:errorEventDefinition</code> can only be used as a child of <code>serviceTask</code> when the <code>operaton:type</code> attribute is set to <code>external</code>.
    </td>
  </tr>
</table>


# Additional Resources

* [Tasks](http://operaton.org/bpmn/reference.html#activities-task) in the [BPMN Modeling Reference](http://operaton.org/bpmn/reference.html) section
* [How to call a Webservice from BPMN](http://www.bpm-guide.de/2010/12/09/how-to-call-a-webservice-from-bpmn/). Please note that this article is outdated. However, it is still valid regarding how you would call a Web Service using the process engine.
