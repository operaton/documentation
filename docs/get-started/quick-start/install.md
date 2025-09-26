---
title: 'Download and Installation'
sidebar_position: 1
---
# Download and Installation (1/6)

First, you need to install the Operaton Platform and the Camunda Modeler.

In the following section, we'll describe how to install the Operaton Platform locally on your machine.

:::note[Hint]
If you prefer, you can also run the Operaton Platform with Docker:

```sh
docker pull operaton/operaton:latest
docker run -d --name camunda -p 8080:8080 operaton/operaton:run-latest
```

Afterwards, you can [install the Camunda Modeler](#camunda-modeler).

[More information regarding the docker image](https://hub.docker.com/r/operaton/operaton)
:::


# Prerequisites

Please make sure you have the following installed:

* Java Runtime Environment 11

You can verify this by using your terminal, shell, or command line:

```sh
java -version
```
If you need to install Java Runtime Environment, you can [find the download from Oracle here](https://www.oracle.com/technetwork/java/javase/downloads/index.html).

:::note[Supported Java versions]
Make sure to use a Java version from [Operaton's list of supported environments](/docs/documentation/introduction/supported-environments/#java-runtime).
:::

# Operaton Platform

First, download a distribution of the Operaton Platform. You can choose from different distributions for [various application servers](/docs/documentation/installation/full/). In this tutorial, we'll use Operaton Platform Run. Download it from [the download page](https://camunda.com/download/).

After downloading the distribution, unpack it inside a directory of your choice.

After you've successfully unpacked your distribution of the Operaton Platform, execute the script named `start.bat` (for Windows users) or `start.sh` (for Unix users).

This script will start the application server. Open your web browser and navigate to [http://localhost:8080/](http://localhost:8080/) to visit the Welcome Page.

# Camunda Modeler

Download the Camunda Modeler from [the download page](https://camunda.com/download/modeler/).

After downloading the Modeler, simply unzip the download in a folder of your choice.

After you have successfully unpacked the zip, run `camunda-modeler.exe` (for Windows users), `camunda-modeler.app` (for Mac users), or `camunda-modeler.sh` (for Linux users).

:::note[Next Step]
Once you've installed the Operaton Platform and the Camunda Modeler, you can move to the next step to [model and execute your first process](/docs/get-started/quick-start/service-task/).
:::
