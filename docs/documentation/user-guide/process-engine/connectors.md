---

title: 'Connectors'
sidebar_position: 100

menu:
  main:
    identifier: "user-guide-process-engine-connectors"
    parent: "user-guide-process-engine"

---


With the dependency [operaton-connect](https://github.com/operaton/operaton-bpm-platform/tree/master/connect), the process engine supports simple
connectors. Currently the following connector implementations exist:

<table class="table">
  <tr>
    <th>Connector</th>
    <th>ID</th>
  </tr>
  <tr>
    <td>REST HTTP</td>
    <td>http-connector</td>
  </tr>
  <tr>
    <td>SOAP HTTP</td>
    <td>soap-http-connector</td>
  </tr>
</table>

It is also possible to implement your own custom connector in camunda. For more information about extending connectors please visit the [Connector reference](../../reference/connect/extending-connect.md).


# Configure Operaton Connect

As Operaton Connect is available only partially when using the process engine (check the list below). With a pre-built distribution, Operaton Connect is already preconfigured.

The following `connect` artifacts exist:

* `operaton-connect-core`: a jar that contains only the core Connect classes. The artifact already is available as dependency to the process engine. In addition to `operaton-connect-core`, single connector implementations like `operaton-connect-http-client` and `operaton-connect-soap-http-client` exist. These dependencies should be used when the default connectors have to be reconfigured or when custom connector implementations are used.
* `operaton-connect-connectors-all`: a single jar without dependencies that contains the HTTP and SOAP connectors.
* `operaton-engine-plugin-connect`: a process engine plugin to add Connect to Operaton.


# Maven Coordinates

:::note
  Please import the [Operaton BOM](/get-started/apache-maven/) to ensure correct versions for every Operaton project.
:::


## operaton-connect-core

`operaton-connect-core` contains the core classes of Connect. Additionally, the HTTP and SOAP connectors can be added with the dependencies `operaton-connect-http-client` and `operaton-connect-soap-http-client`. These artifacts will transitively pull in their dependencies, like Apache HTTP client. For integration with the engine, the artifact `operaton-engine-plugin-connect` is needed. Given that the BOM is imported, the Maven coordinates are as follows:

```xml
<dependency>
  <groupId>org.operaton.connect</groupId>
  <artifactId>operaton-connect-core</artifactId>
</dependency>
```

```xml
<dependency>
  <groupId>org.operaton.connect</groupId>
  <artifactId>operaton-connect-http-client</artifactId>
</dependency>
```

```xml
<dependency>
  <groupId>org.operaton.connect</groupId>
  <artifactId>operaton-connect-soap-http-client</artifactId>
</dependency>
```

```xml
<dependency>
  <groupId>org.operaton.bpm</groupId>
  <artifactId>operaton-engine-plugin-connect</artifactId>
</dependency>
```


## operaton-connect-connectors-all

This artifact contains the HTTP and SOAP connectors as well as their dependencies. To avoid conflicts with other versions of these dependencies, the dependencies are relocated to different packages. `operaton-connect-connectors-all` has the following Maven coordinates:

```xml
<dependency>
  <groupId>org.operaton.connect</groupId>
  <artifactId>operaton-connect-connectors-all</artifactId>
</dependency>
```


## Configure the Process Engine Plugin

`operaton-engine-plugin-connect` contains a class called `org.operaton.connect.plugin.impl.ConnectProcessEnginePlugin` that can be registered with a process engine using the [plugin mechanism](../process-engine/process-engine-plugins.md). For example, a `bpm-platform.xml` file with the plugin enabled would look as follows:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpm-platform xmlns="http://www.operaton.org/schema/1.0/BpmPlatform"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.operaton.org/schema/1.0/BpmPlatform http://www.operaton.org/schema/1.0/BpmPlatform ">
  ...
  <process-engine name="default">
    ...
    <plugins>
      <plugin>
        <class>org.operaton.connect.plugin.impl.ConnectProcessEnginePlugin</class>
      </plugin>
    </plugins>
    ...
  </process-engine>
</bpm-platform>
```

:::note
  When using a pre-built distribution of Operaton, the plugin is already pre-configured.
:::


# Use Connectors

To use a connector, you have to add the Operaton extension element [connector](../../reference/bpmn20/custom-extensions/extension-elements.md#operaton-connector). The connector is configured by a unique [connectorId](../../reference/bpmn20/custom-extensions/extension-elements.md#operaton-connectorid), which specifies the used connector implementation. The ids of the currently supported connectors can be found at the beginning of this section. Additionally, an [input/output mapping](../process-engine/variables.md#input-output-variable-mapping) is used to configure the connector. The required input parameters and the available output parameters depend on the connector implementation. Additional input parameters can also be provided to be used within the connector.

As an example, a shortened configuration of the Operaton SOAP connector implementation is shown. A complete [example](https://github.com/operaton/operaton-bpm-examples/tree/master/servicetask/soap-service) can be found in the [Operaton examples repository](https://github.com/operaton/operaton-bpm-examples) on GitHub.

```xml
<serviceTask id="soapRequest" name="Simple SOAP Request">
  <extensionElements>
    <operaton:connector>
      <operaton:connectorId>soap-http-connector</operaton:connectorId>
      <operaton:inputOutput>
        <operaton:inputParameter name="url">
          http://example.com/webservice
        </operaton:inputParameter>
        <operaton:inputParameter name="payload">
          <![CDATA[
            <soap:Envelope ...>
              ... // the request envelope
            </soap:Envelope>
          ]]>
        </operaton:inputParameter>
        <operaton:outputParameter name="result">
          <![CDATA[
            ... // process response body
          ]]>
        </operaton:outputParameter>
      </operaton:inputOutput>
    </operaton:connector>
  </extensionElements>
</serviceTask>
```

A full [example](https://github.com/operaton/operaton-bpm-examples/tree/master/servicetask/rest-service) of the REST connector can also be found in the [Operaton examples repository](https://github.com/operaton/operaton-bpm-examples) on GitHub.
