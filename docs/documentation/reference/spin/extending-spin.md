---
title: "Extending Spin"
sidebar_position: 30

menu:
  main:
    identifier: "spin-ref-extending-spin"
    parent: "spin-ref"

---

## Configuring Data Formats

The data formats available to Spin may not always suit your needs. Sometimes, it is necessary to provide configuration. For example, when using Spin to map Java objects to JSON, a format for how dates are serialized has to be specified. While the Spin data formats use reasonable default values, they can also be changed.

To configure a data format detected by Spin, the SPI `org.operaton.spin.spi.DataFormatConfigurator` can be implemented. A configurator specifies which classes it can configure. Spin discovers a configurator by employing Java's service loader mechanism and will then provide it with all data formats that match the specified class (or are a subclass thereof). The concrete configuration options depend on the actual data format. For example, a Jackson-based JSON data format can modify the `ObjectMapper` that the data format uses.

To provide a custom configurator, you have to

* Provide a custom implementation of `org.operaton.spin.spi.DataFormatConfigurator`
* Add the configurator's fully qualified class name to a file named `META-INF/services/org.operaton.spin.spi.DataFormatConfigurator`
* Ensure that the artifact containing the configurator is reachable from Spin's class loader


## Custom Data Formats {#custom-dataformats}

A Spin data format is an implementation of the interface `org.operaton.spin.spi.DataFormat`. An implementation of this interface can be registered by implementing the SPI `org.operaton.spin.spi.DataFormatProvider`. Spin uses the Java platform's service loader mechanism to look up provider implementations at runtime.

To provide a custom data format, you have to

* Provide a custom implementation of `org.operaton.spin.spi.DataFormat`
* Provide a custom implementation of `org.operaton.spin.spi.DataFormatProvider`
* Add the provider's fully qualified class name to a file named `META-INF/services/org.operaton.spin.spi.DataFormatProvider`
* Ensure that the artifact containing the provider is reachable from Spin's class loader

If you now call `org.operaton.spin.DataFormats.getAvailableDataFormats()`, then the custom data format is returned along with the built-in data formats. Furthermore, `org.operaton.spin.DataFormats.getDataFormat(String dataFormatName)` can be used to explicitly retrieve the data format by name.
