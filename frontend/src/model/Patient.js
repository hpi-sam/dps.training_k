export class Patient {
    /**
     * @param {String} name
     * @param {String} patientCode
     * @param {String} patientId
     * @param {String} patientDatabaseId
     */
    constructor(name, patientCode, patientId, patientDatabaseId) {
        this.name = name;
        this.patientCode = patientCode;
        this.patientId = patientId;
        this.patientDatabaseId = patientDatabaseId;
    }
}

export class PatientLogin {
    /**
     * @param {String} exerciseCode
     * @param {String} patientCode
     */
    constructor(exerciseCode, patientCode) {
        this.exerciseCode = exerciseCode;
        this.patientCode = patientCode;
    }

    /**
     * Temporary method as long as there is just one dummy patient
     * @returns {boolean}
     */
    isCorrect() {
        return this.exerciseCode === "123" && this.patientCode === "123";
    }
}

export class PatientLoadNotRunning {
    /**
     * @param {String} patientName
     * @param {String} areaName
     */
    constructor(patientName, areaName) {
        this.patientName = patientName;
        this.areaName = areaName;
    }
}

export class PatientLoadRunning {
    /**
     * @param {String} patientName
     * @param {String} areaName
     * @param {PatientState} patientState
     */
    constructor(patientName, areaName, patientState) {
        this.patientName = patientName;
        this.areaName = areaName;
        this.patientState = patientState;
    }
}

export class PatientState {
    /**
     * @param {String} airway
     * @param {String} breathing
     * @param {String} circulation
     * @param {String} consciousness
     * @param {String} pupils
     * @param {String} psyche
     * @param {String} skin
     */
    constructor(airway, breathing, circulation, consciousness, pupils, psyche, skin) {
        this.airway = airway;
        this.breathing = breathing;
        this.circulation = circulation;
        this.consciousness = consciousness;
        this.pupils = pupils;
        this.psyche = psyche;
        this.skin = skin;
    }
}

export class PatientPhaseChange {
    /**
     * @param {int} phaseNumber
     * @param {PatientState} patientState
     */
    constructor(phaseNumber, patientState) {
        this.phaseNumber = phaseNumber;
        this.patientState = patientState;
    }
}