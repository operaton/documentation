---

title: 'BPMN 2.0'
sidebar_position: 20

---

This page gives you an overview of the BPMN 2.0 elements and the current coverage of the process engine.

:::note[BPMN - Business Process Model and Notation
If you are unfamiliar with BPMN 2.0, you might want to check out the
<a href="http://operaton.org/bpmn/tutorial.html">BPMN Tutorial</a> first.
:::

# Coverage

The elements marked in <span class="label label-warning label-implemented">orange</span> are supported.

## Symbols

<div class="bpmn-symbols">

  <div class="row">
    <div class="col-md-12">
      <h3>Participants</h3>
      <div >
        <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image01.svg" />
        </div>
        <div class="bpmn-symbol-container implemented">
          <img src="/img/reference/bpmn20/image02.svg" />
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h3>Subprocesses</h3>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image03.svg" />
        <a href="../reference/bpmn20/subprocesses/embedded-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image04.svg" />
        <a href="../reference/bpmn20/subprocesses/call-activity.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image05.svg" />
        <a href="../reference/bpmn20/subprocesses/event-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image06.svg" />
        <a href="../reference/bpmn20/subprocesses/transaction-subprocess.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h3>Tasks</h3>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image07.svg" />
        <a href="../reference/bpmn20/tasks/service-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image08.svg" />
        <a href="../reference/bpmn20/tasks/user-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image09.svg" />
        <a href="../reference/bpmn20/tasks/script-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image10.svg" />
        <a href="../reference/bpmn20/tasks/business-rule-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image11.svg" />
        <a href="../reference/bpmn20/tasks/manual-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image12.svg" />
        <a href="../reference/bpmn20/tasks/receive-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container">
        <img src="/img/reference/bpmn20/image13.svg" />
      </div>
      <div class="bpmn-symbol-container implemented">
      <img src="/img/reference/bpmn20/image14.svg" />
        <a href="../reference/bpmn20/tasks/send-task.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image15.svg" />
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-6">
      <h3>Gateways</h3>
      <div class="bpmn-symbol-container implemented">
      <img src="/img/reference/bpmn20/image16.svg" /> 
        <a href="../reference/bpmn20/gateways/exclusive-gateway.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image17.svg" />
        <a href="../reference/bpmn20/gateways/inclusive-gateway.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <img src="/img/reference/bpmn20/image18.svg" />
        <a href="../reference/bpmn20/gateways/parallel-gateway.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container implemented">
      <img src="/img/reference/bpmn20/image19.svg" />
        <a href="../reference/bpmn20/gateways/event-based-gateway.md">
          <span class="glyphicon glyphicon-eye-open"></span>
        </a>
      </div>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image20.svg" />
      </div>
    </div>
    <div class="col-md-3">
      <h3>Data</h3>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image21.svg" />
      </div>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image22.svg" />
      </div>
    </div>
    <div class="col-md-3">
      <h3>Artifacts</h3>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image23.svg" />
      </div>
      <div class="bpmn-symbol-container">
      <img src="/img/reference/bpmn20/image24.svg" />
      </div>
    </div>
  </div>
</div>

## Events

In BPMN there are start events, intermediate events and end events. These three event types can be catching events or throwing events. Intermediate events can be used as boundary events on tasks, in which case they can be interrupting or non-interrupting. This gives you a lot of flexibility to use events in your processes.

:::note[Understanding BPMN Events
To help understand the principle behavior of events in BPMN, we recommend to check the
[Events: Basic Concepts](http://operaton.org/bpmn/reference.html#events-basic-concepts)
chapter of the [BPMN Modeling Reference](http://operaton.org/bpmn/reference.html).
:::

<table class="table table-responsive table-bordered bpmn-events">
  <tbody>
    <tr>
      <td>Type</td>
      <td colspan="3">Start</td>
      <td colspan="4">Intermediate</td>
      <td>End</td>
    </tr>
    <tr>
      <td></td>
      <td>Normal</td>
      <td>Event Subprocess</td>
      <td>
        Event Subprocess
        <br/>
        non-interrupt
      </td>
      <td>catch</td>
      <td>boundary</td>
      <td>
        boundary
        <br/>
        non-interrupt
      </td>
      <td>throw</td>
      <td></td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/none-events.md">None</a></td>
      <td>
      <img src="/img/reference/bpmn20/image25.svg" />
      </td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image26.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image27.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/message-events.md">Message</a></td>
      <td>
      <img src="/img/reference/bpmn20/image28.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image29.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image30.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image31.svg" />   
      </td>
      <td>
      <img src="/img/reference/bpmn20/image32.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image33.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image34.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image35.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/timer-events.md">Timer</a></td>
      <td>
      <img src="/img/reference/bpmn20/image36.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image37.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image38.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image39.svg" /> 
      </td>
      <td>
      <img src="/img/reference/bpmn20/image40.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image41.svg" />
      </td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td><a href="../reference/bpmn20/events/conditional-events.md">Conditional</a></td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image42.svg" />
      </td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image43.svg" />
      </td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image44.svg" />
      </td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image45.svg" />
      </td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image46.svg" />
      </td>
      <td class="implemented">
      <img src="/img/reference/bpmn20/image47.svg" />
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
      <img src="/img/reference/bpmn20/image48.svg" />
      </td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image49.svg" />
      </td>
      <td></td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/signal-events.md">Signal</a></td>
      <td>
      <img src="/img/reference/bpmn20/image50.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image51.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image52.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image53.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image54.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image55.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image56.svg" />  
      </td>
      <td>
      <img src="/img/reference/bpmn20/image57.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/error-events.md">Error</a></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image58.svg" />
      </td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image59.svg" />
      </td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image60.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/escalation-events.md">Escalation</a></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image61.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image62.svg" />
      </td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image63.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image64.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image65.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image66.svg" />  
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
      <img src="/img/reference/bpmn20/image67.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/cancel-and-compensation-events.md">Compensation</a></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image68.svg" />
      </td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image69.svg" />
      </td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image70.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image71.svg" />
      </td>
    </tr>
    <tr class="implemented">
      <td><a href="../reference/bpmn20/events/cancel-and-compensation-events.md">Cancel</a></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image72.svg" />
      </td>
      <td></td>
      <td></td>
      <td>
      <img src="/img/reference/bpmn20/image73.svg" />
      </td>
    </tr>
    <tr>
      <td>Multiple</td>
      <td>
      <img src="/img/reference/bpmn20/image74.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image75.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image76.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image77.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image78.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image79.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image80.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image81.svg" />
      </td>
    </tr>
    <tr>
      <td>Multiple Parallel</td>
      <td>
      <img src="/img/reference/bpmn20/image82.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image83.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image84.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image85.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image86.svg" />
      </td>
      <td>
      <img src="/img/reference/bpmn20/image87.svg" />
      </td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
