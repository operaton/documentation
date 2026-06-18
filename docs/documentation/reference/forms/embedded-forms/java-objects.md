---

title: 'Working with Java Objects'
sidebar_position: 50

menu:
  main:
    identifier: "embedded-forms-ref-java-objects"
    parent: "embedded-forms-ref"

---

This section explains how to work with serialized Java objects in embedded task forms.

:::note
Out of the box, you can only work with Java objects that are serialized in *JSON format*.
If Java classes are serialized using JAX-B, you need to add custom XML parsing and writing logic
to the embedded form. Java objects serialized using Java Serialization cannot be used in forms.
:::


## Fetching an Existing Serialized Java Object Variable

The Form SDK will only fetch variables that are actually used in a form. Since a complex Java
object is usually not bound to a single input field, we cannot use the `cam-variable-name` directive.
Therefore, we need to fetch the variable programmatically:

```html
<script cam-script type="text/form-script">
  camForm.on('form-loaded', function() {
    // tell the form SDK to fetch the variable named 'invoiceData'
    camForm.variableManager.fetchVariable('invoiceData');
  });
  camForm.on('variables-fetched', function() {
    // work with the variable (bind it to the current AngularJS $scope)
    $scope.invoiceData = camForm.variableManager.variableValue('invoiceData');
  });
</script>
```


## Creating a New Serialized Java Object

In case the variable does not yet exist (for instance in a Start Form), you have to create the variable and specify the necessary metadata in order for the process engine to correctly handle the variable as a Java object.

```html
<script cam-script type="text/form-script">

  var dataObject = $scope.dataObject = {};

  camForm.on('form-loaded', function() {

    // declare variable 'customerData' including metadata for serialization
    camForm.variableManager.createVariable({
      name: 'customerData',
      type: 'Object',
      value: dataObject,
      valueInfo: {
        // indicate that object is serialized as JSON
        serializationDataFormat: 'application/json',
        // provide class name of Java object to map to
        objectTypeName: 'org.operaton.bpm.example.CustomerData'
      }
    });

  });

</script>
```
