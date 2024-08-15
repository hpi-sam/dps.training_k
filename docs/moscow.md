# MoSCoW Prioritization
This document contains the planned features and other development goals and their prioritization according to the 
[MoSCoW method](https://en.wikipedia.org/wiki/MoSCoW_method) (with the addition of Nice to Have below Could Have and above Won't have).
Features and requirements always have a code which can be used to reference them. 

Small UX improvements and bug fixes are not included in this list and should instead immediately be documented as a prioritized issue instead.

## Color Legend
🟢 → feature fully implemented <br/>
🟡 → feature only implemented in frontend <br/>
🔵 → feature only implemented in backend <br/>
🔴 → feature not implemented

## Non-functional Requirements
Requirements that are not directly related to the functionality of the software, but rather to its quality, performance, and usability and should 
always be considered when developing new features.

- A00: **Customizability**: Our software allows for high customizability before and during the exercise, recognizing the educational key role of 
  exercise instructors.
- A01: **Intuitive Interface**: The interface is intuitive for hospital personnel.
- A02: **Easy Simulation Execution**: The simulation should be quick to prepare and execute.
- A03: **8-25 Participants**: The exercises are effectively playable by 8-25 participants.
- A04: **Screen Ratio 3:4 to 1:2**: The web app should correctly scale on all screen ratios from 3:4 to 1:2.
- A05: **Samsung S7 FE**: The web app should look good on the Samsung S7 FE.
- A06: **Chrome, Firefox, and Safari**: The web app should work on the latest versions of Chrome, Firefox, and Safari.
- A07: **Backend Performance**: A backend should be able to handle a single exercise with 30 clients.

## Must Have
This category is further divided into those necessary for a basic demonstration of our application (MVP) 
and those that are necessary for a fully functional application (Non-MVP).

### MVP
- 🟢 M00: **Exercise Creation**
  - Without configuration
  - At least one patient (hardcoded patient code)
  - Exercise code display = 123
- 🟢 M01: **Patient Login**
  - Login
  - Load patient + triage color coding
  - Display patient names
- 🟢 M02: **Start / End Exercise**
  - No evaluation!
- 🟢 M03: **Patient Phase Change**
  - Backend: Change phase, send data to frontend
  - Frontend: Display updated patient data
- 🟢 M04: **Execute action**: At least one action can be performed
- 🟢 M05: **Docker**: Set up Docker for Front- & Backend

### Non-MVP
- 🟢 N00: Configuration before starting exercise
  - Add/delete areas
  - Add/delete patients and select code & display ID
    - → Patient: Exercise not started screen
  - Add/delete personnel
  - Add/delete materials (equipment+blood)
  - (Not: active/inactive, roles in personnel)
- 🟢 N01: Action List
  - Include all actions (treatments & examinations including lab tests) from stakeholders with final data
  - Actions like medications that expire
  - Includes standard structure for examinations and treatments
  - Lab
    - Lab tests are depicted as actions with zero personnel effort
    - Requesting blood from lab as an action
  - Examinations return something after completion; treatments confirm completion
- 🟢 N02: Logbook
  - Logging
  - Logbook screen
  - BACKEND: Risk of a bottleneck, as caching is ineffective and all actions need this module!
- 🟢 N03: State Visualization #1
  - Info: Injuries, personal details
- 🟢 N04: Resource Allocation
  - Listing per type in resource tab
  - Assign personnel & equipment to patients
- 🟢 N05: Prerequisites for Actions
  - Number of personnel
  - Equipment
  - NOT: Dependencies between actions
- 🟢 N06: Phase Changes
  - Import patient states
  - Check phase change conditions
- 🟢 N07: Scheduling #1
  - Action confirmation only if action can be executed immediately
- 🟢 N08: Action Overview
  - Visualization of scheduling
  - Action history with results
  - Remove actions (ongoing actions are thereby cancelled)
- 🟢 N09: Patient Transfer
- 🟢 N10: Minimal Lab
  - Represent lab hardcoded in backend with devices
  - Trainer does not see lab devices anymore when adding material
  - Actions can be executed via the lab
  - Thaw blood (as often as one wants) & analyze blood type
- 🟢 N11: Imaging Actions
  - Imaging actions can be ordered without extra configuration in frontend
  - They return everything by default
  - Patient is removed from area, everything unassigned, dealt with in an external place, and then delivered back to area
    - This should also have log events

## Should Have
- 🟢 C00: Prerequisites for Actions #2
  - Action conditions, aka dependencies between actions
- 🟢 S01: Berlin Triage System instead of previous one
- 🟡 S02: Move personnel and materials
- 🟡 S03: Pause Exercise
- 🟡 S04: Scale Time / Adjust Speed
  - Only implemented as fixed speed-up in dev mode currently
  - Support time scaling interface from frontend
- 🟢🔴 S05: Configuration During Exercise
  - Added experimentally without safeguards and guarantees at the moment
  - Delete patient
  - Delete personnel and materials if not assigned anywhere
  - Add patients, materials and personnel 
- 🟢 S06: Rename areas, patients, and personnel
- 🟢 S07: Sort Patient Information
  - Reorder currently displayed static patient information
  - Name at the very top left instead of ID
  - Our patient ID can replace the unique number
- 🟡 S08: Scheduling #2
  - Several things can be scheduled simultaneously / automatic sequential processing depending on available resources
  - Also means updating the system about the availability of actions for the frontend
- 🟡 S09: State Visualization #2
  - Patient picture
  - Display injuries
- 🟢 S10: Trainer Login
  - Registration
  - Store login data in backend
  - Display trainer name
  - Trainer account corresponds to exercise
- 🔴 S11: Automatic Patient Resubscribe after connection loss
  - If tablet fails, window is closed, etc.

## Could Have

- 🔴 C00: OP #1
  - 🟢 Add op as action
  - 🔴 OP capacities
- 🔴 C01: Multiple Triage Systems
  - Pre-triage marked by pre-clinic process
  - Add Manchester
  - Type of triage selectable in exercise setting
  - Possibly no letters?
- 🔴 C02: Choose Medical Access
  - Different accesses result in different action durations and effectiveness times for subsequent actions
- 🔴 C03: State Visualization #3
  - E.g., "EKG Monitor" with continuous value as another action
  - Devices
  - Personnel
  - Mobility
  - Screaming
- 🔴 C04: Display Resource Assignment in Action Overview
- 🔴 C05: Categorize Available Patients
  - WHen adding a new patient to an area, the code colors and numbers are not sufficient to find the best patient for the situation
- 🔴 C06: Implement Lab Actions the right way
  - Configure Imaging actions
  - FIFO scheduling per lab device
- 🔴 C07: Active/Inactive & (not) Pausing
  - Setting per Patient/ressource to only pause and hide this one instance
  - Area setting (pausing)
  - Patient, personnel, device setting
  - Patient inactive screen
- 🔴 C08: Check Role Requirements for Actions
  - Define roles for personnel (configuration)
  - Define role conditions, consider role conditions in scheduling
  - Build system to be able to ignore role conditions - should probably be explicitly logged though
- 🔴 C09: OP #2
  - Show op status / get result
  - Needs a more sophisticated role and number requirement system, currently the “Operation einleiten” measure has garbage values for this
- 🔴 C10: Edit Action Overview
  - Edit role quota
  - Move actions
- 🔴 C11: Move Equipment
  - With time
  - With personnel
- 🔴 C12: Export Final Results
  - Probably log + statistics 
  - As CSV
  - As PDF
- 🔴 C13: Save Exercises
  - Save exercises (one or more per Account?)
  - Load exercises
  - Possibly also save interim states during an ongoing exercise?
- 🔴 C14: Filter Logbook...
  - Filters
  - Search function
  - Categories
- 🔴 C15: Filter Action List...
  - Filters
  - Search function
  - Categories
- 🔴 C16: Individually Schedule Lab Actions
  - Instead of just FIFO, order should be adjustable by the user
  - Additional interface for the lab
- 🔴 C17: Vital Parameter History
  - Histogram / history
  - A fever curve / progression curve would be good for players - self-created or automatically generated
- 🔴 C18: Add different Blood Groups
  - 0, A, B, AB, +- for each
- 🔴 C19: Dynamically adjust birthdate
  - Birthdate of the available patients should be automatically adjusted for their age to stay consistent

## Nice to Have
- 🔴 T00: Evaluation (statistics, etc.)
  - Show automatic evaluation screen at the end of an exercise
- 🔴 T01: Prevent Screen Saver
- 🔴 T02: Trainer Mode: Spectate Patient
  - When tapping on a patient in the trainer module, the action overview and info screen of that patient pop up 
  - Without interaction possibility and with back button
- 🔴 T03: Admittable Label in Exercise Creation
  - Visual indicator whether the patient is intended to have been in the hospital at the start of the exercise or if the patient is just being 
    admitted
- 🔴 T04: Modify Patient Metadata
  - Possibly make all patient data adjustable
- 🔴 T05: Patient Transfer with personnel
  - Assign personnel for transferring
  - With time
- 🔴 T06: As a Trainer, Move Things
  - Patients, Personnel, Material
  - Without time
- 🔴 T07: Sharing of Exercises
  - Make prepared exercises available to other people / trainer accounts
- 🔴 T08: Multiple Trainers
  - Multiple different trainer should be able to join the same exercise
- 🔴 T09: Time Until Status Values Displayed
  - Do not show all status values permanently, but only after a certain time and/or just a certain set of them
  - Make it more realistic
- 🔴 T10: Rewind Exercise
  - Useful for debriefing
- 🔴 T11: QR Code Login
- 🔴 T12: Configure existing actions
  - Change e.g. preconditions or time

## Won't Have
- Adding actions
- Mobile compatibility
- Patient generator
- Own app for leadership personnel
- Non-verbal communication between trainers
- Automated Areas
  - Dynamic patients continue nonetheless
- Nested Areas

## Miscellaneous Goals
- Learning Objectives
  - **Prioritization**: Our software creates a situation of scarcity of time and resources. Prioritization thus becomes essential.
  - **Crew Resource Management**: Our software supports all aspects relevant to learning Crew Resource Management.
    - Possibility of human hierarchy levels
    - A non-reflective activity (e.g., diagnosis, treatment) that must be switched in and out of
    - Visibility of errors to others and in retrospect
  - Communication: Participants should learn to communicate effectively.

- **Objective Measurability**: Objective measurability through patient simulation prevents subjective assessments.
