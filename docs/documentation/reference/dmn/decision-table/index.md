---

title: "Decision Table"
sidebar_position: 10

---

![Dish table](/img/documentation/reference/dmn/decision-table/dish-table.png)
<script type="text/javascript" src="./img/map.js"></script>

A decision table represents decision logic which can be depicted as a table in
DMN 1.3. It consists of [inputs], [outputs] and [rules].

A decision table is represented by a `decisionTable` element inside a
`decision` XML element.

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="definitions" name="definitions" namespace="http://camunda.org/schema/1.0/dmn">
  <decision id="dish" name="Dish">
    <decisionTable id="decisionTable">
    <!-- ... -->
    </decisionTable>
  </decision>
</definitions>
```

## Decision Name

![Decision Name](/img/documentation/reference/dmn/decision-table/decision-name.png)

The name describes the decision for which the decision table provides the
decision logic. It is set as the `name` attribute on the `decision` element.
It can be changed via the Properties Panel after selecting the respective 
"Decision" in the [Decision Requirements Diagram] view.

```xml
<decision id="dish" name="Dish">
  <decisionTable id="decisionTable">
  <!-- ... -->
  </decisionTable>
</decision>
```

## Decision Id

![Decision Id](/img/documentation/reference/dmn/decision-table/decision-id.png)

The id is the technical identifier of the decision. It is set in the `id`
attribute on the `decision` element.
Just as the `name`, the `id` can be changed via the Properties Panel after selecting 
the respective "Decision" in the [Decision Requirements Diagram] view.

Each decision should have an unique id when it is [deployed] to Operaton.
The engine uses the id as the decision key of the deployed
`DecisionDefinition`.

```xml
<decision id="dish" name="Dish">
  <decisionTable id="decisionTable">
  <!-- ... -->
  </decisionTable>
</decision>
```


[inputs]:../../../reference/dmn/decision-table/input.md
[outputs]:../../../reference/dmn/decision-table/output.md
[rules]:../../../reference/dmn/decision-table/rule.md
[deployed]:../../../user-guide/process-engine/decisions/repository.md
[Decision Requirements Diagram]:../../../reference/dmn/drg/index.md