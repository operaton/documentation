---

title: 'Collapsed Subprocesses'
sidebar_position: 80

menu:
  main:
    identifier: "user-guide-cockpit-drilldown"
    parent: "user-guide-cockpit-bpmn"
    description: "Collapsed Subprocesses"

---

Diagrams can contain collapsed subprocesses to hide complexity on multiple levels. You can drill down into
collapsed subprocesses with the drilldown icon.

## Process diagram

If you have a collapsed subprocess in your diagram, a drilldown icon will appear in the lower right of the activity.

![Example img](./../img/drilldown/shape.png" alt="A Collapsed Subprocess Shape with a drilldown Action">}}

The collapsed shape indicates if there are running child instances or if an incident occurred in a child activity.

If you click on the drilldown icon, the diagram will show the contents of the collapsed subprocess. Use the breadcrumbs in the upper left corner
of the diagram to navigate back to the parent process.

![Example img](./../img/drilldown/breadcrumbs.png" alt="Breadcrumb links showing the process hirarchy">}}

The breadcrumbs show the process hierarchy. Opening an expanded subprocess opens the nearest collapsed subprocess.

## Migration

When migrating collapsed subprocesses, be aware that the collapsed shapes hide other activities. The wizard only displays connections for the current layer.

![Example img](./../img/drilldown/migration.png" alt="Migration view for collapsed subprocesses">}}

Additionally, collapsed subprocesses can have two badges:

  * Status of the subprocess activity
  * Status of the child activities

If a child activity of the collapsed subprocess is not mapped or has an error, an additional badge is shown on the left of the shape.
