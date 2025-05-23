---

title: 'Time zones'
sidebar_position: 255

---

## Process engine

The Operaton engine uses the default time zone of the JVM when operating with dates:

* When reading datetime values from BPMN XML
* In REST responses
* When reading/writing DateTime values from/to the database

## Database

Database time zone and database sessions time zone are out of scope of the Operaton engine and must be configured explicitly.

However, Timestamp columns in the Operaton engine are using the `TIMESTAMP [WITHOUT TIME ZONE]` data type (the name differs in different database servers).
For this reason, it is not recommended to change the time zone on the database side once set, since it may lead to an incorrect operation of the Operaton engine.

:::warning[Daylight Saving Time]
Timezone information is not saved in the timestamp columns. In order to avoid ambiguous timestamps, it is recommended to use a timezone like `UTC` as the JVM's default timezone
that is not adjusted for `Daylight Saving Time (DST)` and therefore cannot produce ambiguous timestamps.

If this is not an option in your setting, please consider disabling the [JobExecutor](../user-guide/process-engine/the-job-executor.md) during the DST switch in order
to avoid unexpected job executions.
:::

## Operaton Web Applications

It is possible to use the Operaton Web Applications in different timezones. All dates are translated to/from the local timezone when working with the UI.

## Cluster Setup

In case the process engine is running in a [cluster](../introduction/architecture.md#clustering-model),
all cluster nodes must run in one and the same time zone. In case cluster nodes exist in different time zones,
correct behaviour when operating with DateTime values can not be guaranteed.