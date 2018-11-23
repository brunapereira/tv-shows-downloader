# TV Shows Downloader

#### Dependences
 - python >= 3.4
 - aria2 => 1.34.0

#### Docker dependences
- Docker Engine CE >= 18.09.0
- docker-compose version 1.23.1

#### Build docker images
```
$ make docker-prepare
```

#### Executing routines with docker-compose
```
$ docker-compose run --rm --service-ports app python3 <path-to-routine>
```
