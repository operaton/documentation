---

title: 'FEEL Engine Legacy Behavior'
sidebar_position: 50

menu:
  main:
    name: "Legacy Behavior"
    identifier: "user-guide-dmn-engine-feel-legacy-behavior"
    parent: "user-guide-dmn-engine-feel"

---

The FEEL engine supports a legacy mode that restores an older evaluation behavior for FEEL expressions.
This is primarily useful when migrating DMN models that rely on the legacy FEEL semantics.

To enable the legacy mode, set the [`dmnFeelEnableLegacyBehavior`][legacy behavior flag] flag in the
process engine configuration.

To enable this behavior in a standalone DMN Engine setup, refer to the `DefaultDmnEngineConfiguration`
[enableFeelLegacyBehavior][fluent feel flag setter] and [setEnableFeelLegacyBehavior][feel flag setter]
methods.

:::note[Heads Up!]
By using the legacy FEEL Engine, the Operaton DMN Engine **only** supports `FEEL` for
<a href="../../../reference/dmn/decision-table/rule.md#input-entry-condition">Input Entries</a> of a decision table – this corresponds to FEEL
simple unary tests.
:::

[legacy behavior flag]: ../../../reference/deployment-descriptors/tags/process-engine.mdx#dmnFeelEnableLegacyBehavior
[fluent feel flag setter]: https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/DefaultDmnEngineConfiguration.html#enableFeelLegacyBehavior
[feel flag setter](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/DefaultDmnEngineConfiguration.html#setEnableFeelLegacyBehavior)
