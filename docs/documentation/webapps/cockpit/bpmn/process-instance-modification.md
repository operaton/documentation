---

title: 'Process Instance Modification'
sidebar_position: 50

menu:
  main:
    identifier: "user-guide-cockpit-pi-modification"
    parent: "user-guide-cockpit-bpmn"
    description: "Modify the execution state of a running process instance."
    name: "Instance Modification"

---



![Example img](./../img/cockpit-modification.png)Process Instance Modification

In the detail view, you can modify the process instance's execution state. A modification can be one or multiple of the following operations:

* Starting execution before an activity
* Starting execution after an activity on its single outgoing sequence flow
* Canceling an activity instance or all instances of an activity


# Perform a Modification

A modification consists of multiple instructions, which are displayed in the modification tab at the bottom half of the screen (1). To add an instruction to the modification, hover over an activity of the process instance diagram. Using the modification button (2), you can select the operation to be performed with this activity. In the top-left corner of the activity, a modification badge will appear, indicating how many new instances of this activity will be created and how many activity instances will be canceled when applying this modification (3). This number represents the directly created/canceled instances only. Instances created during the modification (e.g., by service tasks) are not counted.

The option to cancel an activity or activity instance is only available if there are running instances of this activity.

You can also drag an instance badge (4) from one activity to another to create a "move token" operation which is represented by start and cancel operations.

When executing a modification, the instructions are applied in the specified order. You can change the order of instructions by using the up- and down-arrows on the left (5). You can also remove an instruction from the modification (6).

In the modification tab you can then configure the specification of the instruction depending on its type:


## Cancel Running Activity Instances

![Example img](./../img/cockpit-modification-cancel.png)Cancel Modification

When canceling activity instances you can select the instances of the activity you want to cancel. You can select them by their instance ID using the Select Instances button on the right. To better distinguish between activity instances, you can also show variables assigned to this instance using the eye button.

When canceling all instances of an activity using the  Allbutton, all instances which exist at the moment this instruction is executed will be canceled. This will also cancel instances which were created in the same modification (e.g., using a startBefore instruction before the cancel instruction). In most cases, you probably want to explicitly state the instances to cancel.


## Start New Activity Instances

![Example img](./../img/cockpit-modification-start.png)Modification Start

When starting a new activity instance, you have the option to start before or start after the activity. Using startBefore, the activity will be executed. StartAfter is only possible if there is only one sequence flow going out of the activity. In both cases you have the option to create new variables which are created or updated with the creation of the activity. Starting an activity instantiates all parent scopes (e.g., embedded sub process that contains the activity) that are not instantiated yet before the actual activity is executed.

Additionally, you can specify the ancestor of the new activity instance if it is created in an embedded sub-process or as part of a multi-instance scenario. For every ancestor, the variables are displayed. When an activity is instantiated with a specific ancestor activity instance, all scopes <i>between</i> the ancestor's activity and the target activity are instantiated.

When starting activities with a multi-instance flag, there is the option to either start a new multi-instance body of the activity (which executes the entire multi-instance construct and therefore creates the number of child activities specified in the multi-instance configuration for this task) or a new single instance of the activity in an already existing multi-instance body.


# Review Modification Instructions

![Example img](./../img/cockpit-modification-review.png)Modification Review

At any point during the creation of the modification, you can show the payload of the modification by clicking the eye button. This will show the request payload that will be sent via the [REST API](../../../reference/rest/index.md).

To perform the modification, you have to click on *Apply modifications*. Then you have a last chance to review the changes you are about to make and also review the request payload. You have an option to execute an *Asynchronous* modification and to add an annotation which will be added to the user operation log. After confirming the change, the modification is executed and the page is updated with the new execution state of the process instance.

:::warning[Semantics of Process Instance Modification]
  The exact semantics of process instance modification as well as the underlying REST and Java API can be read about in the [Process Instance Modification section](../../../user-guide/process-engine/process-instance-modification.md) of the user guide.
:::

# Perform a Batch Modification

![Example img](./../img/cockpit-batch-modification-view.png)Batch Modification View


When multiple process instances are required to be modified the batch modification feature can be used. To perform batch modifications, you need to click on the *Modify* tab in the process definition view.

![Example img](./../img/cockpit-batch-modification-detail.png)Batch Modification Detail View


The batch modification operation is handled similarly to the modification of a single process instance.

![Example img](./../img/cockpit-batch-modification-instance-selection.png)Instance Selection

However, to get to the **Apply Modifications** modal, first click **Select Instances**. This opens another modal which allows you to select the process instances the modification should be applied to.

Initially, all instances are displayed. You can use the filter bar above the list of instances to filter the displayed instances. You can select specific instances or click on the **Query** radio button to select all instances matching the filter.

:::warning[Warning]
Selecting all instances might create a high load on the database and application runtime/server if the query has a high number of results.
:::

When you have made your selection click on **Modify Selected Instances**. This leads you to the **Apply Modification** modal.


![Example img](./../img/cockpit-batch-modification-options.png)Additions Options


Here you have two additional options to select - *Asynchronous* and *Only Cancel Currently Active Activity Instances*. By default both options are checked.

It is recommended to keep *Asynchronous* ticked when you want to process a large number of instances. Otherwise, unchecking the box allows you to process the batch in a synchronous manner.

The second option, *Only Cancel Currently Active Activity Instances*, only concerns modification operations which contain cancel instructions. This option prevents activity instances which are newly created during the modification operation to be instantly canceled by the same operation again.