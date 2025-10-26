---

title: 'Decision Automation'
sidebar_position: 6
description: "Learn how to integrate DMN decision tables in the Process."

---
# Leverage business rules (6/6)

In this section, you'll learn how to add decision automation to your process by using [BPMN 2.0 *Business Rule Tasks*](/docs/documentation/reference/bpmn20/tasks/business-rule-task/) and [DMN 1.3 Decision Tables](/docs/documentation/reference/dmn11/).

## Add a Business Rule Task to the Process
Use the Camunda Modeler to open the Payment Retrieval process then click on the Approve Payment Task. Change the activity type to *Business Rule Task* in the wrench button menu.

![Example image](./img/modeler-businessrule-task1.png)

Next, link the Business Rule Task to a DMN table by changing `Implementation` to `DMN` and `Decision Ref` to `approve-payment` in the properties panel. In order to retrieve the result of the evaluation and save it automatically as a process instance variable in our process, we also need to change the `Result Variable` to `approved` and use `singleEntry` as the `Map Decision Result` in the properties panel.

![Example image](./img/modeler-businessrule-task2.png)

Save your changes and deploy the updated process using the `Deploy` Button in the Camunda Modeler.

## Create a DMN table using the Camunda Modeler
First, create a new DMN diagram by clicking *File > New File > DMN Diagram*.
![Example image](./img/modeler-new-dmn-diagram.png)

Now the newly created diagram will already have a decision element added to it. Select it by clicking it and then give it a name of *Approve Payment* and an ID of `approve-payment` (the decision ID must match the the `Decision Ref` in your BPMN process).
![Example image](./img/modeler-new-dmn-diagram-properties.png)

Next, create a new DMN table by clicking the table button.
![Example image](./img/modeler-new-dmn-table.png)

## Specify the DMN table
First, specify the input expressions for the DMN table. In this example, we'll decide whether a payment is approved based on the item name. Your rules can also make use of the FEEL Expression Language, JUEL or Script. If you like, you can [read more about Expressions in the DMN Engine](/docs/documentation/user-guide/dmn-engine/expressions-and-scripts/).

Double click *Input* to configure the input column. Use `Item` as the *Input Label* and `item` as the *Input Expression*:
![Example image](./img/modeler-dmn2.png)

Next, set up the output column. Use `Approved` as the *Output Label* and `approved` as the *Output Name* for the output column "Approved":
![Example image](./img/modeler-dmn3.png)

Let's create some rules by clicking on the plus icon on the left side of the DMN table. We should also change the Output Column to the Data Type `boolean`:
![Example image](./img/modeler-dmn4.png)

After setup, your DMN table should look like this:
![Example image](./img/modeler-dmn5.png)

## Deploy the DMN table
To deploy the Decision Table, click on the Deploy button in the Camunda Modeler, give it Deployment Name "Payment Retrieval Decision", then hit the Deploy button.
![Example image](./img/modeler-dmn6.png)

## Verify the Deployment with Cockpit
Now, use Cockpit to see if the decision table was successfully deployed. Go to [http://localhost:8080/operaton/app/cockpit/](http://localhost:8080/operaton/app/cockpit/). Log in with the credentials *demo / demo*. Navigate to the "Decisions" section. Your decision table *Approve Payment* should be listed as deployed decision definition.

![Example image](./img/cockpit-approve-payment.png)

## Inspect using Cockpit and Tasklist

Next, use Tasklist to start two new Process Instances and verify that depending on your input, the Process Instance will be routed differently.
To do so, go to [http://localhost:8080/operaton/app/tasklist/](http://localhost:8080/operaton/app/tasklist/). Log in with *demo / demo*.

Click on the Start process button to start a process instance and choose the `Payment` process.
Use the generic form to add the variables as follows:
![Example image](./img/tasklist-dmn1.png)

Hit the Start Instance button.

Next, click again on the Start process button to start another process instance and choose the `Payment` process.
Use the generic form to add the variables as follows:
![Example image](./img/tasklist-dmn2.png)

You'll see that depending on the input, the worker will either charge or not charge the credit card.
You can also verify that the DMN tables were evaluated by using Operaton Cockpit. Go to [http://localhost:8080/operaton/app/cockpit/](http://localhost:8080/operaton/app/cockpit/). Log in with the credentials *demo / demo*. Navigate to the "Decisions" section and click on Approve Payment. Check the different Decision Instances that were evaluated by clicking on the ID in the table.

A single DMN table that was executed could look like this in Operaton Cockpit:
![Example image](./img/cockpit-dmn-table.png)

:::note[Success!]
Congratulations! You've successfully completed the Operaton Platform Quick Start. Ready to continue? We recommend the [Operaton Platform documentation](https://docs.operaton.org/manual/latest/).
:::