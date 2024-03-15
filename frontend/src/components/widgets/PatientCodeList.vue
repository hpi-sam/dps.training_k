<template>
	<div id="list">
		<button
			v-for="patient in availablePatients"
			:key="patient.patientCode"
			class="availablePatientButton"
			:class="patient.triage"
			@click="changePatient(patient.patientCode)"
		>
			{{ patient.patientCode }}
		</button>
	</div>
</template>
  
  <script setup lang="ts">
    import { useAvailablesStore } from "@/stores/Availables"
  
    const availablesStore = useAvailablesStore()
    const availablePatients = availablesStore.patients
  
    const emit = defineEmits(['change-patient'])
  
    function changePatient(patientCode: number) {
      emit('change-patient', patientCode)
    }
  </script>
  
  <style scoped>
    #list {
        display: flex;
    }

    .availablePatientButton {
        position: relative;
        background-color: #FFFFFF;
        border: 1px solid rgb(209, 213, 219);
		display: flex;
		align-items: center;
		margin-top: -1px;
		font-size: 1.25rem;
		padding: .75rem 1rem;
		text-align: left;
		height: 50px;
		width: 100%;
	}
	
	.red {
        background-color: red;
	}

	.yellow {
        background-color: yellow;
	}

	.green {
        background-color: green;
	}
  </style>
  