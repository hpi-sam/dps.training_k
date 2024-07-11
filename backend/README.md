# Klinik-dPS Backend
The simulation logic and database management for the K-dPS project. For the interactive website see the [frontend folder](../frontend/README.md).

For general information on the project like e.g. licensing information or future plans, see the [Project README](../README.md).

## Setup
### Install Python
- install from official [python website](https://www.python.org/downloads/)
- version should be at least 3.12


### Install requirements
- navigate into backend folder
- `pip install -r requirements.txt`

### Setup Black Formatter
We are using black as a biased formatter for the whole project. For more information about black see: [Black](https://black.readthedocs.io/en/stable/)
- make sure you have python extension installed
- download "Black Formatter" from marketplace
- right-click on a python file
- select "Format Document with"
- select "Configure Default formatter"
- select "Black"
- head to VS Code settings
- search for "format on save"
- enable "Editor: Format on Save"

## Running the project using Docker
Running the project without docker is currently not tested/supported. 
For more information on the difference between `prod` and `dev`, see the [docs file](../docs/deployment-process.md).
Note that the `prod` env file here still assumes this is running locally - 
meaning it will expect the frontend to run on localhost.

Build and run:
```bash
docker compose --env-file .env.<prod/dev> up
```

Optionally, to access the database, create a superuser account: 
```bash
docker exec -it K-dPS-django python manage.py createsuperuser
```
Afterwards, you can log into the admin interface at e.g. `http://localhost:80/admin/`<br/>
Note: this is only available if DEBUG = true, which is the case in the dev environment.


## Development

### Migrations
When changing models, you need to create migrations in order to update existing databases.
- Create new migrations: `docker exec -it K-dPS-django python manage.py makemigrations`
- Optionally, if you have conflicting migrations: `docker exec -it K-dPS-django python manage.py migrate --merge`
- Execute these migrations to update the database: `docker exec -it K-dPS-django python manage.py migrate`

### Running Tests
- start docker container with docker compose(see Running the project using Docker)
- wait until Application Startup is Completed
- run: `docker exec -it K-dPS-django python manage.py test`

### Working with Fixtures
- (clear database)
- fill database with data you want to export as fixture (e.g. `docker exec -it K-dPS-django python manage.py import_patient_states`)
  - if updating a fixture that is used by a model that doesn't allow null fields, make them nullable, migrate and discard the migration file 
    afterwards.
- create fixture: 
  - `docker exec -it K-dPS-django bash`
  - `export PYTHONIOENCODING=utf8`
  - `python manage.py dumpdata template > patient_states.json`
- move the fixture to the "fixtures" directory
- now you can load it: `docker exec -it K-dPS-django python manage.py loaddata patient_states.json`
