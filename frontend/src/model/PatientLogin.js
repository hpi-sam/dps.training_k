export class PatientLogin {
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