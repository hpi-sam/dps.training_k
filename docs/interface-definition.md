# Interface Definition
This document describes the interface between the frontend and the backend of the K-dPS project. The events are divided into three categories: 
events used to log in, events available on the patient route and event available on the trainer route. They are then further divided within their 
categories into events that can be sent from the frontend to the backend and events that can be sent from the backend to the frontend. Within 
these subcategories, the events are ordered alphabetically.

## Color Legend
🟢 → event fully implemented <br/>
🟡 → event only implemented in frontend <br/>
🔵 → event only implemented in backend <br/>
🔴 → event not implemented

# Login
via HTTP

## 🟢 Trainer Login
if a new username is entered, a new account is automatically generated and logged in<br/>
debug exercise credentials: username=test, password=password

### Request
```json
{
    "username":"X",
    "password":"X"
}
```

### Response
success:
```json
{
    "token":"X"
}
```
username or password is missing → status code 400 <br/>
username exists, but password is wrong → status code 401


## 🟢 Patient Login
debug exercise credentials: exerciseid=abcdef, patientId=123456

### Request
```json
{
    "exerciseId":"abcdef",
    "patientId":"123456"
}
```
`exerciseId`: always six letters<br/>
`patientId`: always six digits

### Response
success
```json
{
  "token": "X"
}
```
exerciseId or patientId is missing → status code 400 <br/>
either exerciseId or patientId is wrong → status code 401



# Common
Websocket events that are available in Patient and Trainer connections

## Frontend → Backend

### 🟢 test-passthrough
expects to receive `test-passthrough` event back
```json
{
  "messageType": "test-passthrough"
}
```


## Backend → Frontend

### 🟢 available-actions
send after authentication<br/>
at the moment only used in patient module but makes more sense as common because of consistency
```json
{
  "messageType": "available-actions",
  "availableActions": [
    {
      "actionName": "X",
      "actionCategory": "treatment|examination|lab|other"
    }
  ]
}
```

### 🟢 available-materials
send after authentication
```json
{
  "messageType": "available-materials",
  "availableMaterials": [
    {
      "materialName": "X",
      "materialType": "device|blood"
    }
  ]
}
```

### 🟢 available-patients
send after authentication<br/>
```json
{
  "messageType": "available-patients",
  "availablePatients": [
    {
      "code": 1001,
      "personalDetails": "X",
      "injury": "X",
      "biometrics": "X",
      "triage": "-|G|Y|R|A|B|C|D|E",
      "mobility": "X",
      "preexistingIllnesses": "X",
      "permanentMedication": "X",
      "currentCaseHistory": "X",
      "pretreatment": "X"
    }
  ]
}
```
`code`: 1001-1041: IDs corresponding to the dynamic patient templates

### 🟢 exercise
send after authentication and on each exercise update
```json
{
  "messageType": "exercise",
  "exercise": {
    "exerciseId": "X",
    "areas": [
      {
        "areaId": 0,
        "areaName": "X",
        "patients": [
          {
            "patientId": "X",
            "patientName": "X",
            "code": 1001,
            "triage": "-|X|1|2|3"
          }
        ],
        "personnel": [
          {
            "personnelId": 0,
            "personnelName": "X"
          }
        ],
        "material": [
          {
            "materialId": 0,
            "materialType": "X",
            "materialName": "X" 
          }
        ]
      }
    ]
  }
}
```
`code`: 1001-1041: analog to `available-patients` fetch

### 🟢 exercise-end
```json
{
  "messageType": "exercise-end"
}
```

### 🟡 exercise-pause
```json
{
  "messageType":"exercise-pause"
}
```

### 🟡 exercise-resume
```json
{
  "messageType":"exercise-resume"
}
```

### 🟢 exercise-start
```json
{
  "messageType": "exercise-start"
}
```

### 🟢 failure
```json
{
  "messageType": "failure",
  "message": "X"
}
```

### 🟢 test-passthrough
```json
{
  "messageType": "test-passthrough",
  "message": "received test event"
}
```

### 🟢 warning
```json
{
  "messageType": "warning",
  "message": "X"
}
```



# Patient
Websocket events that are available in Patient connections

## Frontend → Backend

### 🟢 action-add
frontend won’t accept new actions by user until either an `action-declination` event or an `action-confirmation` event was sent in response to this
event
```json
{
  "messageType": "action-add",
  "actionName": "X"
}
```

