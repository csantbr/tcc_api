# Judge API

## Setup

The first step is install poetry and then install the project dependencies

```shell
$ pip install poetry
$ make setup
```

After installing poetry and the dependencies, you need to start docker.

```shell
$ docker-compose up -d
```

After this, run the backend:

```shell
$ make run
```

After start backend, run worker:

```shell
$ make run-worker
```
