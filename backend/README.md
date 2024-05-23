# K-dPS Backend

## Running the project using Docker

- inside dps_training_k folder, run `docker compose up -d`
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

### Working with Fixtures on Windows by example
- create fixture: `docker exec -it K-dPS-django python manage.py dumpdata template > patient_states.json`
- this creates a file in UTF-16 format (likely a Windows thing)
- to convert it, open file in Notepad++ > Encoding -> you should see it's UTF-16
- click "convert to UTF-8", save
- make sure the fixture is in the "fixtures" directory
- now you can load it: `docker exec -it K-dPS-django python manage.py loaddata patient_states.json`
