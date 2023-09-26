### Requirements
- python 3.11
- npm 20.7.0
- docker 20

### Run in docker
Run application in docker:
```bash
make docker-build
make docker-up
```
Application is available on localhost:9000

You need to run ```make docker-build``` after changing dependencies, but changes in the code appear in running containers automatically.

The current docker configuration is intended only for development, but not for production.


### Local run
Backend on localhost:8080
```bash
make init-backend
. .venv/bin/activate
make backend
```

Frontend on localhost:8090
```bash
make init-frontend
. .venv/bin/activate
make frontend
```