---

title: 'Download and Installation'
sidebar_position: 10

menu:
  main:
    name: "Download and Installation"
    parent: "get-started-dmn"
    identifier: "get-started-dmn-install"
    description: "Install the Operaton Platform and Operaton Modeler on your machine."

aliases: [/dmn/install/]
---

First you need to set up your development environment and install the Operaton Platform and the Operaton Modeler.


## Prerequisites

Make sure you have the following set of tools installed:

* Java JDK 11+,
* Apache Maven (optional, if not installed you can use embedded Maven inside Eclipse.)
* A modern web browser (recent Firefox, Chrome or Microsoft Edge will work fine)
* Eclipse integrated development environment (IDE)


## Operaton Platform

First, download a distribution of the Operaton Platform. You can choose from different distributions for various application servers. In this tutorial, we will use the Apache Tomcat based distribution. Download it from [the latest Operaton release](https://github.com/operaton/operaton/releases/latest).

After having downloaded the distribution, unpack it inside a directory of your choice. We will call that directory `$OPERATON_HOME`.

After you have successfully unpacked your distribution of the Operaton Platform, execute the script named `start.bat` (for Windows users) or `start.sh` (for Unix users).

This script will start the application server and open a welcome screen in your web browser. If the page does not open, go to [http://localhost:8080/operaton-welcome/index.html](http://localhost:8080/operaton-welcome/index.html).

:::note[Getting Help]
If you have trouble setting up the Operaton Platform, you can ask for assistance in the [Operaton Users Forum](https://forum.operaton.org/).
:::

## Operaton Modeler

Follow the instructions in the [Operaton Modeler](../../documentation/installation/operaton-modeler) section.
