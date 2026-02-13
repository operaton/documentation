---

title: "Decision Requirements Graph"
sidebar_position: 30

---

![Decision Requirements Graph](../../../../assets/documentation/reference/dmn/drg/drd.png)

A Decision Requirements Graph (DRG) models a domain of decision-making, showing the most important elements involved in it and the dependencies
between them. The elements modeled are [decisions], [input data], and [knowledge sources].

The visual representation of a DRG is called Decision Requirements Diagram (DRD).

In the XML a DRG is represented by the `definitions` element.

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="dinnerDecisions" name="Dinner Decisions" namespace="http://operaton.org/schema/1.0/dmn">
  <decision id="dish" name="Dish">
    <!-- ... -->
  </decision>
  <decision id="beverages" name="Beverages">
    <!-- ... -->
  </decision>
</definitions>
```

## Decision Requirements Graph Name

![Decision Requirements Graph Name](../../../../assets/documentation/reference/dmn/drg/drg-name.png)

The name describes the DRG. It is set as the `name` attribute on the `definitions` element.

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" 
             id="dinnerDecisions" 
             name="Dinner Decisions" 
             namespace="http://operaton.org/schema/1.0/dmn">
  <!-- ... -->
</definitions>
```

## Decision Requirements Graph Id

![Decision Requirements Graph Id](../../../../assets/documentation/reference/dmn/drg/drg-id.png)

The id is the technical identifier of the DRG. It is set in the `id` attribute on the `definitions` element.

Each DRG should have an unique id when it is [deployed] to Operaton.
The engine uses the id as the decision requirements definition key of the deployed
`DecisionRequirementsDefinition`.

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" 
             id="dinnerDecisions" 
             name="Dinner Decisions" 
             namespace="http://operaton.org/schema/1.0/dmn">
  <!-- ... -->
</definitions>
```

## Decision

![Decision](../../../../assets/documentation/reference/dmn/drg/decision.png)

A decision requirements graph can have one or more decisions. A decision has a [name] which is shown in the DRD and an [id]. The decision logic inside the decision must be either a [decision table] or a [decision literal expression].

A decision is represented by a `decision` element inside the `definitions` XML element.

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="dish" name="Desired Dish" namespace="party">
  <decision id="beverages" name="Beverages">
    <decisionTable id="decisionTable">
    <!-- ... -->
    </decisionTable>
  </decision>
</definitions>
```

### Required Decisions

![Required Decision](../../../../assets/documentation/reference/dmn/drg/required-decision.png)

A decision can have one or more required decisions which it depends on. 

A required decision is represented by a `requiredDecision` element inside an `informationRequirement` XML element. 
It has a `href` attribute and the value starts with `#` followed by the [decision id](../../../reference/dmn/decision-table/#decision-id) of the required decision.

```xml
<decision id="beverages" name="Beverages">
  <informationRequirement>
      <requiredDecision href="#dish" />
  </informationRequirement>
  <!-- ... -->
</decision>
```

## Input Data

![Input Data](../../../../assets/documentation/reference/dmn/drg/input-data.png)

An input data denotes information used as an input by one or more decisions. 

It is represented by an `inputData` element inside the `definitions` element. 

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="dinnerDecisions" name="Dinner Decisions" namespace="http://operaton.org/schema/1.0/dmn">
  <inputData id="guestsWithChildren" name="Guests with children?" />
  
  <decision id="beverages" name="Beverages">
    <informationRequirement>
      <requiredInput href="#guestsWithChildren" />
    </informationRequirement>
    <!-- ... -->
</definitions>
```

Note that an input data has no execution semantics and is ignored by the Operaton DMN engine.

## Knowledge Source

![Knowledge Source](../../../../assets/documentation/reference/dmn/drg/knowledge-source.png)

A knowledge source denotes an authority for a Decision.

It is represented by a `knowledgeSource` element inside the `definitions` element. 

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="dinnerDecisions" name="Dinner Decisions" namespace="http://operaton.org/schema/1.0/dmn">
  <knowledgeSource id="cookbook" name="Men's Cookbook" />
  
  <decision id="dish" name="Dish">
    <authorityRequirement>
      <requiredDecision href="#cookbook" />
    </authorityRequirement>
    <!-- ... -->
</definitions>
```

Note that a knowledge source has no execution semantics and is ignored by the Operaton DMN engine.



[decisions]:#decision
[input data]:#input-data
[knowledge sources]:#knowledge-source
[decision table]:../../../reference/dmn/decision-table/index.md
[deployed]:../../../user-guide/process-engine/decisions/repository.md#deploying-a-decision
[decision literal expression]:../../../reference/dmn/decision-literal-expression/index.md
[id]:../../../reference/dmn/decision-table/index.md#decision-id
[name]:../../../reference/dmn/decision-table/index.md#decision-name