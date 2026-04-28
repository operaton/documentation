---

title: "Quarkus Version Compatibility"
sidebar_position: 10

menu:
  main:
    name: "Version Compatibility"
    identifier: "user-guide-quarkus-version-compatibility"
    parent: "user-guide-quarkus-integration"

---

Each version of the Operaton Engine Quarkus Extension is bound to a specific version of Operaton and Quarkus.
Only these default combinations are recommended (and supported) by Operaton.

<table class="table table-striped">
  <tr>
    <th>Operaton version</th>
    <th>Quarkus version</th>
  </tr>
  <tr>
    <td>1.0.0</td>
    <td>3.28.3</td>
  </tr>
  <tr>
    <td>1.0.1</td>
    <td>3.28.5</td>
  </tr>
  <tr>
    <td>1.0.2</td>
    <td>3.28.5</td>
  </tr>
  <tr>
    <td>1.0.3</td>
    <td>3.28.5</td>
  </tr>
  <tr>
    <td>1.1.0</td>
    <td>3.30.8</td>
  </tr>
  <tr>
    <td>1.1.1</td>
    <td>3.30.8</td>
  </tr>
  <tr>
    <td>1.1.2</td>
    <td>3.30.8</td>
  </tr>
  <tr>
    <td>2.0.0</td>
    <td>3.32.0</td>
  </tr>
  <tr>
    <td>2.1.0</td>
    <td>3.33.1 (LTS)</td>
  </tr>
</table>

In case a certain Quarkus version has a bug, you can override the existing Quarkus version by adding the following
inside your `pom.xml`. Note that this new Operaton/Quarkus version combination should also be supported by Operaton.

```xml
<dependencyManagement>
  <dependencies>
    ...
    <dependency>
      <groupId>io.quarkus.platform</groupId>
      <artifactId>quarkus-bom</artifactId>
      <version>${quarkus.framework.version}</version><!-- set correct version here -->
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    ...
  </dependencies>
</dependencyManagement>
```
