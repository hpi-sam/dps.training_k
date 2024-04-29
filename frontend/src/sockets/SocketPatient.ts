import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "@/stores/Availables"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {ScreenPosition, Screens, setScreen} from "@/components/ModulePatient.vue"
import {allowNewActions} from "@/components/widgets/ActionConfig.vue"
import {useRessourceAssignmentsStore} from "@/stores/RessourceAssignments"
import { useActionOverviewStore } from "@/stores/ActionOverview"
import { useVisibleInjuriesStore } from "@/stores/VisibleInjuries"
import { commonMockEvents } from "./commonMockEvents"

class SocketPatient {
	private readonly url: string
	socket: WebSocket | null = null

	constructor(url: string) {
		this.url = url
	}

	connect(): void {
		const patientStore = usePatientStore()
		const exerciseStore = useExerciseStore()
		const availablesStore = useAvailablesStore()
		const ressourceAssignmentsStore = useRessourceAssignmentsStore()
		const actionOverview = useActionOverviewStore()
		const visibleInjuriesStore = useVisibleInjuriesStore()

		this.socket = new WebSocket(this.url + usePatientStore().token)

		this.socket.onopen = () => {
			console.log('Patient WebSocket connection established')
			connection.patientConnected = true
		}

		this.socket.onclose = () => {
			console.log('Patient WebSocket connection closed')
			connection.patientConnected = false
		}

		this.socket.onerror = (error) => {
			console.error('Patient WebSocket error:', error)
		}

		this.socket.onmessage = (message) => {
			let data: MessageData
			try {
				data = JSON.parse(message.data)
			} catch (e) {
				console.error('Error parsing message data:', e)
				console.error('Problematic message data:', message.data)
				return
			}

			switch (data.messageType) {
				case 'failure':
					showErrorToast(data.message || '')
					break
				case 'test-passthrough':
					showWarningToast(data.message || '')
					break
				case 'state':
					patientStore.loadStatusFromJSON(data.state as State)
					break
				case 'available-patients':
					availablesStore.loadAvailablePatients(data.availablePatients as AvailablePatients)
					patientStore.initializePatientFromAvailablePatients()
					break
				case 'available-actions':
					console.log('Socket: Available actions:', data.availableActions)
					if (data.availableActions === undefined) showErrorToast('Fehler: Keine verfügbaren Aktionen erhalten')
					else availablesStore.loadAvailableActions(data.availableActions as AvailableActions)
					break
				case 'exercise':
					exerciseStore.createFromJSON(data.exercise as Exercise)
					patientStore.initializePatientFromExercise()
					break
				case 'exercise-started':
					setScreen(Screens.STATUS, ScreenPosition.LEFT)
					setScreen(Screens.ACTIONS, ScreenPosition.RIGHT)
					break
				case 'exercise-paused':
					setScreen(Screens.INACTIVE, ScreenPosition.FULL)
					break
				case 'exercise-resumed':
					setScreen(Screens.STATUS, ScreenPosition.LEFT)
					setScreen(Screens.ACTIONS, ScreenPosition.RIGHT)
					break
				case 'exercise-ended':
					setScreen(Screens.INACTIVE, ScreenPosition.FULL)
					break
				case 'delete':
					console.log('Patient Websocket ToDo: handle delete event ', data)
					break
				case 'information':
					console.log('Patient Websocket ToDo: handle information event ', data)
					break
				case 'action-confirmation':
					allowNewActions()
					console.log('Patient Websocket ToDo: handle action-confirmation event ', data)
					break
				case 'action-declination':
					allowNewActions()
					showErrorToast('Aktion ' + data.actionName + ' konnte nicht angeordnet werden:\n ' + data.actionDeclinationReason)
					console.log('Patient Websocket ToDo: handle action-declination event ', data)
					break
				case 'action-result':
					console.log('Patient Websocket ToDo: handle action-result event ', data)
					break
				case 'ressource-assignments':
					ressourceAssignmentsStore.setRessourceAssignments(data.ressourceAssignments as RessourceAssignments)
					break
				case 'action-list':
					actionOverview.loadActions(data.actions as Action[])
					actionOverview.startUpdating()
					break
				case 'visible-injuries':
					visibleInjuriesStore.loadVisibleInjuries(data.injuries as Injury[])
					break
				default:
					showErrorToast('Unbekannten Nachrichtentypen erhalten:' + data.messageType)
					console.error('Patient received unknown message type:', data.messageType, 'with data:', data)
			}
		}
	}

