---

title: 'Script Task'
sidebar_position: 50

menu:
  main:
    identifier: "bpmn-ref-tasks-script-task"
    parent: "bpmn-ref-tasks"
    description: "Execute a Script."

---

A Script Task is an automated activity. When a process execution arrives at the Script Task, the corresponding script is executed.

A Script Task is defined by specifying the script and the scriptFormat.

```xml
<scriptTask id="theScriptTask" name="Execute script" scriptFormat="groovy">
  <script>
    sum = 0
    for ( i in inputArray ) {
      sum += i
    }
  </script>
</scriptTask>
```

The value of the scriptFormat attribute must be a name that is compatible with JSR-223 (Scripting
for the Java Platform). If you want to use a (JSR-223 compatible) scripting engine, you need to to
add the corresponding jar to the classpath and use the appropriate name.

The script source code has to be added as the text content of the `script` child element.
Alternatively, the source code can be specified as an expression or external resource. For more
information on the possible ways of providing the script source code please see the corresponding
 [section][script-source] of the [User Guide][user-guide].

For general information about scripting in the process engine, please see the [Scripting](../../../user-guide/process-engine/scripting.md) section of the [User Guide][user-guide].

:::note[Supported Script Languages]

Operaton should work with most of the JSR-223 compatible script engine implementations. We test integration for Groovy, JavaScript, JRuby and Jython. See the <a href="../introduction/third-party-libraries/index.md#process-engine">Third Party Dependencies</a> section of the <a href="../user-guide/index.md">User Guide</a> for more details.

:::

## Variables in Scripts

All process variables that are accessible through the execution that arrives in the Script Task can be used within the script. In the example below, the script variable `inputArray` is in fact a process variable (an array of integers).

```xml
<script>
    sum = 0
    for ( i in inputArray ) {
      sum += i
    }
</script>
```

It's also possible to set process variables in a script. Variables can be set by using the `setVariable(...)` methods provided by the `VariableScope` interface:


```xml
<script>
    sum = 0
    for ( i in inputArray ) {
      sum += i
    }
    execution.setVariable("sum", sum);
</script>
```

### Enabling auto-storing of Script Variables

By setting the property `autoStoreScriptVariables` to `true` in the process engine configuration, the process engine will automatically store all _global_ script variables as process variables. This was the default behavior in Operaton.0 and 7.1 but it only reliably works for the Groovy scripting language (see the [Set autoStoreScriptVariables][autostore-variables] section of the [Migration Guide](../../../update/index.md) for more information).

To use this feature, you have to

* set `autoStoreScriptVariables` to `true` in the process engine configuration
* prefix all script variables that should not be stored as script variables using the `def` keyword: `def sum = 0`. In this case the variable `sum` will not be stored as process variable.

:::note[Groovy-Support only]
The configuration flag <code>autoStoreScriptVariables</code> is only supported for Groovy Script Tasks. If enabled for other script languages,
it is not guaranteed which variables will be exported by the script engine. For
example, Ruby will not export any of the script variables at all.
:::

Note: the following names are reserved and cannot be used as variable names:
`out`, `out:print`, `lang:import`, `context`, `elcontext`.


## Script Results

The return value of a Script Task can be assigned to a previously existing or to a new process variable by specifying the process variable name as a literal value for the `operaton:resultVariable` attribute of a Script Task definition. Any existing value for a specific process variable will be overwritten by the result value of the script execution. When a result variable name is not specified, the script result value gets ignored.

```xml
<scriptTask id="theScriptTask" name="Execute script" scriptFormat="juel" operaton:resultVariable="myVar">
  <script>#{echo}</script>
</scriptTask>
```

In the above example, the result of the script execution (the value of the resolved expression `#{echo}`) is set to the process variable named `myVar` after the script completes.

:::note[Result variables and multi-instance]
Note that when you use <code>operaton:resultVariable</code> in a multi-instance construct, for example in a multi-instance subprocess, the result variable is overwritten every time the task completes, which may appear as random behavior. See <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resultvariable">operaton:resultVariable</a> for details.
:::


## Operaton Extensions

<table class="table table-striped">
  <tr>
    <th>Attributes</th>
    <td>
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">operaton:asyncBefore</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">operaton:asyncAfter</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#exclusive">operaton:exclusive</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#jobpriority">operaton:jobPriority</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resultvariable">operaton:resultVariable</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resource">operaton:resource</a>
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


[script-source]: ../../../user-guide/process-engine/scripting.md#script-source
[user-guide]: ../../../user-guide/index.md
<!-- [autostore-variables]: ../../../update/minor/71-to-72/index.md#script-variable-storing -->
