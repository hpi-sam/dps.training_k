import {defineStore} from "pinia"

export const useTrainerStore = defineStore('trainer', {
	state: () => ({
		username: '',
		token: ''
	})
})