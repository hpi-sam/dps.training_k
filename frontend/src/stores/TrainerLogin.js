import { defineStore } from "pinia"

export const useTrainerLoginStore = defineStore('trainerLogin', {
    state: () => ({
        username: '',
        password: ''
    }),
    getters: {
        isCorrect: (state) => {
            return state.username === "test" && state.password === "test";
        }
    }
})