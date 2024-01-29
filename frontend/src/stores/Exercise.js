import {defineState} from 'pinia'

export const useExerciseStore = defineState('exercise', {
    state: ({
        exerciseCode: '',
        areas: []
    })
})