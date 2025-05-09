---

title: 'Public API'
sidebar_position: 80

menu:
  main:
    identifier: "user-guide-introduction-public-api"
    parent: "user-guide-introduction"

---


Operaton provides a public API. This section covers the definition of the public API and backwards compatibility for version updates.


# Definition of Public API

The Operaton public API is limited to the following items:

Java API:

All non-implementation Java packages (package name does not contain `impl`) of the following modules.

* `operaton-engine`
* `operaton-engine-spring`
* `operaton-engine-cdi`
* `operaton-engine-dmn`
* `operaton-bpmn-model`
* `operaton-cmmn-model`
* `operaton-dmn-model`
* `operaton-spin-core`
* `operaton-connect-core`
* `operaton-commons-typed-values`

HTTP API (REST API):

* `operaton-engine-rest`: HTTP interface (set of HTTP requests accepted by the REST API as documented in [REST API reference](../reference/rest/index.md). Java classes are not part of the public API.


# Backwards Compatibility for Public API

The Operaton versioning scheme follows the MAJOR.MINOR.PATCH pattern put forward by [Semantic Versioning](http://semver.org/). Operaton will maintain public API backwards compatibility for MINOR version updates. Example: Update from version `7.1.x` to `7.2.x` will not break the public API.
