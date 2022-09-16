# PLBuildings server
## Description
API server which is responsible for obtaining buildings data for [JOSM PLBuildings Plugin](https://github.com/praszuk/josm-plbuildings-plugin)    

Currently, only BDOT is available as a data source.
It fetches data from the [budynki](https://budynki.openstreetmap.org.pl/) page,
which has previously processed and parsed it. 

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
```

### Run development
```
docker-compose -f docker-compose-dev.yml -p dev up
```

### Run production
```
PORT=80 docker-compose -f docker-compose-prod.yml -p prod up -d
```

## License
[GPLv3](LICENSE)