	close() {
		if (this.socket) this.socket.close()
	}

	private sendMessage(message: string) {
		if (connection.patientConnected && this.socket) {
			this.socket.send(message)
		} else {
			console.log('Patient WebSocket is not connected.')
		}
	}

	actionAdd(actionName: string) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-add',
			'actionName': actionName,
		}))
	}

	testPassthrough() {
		this.sendMessage(JSON.stringify({'messageType': 'test-passthrough'}))
	}

	triage(triage: string) {
		this.sendMessage(JSON.stringify({
			'messageType': 'triage',
			'triage': triage,
		}))
	}

	releasePersonnel(personnelId: number) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-release',
			'personnelId': personnelId,
		}))
	}

	assignPersonnel(personnelId: number) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-assign',
			'personnelId': personnelId,
		}))
	}

	releaseMaterial(materialId: number) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-release',
			'materialId': materialId,
		}))
	}

	assignMaterial(materialId: number) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-assign',
			'materialId': materialId,
		}))
	}

	deleteAction(actionId: number) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-delete',
			'actionId': actionId,
		}))
	}

	movePatient(areaName: string) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-move',
			'areaName': areaName,
		}))
	}
}

const socketPatient = new SocketPatient('ws://localhost:8000/ws/patient/?token=')
export default socketPatient

