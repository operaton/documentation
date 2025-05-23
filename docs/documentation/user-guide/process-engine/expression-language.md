---

title: 'Expression Language'
sidebar_position: 70

menu:
  main:
    identifier: "user-guide-process-engine-expression-language"
    parent: "user-guide-process-engine"

---

Operaton supports the Unified Expression Language (EL), specified by the [Jakarta Expression
Language 4.0 standard][JakartaEL]. To do so, it maintains a custom version of the open source [JUEL][] implementation.

Note, compared to EL 4.0 this JUEL implementation has the following limitations:


- Initializing collections directly within expressions (e.g., `${[1,2,3]}`) is NOT supported.

- Lambda expressions (e.g., inline functions `${((x,y)->x+y)(3,4)}`) are NOT supported.

- Referencing static fields (e.g., `${Boolean.TRUE}`), static functions (e.g., `${Integer.parseInt("123")}`), and enums (e.g., `${Thread.State.TERMINATED}`) are NOT supported.

- The Assignment Operator `(A=B)`, the String Concatenation Operator `(A+=B)`, and the Semicolon Operator `(A ; B)` are NOT supported.

To get more general information about the usage of Expression Language,
please read the [official documentation][]. It provides examples that give a good overview of
the syntax of expressions.

Within Operaton, EL can be used in many circumstances to evaluate small script-like
expressions. The following table provides an overview of the BPMN elements which support
usage of EL.

<table class="table desc-table">
  <tr>
    <th>BPMN element</th>
    <th>EL support</th>
  </tr>
  <tr>
    <td>
      <a href="#delegation-code">
        Service Task, Business Rule Task, Send Task,
        Message Intermediate Throwing Event, Message End Event, Execution Listener and
        Task Listener
      </a>
    </td>
    <td>Expression language as delegation code</td>
  </tr>
  <tr>
    <td>
      <a href="#conditions">
        Sequence Flows, Conditional Events
      </a>
    </td>
    <td>Expression language as condition expression</td>
  </tr>
  <tr>
    <td>
        <a href="#inputoutput-parameters">
          All Tasks, All Events, Transaction, Subprocess and Connector
        </a>
    </td>
    <td>Expression language inside an inputOutput parameter mapping</td>
  </tr>
  <tr>
    <td>
        <a href="#value">
          Different Elements
        </a>
    </td>
    <td>Expression language as the value of an attribute or element</td>
  </tr>
  <tr>
    <td>
      <a href="../process-engine/the-job-executor.md#specifying-priorities-in-bpmn-xml">
        All Flow Nodes, Process Definition
      </a>
    </td>
    <td>Expression language to determine the priority of a job</td>
  </tr>
</table>


# Usage of Expression Language

## Delegation Code

Besides Java code, Operaton also supports the evaluation of expressions as delegation code. For
general information about delegation code, see the corresponding
[section](../process-engine/delegation-code.md).

Two types of expressions are currently supported: `operaton:expression` and
`operaton:delegateExpression`.

With `operaton:expression` it is possible to evaluate a value expression or to invoke
a method expression. You can use special variables which are available inside an expression or
Spring and CDI beans. For more information about [variables][] and [Spring][], respectively [CDI][] beans,
please see the corresponding sections.

```xml
  <process id="process">
    <extensionElements>
      <!-- execution listener which uses an expression to set a process variable -->
      <operaton:executionListener event="start" expression="${execution.setVariable('test', 'foo')}" />
    </extensionElements>

    <!-- ... -->

    <userTask id="userTask">
      <extensionElements>
        <!-- task listener which calls a method of a bean with current task as parameter -->
        <operaton:taskListener event="complete" expression="${myBean.taskDone(task)}" />
      </extensionElements>
    </userTask>

    <!-- ... -->

    <!-- service task which evaluates an expression and saves it in a result variable -->
    <serviceTask id="serviceTask"
        operaton:expression="${myBean.ready}" operaton:resultVariable="myVar" />

    <!-- ... -->

  </process>
```

The attribute `operaton:delegateExpression` is used for expressions which evaluate to a delegate
object. This delegate object must implement either the `JavaDelegate` or `ActivityBehavior`
interface.

```xml
  <!-- service task which calls a bean implementing the JavaDelegate interface -->
  <serviceTask id="task1" operaton:delegateExpression="${myBean}" />

  <!-- service task which calls a method which returns delegate object -->
  <serviceTask id="task2" operaton:delegateExpression="${myBean.createDelegate()}" />
```


