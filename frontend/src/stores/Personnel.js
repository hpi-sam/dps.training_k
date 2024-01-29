import { defineStore } from "pinia"

export const usePersonnelStore = defineStore('personnel', {
    state: ({
        name: '',
        role: '',
        personnelDatabaseId: ''
    })
})