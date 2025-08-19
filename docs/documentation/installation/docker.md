---

title: "Docker"
sidebar_position: 20
description: "Run the Full Distribution using Docker"

---
# Run Operaton using Docker

The Community Edition docker images can be found on [Docker Hub](https://hub.docker.com/r/operaton/operaton/).

## Start Operaton using Docker

To start [Operaton](../user-guide/operaton-bpm-run.md) execute the following commands:

```shell
docker pull operaton/operaton:latest
docker run -d --name Operaton-p 8080:8080 operaton/operaton:latest
```