export const serverMockEvents = [
	{
		id: 'state',
		data: '{"messageType":"state","state":{"phaseNumber":"123","airway":"Normal","breathing":"Regelmäßig","circulation":"Stabil",' +
			'"consciousness":"Bewusstlos","pupils":"Geweitet","psyche":"Ruhig","skin":"Blass"}}'
	},
	{
		id: 'available-actions',
		data: '{"messageType":"available-actions","availableActions":{"availableActions":[' +
			'{"actionName":"Blutdruck messen","actionType":"treatment"},{"actionName":"Blutprobe untersuchen","actionType":"lab"},' +
			'{"actionName":"Beatmungsmaske anlegen","actionType":"treatment"},' +
			'{"actionName":"Infusion anlegen","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen1","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen2","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen3","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen4","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen5","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen6","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen7","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen8","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen9","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen10","actionType":"treatment"},' +
			'{"actionName":"Blut abnehmen11","actionType":"treatment"},' +
			'{"actionName":"Medikament verabreichen","actionType":"treatment"},' +
			'{"actionName":"Ruheposition einnehmen","actionType":"treatment"},{"actionName":"Röntgen","actionType":"lab"},' +
			'{"actionName":"Wundversorgung","actionType":"treatment"},{"actionName":"Stabile Seitenlage","actionType":"treatment"},' +
			'{"actionName":"Schienung anlegen","actionType":"treatment"},{"actionName":"Vitalwerte messen","actionType":"treatment"}' +
			']}}'
	},
	{id: 'delete', data: '{"messageType":"delete"}'},
	{
		id: 'information',
		data: '{"messageType":"information","patientInjury":"Fractured limb","patientHistory":"No known allergies",' +
			'"patientPersonalDetails":"John Doe, Male, 30 years old","patientBiometrics":"Height: 180cm, Weight: 75kg"}'
	},
	{
		id: 'action-confirmation',
		data: '{"messageType":"action-confirmation","actionName":"Stabile Seitenlage","actionId":"123"}'
	},
	{
		id: 'action-declination',
		data: '{"messageType":"action-declination","actionName":"Stabile Seitenlage","actionDeclinationReason":"Es fehlen die nötigen Ressourcen."}'
	},
	{
		id: 'action-result',
		data: '{"messageType":"action-result","actionName":"Blutprobe untersuchen","actionId":"125",' +
			'"actionResult":"Der Patient hat eine Blutgruppe von 0+."}'
	},
	{
		id: 'ressource-assignments',
		data: '{"messageType":"ressource-assignments","ressourceAssignments":{"ressourceAssignments":[' +
			'{"areaName":"Intensiv",' +
			'"personnel":[' +
			'{"personnelId":1,"personnelName":"Albert Spahn","patientId":5},' +
			'{"personnelId":2,"personnelName":"Anna Neumann","patientId":3}' +
			'],' +
			'"material":[' +
			'{"materialId":1,"materialName":"Beatmungsgerät","patientId":3},' +
			'{"materialId":2,"materialName":"Defibrillator","patientId":5}' +
			']},' +
			'{"areaName":"ZNA",' +
			'"personnel":[' +
			'{"personnelId":3,"personnelName":"Jens Schweizer","patientId":2},' +
			'{"personnelId":4,"personnelName":"Lena Schulze","patientId":6},' +
			'{"personnelId":8,"personnelName":"Julian Mohn","patientId":2},' +
			'{"personnelId":9,"personnelName":"Elisabeth Bauer","patientId":8}' +
			'],' +
			'"material":[' +
			'{"materialId":3,"materialName":"Defibrillator","patientId":2},' +
			'{"materialId":4,"materialName":"EKG-Monitor","patientId":2},' +
			'{"materialId":9,"materialName":"Narkosegerät","patientId":9}' +
			']},' +
			'{"areaName":"Wagenhalle",' +
			'"personnel":[' +
			'{"personnelId":5,"personnelName":"Finn Heizmann","patientId":1},' +
			'{"personnelId":6,"personnelName":"Ursula Seiler","patientId":4}' +
			'],' +
			'"material":[' +
			'{"materialId":5,"materialName":"EKG-Gerät","patientId":1},' +
			'{"materialId":6,"materialName":"Blutdruckmessgerät","patientId":4}' +
			']' +
			'}]}}'
	},
	{
		id: 'action-list',
		data: '{"messageType":"action-list","actions":[' +
			'{"actionId":1,"orderId":5,"actionName":"Stabile Seitenlage","actionStatus":"running","timeUntilCompletion":20,"actionResult":null},' +
			'{"actionId":2,"orderId":6,"actionName":"Blutdruck messen","actionStatus":"running","timeUntilCompletion":220,"actionResult":null},' +
			'{"actionId":4,"orderId":3,"actionName":"Beatmungsmaske anlegen","actionStatus":"waiting","timeUntilCompletion":320,"actionResult":' +
			'null},' +
			'{"actionId":3,"orderId":4,"actionName":"Blutprobe untersuchen","actionStatus":"finished","timeUntilCompletion":null,"actionResult":' +
			'"Der Patient hat eine Blutgruppe von 0+."},' +
			'{"actionId":6,"orderId":1,"actionName":"Tornique anlegen","actionStatus":"finished","timeUntilCompletion":null,"actionResult":null},' +
			'{"actionId":5,"orderId":2,"actionName":"Infusion anlegen","actionStatus":"blocked","timeUntilCompletion":110,"actionResult":null}' +
			']}'
	},
	{
		id: 'visible-injuries',
		data: '{"messageType":"visible-injuries","injuries":[' +
			'{ "injuryId": 1, "injuryType": "fracture", "position": "left hand" },' +
			'{ "injuryId": 2, "injuryType": "blood", "position": "right lower leg" },' +
			'{ "injuryId": 3, "injuryType": "blood", "position": "head" },' +
			'{ "injuryId": 4, "injuryType": "fracture", "position": "right collarbone" },' +
			'{ "injuryId": 5, "injuryType": "blood", "position": "left rip" }' +
			']}'
	},
	...commonMockEvents
]