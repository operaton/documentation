---

title: 'Dashboard'
sidebar_position: 5

menu:
  main:
    identifier: "user-guide-cockpit-dmn-dashboard"
    parent: "user-guide-cockpit-dmn"
    description: "Entry point for decision monitoring."
    name: "Dashboard"

---

The decisions dashboard of Cockpit is the entry point for decision monitoring. It comes with a pre-installed plugin, which lets you see deployed decision definitions. Additional [plugins](../extend/plugins.md) can be added to the decisions dashboard.


# Deployed Decisions

![Example img](./../img/cockpit-decision-definition-list.png)Deployed Decision Definitions

This plugin provides you with a list of deployed decision definitions. You can click on the name of a decision to go to the [decision definition view][decision-definition-view] and access more details, like the DMN table or executed [decision instances view][decision-instance-view]. 
You can also click on the name of a decision requirements definition to go to the [decision requirements definition view][decision-requirements-definition-view].


# Deployed Decision Requirements Definition

![Example img](./../img/cockpit-drd-list.png)Deployed Decision Definitions

This plugin provides you with a list of deployed decision requirements definitions. You can click on the name of a decision requirements definition to go to the [decision requirements definition view][decision-requirements-definition-view] and access more details, like the decision requirements definition diagram or executed [decision requirements definition instances view][decision-requirements-definition-instance-view]. 


# Search

![Example img](./../img/dmn/decision-instance-search.png)Decision Instance Search

At the top of the dashboard, you can search for decision instances which fulfill certain search criteria. To do so, click in the search box and select the parameters to search for. You can also begin typing to find the required parameter faster. Depending on the selected property, you have to specify the value of the property. You can combine multiple search pills to narrow down the search results.

To add additional columns to the details of the search results, click on the 'Add column' button and select the desired details in the drop down menu that appears.

Furthermore, you can copy a link to the current search query to your clipboard by clicking on the <button class="btn btn-xs"><i class="glyphicon glyphicon-link"></i></button> button and you can save search queries to your local browser storage by clicking on the <button class="btn btn-xs"><i class="glyphicon glyphicon-floppy-disk"></i></button> button and inserting a name in the drop down menu that appears. You can then retrieve the search query by clicking on the <button class="btn btn-xs"><i class="glyphicon glyphicon-floppy-disk"></i></button> button and selecting the chosen name in the drop down menu.

:::note[Heads-up!]
  The decision instance search operates on the history endpoint of the engine. In case the requested historic data is not persisted to the database, then the search does not deliver the desired results.
:::

[decision-definition-view]: ../dmn/decision-definition-view.md
[decision-instance-view]: ../dmn/decision-instance-view.md
[decision-requirements-definition-view]: ../dmn/decision-requirements-definition-view.md
[decision-requirements-definition-instance-view]: ../dmn/decision-requirements-instance-view.md
