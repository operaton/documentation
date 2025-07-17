---

title: "Docker"
sidebar_position: 20
description: "Run the Full Distribution using Docker"

---
# Run Operaton using Docker

## Community Edition

The Community Edition docker images can be found on [GitHub](https://github.com/operaton/docker-operaton-bpm-platform) and [Docker Hub](https://hub.docker.com/r/operaton/operaton/).

## Start Operaton Run using Docker

To start [Operaton Run](../user-guide/operaton-bpm-run.md) execute the following commands:

```shell
docker pull operaton/operaton:run-latest
docker run -d --name Operaton-p 8080:8080 operaton/operaton:run-latest
```

## Start Operaton(Tomcat) using Docker

To start Operaton, execute the following commands:

```shell
docker pull operaton/operaton:latest
docker run -d --name Operaton-p 8080:8080 operaton/operaton:latest
```

Please note that by default the Apache Tomcat distribution is used. For a guide on how to use one of the other distributions, see the [tag schema](https://github.com/operaton/docker-operaton-bpm-platform#supported-tagsreleases).
