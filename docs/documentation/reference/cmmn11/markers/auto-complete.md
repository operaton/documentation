---

title: 'Auto Complete'
sidebar_position: 30

menu:
  main:
    identifier: "cmmn-ref-markers-auto-complete"
    parent: "cmmn-ref-markers"
    description: "Controls whether a Stage auto completes."

---

**Can be used with**: [Stage](../grouping-tasks/stage.md), CasePlanModel

<a href="#" class="cmmn-symbol" data-type="marker-auto-complete"></a>

The attribute `autoComplete` controls the completion of a stage instance. The following table describes the completion criteria of a stage instance based on the `autoComplete` property.

* `autoComplete = true`: There are no children in the `ACTIVE` state, and all required (<a href="../reference/cmmn11/markers/required-rule.md">see Required Rule</a>) children are `COMPLETED`, `DISABLED` or `TERMINATED`.
* `autoComplete = false`: There are no children in the `ACTIVE` state, and
    * all children are `COMPLETED`, `DISABLED` or `TERMINATED`, or
    * on manual completion using `CaseService#completeCaseExecution`, all required (<a href="../reference/cmmn11/markers/required-rule.md">see Required Rule</a>) children are `COMPLETED`, `DISABLED` or `TERMINATED`.

For a CasePlanModel the property `autoComplete` can be set as follows:

```xml
<case id="case">
  <casePlanModel id="CasePlanModel_1" autoComplete="true">

    ...

  </casePlanModel>
</case>
```

For a Stage, the following XML can be used:

```xml
<case id="case">
  <casePlanModel id="CasePlanModel_1" autoComplete="true">

    <planItem id="PI_Stage_1" definitionRef="Stage_1" />

    <stage id="Stage_1" autoComplete="true"/>

  </casePlanModel>
</case>
```