## Conditions

To use conditional sequence flows or conditional events, expression language is usually used.
For conditional sequence flows, a `conditionExpression` element of a sequence flow has to be used.
For conditional events, a `condition` element of a conditional event has to be used. Both are
of the type `tFormalExpression`. The text content of the element is the expression to be evaluated.

Within the expression, some special variables are available which enable access of the current
context. To find more information about the available variables, please see the [corresponding
section][variables].

The following example shows usage of expression language as condition of a sequence flow:

```xml
  <sequenceFlow>
    <conditionExpression xsi:type="tFormalExpression">
      ```${test == 'foo'}
    </conditionExpression>
  </sequenceFlow>
```

For usage of expression language on conditional events, see the following example:

```xml
<conditionalEventDefinition>
  <condition type="tFormalExpression">${var1 == 1}</condition>
</conditionalEventDefinition>
```


## inputOutput Parameters

With the Operaton`inputOutput` extension element you can map an `inputParameter` or `outputParameter`
with expression language.

Inside the expression some special variables are available which enable the access of the current
context. To find more information about the available variables please see the [corresponding
section][variables].

The following example shows an `inputParameter` which uses expression language to call a method of
a bean.

```xml
  <serviceTask id="task" operaton:class="org.operaton.bpm.example.SumDelegate">
    <extensionElements>
      <operaton:inputOutput>
        <operaton:inputParameter name="x">
          ```${myBean.calculateX()}
        </operaton:inputParameter>
      </operaton:inputOutput>
    </extensionElements>
  </serviceTask>
```

## External Task Error Handling

