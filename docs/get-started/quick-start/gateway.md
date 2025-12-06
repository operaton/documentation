---

title: 'Make It Dynamic'
sidebar_position: 5
description: 'Learn how to make your Process more dynamic by adding Gateways to the Process.'

---

# Add Gateways to the Process (5/6)

In this section, you'll learn how to make your process more dynamic by using BPMN 2.0 *Exclusive Gateways*.

## Add Two Gateways
We want to modify our process so that it's more dynamic.

To do so, open the process in the Camunda Modeler.

Next, from the Modeler's left-hand menu, select the gateway shape (diamond) and drag it into position between the Start Event and the Service Task. Use the create space tool again as needed. Move the User Task down and add another Gateway after it. Lastly, adjust the Sequence Flows so that the model looks like this:
![Example image](/img/get-started/quick-start/modeler-gateway1.png)

Now also name the new elements accordingly:
![Example image](/img/get-started/quick-start/modeler-gateway2.png)

## Configure the Gateways

Next, open the properties panel and select the `<1000 €` Sequence Flow after the Gateway on the canvas. This will update the selection in the properties panel.
Scroll to the property named `Condition Type` and change it to `Expression`. Then input `${amount<1000}` as the Expression.
We are using the [Java Unified Expression Language](https://docs.operaton.org/docs/documentation/user-guide/process-engine/expression-language/) to evaluate the Gateway.

![Example image](/img/get-started/quick-start/modeler-gateway3.png)

Next, change the Expressions for the other Sequence Flows, too.

For the `$\geq$1000 €` Sequence Flow, use the Expression `${amount$\geq$1000}`:
![Example image](/img/get-started/quick-start/modeler-gateway4.png)


For the `Yes` Sequence Flow, use the Expression `${approved}`:
![Example image](/img/get-started/quick-start/modeler-gateway5.png)

For the `No` Sequence Flow, use the Expression `${!approved}`:
![Example image](/img/get-started/quick-start/modeler-gateway6.png)

## Deploy the Process

Use the `Deploy` Button in the Camunda Modeler to deploy the updated process to Operaton.

## Work on the Task

Go to Tasklist ([http://localhost:8080/operaton/app/tasklist/](http://localhost:8080/operaton/app/tasklist/)) and log in with the credentials "demo / demo".
Click on the Start process button to start a process instance for the *Payment Retrieval* Process.
Next, set variables for the process instance using the generic form as we learned in the *User Tasks* section.

![Example image](/img/get-started/quick-start/start-form-generic.png)

Fill in the form as shown in the screenshot and make sure you use an amount that is larger or equal to 1000 in order to see the User Task *Approve Payment*.
When you are done, click *Start*.

You should see the *Approve Payment* task when you click on *All Tasks*. In this quick start, we're logged into Tasklist as an admin user, and so we can see all tasks associated with our processes. However, it's possible to create [filters in Tasklist](/docs/documentation/webapps/tasklist/filters/) to determine which users can see which tasks based on [user authorization](/docs/documentation/webapps/admin/authorization-management/) as well as other criteria.

To work on the task, select the *Form* tab and check the *approved* checkbox so that our payment retrieval gets approved.
We should see that our worker prints something to the console.

Next, repeat the same steps, and this time, reject the payment. You should also create one instance with an amount less than 1000 to confirm that the first gateway works correctly.

:::note[Next Step]
Now you're ready for Decision Automation. Let's have a look how you can [add Business Rules to your Process](/docs/get-started/quick-start/decision-automation/).
:::