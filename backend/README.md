# K-dPS Backend

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
- right click on a python file
- select "Format Document with"
- select "Configure Default formatter"
- select "Black"
- head to VS Code settings
- search for "format on save"
- enable "Editor: Format on Save"

## Running the project using Docker
Running the project without docker is currently not supported. For more information on the difference between `prod` and `dev`, see the project README.
Note that the `prod` env file here still assumes this is running locally - 
meaning it will expect the frontend to run on localhost.

- inside backend/dps_training_k folder
  - on Windows run: `docker-compose --env-file .env.<prod/dev> up`
  - on Linux run: `docker compose --env-file .env.<prod/dev> up`
- (optionally, to access data base) create superuser account: `docker exec -it K-dPS-django python manage.py createsuperuser`

## Development

### Running Tests
- start docker container with docker compose(see Running the project using Docker)
- wait until Application Startup is Completed
- run: `docker exec -it K-dPS-django python manage.py test`

### Working with Fixtures
- (clear database)
- fill database with data you want to export as fixture (e.g. `docker exec -it K-dPS-django python manage.py import_patient_states`)
  - if updating a fixture that is used by a model that doesn't allow null fields, make them nullable, migrate and discard the migrationfile afterwards.
- create fixture: 
  - `docker exec -it K-dPS-django bash`
  - `export PYTHONIOENCODING=utf8`
  - `python manage.py dumpdata template > patient_states.json`
- move the fixture to the "fixtures" directory
- now you can load it: `docker exec -it K-dPS-django python manage.py loaddata patient_states.json`
