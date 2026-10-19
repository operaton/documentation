---

title: 'Getting a Distribution'
sidebar_position: 10

menu:
  main:
    identifier: "embedded-forms-ref-integration-download"
    parent: "embedded-forms-ref-integration"

---

# Source

The Forms SDK source is maintained in the
[Operaton repository](https://github.com/operaton/operaton/tree/main/webapps/frontend/operaton-bpm-sdk-js).

Operaton does not currently publish a standalone Bower package or a separate Bower release repository.
Use the SDK files from your Operaton distribution, or build them from the source tree when embedding
forms in a custom application.


# Dependency Management

The Forms SDK depends on the following libraries:

* JQuery (or a compatible DOM manipulation Library).

The Forms SDK *optionally* depends on the following libraries:

* AngularJS (v1.2.16).


# Including the Library

Next, you need to add the JavaScript Library to the page.

```html
<script src="jquery-2.1.1.min.js" type="text/javascript"></script>
<script src="operaton-bpm-sdk.min.js" type="text/javascript"></script>
```

Or, with AngularJS Support:

```html
<script src="angular.min.js" type="text/javascript"></script>
<script src="operaton-bpm-sdk-angular.js" type="text/javascript"></script>
```
