---

title: 'BPMN 2.0'
sidebar_position: 20

---

This page gives you an overview of the BPMN 2.0 elements and the current coverage of the process engine.

:::note[BPMN - Business Process Model and Notation]
If you are unfamiliar with BPMN 2.0, you might want to check out the
<a href="http://operaton.org/bpmn/tutorial.html">BPMN Tutorial</a> first.
:::

## Coverage

The elements marked in <span class="label label-warning label-implemented">orange</span> are supported.

### Symbols


<div class="bpmn-symbols" style={{border: '0px solid #000', paddingLeft: '16px'}}>

  <div class="row">
    <div class="col-md-12">
      <h3>Participants</h3>
      <div style={{position: 'relative'}}>
        <div class="bpmn-symbol-container implemented">
            ![Pool Symbol](/img/documentation/reference/bpmn20/pool.svg)
        </div>
        <div style={{position: 'absolute', top: '0', left: '24px', zIndex: '2'}} class="bpmn-symbol-container implemented">
        ![Lane Symbol](/img/documentation/reference/bpmn20/lane.svg)
        </div>
      </div>
    </div>
  </div>  
  <!-- Subprocesses -->
  <div class="row" style={{display:'flex', flexDirection: 'column'}}>
    <h3>Subprocesses</h3>
    <div class="col-md-12" style={{display:'flex', columnGap: '15px'}}>
      <div class="bpmn-symbol-container implemented">
        ![Subprocess Symbol](/img/documentation/reference/bpmn20/subprocess.svg)
        <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![CallActivity Symbol](/img/documentation/reference/bpmn20/call_activity.svg)
        <a href="../reference/bpmn20/subprocesses/call-activity.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Event Subprocess Symbol](/img/documentation/reference/bpmn20/event_subprocess.svg)
        <a href="../reference/bpmn20/subprocesses/event-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Transaction Symbol](/img/documentation/reference/bpmn20/transaction.svg)
        <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
    </div>
  </div>        

  <!-- Tasks -->
  <div class="row" style={{display:'flex', flexDirection: 'column'}}>
    <h3>Tasks</h3>
    <div class="col-md-12" style={{display:'flex', flexWrap: 'wrap', columnGap: '15px'}}>
      
      <div class="bpmn-symbol-container implemented">
        ![ServiceTask Symbol](/img/documentation/reference/bpmn20/service_task.svg)
        <a href="../reference/bpmn20/tasks/service-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![UserTask Symbol](/img/documentation/reference/bpmn20/user_task.svg)
        <a href="../reference/bpmn20/tasks/user-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![ScriptTask Symbol](/img/documentation/reference/bpmn20/script_task.svg)
        <a href="../reference/bpmn20/tasks/script-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Business Rule Task Symbol](/img/documentation/reference/bpmn20/business_rule_task.svg)
        <a href="../reference/bpmn20/tasks/business-rule-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Manual Task Symbol](/img/documentation/reference/bpmn20/manual_task.svg)
        <a href="../reference/bpmn20/tasks/manual-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Receive Task Symbol](/img/documentation/reference/bpmn20/receive_task.svg)
        <a href="../reference/bpmn20/tasks/receive-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container">
        ![Undefined Task Symbol](/img/documentation/reference/bpmn20/undefined_task.svg)
      </div>
      <div class="bpmn-symbol-container implemented">
        ![Send Task Symbol](/img/documentation/reference/bpmn20/send_task.svg)
        <a href="../reference/bpmn20/tasks/send-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container">
        ![Instantiated Receive Task Symbol](/img/documentation/reference/bpmn20/instantiated_receive_task.svg)
      </div>
    </div>
  </div>

    <div class="row" style={{display:'flex', justifyContent: 'space-between'}}>
    <div class="col-md-6" style={{}}>
      <h3>Gateways</h3>
      <div style={{display:'flex'}}>
        <div class="bpmn-symbol-container implemented">
            ![XOR Gateway Symbol](/img/documentation/reference/bpmn20/xor_gateway.svg)
            <a href="../reference/bpmn20/gateways/exclusive-gateway.md">
            <span class="glyphicon glyphicon-eye-open"></span>
            </a>
        </div>
        <div class="bpmn-symbol-container implemented">
            ![OR Gateway Symbol](/img/documentation/reference/bpmn20/or_gateway.svg)
            <a href="../reference/bpmn20/gateways/inclusive-gateway.md">
            <span class="glyphicon glyphicon-eye-open"></span>
            </a>
        </div>
        <div class="bpmn-symbol-container implemented">
            ![AND Gateway Symbol](/img/documentation/reference/bpmn20/and_gateway.svg)
            <a href="../reference/bpmn20/gateways/parallel-gateway.md">
            <span class="glyphicon glyphicon-eye-open"></span>
            </a>
        </div>
        <div class="bpmn-symbol-container implemented">
            ![Event Gateway Symbol](/img/documentation/reference/bpmn20/event_gateway.svg)
            <a href="../reference/bpmn20/gateways/event-based-gateway.md">
            <span class="glyphicon glyphicon-eye-open"></span>
            </a>
        </div>
        <div class="bpmn-symbol-container">
            ![Complex Gateway Symbol](/img/documentation/reference/bpmn20/complex_gateway.svg)
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <h3>Data</h3>
      <div class="bpmn-symbol-container">
        ![Data Object Symbol](/img/documentation/reference/bpmn20/data_object.svg)
      </div>
      <div class="bpmn-symbol-container">
        ![Data Store Symbol](/img/documentation/reference/bpmn20/data_store.svg)
      </div>
    </div>
    <div class="col-md-3">
      <h3>Artifacts</h3>
      <div class="bpmn-symbol-container">
        ![Text Annotation Symbol](/img/documentation/reference/bpmn20/text_annotation.svg)
      </div>
      <div class="bpmn-symbol-container">
        ![Group Symbol](/img/documentation/reference/bpmn20/group_symbol.svg)
      </div>
    </div>
  </div>
