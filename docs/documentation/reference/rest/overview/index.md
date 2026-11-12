---

title: "Overview"
sidebar_position: 10

---

The goal of the REST API is to provide access to all relevant interfaces of the engine.


## Structure

These documents explain all existing methods in the REST API. For each method they provide:

* An informal description
* HTTP verb and URL
* Possible query, path or message body parameters
* A detailed description of the response content
* Possible response codes
* A brief example request and response


## Engine Usage

The methods as described work on the default process engine as given by the available `ProcessEngineProvider` service.

You may prepend `/engine/{name}` to any of the methods (unless otherwise documented) to access another engine where `{name}` is the name of the process engine as returned by `ProcessEngine#getName()`, e.g., `/engine/myEngineName/task`.


## Error Handling

For every method this documentation gives possible HTTP status codes. The error explanations do not cover all possible error causes that may arise when the request is served, for example, most of the requests will not work properly if there are problems with database access. Any of these undocumented errors will be translated to a HTTP 500 error.

### Error Response Body

Errors are returned with the content type `application/json`, regardless of the media type requested by the client. The response body has the following form:

```json
{
  "type" : "SomeExceptionClass",
  "message" : "a detailed message",
  "code" : 10000
}
```

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>type</td>
    <td>String</td>
    <td>
      The simple class name of the exception that caused the error, e.g., <code>AuthorizationException</code>.
      If the REST API wraps an engine exception, this is the name of the wrapping exception
      (<code>InvalidRequestException</code> or <code>RestException</code>), not the name of the engine exception.
    </td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>
      A human-readable error message. The message is meant for logging and display; it may change with
      newer versions, so do not parse it in your client.
    </td>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>
      A numeric code identifying the error, or <code>null</code> if the error did not originate from
      the process engine. See <a href="#exception-codes">Exception Codes</a>.
    </td>
  </tr>
</table>

Some exception types extend this body with additional properties. These are described in the sections below.

### HTTP Status Codes

The REST API maps exceptions to HTTP status codes as follows:

<table class="table table-striped">
  <tr>
    <th>Status</th>
    <th>Cause</th>
    <th>Response body</th>
  </tr>
  <tr>
    <td>400 Bad Request</td>
    <td>
      Invalid request parameters or request body, e.g., malformed JSON, invalid variable values, or an exceeded
      <a href="#query-maximum-results-limit-exceptions">query maximum results limit</a>.
      Engine exceptions of type <code>BadUserRequestException</code> and its subclasses
      (e.g., <code>NotValidException</code>, <code>NotFoundException</code>), as well as
      <a href="#parse-exceptions"><code>ParseException</code></a> and the
      <a href="#migration-validation-exceptions">migration validation exceptions</a>.
    </td>
    <td>Error response body; specific properties for parse and migration validation exceptions</td>
  </tr>
  <tr>
    <td>401 Unauthorized</td>
    <td>
      <a href="/docs/documentation/reference/rest/overview/authentication">Authentication</a> is enabled and the request does not contain valid credentials.
    </td>
    <td>No body; the <code>WWW-Authenticate</code> response header contains the authentication challenge</td>
  </tr>
  <tr>
    <td>403 Forbidden</td>
    <td>
      The authenticated user lacks a required permission
      (<a href="#authorization-exceptions"><code>AuthorizationException</code></a>), or the operation is
      forbidden for other reasons documented for the specific method.
    </td>
    <td>Error response body; specific properties for <code>AuthorizationException</code></td>
  </tr>
  <tr>
    <td>404 Not Found</td>
    <td>
      The resource addressed by the request path does not exist, e.g., a process instance with the given id,
      or the process engine addressed as described in <a href="#engine-usage">Engine Usage</a>. Also returned for unknown URLs.
    </td>
    <td>Error response body</td>
  </tr>
  <tr>
    <td>405, 406, 415</td>
    <td>
      The HTTP method is not supported for the URL, the requested media type cannot be produced,
      or the request content type is not supported.
    </td>
    <td>Error response body</td>
  </tr>
  <tr>
    <td>500 Internal Server Error</td>
    <td>
      Any other error, e.g., database problems or an <code>OptimisticLockingException</code>.
    </td>
    <td>Error response body</td>
  </tr>
</table>

Note the following details:

