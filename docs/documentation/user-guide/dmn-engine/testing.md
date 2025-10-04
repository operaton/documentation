---

title: "Testing"
sidebar_position: 50

menu:
  main:
    name: "Testing"
    identifier: "user-guide-dmn-engine-testing"
    parent: "user-guide-dmn-engine"
    description: "Test Decisions in Unit Tests"

---

To easily test DMN decisions in a JUnit test, the DMN engine provides a
JUnit Rule. The <a class="javadocref" href="https://operaton.github.io/operaton/javadoc/operaton/1.0/org/operaton/bpm/dmn/engine/test/DmnEngineRule.html">DmnEngineRule</a> creates a new default DMN engine. The DMN engine can be used in test cases to parse and evaluate decisions.

```java
public class DecisionTest {

  @Rule
  public DmnEngineRule dmnEngineRule = new DmnEngineRule();

  @Test
  public void test() {
    DmnEngine dmnEngine = dmnEngineRule.getDmnEngine();
    // load DMN file
    InputStream inputStream = ...;
    //create and add variables
    VariableMap variables = Variables.createVariables();

    DmnDecision decision = dmnEngine.parseDecision("decision", inputStream);
    DmnDecisionResult result = dmnEngine.evaluateDecision(decision, variables);

    // assert the result
    // ...
  }

}
```

If you want to create a DMN engine with a custom configuration, you can pass
this to the DMN engine rule.


```java
public class DecisionTest {

  @Rule
  public DmnEngineRule dmnEngineRule = new DmnEngineRule(createCustomConfiguration());

  public DmnEngineConfiguration createCustomConfiguration() {
    // create and return custom configuration
    return ...;
  }

  @Test
  public void test() {
    DmnEngine customDmnEngine = dmnEngineRule.getDmnEngine();
    // ...
  }

}
```

The [DmnDecisionResult](https://operaton.github.io/operaton/javadoc/operaton/1.0/org/operaton/bpm/dmn/engine/DmnDecisionResult.html) implements the interface `List<DmnDecisionResultEntries>`. Whereas the
[DmnDecisionResultEntries](https://operaton.github.io/operaton/javadoc/operaton/1.0/org/operaton/bpm/dmn/engine/DmnDecisionResultEntries.html) implements the interface `Map<String, Object>`.
This allows you to use common `List` or `Map` asserts.
