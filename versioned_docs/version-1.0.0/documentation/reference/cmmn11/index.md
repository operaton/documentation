---

title: 'CMMN 1.1'
sidebar_position: 40
layout: "single"

---

This page provides an overview of the CMMN 1.1 elements and the current coverage of the process engine.

The CMMN editor is disabled using a flag per default in the latest version (4.5) of the Camunda Modeler. But you have full power to modify the flags and therefore you can still enable it if you wish!

In order to do that, you need to set a “flag”. You can choose between two options to do that:

#### Option 1. Pass the `--no-disable-cmmn` flag via the Comand Line Interface

When starting the Modeler, you need to pass the `--no-disable-cmmn` via the Command Line.
So for example on linux, you run a command:

```$ ./camunda-modeler --no-disable-cmmn```

Likewise for example on Windows, you could start the .exe over the commandLine with the flag, or you could create a shortcut to the camunda-modeler.exe and append `--no-disable-cmmn` to the `target` of the shortcut.

#### Option 2. Define a flags.json file

You can locally create a file called `flags.json`, which defines the flags which the Camunda-Modeler should pick up when starting. In the file you would need to save the following text content:

```
{
    "disable-cmmn": false
}
```

The `flags.json` file needs to be saved either in your user-data-directory or application-data-directory.

There are more flags and therefore more options how to customize the Camunda Modeler to your specific use-case with flags. Please refer to the [flags documentation](https://docs.camunda.io/docs/components/modeler/desktop-modeler/flags/) to find out more.

> Thx Max for this detailed information, which comes from this [forum post](https://forum.camunda.io/t/how-to-access-cmmn-in-the-modeler/25127/4).
 
# Coverage

The elements marked in <span class="label label-warning">orange</span> are supported.

## Definitions

<div class="cmmn-symbols">
  <div class="row">
    <div class="col-md-12">
      <h3>Grouping</h3>
      <div class="bpmn-symbol-container implemented">
        <a href="../reference/cmmn11/grouping-tasks/stage.md"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="case-plan-model-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../reference/cmmn11/grouping-tasks/stage.md"><span class="glyphicon glyphicon-eye-open"></span></a>
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
        <a href="../reference/cmmn11/tasks/human-task.md"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="human-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container">
        <a href="#" class="cmmn-symbol" data-type="manual-task"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../reference/cmmn11/tasks/process-task.md"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="process-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../reference/cmmn11/tasks/case-task.md"><span class="glyphicon glyphicon-eye-open"></span></a>
        <a href="#" class="cmmn-symbol" data-type="case-task-colored"></a>
      </div>
      <div class="bpmn-symbol-container implemented">
        <a href="../reference/cmmn11/tasks/decision-task.md"><span class="glyphicon glyphicon-eye-open"></span></a>
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
        <a href="../reference/cmmn11/milestone.md"><span class="glyphicon glyphicon-eye-open"></span></a>
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
        <a class="text" href="../reference/cmmn11/sentry.md">Entry Criterion</a>
        <a href="#" class="cmmn-symbol" data-type="marker-entry-criterion"></a>
      </td>
      <td>
        <a class="text" href="../reference/cmmn11/sentry.md">Exit Criterion</a>
        <a href="#" class="cmmn-symbol" data-type="marker-exit-criterion"></a>
      </td>
      <td>
        <a class="text" href="../reference/cmmn11/markers/auto-complete.md">AutoComplete</a>
        <a href="#" class="cmmn-symbol" data-type="marker-auto-complete"></a>
      </td>
      <td>
        <a class="text" href="../reference/cmmn11/markers/manual-activation-rule.md">Manual Activation</a>
        <a href="#" class="cmmn-symbol" data-type="marker-manual-activation"></a>
      </td>
      <td>
        <a class="text" href="../reference/cmmn11/markers/required-rule.md">Required</a>
        <a href="#" class="cmmn-symbol" data-type="marker-required"></a>
      </td>
      <td>
        <a class="text" href="../reference/cmmn11/markers/repetition-rule.md">Repetition</a>
        <a href="#" class="cmmn-symbol" data-type="marker-repetition"></a>
      </td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="../reference/cmmn11/grouping-tasks/stage.md">Case Plan Model</a></td>
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
      <td><a href="../reference/cmmn11/grouping-tasks/stage.md">Stage</a></td>
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
      <td><a href="../reference/cmmn11/tasks/index.md">Task</a></td>
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
      <td><a href="../reference/cmmn11/milestone.md">Milestone</a></td>
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
