import { defineStore } from "pinia"

export const useAreaStore = defineStore('area', {
    state: () => ({
        name: '',
        patients: [],
        personnel: [],
        devices: []
    })
})