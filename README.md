# PLBuildings server
## Description
API server which is responsible for obtaining buildings data for [JOSM PLBuildings Plugin](https://github.com/praszuk/josm-plbuildings-plugin)    

It uses [BDOT](https://budynki.openstreetmap.org.pl/) and [EGiB](https://github.com/praszuk/egib-plbuildings) as a data sources.

## How to use it
### Example .env file
```
# Database
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_USER=database_user
POSTGRES_PASSWORD=database_password
# External servers
BUDYNKI_SERVER_URL=https://budynki.openstreetmap.org.pl
EGIB_PLBUILDINGS_SERVER_URL=https://egib
```
You can also add variables for docker.
It prevents a permissions error (read-only files) on e.g. creating migrations
from container.
Note: Below are default – not needed to set.
```
USER_ID=1000
GROUP_ID=1000
```

### Run development
_Note: Port 8080_
```
docker-compose -f docker-compose-dev.yml -p dev up
```

### Run production
```
PORT=80 docker-compose -f docker-compose-prod.yml -p prod up -d
```

## License
[GPLv3](LICENSE)