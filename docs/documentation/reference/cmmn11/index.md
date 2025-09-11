---

title: 'CMMN 1.1'
sidebar_position: 40
layout: "single"

---

This page provides an overview of the CMMN 1.1 elements and the current coverage of the process engine.

The CMMN editor is disabled in recent versions of Camunda Modeler but can be enabled with a feature flag. For more context and information on how to enable this feature flag in Camunda Modeler, please see [this forum post](https://forum.operaton.org/t/how-to-access-cmmn-in-the-modeler/25127).

# Coverage

The elements marked in <span class="label label-warning">orange</span> are supported.

## Definitions

<div class="cmmn-symbols">
  <div class="row">
    <div class="col-md-12">
      <h3>Grouping</h3>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/grouping-tasks/stage/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="case-plan-model-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/grouping-tasks/stage/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="stage-collapsed-colored"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="plan-fragment"></a>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-12">
      <h3>Tasks</h3>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/tasks/human-task/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="human-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="manual-task"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/tasks/process-task/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="process-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/tasks/case-task/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="case-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/tasks/decision-task/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="decision-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="task"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="discretionary-task"></a>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-9">
      <h3>Event-Triggered Elements</h3>
      <div class="bpmn-symbol-container implemented">
        <a href="../cmmn11/milestone/"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="milestone-colored"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="event-listener"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="event-listener-timer"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="event-listener-user"></a>
      </div>
    </div>
    <div class="col-md-3">
      <h3>CaseFileItem</h3>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="case-file-item"></a>
      </div>
    </div>
  </div>
</div>

## Markers


<table class="table table-bordered table-responsive table-cmmn-events">
  <thead>
    <tr>
      <td>Type</td>
      <td colspan="7">Marker</td>
    </tr>
    <tr class="collapse-bottom">
      <td></td>
      <td>
        <span class="text">Planning Table</span>
        <a href="#" class="cmmn-symbol" data-type="marker-planning-table"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/sentry/">Entry Criterion</a>
        <a href="#" class="cmmn-symbol" data-type="marker-entry-criterion"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/sentry/">Exit Criterion</a>
        <a href="#" class="cmmn-symbol" data-type="marker-exit-criterion"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/markers/auto-complete/">AutoComplete</a>
        <a href="#" class="cmmn-symbol" data-type="marker-auto-complete"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/markers/manual-activation-rule/">Manual Activation</a>
        <a href="#" class="cmmn-symbol" data-type="marker-manual-activation"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/markers/required-rule/">Required</a>
        <a href="#" class="cmmn-symbol" data-type="marker-required"></a>
      </td>
      <td>
        <a class="text" href="../cmmn11/markers/repetition-rule/">Repetition</a>
        <a href="#" class="cmmn-symbol" data-type="marker-repetition"></a>
      </td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="../cmmn11/grouping-tasks/stage/">Case Plan Model</a></td>
      <td>
        <span class="glyphicon glyphicon-remove"></span>
      </td>
      <td>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td></td>
      <td></td>
      <td></td>
    </tr>  
    <tr>
      <td><a href="../cmmn11/grouping-tasks/stage/">Stage</a></td>
      <td>
        <span class="glyphicon glyphicon-remove"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
    </tr>
    <tr>
      <td><a href="../cmmn11/tasks/">Task</a></td>
      <td>
        <span class="glyphicon glyphicon-remove"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td></td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
    </tr>
    <tr>
      <td><a href="../cmmn11/milestone/">Milestone</a></td>
      <td></td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td></td>
      <td></td>
      <td></td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
      <td>
        <span class="glyphicon glyphicon-ok"></span>
      </td>
    </tr>
    <tr>
      <td>EventListener</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>CaseFileItem</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>PlanFragment</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
