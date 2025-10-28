---

title: 'Templating'
sidebar_position: 90

menu:
  main:
    identifier: "user-guide-process-engine-templating"
    parent: "user-guide-process-engine"

---


Operaton supports template engines which are implemented as script engines compatible with
JSR-223. As a result, templates can be used everywhere where scripts can be used.

In community distributions of Operaton, the following template engine is provided out of the
box:

* [FreeMarker][freemarker]

The script engine Freemarker wrapper implementation can be found in the
[operaton-bpmn-platform](https://github.com/operaton/operaton/tree/master/freemarker-template-engine) repository.

The following template engines are provided as optional community extensions:

* [Apache Velocity][velocity]
* [Saxon XQuery](https://www.saxonica.com/html/documentation12/using-xquery/)
* [Saxon XSLT](https://www.saxonica.com/html/documentation12/using-xsl/)

The script engine wrapper implementations can be found in the
[operaton-template-engines-jsr223][operaton-template-engines-jsr223] community hub repository.

## Install a Template Engine

### Install a Template Engine for an Embedded Process Engine

A template engine must be installed in the same way as a script engine. This means that the template
engine must be added to the process engine classpath.

When using an embedded process engine, the template engine libraries must be added to the
application deployment. When using the process engine in a maven `war` project, the template engine
dependencies must be added as dependencies to the maven `pom.xml` file:

:::note
  The [Operaton BOM](/get-started/apache-maven/) only contains the officially supported freemarker template engine.
  For the community-driven template engines, please check the Maven coordinates below.
:::

```xml
<dependencies>

  <!-- freemarker -->
  <dependency>
    <groupId>org.operaton.template-engines</groupId>
    <artifactId>operaton-template-engines-freemarker</artifactId>
  </dependency>

</dependencies>
```

Here are the Maven coordinates of the community extensions:

```xml
<dependencies>

  <!-- saxon xquery -->
  <dependency>
    <groupId>org.operaton.community.template.engine</groupId>
    <artifactId>operaton-template-engine-xquery</artifactId>
  </dependency>

  <!-- saxon xslt -->
  <dependency>
    <groupId>org.operaton.community.template.engine</groupId>
    <artifactId>operaton-template-engine-xslt</artifactId>
  </dependency>

  <!-- apache velocity -->
  <dependency>
    <groupId>org.operaton.community.template.engine</groupId>
    <artifactId>operaton-template-engine-velocity</artifactId>
  </dependency>

</dependencies>
```


### Install a Template Engine for a Shared Process Engine

When using a shared process engine, the template engine must be added to the shared process engine
classpath. The procedure for this depends on the application server. In Apache Tomcat, the
libraries have to be added to the shared `lib/` folder.

:::note
  [FreeMarker](http://freemarker.org/) is pre-installed in the Operaton pre-packaged distribution.
:::


## Use a Template Engine

If the template engine library is in the classpath, you can use templates everywhere in the BPMN
process where you can [use scripts][use-scripts], for example as a script task or inputOutput mapping.
The FreeMarker template engine is part of the Operaton distribution.

Inside the template, all process variables of the BPMN element scope are available. The
template can also be loaded from an external resource as described in the [script source
section][script-source].

The following example shows a FreeMarker template, of which the result is saved in the process variable
`text`.

```xml
<scriptTask id="templateScript" scriptFormat="freemarker" operaton:resultVariable="text">
  <script>
    Dear ```${customer},

    thank you for working with Operaton${version}.

    Greetings,
    Operaton Developers
  </script>
</scriptTask>
```

In an inputOutput mapping it can be very useful to use an external template to generate the
payload of a `operaton:connector`.

```xml
<bpmn2:serviceTask id="soapTask" name="Send SOAP request">
  <bpmn2:extensionElements>
    <operaton:connector>
      <operaton:connectorId>soap-http-connector</operaton:connectorId>
      <operaton:inputOutput>

        <operaton:inputParameter name="soapEnvelope">
          <operaton:script scriptFormat="freemarker" resource="soapEnvelope.ftl" />
        </operaton:inputParameter>

        <!-- ... remaining connector config omitted -->

      </operaton:inputOutput>
    </operaton:connector>
  </bpmn2:extensionElements>
</bpmn2:serviceTask>
```

## Use XSLT as Template Engine

### Use XSLT Template Engine with an embedded process engine

When using an embedded process engine, the XSLT template engine library must be added to the
application deployment. When using the process engine in a maven `war` project, the template engine
dependency must be added as dependencies to the maven `pom.xml` file:

```xml
<dependencies>

  <!-- XSLT -->
  <dependency>
    <groupId>org.operaton.community.template.engine</groupId>
    <artifactId>operaton-template-engine-xslt</artifactId>
  </dependency>

</dependencies>
```

### Use XSLT Templates

The following is an example of a BPMN ScriptTask used to execute an XSLT Template:

```xml
<bpmn2:scriptTask id="ScriptTask_1" name="convert input"
                  scriptFormat="xslt"
                  operaton:resource="org/operaton/bpm/example/xsltexample/example.xsl"
                  operaton:resultVariable="xmlOutput">

  <bpmn2:extensionElements>
    <operaton:inputOutput>
      <operaton:inputParameter name="operaton_source">${customers}</operaton:inputParameter>
    </operaton:inputOutput>
  </bpmn2:extensionElements>

</bpmn2:scriptTask>
```

As shown in the example above, the XSL source file can be referenced using the `operaton:resource`
attribute. It may be loaded from the classpath or the deployment (database) in the same way as
described for [script tasks][script-source].

The result of the transformation can be mapped to a variable using the `operaton:resultVariable`
attribute.

Finally, the input of the transformation must be mapped using the special variable `operaton_source`
using a `<operaton:inputParameter ... />` mapping.

A [full example of the XSLT Template Engine][xslt-example] in Operaton can be found in the
examples' repository.


[freemarker]: http://freemarker.org/
[velocity]: http://velocity.apache.org/
[operaton-template-engines-jsr223]: https://github.com/operaton-community-hub/operaton-template-engines-jsr223
[use-scripts]: ../process-engine/scripting.md
[script-source]: ../process-engine/scripting.md#script-source
[xslt-example]: https://github.com/operaton/operaton-bpm-examples/tree/master/scripttask/xslt-scripttask
