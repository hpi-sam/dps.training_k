# K-dPS Backend

## Running the project using Docker

For more information on the difference between `prod` and `dev`, see the project README.
Note that the `prod` env file here still assumes this is running locally - 
meaning it will expect the frontend to run on localhost.

- inside dps_training_k folder, run `docker-compose --env-file .env.<prod/dev> up -d`
- create superuser account: `docker exec -it K-dPS-django python manage.py createsuperuser`

## Running the project locally (NOT UP TO DATE)
### Install Python
- install from official [python website](https://www.python.org/downloads/)
- version should be at least 3.12

### Setup a virtual environment for python
#### Linux

- navigate to backend folder
- `python3 -m venv env`
- `source env/bin/activate`

#### Windows

- navigate to backend folder
- `python -m venv env`
- `env/Scripts/Activate.ps1`
- in case the previous command failed due to execution policy, run: `powershell.exe -exec bypass`

### install requirements

- `pip install -r requirements.txt`

## Setup Black Formatter
### Linux (for this project only)

- make sure python extension is installed
- type "Python: Select Interpreter" in command palette and set newest interpreter for virtual environment
- neavigate to venv in terminal
- pip install black
- create .vscode file in venv
- create settings.json file in .vscode folder
- paste: 
```json
{
  "python.formatting.blackPath": "path/to/bin/of black/formatter/in/venv",
  "python.formatting.blackArgs": [
    "-l 150"
  ],
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "editor.formatOnType": true,
}
```

### Windows (for all python files open with VS Code)

- make sure you have python extension installed
- download "Black Formatter" from marketplace
- right click on a python file
- select "Format Document with"
- select "Configure Default formatter"
- select "Black"
- head to VS Code settings
- search for "format on save"
- enable "Editor: Format on Save"

## Development

- to run tests: `docker exec -it K-dPS-django python manage.py test`

### Working with Fixtures
- (clear database)
- fill database with data you want to export as fixture (e.g. `docker exec -it K-dPS-django python manage.py import_patient_states`)
  - in this example, make PatientState.transition null=True and blank=True, migrate that
- create fixture: 
  - `docker exec -it K-dPS-django bash`
  - `export PYTHONIOENCODING=utf8`
  - `python manage.py dumpdata template > patient_states.json`
- move the fixture to the "fixtures" directory
- now you can load it: `docker exec -it K-dPS-django python manage.py loaddata patient_states.json`
