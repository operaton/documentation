---

title: 'Extension Attributes'
sidebar_position: 60

menu:
  main:
    identifier: "user-guide-dmn-model-api-extension-attributes"
    parent: "user-guide-dmn-model-api"

---


[Custom extensions](../../../reference/dmn/custom-extensions/index.md) are a standardized way to extend the DMN model.
The [Operaton extension attributes](../../../reference/dmn/custom-extensions/operaton-attributes.md) are fully implemented in the DMN model API.

Every DMN `Decision` element can have the attributes `historyTimeToLive` and `versionTag`.
To access the extension attributes, you have to call the `Decision#getOperatonHistoryTimeToLiveString()` and
`Decision#getVersionTag()` methods.

```java
String historyTimeToLive = decision.getOperatonHistoryTimeToLiveString();
String versionTag = decision.getVersionTag();
```
To set attributes, use `Decision#setOperatonHistoryTimeToLiveString()` and `Decision#setVersionTag()`
```java
decision.setOperatonHistoryTimeToLiveString("1000");
decision.setVersionTag("1.0.0");
```

Every `Input` element can have an `inputVariable` attribute.
This attribute specifies the variable name which can be used to access the result of the input expression in an input entry expression.
It can be set and fetched similarly, calling `Input#setOperatonInputVariable()` and `Input#getOperatonInputVariable()`:

```java
input.setOperatonInputVariable("operatonInput");
String operatonInput = input.getOperatonInputVariable();
```
