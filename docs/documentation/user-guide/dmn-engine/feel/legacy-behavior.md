---

title: 'FEEL Engine Legacy Behavior'
sidebar_position: 50

menu:
  main:
    name: "Legacy Behavior"
    identifier: "user-guide-dmn-engine-feel-legacy-behavior"
    parent: "user-guide-dmn-engine-feel"
    description: "Only relevant for users coming from Operaton version <= 7.12.0"

---

If you come from a Operaton version $\leq$ 7.12.x and already use FEEL, it might be that you need to
migrate your DMN models. To do this, please check out the [Migration Guide], where we've documented
all breaking changes.

If you don't want to migrate your DMN models right now, you can also restore the legacy FEEL
behavior by flipping a config flag:

* To see how this legacy behavior can be enabled again in Operaton, please see the
[dmnFeelEnableLegacyBehavior][legacy behavior flag] engine configuration property.
* To enable this behavior in a standalone DMN Engine setup, please refer to the `DefaultDmnEngineConfiguration`
[enableFeelLegacyBehavior][fluent feel flag setter] and [setEnableFeelLegacyBehavior][feel flag setter]
methods

:::note[Heads Up!]
By using the legacy FEEL Engine, the Operaton DMN Engine **only** supports `FEEL` for
<a href="../../../reference/dmn/decision-table/rule.md#input-entry-condition">Input Entries</a> of a decision table – this corresponds to FEEL
simple unary tests.
:::

[legacy behavior flag]: ../../../reference/deployment-descriptors/tags/process-engine.mdx#dmnFeelEnableLegacyBehavior
[fluent feel flag setter]: https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/DefaultDmnEngineConfiguration.html#enableFeelLegacyBehavior
[feel flag setter](https://docs.operaton.org/reference/latest/javadoc/org/operaton/bpm/dmn/engine/impl/DefaultDmnEngineConfiguration.html#setEnableFeelLegacyBehavior)
