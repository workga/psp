### Requirements
- python 3.11
- npm 20.7.0

Backend API and admin panel are available on localhost:9080
The project is configured only for development!


### Initialization
```bash
make init
make prepare
```

### Local run
Firstly, run backend (available on localhost:9080):
```bash
make backend
```

Secondly, Run frontend (available on localhost:9000):
```bash
make frontend
```

Admin panel is available on ```ocalhost:9080/admin```. Use admin credentials:
```
email: admin@example.com
password: admin_profile
```

You also can register new profile or use existing profiles with credentials:
```
email: testing0@example.com
password: testing_profile

...

email: testing9@example.com
password: testing_profile
```