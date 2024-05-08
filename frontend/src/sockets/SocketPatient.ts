import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "@/stores/Availables"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {ScreenPosition, Screens, setScreen} from "@/components/ModulePatient.vue"
import {allowNewActions} from "@/components/widgets/ActionConfig.vue"
import {useRessourceAssignmentsStore} from "@/stores/RessourceAssignments"
import {useActionOverviewStore} from "@/stores/ActionOverview"
import {useVisibleInjuriesStore} from "@/stores/VisibleInjuries"
import {commonMockEvents} from "./commonMockEvents"

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
					availablesStore.loadAvailablePatients(data.availablePatients as AvailablePatient[])
					patientStore.initializePatientFromAvailablePatients()
					break
				case 'available-actions':
					availablesStore.loadAvailableActions(data.availableActions as AvailableAction[])
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
		data: '{"messageType":"state","state":{"phaseNumber":"1","airway":"freie Atemwege",' +
			'"breathing":"Atemfreq: 13 /min, SpO2: 98 %, normales AG hörbar","circulation":"Herzfreq: 72 /min, peripher tastbar, RR: 125.063",' +
			'"consciousness":"wach, orientiert","pupils":"mittelweit","psyche":"unauffällig","skin":"trocken, rosig"}}'
	},
	{
		id: 'available-actions',
		data: '{"messageType":"available-actions","availableActions":[' +
			'{"actionName":"Blutdruck messen","actionCategory":"TR"},{"actionName":"Blutprobe untersuchen","actionCategory":"LA"},' +
			'{"actionName":"Beatmungsmaske anlegen","actionCategory":"TR"},' +
			'{"actionName":"Infusion anlegen","actionCategory":"TR"},' +
			'{"actionName":"Blut abnehmen","actionCategory":"TR"},' +
			'{"actionName":"Medikament verabreichen","actionCategory":"TR"},' +
			'{"actionName":"Ruheposition einnehmen","actionCategory":"TR"},{"actionName":"Röntgen","actionCategory":"LA"},' +
			'{"actionName":"Wundversorgung","actionCategory":"TR"},{"actionName":"Stabile Seitenlage","actionCategory":"TR"},' +
			'{"actionName":"Schienung anlegen","actionCategory":"TR"},{"actionName":"Vitalwerte messen","actionCategory":"EX"}' +
			']}'
	},
	{id: 'delete', data: '{"messageType":"delete"}'},
	{
		id: 'action-confirmation',
		data: '{"messageType":"action-confirmation","actionName":"Stabile Seitenlage","actionId":"123"}'
	},
	{
		id: 'action-declination',
		data: '{"messageType":"action-declination","actionName":"Stabile Seitenlage","actionDeclinationReason":"Es fehlen die nötigen Ressourcen."}'
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
			'{"personnelId":3,"personnelName":"Jens Schweizer","patientId":123456},' +
			'{"personnelId":4,"personnelName":"Lena Schulze","patientId":6},' +
			'{"personnelId":8,"personnelName":"Julian Mohn","patientId":123456},' +
			'{"personnelId":9,"personnelName":"Elisabeth Bauer","patientId":8}' +
			'],' +
			'"material":[' +
			'{"materialId":3,"materialName":"Defibrillator","patientId":123456},' +
			'{"materialId":4,"materialName":"EKG-Monitor","patientId":123456},' +
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
			'{"actionId":1,"orderId":4,"actionName":"Stabile Seitenlage","actionStatus":"FI","timeUntilCompletion":null,"actionResult":null},' +
			'{"actionId":2,"orderId":6,"actionName":"Blutdruck messen","actionStatus":"IP","timeUntilCompletion":220,"actionResult":null},' +
			'{"actionId":4,"orderId":2,"actionName":"Adrenalin","actionStatus":"OH","timeUntilCompletion":40,"actionResult":' +
			'null},' +
			'{"actionId":3,"orderId":5,"actionName":"Blutprobe untersuchen","actionStatus":"FI","timeUntilCompletion":null,"actionResult":' +
			'"Der Patient hat eine Blutgruppe von 0+."},' +
			'{"actionId":5,"orderId":3,"actionName":"Infusion anlegen","actionStatus":"PL","timeUntilCompletion":110,"actionResult":null}' +
			']}'
	},
	{
		id: 'visible-injuries',
		data: '{"messageType":"visible-injuries","injuries":[' +
			'{ "injuryId": 1, "injuryType": "fracture", "position": "left collarbone" },' +
			'{ "injuryId": 1, "injuryType": "blood", "position": "left collarbone" },' +
			'{ "injuryId": 2, "injuryType": "fracture", "position": "left upper arm" },' +
			'{ "injuryId": 3, "injuryType": "fracture", "position": "left thorax" },' +
			'{ "injuryId": 3, "injuryType": "blood", "position": "left thorax" }' +
			']}'
	},
	...commonMockEvents
]