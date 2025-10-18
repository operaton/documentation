---

title: "Remote Engine Distribution"
sidebar_position: 5
description: "Install Operaton Run, an easy to configure remote engine distribution of Operaton. No Java knowledge necessary."

---
# Install Operaton Run

:::note[What is a Remote Engine Distribution?]
If you need a Remote or Shared Engine Distribution depends on your use-case. Check out the [architecture overview](../introduction/architecture.md) for more information.
:::note

This page describes the steps to execute Operaton Run.

# Requirements
Please make sure that you have the Java Runtime Environment 17 installed.

You can verify this by using your terminal, shell, or command line:

```sh
java -version
```
If you need to install Java Runtime Environment, you can [find the download from Oracle here](https://www.oracle.com/java/technologies/javase-downloads.html).

# Installation Procedure
1. Download the pre-packed distribution of  [Operaton here](https://operaton.org/download/).
2. Unpack the distro to a directory.
3. Configure the distro as described in the [User Guide](../user-guide/operaton-bpm-run.md).
4. Start Operaton Run by executing the start script (start.bat for Windows, start.sh for Linux/Mac).
5. Access the Operaton webapps (Cockpit, Tasklist, Admin) via http://localhost:8080/operaton/app/.
6. Access the [REST API](../reference/rest/overview/index.md) via http://localhost:8080/engine-rest (e.g. http://localhost:8080/engine-rest/engine).
