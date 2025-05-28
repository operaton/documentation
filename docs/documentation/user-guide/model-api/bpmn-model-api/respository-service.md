---

title: 'Repository Service'
sidebar_position: 50

menu:
  main:
    identifier: "user-guide-bpmn-model-api-repository-service"
    parent: "user-guide-bpmn-model-api"

---


It is also possible to access the BPMN model instance by the process definition id using the [Repository Service](../../../user-guide/process-engine/process-engine-api.md#services-api), as the following incomplete test sample code shows. Please see the [generate-jsf-form](https://github.com/operaton/operaton-bpm-examples/tree/master/bpmn-model-api/generate-jsf-form) quickstart for a complete example.

```java
public void testRepositoryService() {
  runtimeService.startProcessInstanceByKey(PROCESS_KEY);
  String processDefinitionId = repositoryService.createProcessDefinitionQuery()
    .processDefinitionKey(PROCESS_KEY).singleResult().getId();
  BpmnModelInstance modelInstance = repositoryService.getBpmnModelInstance(processDefinitionId);
}
```
