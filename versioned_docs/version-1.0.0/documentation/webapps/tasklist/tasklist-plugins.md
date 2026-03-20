---

title: 'Plugins'
sidebar_position: 60

menu:
  main:
    identifier: "webapps-tasklist-plugins"
    parent: "webapps-tasklist"

---

:::note[Plugin Compatibility]
  Please note that the code of Tasklist plugins might need to be migrated when updating Operaton to a higher version (e.g. CSS styles).
:::

Tasklist uses the concept of plugins to add own functionality without having to extend or hack the Tasklist web application.

For further details about the concepts behind plugins, please read the [Cockpit plugins section](../cockpit/extend/plugins.md).

:::warning[Difference between Cockpit and Tasklist plugins:]
  * To publish the plugin with Tasklist, its class name must be put into a file called ```org.operaton.bpm.tasklist.plugin.spi.TasklistPlugin``` that resides in the directory ```META-INF/services```.
  * The plugin mechanism of Tasklist does not allow to provide additional SQL queries by using [MyBatis](http://www.mybatis.org/) mappings.
:::

## Plugin Points

Here you can see the various points at which you are able to add your own plugins.


**Name:** `tasklist.navbar.action`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-navbar-action.png)Plugin Point

---

**Name:** `tasklist.task.action`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-task-action.png)Plugin Point

---

**Name:** `tasklist.header`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-tasklist-header.png)Plugin Point

---

**Name:** `tasklist.task.detail`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-task-detail.png)Plugin Point

This plugin points properties contain the attribute `label`, which will be rendered in the navigation even when the plugin is not selected.

```Javascript
properties: {
  label: "My Plugin"
}
```

This additional data is passed into the render function:

  * `taskId`

---

**Name:** `tasklist.list`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-list.png)Plugin Point

---

**Name:** `tasklist.card`.

![Example img](../../../assets/documentation/webapps/tasklist/tasklist-plugin-card.png)Plugin Point

This additional data is passed into the render function:

  * `taskId`

---

Configure where to place your plugin as shown in the following example:

```html
var ViewConfig = [ 'ViewsProvider', function(ViewsProvider) {
  ViewsProvider.registerDefaultView('tasklist.task.detail', {
    id: 'sub-tasks',
    priority: 20,
    label: 'Sub Tasks'
  });
}];
```

For more information on creating and configuring your own plugin, please have a look at the following examples:

* [How to build the server side](https://github.com/operaton/operaton/tree/master/webapps/assembly/src/main/java/org/operaton/bpm/tasklist/impl/plugin)
* [How to build the client side](https://github.com/operaton/operaton/tree/master/webapps/frontend/ui/tasklist/plugins/standaloneTask/app)
