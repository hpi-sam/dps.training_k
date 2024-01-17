export class TrainerLogin {
    constructor(username, password) {
        this.username = username;
        this.password = password;
    }

    /**
     * Temporary method as long as trainer accounts do not exist
     * @returns {boolean}
     */
    isCorrect() {
        return this.username === "test" && this.password === "test";
    }
}