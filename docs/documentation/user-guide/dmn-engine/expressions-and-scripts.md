---

title: "Expressions in the DMN Engine"
sidebar_position: 30

menu:
  main:
    name: "Expressions"
    identifier: "user-guide-dmn-engine-expressions-scripts"
    parent: "user-guide-dmn-engine"
    description: "Define Input/Output and Conditions of Decisions"

---

Decision tables and decision literal expressions allow specifying different types of expressions.
This section describes which types of expressions exist.
It lists which expression languages are supported and demonstrates how to change the used expression language for an expression.

# Expressions in DMN

As shown in the [decision table] and [decision literal expression] reference, four types of expressions are supported:

- *Input Expression*: sets the input value for an input column
  of the decision table
- *Input Entry*: used to determine if a rule of the decision
  table is applicable
- *Output Entry*: returns a value which is added to the output of a matched rule
  of the decision table
- *Literal Expression*: used to determine the value of a decision literal expression

You can read more on this in the [DMN 1.3 reference][decision table]. In
the DMN 1.3 XML, expressions can be found in the XML
elements `inputExpression`, `inputEntry`, `outputEntry` and `literalExpression`:

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="definitions" name="definitions" namespace="http://operaton.org/schema/1.0/dmn">

  <decision id="decision" name="Decision">
    <decisionTable>
      <input id="input">
        <!-- the input expression determines the input value of a column -->
        <inputExpression>
          <text>age</text>
        </inputExpression>
      </input>
      <output id="output"/>
      <rule id="rule1">
      <!-- the input entry determines if the rule is applicable -->
        <inputEntry>
          <text>[18..30]</text>
        </inputEntry>
        <!-- the output entry determines the rule if it is applicable -->
        <outputEntry>
          <text>"okay"</text>
        </outputEntry>
      </rule>
    </decisionTable>
  </decision>

   <decision id="decision2 name="Decision 2">
    <!-- the literal expression determines the value of this decision -->
    <literalExpression>
      <text>a + b</text>
    </literalExpression>
  </decision>

</definitions>
```

# Supported Expression Languages

The Operaton DMN engine supports two expression languages out of the box:

- `JUEL`: A Operaton-maintained [implementation][juel] of the Java [Unified Expression Language][EL]
- `FEEL`: The Friendly Enough Expression Language of the [DMN 1.2] standard.

Depending on the JDK you use, there may also be a `Javascript` implementation
available like [Rhino] or [Nashhorn].

You can also use every other script language which provides a [JSR-223]
implementation. This includes `groovy`, `python` and `ruby`. To use these
languages you have to add the corresponding dependency to your project.

For example, to use `groovy` as language for expressions add these dependencies
to your project `pom.xml`:

```xml
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-jsr223</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-json</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-xml</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-templates</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-dateutil</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
    <dependency>
      <groupId>org.apache.groovy</groupId>
      <artifactId>groovy-datetime</artifactId>
      <version>${GROOVY_VERSION}</version>
    </dependency>
```

# Default Expression Languages

The default expression languages of the different expression types in the
DMN engine are as follows:

- *Input Expression*: `FEEL`
- *Input Entry*: `FEEL`
- *Output Entry*: `FEEL`
- *Literal Expression*: `FEEL`

:::note[Legacy Behavior]
You can find how to go back to the legacy behavior, where `JUEL` was used for input expressions,
output entries and literal expressions [here](../../reference/deployment-descriptors/tags/process-engine.md#dmnFeelEnableLegacyBehavior).
:::

The default language can be changed by setting it directly in the DMN 1.3 XML as global expression language with the `expressionLanguage` attribute of
the `definitions` element:

```xml
<!-- this sets the default expression language for all expressions -->
<!-- in this file to javascript -->
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="definitions" name="definitions" namespace="http://operaton.org/schema/1.0/dmn" expressionLanguage="javascript">
  <decision  id="decision" name="Decision">
    <decisionTable>
      <!-- ... -->
    </decisionTable>
  </decision>
</definitions>
```

Additionally, it is possible to change the default expression language in the default DMN engine configuration as described in the [user guide][default EL].


# Configuring the Expression Language

It is also possible to set the language for each expression individually using the `expressionLanguage` attribute:

```xml
<definitions xmlns="https://www.omg.org/spec/DMN/20191111/MODEL/" id="definitions" name="definitions" namespace="http://operaton.org/schema/1.0/dmn">

  <decision id="decision" name="Decision">
    <decisionTable>
      <input id="input">
        <!-- use javascript for this input expression -->
        <inputExpression expressionLanguage="javascript">
          <text>age</text>
        </inputExpression>
      </input>
      <output id="output"/>
      <rule id="rule1">
        <!-- use juel for this input entry -->
        <inputEntry expressionLanguage="juel">
          <text><![CDATA[cellInput $\geq$ 18 && cellInput $\leq$ 30]]></text>
        </inputEntry>
        <!-- use javascript for this output entry -->
        <outputEntry expressionLanguage="javascript">
          <text>"okay"</text>
        </outputEntry>
      </rule>
    </decisionTable>
  </decision>

  <decision id="decision2" name="Decision 2">
    <!-- use groovy for this literal expression -->
    <literalExpression expressionLanguage="groovy">
      <text>a + b</text>
    </literalExpression>
  </decision>

</definitions>
```

If you want to use another Java Unified Expression Language or FEEL
implementation, you can replace the default implementations in the
[DMN engine configuration][configure EL]. This way you can also change
the JSR-223 script engine resolving, for example if you want to configure
the script engine before using it.


[decision table]: ../../reference/dmn/decision-table/index.md
[decision literal expression]: ../../reference/dmn/decision-literal-expression/index.md
[juel]: http://juel.sourceforge.net/
[EL]: https://jakarta.ee/specifications/expression-language/4.0/
[DMN 1.2]: http://www.omg.org/spec/DMN/
[Rhino]: https://developer.mozilla.org/de/docs/Rhino
[Nashhorn]: https://blogs.oracle.com/nashorn/
[JSR-223]: https://www.jcp.org/en/jsr/detail?id=223
[default EL]: ../../user-guide/dmn-engine/embed.md#change-default-expression-languages
[configure EL]: ../../user-guide/dmn-engine/embed.md#customize-expression-and-script-resolving