</div>

### Events

In BPMN there are start events, intermediate events and end events. These three event types can be catching events or throwing events. Intermediate events can be used as boundary events on tasks, in which case they can be interrupting or non-interrupting. This gives you a lot of flexibility to use events in your processes.

:::note[Understanding BPMN Events]
To help understand the principle behavior of events in BPMN, we recommend to check the
[Events: Basic Concepts](http://operaton.org/bpmn/reference.html#events-basic-concepts)
chapter of the [BPMN Modeling Reference](http://operaton.org/bpmn/reference.html).
:::

<table class="table table-responsive table-bordered bpmn-events" style={{width: '100%', fontSize:'13px'}}>
  <thead>
    <tr>
      <th>Type</th>
      <th colSpan="3" style={{textAlign:'center'}}>Start</th>
      <th colSpan="4" style={{textAlign:'center'}}>Intermediate</th>
      <th>End</th>
    </tr>
    <tr>
      <th></th>
      <th>Normal</th>
      <th>Event Subprocess</th>
      <th>
        Event Subprocess<br/>
        non-interrupt
      </th>
      <th>catch</th>
      <th>boundary</th>
      <th>
        boundary<br/>
        non-interrupt
      </th>
      <th>throw</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/none-events.md">None</a></td>
      <td>
        ![Non Start Event Symbol](/img/documentation/reference/bpmn20/none_start_event.svg)
      </td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
        ![Non Intermediate Event Symbol](/img/documentation/reference/bpmn20/none_intermediate_event.svg)
      </td>
      <td>
        ![Non End Event Symbol](/img/documentation/reference/bpmn20/none_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/message-events.md">Message</a></td>
      <td>
        ![Message Start Event Symbol](/img/documentation/reference/bpmn20/message_start_event.svg)
      </td>
      <td>
        ![Message Start Event Symbol](./img/symbols/events/message_start_event.svg)
      </td>
      <td>
        ![Event Subprocess Message Start Event non-interrupting Symbol](/img/documentation/reference/bpmn20/event_subprocess_message_non_interrupting.svg)
      </td>
      <td>
        ![Message Intermediate Catch Event Symbol](/img/documentation/reference/bpmn20/message_intermediate_catch_event.svg)
      </td>
      <td>
        ![Message Intermediate Catch Event Symbol](./img/symbols/events/message_intermediate_catch_event.svg)
      </td>
      <td>
        ![Message Intermediate Non Interrupting Catch Event Symbol](/img/documentation/reference/bpmn20/message_intermediate_non_interrupting_catch_event.svg)
      </td>
      <td>
        ![Message Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/message_intermediate_throw_event.svg)
      </td>
      <td>
        ![Message Throw End Event Symbol](/img/documentation/reference/bpmn20/message_throw_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
        <td><a href="../reference/bpmn20/events/timer-events.md">Timer</a></td>
        <td>
            ![Timer Start Event Symbol](/img/documentation/reference/bpmn20/timer_start_event.svg)
        </td>
        <td>
            ![Event Subprocess Timer Start Event Symbol](./img/symbols/events/timer_start_event.svg)
        </td>
        <td>
            ![Event Subprocess Timer Start Event Non Interrupting Symbol](/img/documentation/reference/bpmn20/event_subprocess_timer_non_interrupting.svg)
      </td>
      <td>
            ![Timer Intermediate Interrupting Event Symbol](/img/documentation/reference/bpmn20/timer_intermediate_event.svg)
      </td>
      <td>
            ![Timer Intermediate Interrupting Event Symbol](./img/symbols/events/timer_intermediate_event.svg)
      </td>
      <td>
            ![Timer Intermediate None Interrupting Event Symbol](/img/documentation/reference/bpmn20/timer_intermediate_none_interrupting_event.svg)
      </td>
      <td></td>
      <td></td>        
    </tr>
    <tr>
        <td><a href="../reference/bpmn20/events/conditional-events.md">Conditional</a></td>
        <td class="implemented">
            ![Conditional Start Event Symbol](/img/documentation/reference/bpmn20/conditional_start_event.svg)
        </td>
        <td class="implemented">
            ![Conditional Start Event Symbol](./img/symbols/events/conditional_start_event.svg)
        </td>   
        <td class="implemented">
            ![Conditional Event Subprocess Non Interrupting Start Event Symbol](/img/documentation/reference/bpmn20/event_subprocess_conditional_non_interrupting.svg)
        </td>
        <td class="implemented">
            ![Conditional Intermediate Catch Event Symbol](/img/documentation/reference/bpmn20/conditional_intermediate_catch_event.svg)
        </td>  
        <td class="implemented">
            ![Conditional Intermediate Catch Event Symbol](./img/symbols/events/conditional_intermediate_catch_event.svg)
        </td>  
        <td class="implemented">
            ![Conditional Intermediate Non Interrupting Event Symbol](/img/documentation/reference/bpmn20/conditional_intermediate_non_interrupting_event.svg)
        </td>
        <td></td>
        <td></td>       
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/link-events.md">Link</a></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
        ![Link Intermediate Catch Event Symbol](/img/documentation/reference/bpmn20/link_intermediate_catch_event.svg)
      </td>
      <td></td>
      <td></td>
      <td>
        ![Link Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/link_intermediate_throw_event.svg)
      </td>
      <td></td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/signal-events.md">Signal</a></td>
      <td>
        ![Signal Event Symbol](/img/documentation/reference/bpmn20/signal_start_event.svg)
      </td>
      <td>
        ![Signal Event Symbol](./img/symbols/events/signal_start_event.svg)
      </td>
      <td>
      ![Event Subprocess Signal Non Interrupting Start Event Symbol](/img/documentation/reference/bpmn20/event_subprocess_signal_non_interrupting_start_event.svg)
      </td>
      <td>
        ![Signal Intermediate Catch Event Symbol](/img/documentation/reference/bpmn20/signal_intermediate_catch_event.svg)
      </td>
      <td>
        ![Signal Intermediate Catch Event Symbol](./img/symbols/events/signal_intermediate_catch_event.svg)
      </td>
      <td>
        ![Signal Intermediate Non Interrupting Catch Event Symbol](/img/documentation/reference/bpmn20/signal_intermediate_non_interrupting_catch_event.svg)
      </td>
      <td>
        ![Signal Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/signal_intermediate_throw_event.svg)
      </td>
      <td>
        ![Signal Throw End Event Symbol](/img/documentation/reference/bpmn20/signal_throw_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/error-events.md">Error</a></td>
      <td></td>
      <td>
        ![Error EventSubprocess StartEvent Symbol](/img/documentation/reference/bpmn20/error_event_subprocess_start_event.svg)
      </td>
      <td></td>
      <td></td>
      <td>
        ![Error Boundary Catch Event Symbol](/img/documentation/reference/bpmn20/error_boundary_catch_event.svg)
      </td>
      <td></td>
      <td></td>
      <td>
        ![Error Throw End Event Symbol](/img/documentation/reference/bpmn20/error_throw_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/escalation-events.md">Escalation</a></td>
      <td></td>
      <td>
        ![Escalation Event Subprocess Start Event Symbol](/img/documentation/reference/bpmn20/escalation_event_subprocess_start_event.svg)
      </td>
      <td>
      ![Escalation Event Subprocess Non Interrupting Start Event Symbol](/img/documentation/reference/bpmn20/escalation_event_subprocess_non_interrupting_start_event.svg)
      </td>
      <td></td>
      <td>
        ![Escalation Boundary Catch Event Symbol](/img/documentation/reference/bpmn20/escalation_boundary_catch_event.svg)
      </td>
      <td>
        ![Escalation Boundary Catch Non Interrupting Event Symbol](/img/documentation/reference/bpmn20/escalation_boundary_catch_non_interrupting_event.svg)
      </td>
      <td>
        ![Escalation Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/escalation_intermediate_throw_event.svg)
      </td>
      <td>
        ![Escalation Throw End Event Symbol](/img/documentation/reference/bpmn20/escalation_throw_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/terminate-event.md">Termination</a></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
        ![Termination End Event Symbol](/img/documentation/reference/bpmn20/termination_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/cancel-and-compensation-events.md">Compensation</a></td>
      <td></td>
      <td>
        ![Compensation Event Subprocess Startevent Symbol](/img/documentation/reference/bpmn20/compensation_event_subprocess_start_event.svg)
      </td>
      <td></td>
      <td></td>
      <td>
        ![Compensation Boundary Interrupting Event Symbol](/img/documentation/reference/bpmn20/compensation_boundary_event.svg)
      </td>
      <td></td>
      <td>
        ![Compensation Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/compensation_intermediate_throw_event.svg)
      </td>
      <td>
        ![Compensation End Event Symbol](/img/documentation/reference/bpmn20/compensation_end_event.svg)
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/cancel-and-compensation-events.md">Cancel</a></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
        ![Cancel Boundary Symbol](/img/documentation/reference/bpmn20/cancel_boundary_event.svg)
      </td>
      <td></td>
      <td></td>
      <td>
        ![Cancel End Event Symbol](/img/documentation/reference/bpmn20/cancel_end_event.svg)
      </td>
    </tr>
    <tr>
      <td>Multiple</td>
      <td>
        ![Multiple Start Event Symbol](/img/documentation/reference/bpmn20/multiple_start_event.svg)
      </td>
      <td>
          ![Multiple Start Event Symbol](./img/symbols/events/multiple_start_event.svg)
      </td>
      <td>
        ![Multiple Event Subprocess Non Interrupting Start Event Symbol](/img/documentation/reference/bpmn20/multiple_event_subprocess_non_interrupting_start_event.svg)
      </td>
      <td>
        ![Multiple Intermediate Catch Event Symbol](/img/documentation/reference/bpmn20/multiple_intermediate_catch_event.svg)
      </td>
      <td>
        ![Multiple Intermediate Catch Event Symbol](./img/symbols/events/multiple_intermediate_catch_event.svg)
      </td>
      <td>
        ![Multiple Boundary Non Interrupting Catch Event Symbol](/img/documentation/reference/bpmn20/multiple_boundary_non_interrupting_event.svg)
      </td>
      <td>
        ![Multiple Intermediate Throw Event Symbol](/img/documentation/reference/bpmn20/multiple_intermediate_throw_event.svg)
      </td>
      <td>
        ![Multiple End Event Symbol](/img/documentation/reference/bpmn20/multiple_end_event.svg)
      </td>
    </tr>

    <tr>
      <td>Multiple Parallel</td>
      <td>
          ![Multiple Parallel Start Event Symbol](/img/documentation/reference/bpmn20/multiple_parallel_start_event.svg)
      </td>
      <td>
            ![Multiple Parallel Start Event Symbol](./img/symbols/events/multiple_parallel_start_event.svg)
      </td>
      <td>
        ![Multiple Parallel Start Event Symbol](/img/documentation/reference/bpmn20/multiple_parallel_non_interrupting_start_event.svg)
      </td>
      <td>
            ![Multiple Parallel Catch Event Symbol](/img/documentation/reference/bpmn20/multiple_parallel_catch_event.svg)
      </td>
      <td>
          ![Multiple Parallel Catch Event Symbol](./img/symbols/events/multiple_parallel_catch_event.svg)
      </td>
      <td>
        ![Multiple Parallel Intermediate Non Interrupting Event Symbol](/img/documentation/reference/bpmn20/multiple_parallel_intermediate_non_interrupting_event.svg)
      </td>
      <td></td>
      <td></td>
    </tr>    
  </tbody>
</table>