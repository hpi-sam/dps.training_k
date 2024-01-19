export class Area {
    /**
     * @param {String} name
     * @param {List<Patient>} patients
     * @param {List<Personnel>} personnel
     * @param {List<Device>} devices
     */
    constructor(name, patients, personnel, devices) {
        this.name = name;
        this.patients = patients;
        this.personnel = personnel;
        this.devices = devices;
    }
}