* **Not found is not always 404.** By default, an engine `NotFoundException` results in `400 Bad Request`, because it is a subclass of `BadUserRequestException`. Methods that address a resource by its id in the request path translate this into `404 Not Found`. A missing entity referenced elsewhere in the request, for example by an id in the request body, usually results in a `400 Bad Request`. Check the documentation of the specific method for the status codes it returns.
* **Optimistic locking.** If a concurrent modification is detected, the request fails with `500 Internal Server Error` and `code` `1`. The client can usually retry such a request. See [Optimistic Locking](../../../user-guide/process-engine/transactions-in-processes.md#optimistic-locking).
* **Malformed JSON.** If the request body is not valid JSON or does not match the expected structure, the response is `400 Bad Request` with type `InvalidRequestException`, an empty `message`, and `code` `null`.

### Exception Codes

Whenever an error originates from the process engine, the REST API exposes a property `"code"` with a
numeric code as value in the response body of the failed request. Like this, your client application can
handle the error in a reliable and automated fashion. The `type` property might be too coarse-grained, and
the `message` property might change with newer versions.

If no specific code applies, `code` is `0`. Notable built-in codes are:

| Code | Meaning |
|---|---|
| `0` | Fallback, no specific code assigned |
| `1` | Optimistic locking: the entity was modified concurrently |
| `10000` | Database deadlock |
| `10001` | Foreign key constraint violation |
| `10002` | Column size too small for the value |
| `20000` – `39999` | Range for custom codes defined by your application |

If the error did not originate from the process engine, `code` is `null`. This applies to errors raised by
the REST API itself (e.g., invalid request parameters, malformed JSON, unknown URLs, or unsupported media types)
and to unexpected server errors. Your client should therefore handle a `null` value.

You can look up the meaning of all built-in codes and learn how to add custom codes in the
[User Guide](../../../user-guide/process-engine/error-handling.md#exception-codes).

### Handling Errors in a Client

To handle errors reliably, a client should:

1. Evaluate the HTTP status code first.
2. Use the `code` property to identify specific engine errors, such as optimistic locking (`1`) or [custom exception codes](../../../user-guide/process-engine/error-handling.md#exception-codes) your application defines.
3. Use the `type` property for coarse-grained distinctions, and to detect responses with additional properties (e.g., `AuthorizationException`, `ParseException`).
4. Treat `message` as informational text only.

### Authorization Exceptions

If an already authenticated user interacts with a resource in an unauthorized way, the status code of the response will be set to `403 Forbidden`. Details about the unauthorized interaction are provided in the response body.

#### Type

`AuthorizationException`

#### Response Body

In addition to the properties `type`, `message`, and `code`, the response body contains:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>userId</td>
    <td>String</td>
    <td>The id of the user that does not have the required permissions.</td>
  </tr>
  <tr>
    <td>missingAuthorizations</td>
    <td>Array</td>
    <td>
      A JSON array of objects, each with the properties <code>permissionName</code>, <code>resourceName</code>,
      and <code>resourceId</code>. The user needs <strong>at least one</strong> of the listed permissions to
      perform the operation.
    </td>
  </tr>
  <tr>
    <td>permissionName<br/>resourceName<br/>resourceId</td>
    <td>String</td>
    <td>
      <strong>Deprecated</strong>, use <code>missingAuthorizations</code> instead. These properties are only set
      if exactly one authorization is missing; otherwise they are <code>null</code>.
    </td>
  </tr>
</table>

#### Example

```json
{
  "type" : "AuthorizationException",
  "message" : "The user with id 'jonny' does not have 'DELETE' permission on resource 'Mary' of type 'User'.",
  "code" : 0,
  "userId" : "jonny",
  "permissionName" : "DELETE",
  "resourceName" : "User",
  "resourceId" : "Mary",
  "missingAuthorizations" : [
    {
      "permissionName" : "DELETE",
      "resourceName" : "User",
      "resourceId" : "Mary"
    }
  ]
}
```

### Migration Validation Exceptions

If a migration plan from one process definition version to another is not
valid, a migration exception is thrown. It can be a *migration plan validation
exception* where the plan itself is not valid, e.g., it contains an invalid
instruction. Or it can be a *migrating process instance validation exception* when a
migration plan cannot be applied to a specific process instance, e.g., an active
activity was not mapped by the migration plan. In both cases, the status code
of the response is set to `400 Bad Request`.

### Migration Plan Validation Exceptions

#### Type

`MigrationPlanValidationException`

#### Response Body

A JSON object with the following properties:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>type</td>
    <td>String</td>
    <td>The type of exception, here <code>MigrationPlanValidationException</code>.</td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>The error message.</td>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>
        The code allows your client application to identify the error in an automated fashion.
        See <a href="#exception-codes">Exception Codes</a>.
    </td>
  </tr>
  <tr>
    <td>validationReport</td>
    <td>Object</td>
    <td>
      A JSON object containing details about all detected validation errors.
      Its properties are described below.
    </td>
  </tr>
</table>

Every validation report object contains the following properties:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>instructionReports</td>
    <td>Array</td>
    <td>
      A JSON array describing a single instruction validation report.
      Each report object consists of an <code>instruction</code> that is
      invalid and a <code>failures</code> array containing the validation
      messages for this instruction.
    </td>
  </tr>
  <tr>
    <td>variableReports</td>
    <td>Object</td>
    <td>
      A JSON object containing variable key-value pairs. Each key is the name of a variable that
      cannot be set on the migrated process instances. Each value is a JSON object with the properties
      <code>type</code>, <code>value</code>, and <code>valueInfo</code> of the variable and a
      <code>failures</code> array containing the validation messages for this variable.
    </td>
  </tr>
</table>

#### Example

```json
{
  "type": "MigrationPlanValidationException",
  "message": "ENGINE-23001 Migration plan for process definition 'invoice:1:8aa1533c-23e5-11e6-abb7-f6aefe19b687' to 'invoice:2:8accd012-23e5-11e6-abb7-f6aefe19b687' is not valid:\n\t Migration instruction MigrationInstructionImpl{sourceActivityId='approveInvoice', targetActivityId='assignApprover', updateEventTrigger='false'} is not valid:\n\t\tActivities have incompatible types (UserTaskActivityBehavior is not compatible with DmnBusinessRuleTaskActivityBehavior)\n",
  "code" : 0,
  "validationReport": {
    "instructionReports": [
      {
        "instruction": {
          "sourceActivityIds": [
            "approveInvoice"
          ],
          "targetActivityIds": [
            "assignApprover"
          ],
          "updateEventTrigger": false
        },
        "failures": [
          "Activities have incompatible types (UserTaskActivityBehavior is not compatible with DmnBusinessRuleTaskActivityBehavior)"
        ]
      }
    ],
    "variableReports": {}
  }
}
```

### Migrating Process Instance Validation Exceptions

#### Type

`MigratingProcessInstanceValidationException`

#### Response Body

A JSON object with the following properties:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>type</td>
    <td>String</td>
    <td>The type of exception, here <code>MigratingProcessInstanceValidationException</code>.</td>
  </tr>
  <tr>
    <td>code</td>
    <td>Number</td>
    <td>
        The code allows your client application to identify the error in an automated fashion.
        See <a href="#exception-codes">Exception Codes</a>.
    </td>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>The error message.</td>
  </tr>
  <tr>
    <td>validationReport</td>
    <td>Object</td>
    <td>
      A JSON object containing details about all detected validation errors.
      Its properties are described below.
    </td>
  </tr>
</table>

Every validation report object contains the following properties:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>processInstanceId</td>
    <td>String</td>
    <td>The id of the process instance that cannot be migrated when following the migration plan.</td>
  </tr>
  <tr>
    <td>failures</td>
    <td>Array</td>
    <td>
      An array of general failure messages, which are not related to
      a specific activity or transition.
    </td>
  </tr>
  <tr>
    <td>activityInstanceValidationReports</td>
    <td>Array</td>
    <td>
      An array of JSON objects describing the single activity instance
      validation errors. Each activity instance validation report
      consists of a <code>migrationInstruction</code>, if the error is
      related to an existing migration instruction, the
      <code>activityInstanceId</code> and <code>sourceScopeId</code>
      of the activity which cannot be migrated and an array
      <code>failures</code>, which is a list of all validation error
      messages for this report.
    </td>
  </tr>
  <tr>
    <td>transitionInstanceValidationReports</td>
    <td>Array</td>
    <td>
      An array of JSON objects describing the single transition instance
      validation errors. Each transition instance validation report
      consists of a <code>migrationInstruction</code>, if the error is
      related to an existing migration instruction, the
      <code>transitionInstanceId</code> and <code>sourceScopeId</code>
      of the transition which cannot be migrated and an array
      <code>failures</code>, which is a list of all validation error
      messages for this report.
    </td>
  </tr>
</table>

#### Example

```json
{
  "type": "MigratingProcessInstanceValidationException",
  "message": "ENGINE-23004 Cannot migrate process instance '96dc383f-23eb-11e6-8e4a-f6aefe19b687':\n\tCannot migrate activity instance 'approveInvoice:f59925bc-23eb-11e6-8e4a-f6aefe19b687':\n\t\tThere is no migration instruction for this instance's activity\n\tCannot migrate transition instance 'f598897a-23eb-11e6-8e4a-f6aefe19b687':\n\t\tThere is no migration instruction for this instance's activity\n",
  "code": 0,
  "validationReport": {
    "processInstanceId": "96dc383f-23eb-11e6-8e4a-f6aefe19b687",
    "failures": [],
    "activityInstanceValidationReports": [
      {
        "migrationInstruction": null,
        "activityInstanceId": "approveInvoice:f59925bc-23eb-11e6-8e4a-f6aefe19b687",
        "sourceScopeId": "approveInvoice",
        "failures": [
          "There is no migration instruction for this instance's activity"
        ]
      }
    ],
    "transitionInstanceValidationReports": [
      {
        "migrationInstruction": null,
        "transitionInstanceId": "f598897a-23eb-11e6-8e4a-f6aefe19b687",
        "sourceScopeId": "ServiceTask_1",
        "failures": [
          "There is no migration instruction for this instance's activity"
        ]
      }
    ]
  }
}
```

### Parse Exceptions

If the process bpmn resource cannot be parsed during deployment, the deployment of it will fail and the status code of the response will be set to `400 Bad Request`. Details about the parsing problems are provided in the response body.

#### Type

`ParseException`

#### Response Body

In addition to the properties `type`, `message`, and `code`, the response body contains a `details` object. Each key is the name of a deployment resource. Each value is a JSON object with the arrays `errors` and `warnings`. Every entry of these arrays has the following properties:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>message</td>
    <td>String</td>
    <td>The message of the error or warning.</td>
  </tr>
  <tr>
    <td>line</td>
    <td>Number</td>
    <td>The line of the resource where the problem occurred.</td>
  </tr>
  <tr>
    <td>column</td>
    <td>Number</td>
    <td>The column of the resource where the problem occurred.</td>
  </tr>
  <tr>
    <td>mainElementId</td>
    <td>String</td>
    <td>The id of the main element causing the problem.</td>
  </tr>
  <tr>
    <td>elementIds</td>
    <td>Array</td>
    <td>The ids of all elements involved in the problem.</td>
  </tr>
</table>

#### Example

```json
{
  "type": "ParseException",
  "message": "ENGINE-09005 Could not parse BPMN process. Errors: Exclusive Gateway 'ExclusiveGateway_1' has outgoing sequence flow 'SequenceFlow_0' without condition which is not the default flow.",
  "code" : 0,
  "details": {
    "invoice.bpmn": {
      "errors": [
        {
          "message": "Exclusive Gateway 'ExclusiveGateway_1' has outgoing sequence flow 'SequenceFlow_0' without condition which is not the default flow.",
          "line": 77,
          "column": 15,
          "mainElementId": "ExclusiveGateway_1",
          "elementIds": [
            "ExclusiveGateway_1",
            "SequenceFlow_0"
          ]
        }
      ],
      "warnings": [
        {
          "message": "It is not recommended to use a cancelling boundary timer event with a time cycle.",
          "line": 87,
          "column": 20,
          "mainElementId": "BoundaryEvent_1",
          "elementIds": [
            "BoundaryEvent_1"
          ]
        }
      ]
    }
  }
}
```

### Query Maximum Results Limit Exceptions

When the [maximum results limit of a query](../../../user-guide/process-engine/process-engine-api.md#query-maximum-results-limit)
is exceeded, an exception is thrown which results in an HTTP status code 400.

## Authentication

The REST API ships with an implementation of [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). By default it is switched off (in the rest-api web application and therefore also in the pre-built Operaton distributions). You can activate it by adding a servlet filter as described in the [Authentication](authentication.md) section.