### 🟢 action-cancel
```json
{
  "messageType":"action-cancel",
  "actionId":213
}
```

### 🟢 action-check
start sending `action-check` events for the specific action
```json
{
  "messageType":"action-check",
  "actionName":"X"
}
```

### 🟢 action-check-stop
start sending `action-check` events for the specific action
```json
{
  "messageType":"action-check-stop"
}
```

### 🔵 example
used for internal backend tests
```json
{
  "messageType":"example",
  "exerciseId":"abcdef", 
  "patientId":"123456"
}
```

### 🟢 material-assign
```json 
{
  "messageType":"material-assign",
  "materialId":1
}
```

### 🟡 material-move
```json
{
  "messageType":"material-move",
  "materialId":0,
  "areaId":0
}
```

### 🟢 material-release
```json
{
  "messageType":"material-release",
  "materialId":1
}
```

### 🟢 patient-move
```json
{
  "messageType":"patient-move",
  "areaId":0
}
```

### 🟢 personnel-assign
```json
{
  "messageType":"personnel-assign",
  "personnelId":1
}
```

### 🟡 personnel-move
```json
{
  "messageType":"personnel-move",
  "personnelId":0,
  "areaId":0
}
```

### 🟢 personnel-release
```json
{
  "messageType":"personnel-release",
  "personnelId":1
}
```

### 🟢 triage
the current triage color of this patient
```json
{
  "messageType": "triage",
  "triage": "-|X|1|2|3"
}
```


## Backend → Frontend

### 🟢 action-check
check action requirements<br />
will only be sent if `action-check` was sent by frontend before
```json
{
  "messageType": "action-check",
  "actionCheck": {
    "actionName": "X",
    "applicationDuration": 4,
    "effectDuration": 3,
    "personnel": [
      {
        "name": "X",
        "available": 1,
        "assigned": 1,
        "needed": 1
      }
    ],
    "material": [
      {
        "name": "X",
        "available": 1,
        "assigned": 1,
        "needed": 1
      }
    ],
    "lab_devices": [
      {
        "name": "X",
        "available": 1,
        "needed": 1
      }
    ],
    "requiredActions": {
      "singleActions": ["A1"],
      "actionGroups": [
        {
          "groupName": "Tubusse",
          "actions": [
            "A2",
            "A3"
          ]
        }
      ]
    },
    "prohibitiveActions":["A1"]
  }
}
```
`actionName`: important if the user already opened another action
`applicationDuration`: in seconds
`effectDuration`: in seconds
`requiredActions`: only the ones still missing
`prohibitiveActions`: only the ones actually blocking it

### 🟢 action-confirmation
frontend won’t accept new actions by user until this event or an `action-declination` event was sent for the last action added via `action-add`
```json
{
  "messageType": "action-confirmation",
  "actionName": "X",
  "actionId": 123
}
```

### 🟢 action-declination
frontend won’t accept new actions by user until this event or an `action-confirmation` event was sent for the last action added via `action-add`
```json
{
  "messageType": "action-declination",
  "actionName": "X",
  "actionDeclinationReason": "X"
}
```

### 🟢 action-list
send every time the action list of the patient is changed (no timeUntilCompletion updates)
```json
{
  "messageType":"action-list",
  "actions":[{
    "actionId":123,
    "orderId":123,
    "actionName":"X",
    "actionStatus":"IP|FI|PL|OH|IE|EX",
    "timeUntilCompletion":123,
    "actionResult":"X"
  }]
}
```
`timeUntilCompletion`: in seconds, null if completed
`actionResult`: null if not completed or no result

### 🔴 delete
```json
{
  "messageType":"delete"
}
```

### 🟢 ressource-assignments
can consist out of one or multiple areas
```json
{
  "messageType": "ressource-assignments",
  "ressourceAssignments": [
    {
      "areaId": 0,
      "personnel": [
        {
          "personnelId": 1,
          "patientId": 1
        }
      ],
      "material": [
        {
          "materialId": 1,
          "patientId": 1
        }
      ]
    }
  ]
}
```
`patientId`: null if unassigned

### 🔵 response
used for internal backend tests
```json
{
  "messageType":"response",
  "content":"X"
}
```

