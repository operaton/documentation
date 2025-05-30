---

title: 'Extension Attributes'
sidebar_position: 20

---

The following attributes are extension attributes for the `camunda` namespace `http://operaton.org/schema/1.0/bpmn`.

# assignee

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a human performer of a <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a performer as <code>java.lang.String</code> or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${initiator```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# asyncAfter

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      Specifies an asynchronous continuation after an activity, see <a href="../user-guide/process-engine/transactions-in-processes.md#asynchronous-continuations">Asynchronous Continuations</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Boolean</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>true</code>, <code>false</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>false</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/start-events.md">Start Events</a>,
      <a href="../reference/bpmn20/events/index.md">End Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Throw Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Catch Events</a>,

      Task,
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>,
      <a href="../reference/bpmn20/tasks/receive-task.md">Receive Task</a>,
      <a href="../reference/bpmn20/tasks/manual-task.md">Manual Task</a>,

      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>,

      <a href="../reference/bpmn20/gateways/parallel-gateway.md">Parallel Gateway</a>,
      <a href="../reference/bpmn20/gateways/inclusive-gateway.md">Inclusive Gateway</a>,
      <a href="../reference/bpmn20/gateways/exclusive-gateway.md">Exclusive Gateway</a>,

      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a>,

      Boundary Event,
      <a href="../reference/bpmn20/events/message-events.md#message-boundary-event">Message Boundary Event</a>,
      <a href="../reference/bpmn20/events/error-events.md#error-boundary-event">Error Boundary Event</a>,
      <a href="../reference/bpmn20/events/timer-events.md#timer-boundary-event">Timer Boundary Event</a>,
      <a href="../reference/bpmn20/events/escalation-events.md#escalation-boundary-event">Escalation Boundary Event</a>,
      <a href="../reference/bpmn20/events/conditional-events.md#conditional-boundary-event">Conditional Boundary Event</a>,
      <a href="../reference/bpmn20/events/signal-events.md#signal-boundary-event">Signal Boundary Event</a>,
      <a href="../reference/bpmn20/events/cancel-and-compensation-events.md#cancel-boundary-event">Cancel Boundary Event</a>
    </td>
  </tr>
</table>

# asyncBefore

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      Specifies an asynchronous continuation before an activity, see <a href="../user-guide/process-engine/transactions-in-processes.md#asynchronous-continuations">Asynchronous Continuations</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Boolean</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>true</code>, <code>false</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>false</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/start-events.md">Start Events</a>,
      <a href="../reference/bpmn20/events/index.md">End Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Throw Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Catch Events</a>,

      Task,
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>,
      <a href="../reference/bpmn20/tasks/receive-task.md">Receive Task</a>,
      <a href="../reference/bpmn20/tasks/manual-task.md">Manual Task</a>,

      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>,

      <a href="../reference/bpmn20/gateways/parallel-gateway.md">Parallel Gateway</a>,
      <a href="../reference/bpmn20/gateways/event-based-gateway.md">Event Based Gateway</a>,
      <a href="../reference/bpmn20/gateways/inclusive-gateway.md">Inclusive Gateway</a>,
      <a href="../reference/bpmn20/gateways/exclusive-gateway.md">Exclusive Gateway</a>,

      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a>,

      Boundary Event,
      <a href="../reference/bpmn20/events/message-events.md#message-boundary-event">Message Boundary Event</a>,
      <a href="../reference/bpmn20/events/error-events.md#error-boundary-event">Error Boundary Event</a>,
      <a href="../reference/bpmn20/events/timer-events.md#timer-boundary-event">Timer Boundary Event</a>,
      <a href="../reference/bpmn20/events/escalation-events.md#escalation-boundary-event">Escalation Boundary Event</a>,
      <a href="../reference/bpmn20/events/conditional-events.md#conditional-boundary-event">Conditional Boundary Event</a>,
      <a href="../reference/bpmn20/events/signal-events.md#signal-boundary-event">Signal Boundary Event</a>,
      <a href="../reference/bpmn20/events/cancel-and-compensation-events.md#cancel-boundary-event">Cancel Boundary Event</a>
    </td>
  </tr>
</table>

# calledElementBinding

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which process definition version of the subprocess the call activity calls.
      If the value is <code>version</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementversion">operaton:calledElementVersion</a> is required.
      If the value is <code>versionTag</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementversiontag">operaton:calledElementVersionTag</a> is required.
      See <a href="../reference/bpmn20/subprocesses/call-activity.md#calledelement-binding">Called Element Binding</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>latest</code>, <code>deployment</code>, <code>version</code>, <code>versionTag</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>latest</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# calledElementVersion

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which process definition version of the subprocess the call activity calls if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementbinding">operaton:calledElementBinding</a>
      is set to <code>version</code>, see <a href="../reference/bpmn20/subprocesses/call-activity.md#calledelement-binding">Called Element Binding</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Integer</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete version of all deployed version numbers of the subprocess to call as <code>java.lang.Integer</code> or an expression which evaluates to a <code>java.lang.Integer</code> e.g., ```${versionToCall```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# calledElementVersionTag

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which process definition version tag of the subprocess the call activity calls if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#calledelementbinding">operaton:calledElementBinding</a>
      is set to <code>versionTag</code>, see <a href="../reference/bpmn20/subprocesses/call-activity.md#calledelement-binding">Called Element Binding</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete version tag of all deployed version numbers of the subprocess to call as <code>java.lang.String</code> or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${versionTagToCall```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# calledElementTenantId

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the tenant id of the process definition which is to be resolved by a call activity, see <a href="../reference/bpmn20/subprocesses/call-activity.md#calledelement-tenant-id">Called Element Tenant Id</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete tenant id or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${execution.tenantId```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# candidateGroups

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which group(s) will be candidate for performing the <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Comma separated list of group ids as <code>java.lang.String</code> or expressions that evaluate to a <code>java.lang.String</code> or a <code>java.util.Collection</code> of <code>java.lang.String</code>, e.g., <code>management</code> or management, ```${accountancyGroupId()}```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# candidateStarterGroups

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which group(s) will be able to start the process.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Comma separated list of group ids as <code>java.lang.String</code> or expressions that evaluate to a <code>java.lang.String</code> or a <code>java.util.Collection</code> of <code>java.lang.String</code>, e.g., <code>management</code> or management, ```${accountancyGroupId()}```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Process
    </td>
  </tr>
</table>

# candidateStarterUsers

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which user(s) will be able to start the process.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Comma separated list of user ids as <code>java.lang.String</code> or expressions that evaluate to a <code>java.lang.String</code> or a <code>java.util.Collection</code> of <code>java.lang.String</code>, e.g., <code>kermit, gonzo</code> or ```${ldapService.findAllSales()}```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Process
    </td>
  </tr>
</table>

# candidateUsers

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which user(s) will be candidate for performing the <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Comma separated list of user ids as <code>java.lang.String</code> or expressions that evaluate to a <code>java.lang.String</code> or a <code>java.util.Collection</code> of <code>java.lang.String</code>, e.g., <code>kermit, gonzo</code> or ```${ldapService.findAllSales()}```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# caseBinding

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which case definition version of the subcase the call activity calls.
      If the value is <code>version</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#caseversion">operaton:caseVersion</a>
      is required, see <a href="../reference/bpmn20/subprocesses/call-activity.md#create-a-case-instance">Case Binding</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>latest</code>, <code>deployment</code>, <code>version</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md#create-a-case-instance">Call Activity</a>
    </td>
  </tr>
</table>

# caseRef

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute references a case definition by its key to call.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md#create-a-case-instance">Call Activity</a>
    </td>
  </tr>
</table>

# caseVersion

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which case definition version of the subcase the call activity calls if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#casebinding">operaton:caseBinding</a> is set to <code>version</code>, see <a href="../reference/bpmn20/subprocesses/call-activity.md#create-a-case-instance">Case Binding</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Integer</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      All deployed version numbers of the subprocess to call
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md#create-a-case-instance">Call Activity</a>
    </td>
  </tr>
</table>

# caseTenantId

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the tenant id of the case definition which is to be resolved by a call activity, see <a href="../reference/bpmn20/subprocesses/call-activity.md#case-tenant-id">Case  Tenant Id</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete tenant id or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${execution.tenantId```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# class

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which Java class will be executed at runtime. The stated class must implement a <a href="../user-guide/process-engine/delegation-code.md#java-delegate">Java delegate</a> interface.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Fully qualified Java class name of a class which implements a <a href="../user-guide/process-engine/delegation-code.md#java-delegate">Java Delegate</a> interface, e.g., <code>org.operaton.bpm.MyJavaDelegate</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      Message Event Definition of <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a> or <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#tasklistener">operaton:taskListener</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#executionlistener">operaton:executionListner</a>
    </td>
  </tr>
</table>

# collection

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a collection, where an instance will be created for each element, see <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multiple Instance</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a <code>java.util.Collection</code> process variable as <code>java.lang.String</code> or an Expression which evaluates to the name of a collection
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a> of Task,
      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>
    </td>
  </tr>
</table>

# decisionRef

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute references a decision definition to evalute by its key.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A String or an expression which evalutes to the key of a decision definition which should be evaluated by this task, e.g., <code>myDecisionDefinitionKey</code> or ```${decisionKey```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# decisionRefBinding

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which decision definition version the task evaluates.
      If the value is <code>version</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefversion">operaton:decisionRefVersion</a>
      is required.
      If the value is <code>versionTag</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefversiontag">operaton:decisionRefVersionTag</a>
      is required.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>latest</code>, <code>deployment</code>, <code>version</code>, <code>versionTag</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>latest</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# decisionRefVersion

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which decision definition version the task evaluates if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefbinding">operaton:decisionRefBinding</a>
      is set to <code>version</code>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Integer</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete version of all deployed version numbers of the decision to call as <code>java.lang.Integer</code> or an expression which evaluates to a <code>java.lang.Integer</code> e.g., ```${versionToCall```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# decisionRefVersionTag

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which decision definition version tag the task evaluates if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#decisionrefbinding">operaton:decisionRefBinding</a>
      is set to <code>versionTag</code>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete version tag of all deployed version tags of the decision to call as <code>java.lang.String</code> or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${versionTagToCall```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# decisionRefTenantId

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the tenant id of the decision definition which is to be resolved by a business rule task, see <a href="../reference/bpmn20/tasks/business-rule-task.md#decisionref-tenant-id">DecisionRef Tenant Id</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete tenant id or an expression which evaluates to a <code>java.lang.String</code> e.g., ```${execution.tenantId```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# delegateExpression

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute allows specification of an expression which must resolve to an object that implements the corresponding interface (see <a href="../user-guide/process-engine/delegation-code.md">delegation code</a>).
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Expression which evaluates to a Java class implementing a <a href="../user-guide/process-engine/delegation-code.md">delegation</a> interface, e.g., ```${myJavaDelegate``` or ```#{myTaskListener```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      Message Event Definition of <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a> or <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#tasklistener">operaton:taskListener</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#executionlistener">operaton:executionListner</a>
    </td>
  </tr>
</table>

# dueDate

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the initial due date of a <a href="../reference/bpmn20/tasks/user-task.md">User Task</a> when it is created.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      An expression which evaluates to a <code>java.util.Date</code>, <code>java.util.String</code> (<a href="http://en.wikipedia.org/wiki/ISO_8601">ISO 8601</a> formatted) or <code>null</code>, e.g., ```${dateVariable```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# elementVariable

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the process variable which will be set on each created instance, containing an element of the specified collection see
      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multiple Instance</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable as <code>java.lang.String</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a> of Task,
      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>
    </td>
  </tr>
</table>

# errorMessage

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a message to give further information about the error. When an error start event or boudary event catches the error the message will be saved as process variable if `errorMessageVariable` is configured. See <a href="../reference/bpmn20/events/error-events.md">Error Events</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The error message as<code>java.lang.String</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/error-events.md">Error</a>
    </td>
  </tr>
</table>

# errorCodeVariable

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a process variable that holds the error code and the errorCodevariable will be set if an error has been received by the error start or boundary event, see <a href="../reference/bpmn20/events/error-events.md">Error Events</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable as <code>java.lang.String</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/error-events.md">Error Events</a>
    </td>
  </tr>
</table>

# errorMessageVariable

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a process variable that holds the error message and the errorMessageVariable will be set if an error has been received by the error start or boundary event, see <a href="../reference/bpmn20/events/error-events.md">Error Events</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable as <code>java.lang.String</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/error-events.md">Error Events</a>
    </td>
  </tr>
</table>

# escalationCodeVariable

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a process variable which will be set if an escalation has been received by an escalation start or boundary event, see <a href="../reference/bpmn20/events/escalation-events.md">Escalation Events</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable as <code>java.lang.String</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/escalation-events.md">Escalation Events</a>
    </td>
  </tr>
</table>

# exclusive

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies that jobs should be executed exclusively. See <a href="../user-guide/process-engine/the-job-executor.md#exclusive-jobs">Exclusive Jobs</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Boolean</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>true</code>, <code>false</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>true</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/start-events.md">Start Events</a>,
      <a href="../reference/bpmn20/events/index.md">End Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Throw Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Catch Events</a>,

      Task,
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>,
      <a href="../reference/bpmn20/tasks/receive-task.md">Receive Task</a>,
      <a href="../reference/bpmn20/tasks/manual-task.md">Manual Task</a>,

      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>,

      <a href="../reference/bpmn20/gateways/parallel-gateway.md">Parallel Gateway</a>,
      <a href="../reference/bpmn20/gateways/event-based-gateway.md">Event Based Gateway</a>,
      <a href="../reference/bpmn20/gateways/inclusive-gateway.md">Inclusive Gateway</a>,
      <a href="../reference/bpmn20/gateways/exclusive-gateway.md">Exclusive Gateway</a>,

      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a>,

      Boundary Event,
      <a href="../reference/bpmn20/events/message-events.md#message-boundary-event">Message Boundary Event</a>,
      <a href="../reference/bpmn20/events/error-events.md#error-boundary-event">Error Boundary Event</a>,
      <a href="../reference/bpmn20/events/timer-events.md#timer-boundary-event">Timer Boundary Event</a>,
      <a href="../reference/bpmn20/events/escalation-events.md#escalation-boundary-event">Escalation Boundary Event</a>,
      <a href="../reference/bpmn20/events/conditional-events.md#conditional-boundary-event">Conditional Boundary Event</a>,
      <a href="../reference/bpmn20/events/signal-events.md#signal-boundary-event">Signal Boundary Event</a>,
      <a href="../reference/bpmn20/events/cancel-and-compensation-events.md#cancel-boundary-event">Cancel Boundary Event</a>
    </td>
  </tr>
</table>

# expression

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute defines an expression which will be evaluated at runtime.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Expression, e.g., ```${gender == 'male' ? 'Mr.' : 'Mrs.'``` or ```#{printer.printMessage()}```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      Message Event Definition of <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a> or <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#tasklistener">operaton:taskListener</a>,
      <a href="../reference/bpmn20/custom-extensions/extension-elements.md#executionlistener">operaton:executionListner</a>
    </td>
  </tr>
</table>

# followUpDate

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the initial follow-up date of a <a href="../reference/bpmn20/tasks/user-task.md">User Task</a> when it is created.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      An expression which evaluates to a <code>java.util.Date</code>, <code>java.util.String</code> (<a href="http://en.wikipedia.org/wiki/ISO_8601">ISO 8601</a> formatted) or <code>null</code>, e.g., ```${dateVariable```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# formHandlerClass

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the class that will be called during the parsing of the form information of a <a href="../reference/bpmn20/events/start-events.md">Start Event</a> or <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Fully qualified Java class name of a class which implements the <code>org.operaton.bpm.engine.impl.form.handler.StartFormHandler</code>
      or <code>org.operaton.bpm.engine.impl.form.handler.TaskFormHandler</code> interface, e.g., <code>org.operaton.bpm.MyUserTaskFormHandler</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Initial <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# formKey

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a form resource. See <a href="../user-guide/task-forms/index.md">task forms</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A <code>java.lang.String</code> of a form resource which can be evaluated by the <a href="../webapps/tasklist/index.md">Tasklist</a>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Initial <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# formRef

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute references a Operaton form definition by its key. See <a href="../user-guide/task-forms/index.md">task forms</a> for more information.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A <code>java.lang.String</code> or a <code>org.operaton.bpm.engine.delegate.Expression</code> which <a href="../webapps/tasklist/index.md">Tasklist</a> can evaluate to display the referenced Operaton Form, e.g., myOperatonFormDefinitionKey or ```${formKey}```.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Initial <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# formRefBinding

<table class="table table-striped">
  <tr>
    <th>Description</th>
      <td>
      The attribute specifies which Operaton form definition version the activity references. If the value is <code>version</code>, the attribute <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formrefversion">operaton:formRefVersion</a> is required.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
    <tr>
    <th>Possible Values</th>
    <td>
      <code>latest</code>, <code>deployment</code>, <code>version</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>latest</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Initial <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# formRefVersion

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which Operaton form definition version the activity references if the <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#formrefbinding">operaton:formRefBinding</a>
      is set to <code>version</code>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Integer</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A concrete version of all deployed version numbers of the Operaton form definition as <code>java.lang.Integer</code> or an expression which evaluates to a <code>java.lang.Integer</code> e.g., ```${versionToReference```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Initial <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# historyTimeToLive

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the history time to live (in days) for the process definition. It is used within <a href="../user-guide/process-engine/history/history-cleanup.md">History cleanup</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Integer</code> or <code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Any non-negative integer number or string containing a time in days defined by the ISO-8601 date format.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>null - means that process definition history won't ever be removed during history cleanup run</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Process
    </td>
  </tr>
</table>

# initiator

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies a process variable in which the user id of the process initiator is set.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A process variable name to save the process initiator
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/start-events.md">Start Event</a> of a Process
    </td>
  </tr>
</table>

# isStartableInTasklist

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies whether the process is startable in Tasklist or not.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.Boolean</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td><code>true</code>, <code>false</code></td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td><code>true</code></td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>Process</td>
  </tr>
</table>

# jobPriority

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      Specifies the priority a job receives that is created in the context of executing the given process element (e.g., a timer event, or in the case of <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncbefore">asyncBefore</a> and <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#asyncafter">asyncAfter</a>). See the user guide on <a href="../user-guide/process-engine/the-job-executor.md#job-prioritization">Job Prioritization</a> for details.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td>A number in the range of a Java <code>long</code> value or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      An expression must resolve to a valid Java <code>long</code> value.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>none</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/start-events.md">Start Events</a>,
      <a href="../reference/bpmn20/events/index.md">End Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Throw Events</a>,
      <a href="../reference/bpmn20/events/index.md">Intermediate Catch Events</a>,

      Task,
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>,
      <a href="../reference/bpmn20/tasks/receive-task.md">Receive Task</a>,
      <a href="../reference/bpmn20/tasks/manual-task.md">Manual Task</a>,

      <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">Embedded Subprocess</a>,
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>,
      <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">Transaction Subprocess</a>,

      <a href="../reference/bpmn20/gateways/parallel-gateway.md">Parallel Gateway</a>,
      <a href="../reference/bpmn20/gateways/inclusive-gateway.md">Inclusive Gateway</a>,
      <a href="../reference/bpmn20/gateways/exclusive-gateway.md">Exclusive Gateway</a>,

      <a href="../reference/bpmn20/tasks/task-markers.md#multiple-instance">Multi Instance Loop Characteristics</a>,

      Process
    </td>
  </tr>
</table>

# mapDecisionResult

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute references which <a href="../user-guide/process-engine/decisions/bpmn-cmmn.md#predefined-mapping-of-the-decision-result">built-in Decision Result Mapper</a> is used to pass the result of an evaluated decision to a process variable. It should be used in combination with <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#resultvariable">operaton:resultVariable</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      singleEntry, singleResult, collectEntries, resultList
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>resultList</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>
    </td>
  </tr>
</table>

# priority

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the initial priority of a <a href="../reference/bpmn20/tasks/user-task.md">User Task</a> when it is created.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      An expression which evaluates to a <code>java.lang.Number</code> or a <code>java.lang.String</code> which represents a number or <code>null</code>, e.g., ```${dateVariable```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/user-task.md">User Task</a>
    </td>
  </tr>
</table>

# taskPriority

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the initial priority of an <a href="../reference/bpmn20/tasks/service-task.md#external-tasks">External Task</a> when it is created.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td>A number in the range of a Java <code>long</code> value or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      An expression must resolve to a valid Java <code>long</code> value.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>0</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
	  <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md#implementing-as-an-external-task">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      Process
    </td>
  </tr>
</table>

# resource

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies an external resource. The resource can be part of the deployment or
      exists in the classpath. To specify the type of resource, a URL scheme like prefix
      <code>deployment://</code> resp. <code>classpath://</code> can be supplied. If the scheme is
      omitted, it is assumed that the resource exists in the classpath.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The path to a resource or an expression which returns the path. Optional the path can
      start with an URL like scheme <code>classpath://</code> or <code>deployment://</code> to
      specify where to find the resource. If omitted the resource is assumed to exists in the
      classpath.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>
    </td>
  </tr>
</table>


# resultVariable

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      <p>
      The attribute specifies the process variable to save the return value of a <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#expression">operaton:expression</a>.
      </p>
      <p>Note that when you use <code>operaton:resultVariable</code> in a multi-instance construct, for example in a multi-instance subprocess, the result variable is overwritten every time the task completes, unless the variable is a <a href="../user-guide/process-engine/variables.md#variable-scopes-and-variable-visibility">local variable</a> in the scope of the multi-instance construct. This can lead to seemingly random behavior.</p>
      <p>
        This is a known issue. As a workaround, a local variable can be declared by adding an <a href="../user-guide/process-engine/delegation-code.md#execution-listener">execution listener</a> to the subprocess' start event that initializes the variable as <code>null</code>.
      </p>
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable to save the return value
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/script-task.md">Script Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>,
      Message Event Definition of <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a> or <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
    </td>
  </tr>
</table>

# versionTag

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      <p>
      The attribute specifies a version tag for the process definition.
      </p>
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Any value that has a meaning as version tag for the process definition.
      <strong>Note:</strong> Sorting by versionTag is string based. The version will not be interpreted. As an example, the sorting could return v0.1.0, v0.10.0, v0.2.0.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      Process
    </td>
  </tr>
</table>

# topic

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies the topic of an external task instance. The task is going to be offered to workers polling for that topic. It is only relevant when <a href="../reference/bpmn20/custom-extensions/extension-attributes.md#type">operaton:type</a> is set to <code>external</code>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code> or <code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Any value that has a meaning as a topic identifier as <code>java.lang.String</code> or an expression which evaluates to a <code>java.lang.String</code>, e.g. ```${topicName```
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
	  <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md#implementing-as-an-external-task">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>
    </td>
  </tr>
</table>


# type

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which built-in task implementation to use. Currently an email, a shell service, and an external task exists.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      <code>external</code>, <code>mail</code>, <code>shell</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/tasks/service-task.md">Service Task</a>,
	  <a href="../reference/bpmn20/events/message-events.md#message-end-event">Message End Event</a>,
      <a href="../reference/bpmn20/events/message-events.md#message-intermediate-throwing-event">Message Intermediate Throwing Event</a>,
      <a href="../reference/bpmn20/tasks/business-rule-task.md#implementing-as-an-external-task">Business Rule Task</a>,
      <a href="../reference/bpmn20/tasks/send-task.md">Send Task</a>
    </td>
  </tr>
</table>

# variableMappingClass

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute specifies which Java class will be executed at runtime to map the input and output variables for a call activity.
      The stated class must implement the <a href="../user-guide/process-engine/delegation-code.md#delegate-variable-mapping">Delegate Variable Mapping</a> interface.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Fully qualified Java class name of a class which implements the <a href="../user-guide/process-engine/delegation-code.md#delegate-variable-mapping">Delegate Variable Mapping</a> interface, e.g., <code>org.operaton.bpm.MyVariableMappingDelegate</code>
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>


# variableMappingDelegateExpression

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute allows specification of an expression which must resolve to an object that implements the corresponding interface <a href="../user-guide/process-engine/delegation-code.md#delegate-variable-mapping">Delegate Variable Mapping</a>.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>org.operaton.bpm.engine.delegate.Expression</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      Expression which evaluates to a Java class that implements the <a href="../user-guide/process-engine/delegation-code.md#delegate-variable-mapping">Delegate Variable Mapping</a> interface, e.g., ```${myVariableMapping```.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/subprocesses/call-activity.md">Call Activity</a>
    </td>
  </tr>
</table>

# variableName

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute allows to specify a variable name on which a condition of a conditional event should be evaluated exclusively.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      The name of a process variable on which a condition should be evaluated after a change happens.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/conditional-events.md">Conditional Event</a>
    </td>
  </tr>
</table>

# variableEvents

<table class="table table-striped">
  <tr>
    <th>Description</th>
    <td>
      The attribute allows to specify a comma separated list of variable change events.
      These events specify the variable change events on which a condition of a conditional event should be evaluated exclusively.
    </td>
  </tr>
  <tr>
    <th>Type</th>
    <td><code>java.lang.String</code></td>
  </tr>
  <tr>
    <th>Possible Values</th>
    <td>
      A comma separated list of variable change events. Variable change events are: create, update and delete.
    </td>
  </tr>
  <tr>
    <th>Default Value</th>
    <td>&ndash;</td>
  </tr>
  <tr>
    <th>BPMN 2.0 Elements</th>
    <td>
      <a href="../reference/bpmn20/events/conditional-events.md">Conditional Event</a>
    </td>
  </tr>
</table>