For External Tasks it is possible to define
[operaton:errorEventDefinition](../../reference/bpmn20/custom-extensions/extension-elements.md#erroreventdefinition)
elements which can be provided with a JUEL expression. The expression is evaluated on `ExternalTaskService#complete` and
`ExternalTaskService#handleFailure`. If the expression evaluates to `true`, a BPMN error is thrown which can be caught by an
[Error Boundary Event](../../reference/bpmn20/events/error-events.md#error-boundary-event).

In the scope of an External Task, expressions have access to the <a class="javadocref" href="org/operaton/bpm/engine/externaltask/ExternalTask.html">ExternalTaskEntity</a> object via the key `externalTask` which provides getter methods for `errorMessage`, `errorDetails`, `workerId`, `retries` and more.

**Examples:**

How to access the External Task object:

```xml
<bpmn:serviceTask id="myExternalTaskId" name="myExternalTask" operaton:type="external" operaton:topic="myTopic">
  <bpmn:extensionElements>
    <operaton:errorEventDefinition id="myErrorEventDefinition" errorRef="myError" expression="${externalTask.getWorkerId() == 'myWorkerId'}" />
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

How to match an error message:

```xml
<bpmn:serviceTask id="myExternalTaskId" name="myExternalTask" operaton:type="external" operaton:topic="myTopic">
  <bpmn:extensionElements>
    <operaton:errorEventDefinition id="myErrorEventDefinition" errorRef="myError" expression="${externalTask.getErrorDetails().contains('myErrorMessage')}" />
  </bpmn:extensionElements>
</bpmn:serviceTask>
```

For further details on the functionality of error event definitions in the context of external tasks, consult the [External Tasks Guide](../process-engine/external-tasks.md#error-event-definitions).

## Value

Different BPMN and CMMN elements allow to specify their content or an attribute value by an
expression. Please see the corresponding sections for [BPMN][] and [CMMN][] in the references
for more detailed examples.


# Availability of Variables and Functions Inside Expression Language

## Process Variables

All process variables of the current scope are directly available inside an expression. So a
conditional sequence flow can directly check a variable value:

```xml
  <sequenceFlow>
    <conditionExpression xsi:type="tFormalExpression">
      ```${test == 'start'}
    </conditionExpression>
  </sequenceFlow>
```

## Internal Context Variables

Depending on the current execution context, special built-in context variables are available while
evaluating expressions:

<table class="table">
  <thead>
    <tr>
      <th>Variable</th>
      <th>Java Type</th>
      <th>Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>execution</code></td>
      <td><code><a class="javadocref" href="org/operaton/bpm/engine/delegate/DelegateExecution.html">DelegateExecution</a></code></td>
      <td>
        Available in a BPMN execution context like a service task, execution listener or sequence
        flow.
      </td>
    </tr>
    <tr>
      <td><code>task</code></td>
      <td><code><a class="javadocref" href="org/operaton/bpm/engine/delegate/DelegateTask.html">DelegateTask</a></code></td>
      <td>Available in a task context like a task listener.</td>
    </tr>
    <tr>
      <td><code>externalTask</code></td>
      <td><code><a class="javadocref" href="org/operaton/bpm/engine/externaltask/ExternalTask.html">ExternalTask</a></code></td>
      <td>Available during an external task context activity (e.g. in <a href="../../reference/bpmn20/custom-extensions/extension-elements.md#erroreventdefinition">operaton:errorEventDefinition</a> expressions).</td>
    </tr>
    <tr>
      <td><code>caseExecution</code></td>
      <td><code><a class="javadocref" href="org/operaton/bpm/engine/delegate/DelegateCaseExecution.html">DelegateCaseExecution</a></code></td>
      <td>Available in a CMMN execution context.</td>
    </tr>
    <tr>
      <td><code>authenticatedUserId</code></td>
      <td><code>String</code></td>
      <td>
        The id of the currently authenticated user. Only returns a value if the id of the currently
        authenticated user has been set through the corresponding methods of the
        <code>IdentityService</code>. Otherwise it returns <code>null</code>.
      </td>
    </tr>
  </tbody>
</table>

The following example shows an expression which sets the variable `test` to the current
event name of an execution listener.

```xml
  <operaton:executionListener event="start"
    expression="${execution.setVariable('test', execution.eventName)}" />
```


## External Context Variables With Spring and CDI

If the process engine is integrated with Spring or CDI, it is possible to access Spring and CDI
beans inside of expressions. Please see the corresponding sections for [Spring][] and [CDI][]
for more information. The following example shows the usage of a bean which implements the
`JavaDelegate` interface as delegateExecution.

```xml
  <serviceTask id="task1" operaton:delegateExpression="${myBean}" />
```

With the expression attribute any method of a bean can be called.

```xml
  <serviceTask id="task2" operaton:expression="${myBean.myMethod(execution)}" />
```


## Internal Context Functions

Special built-in context functions are available while evaluating expressions:

<table class="table">
  <thead>
    <tr>
      <th>Function</th>
      <th>Return Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>currentUser()</code></td>
      <td><code>String</code></td>
      <td>
        Returns the user id of the currently authenticated user or <code>null</code> no user is authenticated at the moment.
      </td>
    </tr>
    <tr>
      <td><code>currentUserGroups()</code></td>
      <td><code>List of Strings</code></td>
      <td>
        Returns a list of the group ids of the currently authenticated user or <code>null</code> if no user is authorized at the moment.
      </td>
    </tr>
    <tr>
      <td><code>now()</code></td>
      <td><code>Date</code></td>
      <td>Returns the current date as a Java Date object.</td>
    </tr>
    <tr>
      <td><code>dateTime()</code></td>
      <td><code>DateTime</code></td>
      <td>
        Returns a Joda-Time DateTime object of the current date. Please see the
        <a href="http://joda-time.sourceforge.net/api-release/org/joda/time/DateTime.html">Joda-Time</a>
        documentation for all available functions.
      </td>
    </tr>
  </tbody>
</table>

The following example sets the due date of a user task to the date 3 days after the creation
of the task.

```xml
<userTask id="theTask" name="Important task" operaton:dueDate="${dateTime().plusDays(3).toDate()}"/>
```


## Built-In Operaton Spin Functions

If the Operaton Spin process engine plugin is activated, the Spin functions `S`,
`XML` and `JSON` are also available inside of an expression. See the [Data Formats section][spin-section] for a detailed explanation.

```xml
  <serviceTask id="task" operaton:expression="${XML(xml).attr('test').value()}" resultVariable="test" />
```


[JakartaEL](https://jakarta.ee/specifications/expression-language/4.0/)
[JUEL](http://juel.sourceforge.net/)
[official documentation](https://jakarta.ee/specifications/expression-language/4.0/jakarta-expression-language-spec-4.0.html)
[variables](#availability-of-variables-and-functions-inside-expression-language)
[Spring](../spring-framework-integration/index.md#expression-resolving)
[CDI](../cdi-java-ee-integration/expression-resolving.md)
[BPMN](../../reference/bpmn20/index.md)
[CMMN](../../reference/cmmn11/index.md)
[spin-section](../data-formats/index.md)
