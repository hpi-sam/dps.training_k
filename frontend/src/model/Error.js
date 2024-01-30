export class EventError {
    /**
     * @param {String} event
     * @param {any} args
     */
    constructor(event, args) {
        this.event = event;
        this.args = args;
    }
}