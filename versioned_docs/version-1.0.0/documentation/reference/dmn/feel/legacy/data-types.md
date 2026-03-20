---

title: 'FEEL Data Types'
sidebar_position: 20

---

:::note[Heads Up!]
This page provides information on the legacy FEEL Engine, that was used before the
current <a href="../user-guide/dmn-engine/feel/index.md">Scala-based FEEL Engine</a>
was integrated into Operaton.
:::

The Operaton DMN engine supports the following FEEL data types.

## String

![Example img](../../../../../assets/documentation/reference/dmn/feel/legacy/string-type.png)String" class="no-lightbox

FEEL supports Strings. They must be encapsulated in double quotes. They
support only the equal [comparison] operator.

## Numeric Types

![Example img](../../../../../assets/documentation/reference/dmn/feel/legacy/integer-type.png)Integer" class="no-lightbox

FEEL supports numeric types like integer. In the Operaton DMN engine the
following numeric types are available:

- integer
- long
- double

Numeric types support all [comparison] operators and [ranges].

## Boolean

![Example img](../../../../../assets/documentation/reference/dmn/feel/legacy/boolean-type.png)Boolean" class="no-lightbox

FEEL supports the boolean value `true` and `false`. The boolean type only
supports the equal [comparison] operator.

## Date

![Example img](../../../../../assets/documentation/reference/dmn/feel/legacy/date-type.png)Date" class="no-lightbox

FEEL supports date types. In the Operaton DMN engine the following date types
are available:

- date and time

To create a date and time value, the function `date and time` has to be used
with a single String parameter. The parameter specifies the date and time in
the format `yyyy-MM-dd'T'HH:mm:ss`.

Date types support all [comparison] operators and [ranges].


[comparison]: ./language-elements.md#comparison
[ranges]: ./language-elements.md#range