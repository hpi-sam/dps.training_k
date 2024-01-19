# K-dPS Backend

## Setup
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

### Setup Black
#### Linux (for this project only)

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

#### Windows (for all python files open with VS Code)

- make sure you have python extension installed
- download "Black Formatter" from marketplace
- right click on a python file
- select "Format Document with"
- select "Configure Default formatter"
- select "Black"
- head to VS Code settings
- search for "format on save"
- enable "Editor: Format on Save"

### Running the project

- inside backend folder, run `docker compose up -d`
- then, inside "dps.training_k" folder run `python manage.py runserver`