### 🟢 state
dynamic patient information - send on ever phase change
```json
{
  "messageType": "state",
  "state": {
    "airway": "X",
    "breathing": "X",
    "circulation": "X",
    "consciousness": "X",
    "pupils": "X",
    "psyche": "X",
    "skin": "X"
  }
}
```

### 🔴 patient-active
```json
{
  "messageType":"patient-active"
}
```

### 🟢 patient-back
send if lab-side action is finished
```json
{
  "messageType":"patient-back"
}
```

### 🔴 patient-inactive
```json
{
  "messageType":"patient-inactive",
  "inactiveInfo":"X",
  "timeUntilBack":123
}
```
`timeUntilBack`: in seconds

### 🟢 patient-relocating
send if a lab-side action is started
```json
{
  "messageType":"patient-relocating",
  "relocatingInfo":"X",
  "timeUntilBack":123
}
```
`timeUntilBack`: in seconds

### 🟡 visible-injuries
```json
{
  "messageType":"visible-injuries",
  "injuries":[{
    "injuryId":0,
    "injuryType":"blood|fracture",
    "position":"X"
  }]
}
```
`position`: there is a list of possible positions in the frontend



# Trainer
Websocket events that are available in Patient connections

## Frontend → Backend

### 🟢 area-add
```json
{
  "messageType":"area-add"
}
```

### 🟢 area-delete
```json
{
  "messageType":"area-delete",
  "areaId":0
}
```

### 🟢 area-rename
```json
{
  "messageType":"area-rename",
  "areaId":0,
  "areaName":"X"
}
```

### 🔵 example
used for internal backend tests
```json
{
  "messageType":"example",
  "exerciseId":"abcdef"
}
```

### 🟢 exercise-create
```json
{
  "messageType":"exercise-create"
}
```

### 🟢 exercise-end
```json
{
  "messageType":"exercise-end"
}
```

### 🟡 exercise-pause
```json
{
  "messageType":"exercise-pause"
}
```

### 🟡 exercise-resume
```json
{
  "messageType":"exercise-resume"
}
```

### 🟢 exercise-start
```json
{
  "messageType":"exercise-start"
}
```

### 🟢 material-add
```json
{
  "messageType": "material-add",
  "areaId": 0,
  "materialName": "X"
}
```

### 🟢 material-delete
```json
{
  "messageType": "material-delete",
  "materialId": 0
}
```

### 🟢 patient-add
```json
{
  "messageType":"patient-add",
  "areaId":0,
  "patientName":"X",
  "code":1001
}
```
`code`: 1001-1041: analog to `available-patients` fetch

### 🟢 patient-delete
```json
{
  "messageType":"patient-delete",
  "patientId":"X"
}
```

### 🟢 patient-rename
```json
{
  "messageType":"patient-rename",
  "patientId":0,
  "patientName":"X"
}
```

### 🟢 patient-update
```json
{
  "messageType": "patient-update",
  "patientId": "X",
  "code": 1001
}
```
`code`: 1001-1041: analog to `available-patients` fetch

### 🟢 personnel-add
```json
{
  "messageType":"personnel-add",
  "areaId":0,
  "personnelName":"X"
}
```

### 🟢 personnel-delete
```json
{
  "messageType":"personnel-delete",
  "personnelId":0
}
```

### 🟢 personnel-rename
```json
{
  "messageType": "personnel-rename",
  "personnelId": 0,
  "personnelName": "X"
}
```

### 🟡 set-speed
```json
{
  "messageType": "set-speed",
  "speed": 1
}
```
`speed`: from 0.2 to 4 in 0.1 steps


## Backend → Frontend

### 🟢 log-update
on first login during running exercise send all log entries
```json
{
    "messageType":"log-update",
    "logEntries":[{
        "logId":0,
        "logMessage":"X",
        "logTime":0,
        "areaId":0,
        "patientId":"X",
        "personnelIds":[0],
        "materialNames": ["X"]
    }]
}
```
`logTime`: number of milliseconds since January 1, 1970, 00:00:00 UTC.

### 🔵 response
used for internal backend tests
```json
{
  "messageType":"response",
  "content":"X"
}
```

### 🟡 set-speed
```json
{
  "messageType": "set-speed",
  "speed": 1
}
```
`speed`: from 0.2 to 4 in 0.1 steps