---

title: "Embedding the DMN Engine"
sidebar_position: 10

menu:
  main:
    name: "Embed"
    identifier: "user-guide-dmn-engine-embedding"
    parent: "user-guide-dmn-engine"
    description: "Use the DMN Engine as a library in an application"

---

The Operaton DMN engine can be used as a library in a custom application. To achieve this,
add the `operaton-engine-dmn` artifact to the classpath of the application and then
configure and build a decision engine instance. This section provides the
required maven coordinates to add the DMN engine as a dependency to your
project. It then shows how to configure and build a new DMN engine instance.

## Maven Coordinates

The Operaton DMN engine is released to Maven Central.

Start by importing the [`operaton-engine-dmn` BOM](/get-started/apache-maven.md#operaton-bom-bill-of-materials)
to ensure correct dependency management.

Next, include the [`operaton-engine-dmn`](/get-started/apache-maven.md#operaton-dmn)
artifact in the `dependencies` section.

## Building a DMN Engine

To build a new DMN engine, create a DMN engine configuration.
Configure it as needed and then build a new DMN engine from it.

```java
// create default DMN engine configuration
DmnEngineConfiguration configuration = DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// configure as needed
// ...

// build a new DMN engine
DmnEngine dmnEngine = configuration.buildEngine();
```

## Configuration of the DMN Engine
This section gives more insights of embedded DMN engine configuration. In case you want to use DMN engine as part of the BPMN engine, please refer to the [DMN Engine Configuration](../../user-guide/process-engine/decisions/configuration)  section of the [User Guide](../../user-guide/index.md) for the configuration in that scenario.

### Decision Table Evaluation Listeners

The DMN engine configuration allows you add a custom decision table [evaluation listener](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/delegate/DmnDecisionTableEvaluationListener.html).
A decision table evaluation listener is notified after a decision table has been evaluated. It receives an evaluation event which contains the result of the evaluation. You can decide if the listener should be notified before or after the default listeners.

```java
// create default DMN engine configuration
DmnEngineConfiguration configuration = DmnEngineConfiguration
    .createDefaultDmnEngineConfiguration();

// instantiate the listener
DmnDecisionTableEvaluationListener myListener = ...;

// notify before default listeners
configuration.getCustomPreDecisionTableEvaluationListeners()
  .add(myListener);

// notify after default listeners
configuration.getCustomPostDecisionTableEvaluationListeners()
  .add(myListener);
```

A specialized evaluation listener is the
[metric collector](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/spi/DmnEngineMetricCollector.html)
, which records the number of executed decision elements. This metric can be used to monitor the workload of a decision engine.

```java
// create default DMN engine configuration
DmnEngineConfiguration configuration = DmnEngineConfiguration
    .createDefaultDmnEngineConfiguration();

// create your metric collector
DmnEngineMetricCollector metricCollector = ...;

// set the metric collector
configuration.setEngineMetricCollector(metricCollector);
```
### Decision Evaluation Listeners

The DMN engine configuration allows you add a custom [decision evaluation listener](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/delegate/DmnDecisionEvaluationListener.html). A decision evaluation listener is
notified after a decision with all the required decisions has been evaluated. It receives an evaluation event
which contains the result of the evaluation. You can decide if the
listener should be notified before or after the default listeners.

```java
// create default DMN engine configuration
DmnEngineConfiguration configuration = DmnEngineConfiguration
    .createDefaultDmnEngineConfiguration();

// instantiate the listener
DmnDecisionEvaluationListener myListener = ...;

// notify before default listeners
configuration.getCustomPreDecisionEvaluationListeners()
  .add(myListener);

// notify after default listeners
configuration.getCustomPostDecisionEvaluationListeners()
  .add(myListener);
```

## Customizing and Extending the DMN Engine

:::warning[Use of Internal API]

Please be aware that these APIs are **not** part of the [public API](../../introduction/public-api.md) and may change in later releases.

:::

The [default DMN engine configuration](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/DefaultDmnEngineConfiguration.html)
 has further customization and extension points.

### Customize DMN Transformation

It is possible to customize the transformation of DMN by providing a [DMN transformer](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/spi/transform/DmnTransformer.html) or configuring the [default one](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/transform/DefaultDmnTransformer.html).

### Register DMN Transform Listeners

The simplest customization is to provide a [transform listener](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/spi/transform/DmnTransformListener.html). The Listener is notified after a DMN element is
transformed. The listener can modify the transformed object.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// instantiate transform listener
DmnTransformListener myTransformListener = ... ;

// add the transform listener
configuration.getTransformer()
  .getTransformListeners()
  .add(myTransformListener);
```

### Register DMN Element Transform Handler

While the transform listener allows modifying of the transformed objects, it does not support instantiating custom subclasses.
This can be achieved using a custom [transform handler](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/spi/transform/DmnElementTransformHandler.html).

A transform handler is registered for a given [DMN model API] type like a `DecisionTable`.

First, implement a transform handler which can transform a [decision table](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/model/dmn/instance/DecisionTable.html).

```java
public  class MyDecisionTableHandler extends DmnElementTransformHandler<DecisionTable, MyDecisionTableImpl> {

  public MyDecisionTableImpl handleElement(DmnElementTransformContext context, DecisionTable element) {
    // implement
  }
}
```

Then, register an instance of the handler in the default DMN transformer element handler registry.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// add the handler
configuration.getTransformer()
  .getElementTransformHandlerRegistry()
  .addHandler(DecisionTable.class, new MyDecisionTableHandler());
```

### Register DMN Data Type Transformers

The DMN engine supports a set of built-in [data types]. It is possible to override existing types with new types.

Assume you want to support a local date format type.
To achieve this, override the existing date transformer by implementing a custom transformer:

```java
public class GermanDateDataTypeTransformer extends DateDataTypeTransformer {

  protected SimpleDateFormat format = new SimpleDateFormat("dd.MM.yyyy HH:mm:ss");

  protected Date transformString(String value) {
    try {
      return format.parse(value);
    }
    catch (ParseException e) {
      throw new IllegalArgumentException(e);
    }
  }
}
```

Then, register an instance of the handler in the default DMN transformer element handler registry:

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// add the data type transformer,
// overriding the existing type "date":
configuration
  .getTransformer()
  .getDataTypeTransformerRegistry()
  .addTransformer("date", new GermanDateDataTypeTransformer());
```
It is also possible to add a new data type by implementing a new transformer and registering it for a non-existing type name:

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// add the data type transformer for custom type "currency"
configuration
  .getTransformer()
  .getDataTypeTransformerRegistry()
  .addTransformer("currency", new currencyTypeTransformer());
```

### Register Hit Policy Handlers

The DMN engine supports a subset of the DMN 1.3 [hit policies]. It is possible to implement new hit policies or
override an existing hit policy implementation.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// get the DmnHitPolicyHandlerRegistry
DmnHitPolicyHandlerRegistry hitPolicyHandlerRegistry = configuration
  .getTransformer()
  .getHitPolicyHandlerRegistry();

// register handler you own priority hit policy handler
hitPolicyHandlerRegistry
  .addHandler(HitPolicy.PRIORITY, null, new MyPriorityHitPolicyHandler());
```

### Change default expression languages

A [DMN decision table] has multiple expressions which are evaluated when the table is executed.
The default expression language for every expression type can be configured.
The following expression types exist:

- *Input Expression*: Used to specify the input of a column in a decision
  table. The default language for input expressions in the DMN engine is
  `FEEL`.
- *Input Entry*: Used to specify the condition of a rule in a decision
  table. The default language for input entries in the DMN engine is
  `FEEL`.
- *Output Entry*: Used to specify the output of a rule in a decision
  table. The default language for output entries in the DMN engine is
  `FEEL`.

The default expression language of a [DMN decision literal expression] can also be configured, the default in the DMN engine is `FEEL`.

Read more about the default expressions in the corresponding [section][expressions].

It is possible to change the default expression language on the DMN engine configuration:

```java
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

configuration
  .setDefaultInputExpressionExpressionLanguage("javascript");
```

Please note that the chosen language must be available in the classpath. By
default `JUEL` and `FEEL` are available.

If the JDK includes a JavaScript
implementation like Rhino or Nashorn, then `javascript` is available as well.

It is also possible to use other script languages like `groovy`, `python` or `ruby`.
Just make sure that the corresponding libraries are available on the classpath at runtime.

### Customize Expression and Script Resolving

The default DMN engine resolves the supported expression and script languages
using different providers.

To evaluate `JUEL` expressions, the DMN engine uses the <a class="javadocref" href="https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/spi/el/ElProvider.html">ElProvider</a> configured in the
DMN engine configuration. To use another implementation of the Unified Expression Language, replace this implementation.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// set a custom el provider
configuration.setElProvider(new MyElProvider());
```

To configure the `FEEL` engine used you can provide a custom <a class="javadocref" href="https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/feel/impl/FeelEngineFactory.html">FeelEngineFactory</a>.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// set a custom feel engine factory
configuration.setFeelEngineFactory(new MyFeelEngineFactory());
```

Script languages are resolved by the <a class="javadocref" href="https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/spi/el/DmnScriptEngineResolver.html">DmnScriptEngineResolver</a>. To customize the script engine resolving, provide an own implementation.

```java
// with a default DMN engine configuration
DefaultDmnEngineConfiguration configuration = (DefaultDmnEngineConfiguration) DmnEngineConfiguration
  .createDefaultDmnEngineConfiguration();

// set custom script engine resolver
configuration.setScriptEngineResolver(new MyScriptEngineResolver());
```

## Logging

The DMN engine uses [SLF4J] as logging API. The `operaton-dmn-engine` artifact
does not have a dependency to any of the existing [SLF4J] backends. This means that
you can choose which backend you want to use. One example would be [LOGBack], or
if you want to use Java util logging, you could use the `slf4j-jdk14` artifact.
For more information on how to configure and use SLF4J, please refer to the
[user manual].


[evaluation listener]: <a class="javadocref" href="https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/delegate/DmnDecisionTableEvaluationListener.html">DmnDecisionTableEvaluationListener</a> Interface
[DMN model API]: https://github.com/operaton/operaton-dmn-model
[data types]: ../../user-guide/dmn-engine/data-types.md
[hit policies]: ../reference/dmn/decision-table/hit-policy.md
[SLF4J]: http://www.slf4j.org/
[LOGBack]: http://logback.qos.ch/
[user manual]: http://www.slf4j.org/manual.html
[DMN decision table]: ../reference/dmn/decision-table/index.md
[DMN decision literal expression]: ../reference/dmn/decision-literal-expression/index.md
[expressions]: ../../user-guide/dmn-engine/expressions-and-scripts.md
