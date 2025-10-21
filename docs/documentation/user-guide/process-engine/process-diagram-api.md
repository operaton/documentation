---

title: 'Process Diagram Visualization'
sidebar_position: 250

menu:
  main:
    identifier: "user-guide-process-engine-pd-api"
    parent: "user-guide-process-engine"

---


A BPMN process diagram is a formidable place to visualize information around your process. We recommend to use JavaScript libraries to display process diagrams and enrich them with additional information.

In our web applications [Cockpit](../../webapps/cockpit/index.md) and [Tasklist](../../webapps/tasklist/index.md), we use [bpmn.io](http://bpmn.io/), a toolkit for rendering BPMN 2.0 process models directly in the browser. It allows adding additional information to the diagram and includes ways for user interaction. Although bpmn.io is still under development, its API is rather stable.

The previous JavaScript BPMN renderer can still be found at [operaton-bpmn.js](https://github.com/operaton/operaton-bpmn.js), but it is not actively developed anymore.

![Example img](./img/process-diagram-bpmn-js.png)Process Diagram Rendering


# bpmn.io Diagram Renderer

To render a process diagram, you need to retrieve the diagram XML via the <a class="javadocref" href="https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/engine/RepositoryService.html">Java</a>- or [REST API](../getProcessDefinitionBpmn20XmlByKey#Process-Definition). The following example shows how to render the process XML using bpmn.io. For more documentation regarding the annotation of the diagram and user interaction, please refer to the [bpmn.io](https://github.com/bpmn-io/bpmn-js) page.

```javascript
var BpmnViewer = require('bpmn-js');

var xml = getBpmnXml(); // get the process xml via REST
var viewer = new BpmnViewer({ container: 'body' });

viewer.importXML(xml, function(err) {

  if (err) {
    console.log('error rendering', err);
  } else {
    console.log('rendered');
  }
});
```

Alternatively, you can use the  [bpmn-viewer widget](https://github.com/operaton/operaton/blob/master/webapps/frontend/operaton-commons-ui/lib/widgets/bpmn-viewer/cam-widget-bpmn-viewer.html) from the Operaton commons UI.
