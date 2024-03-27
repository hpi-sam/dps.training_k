import {connection} from "@/stores/Connection"
import {useTrainerStore} from "@/stores/Trainer"
import {useExerciseStore} from "@/stores/Exercise"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {Screens, setLeftScreen as moduleTrainerSetLeftScreen, setRightScreen as moduleTrainerSetRightScreen} from "@/components/ModuleTrainer.vue"
import { useAvailablesStore } from "@/stores/Availables"

class SocketTrainer {
	private readonly url: string
	socket: WebSocket | null = null

	constructor(url: string) {
		this.url = url
	}

	connect() {
		this.socket = new WebSocket(this.url + useTrainerStore().token)

		this.socket.onopen = () => {
			console.log('Trainer WebSocket connection established')
			connection.trainerConnected = true
		}

		this.socket.onclose = () => {
			console.log('Trainer WebSocket connection closed')
			connection.trainerConnected = false
		}

		this.socket.onerror = (error) => {
			console.error('Trainer WebSocket error:', error)
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
				case 'available-actions':
					useAvailablesStore().loadAvailableActions(data.availableActions as AvailableActions)
					break
				case 'available-material':
					useAvailablesStore().loadAvailableMaterial(data.availableMaterial as AvailableMaterial)
					break
				case 'available-patients':
					useAvailablesStore().loadAvailablePatients(data.availablePatients as AvailablePatients)
					break
				case 'exercise':
					useExerciseStore().createFromJSON(data.exercise as Exercise)
					moduleTrainerSetLeftScreen(Screens.EXERCISE_CREATION)
					moduleTrainerSetRightScreen(Screens.RESOURCE_CREATION)
					break
				case 'exercise-start':
					moduleTrainerSetLeftScreen(Screens.LOG)
					moduleTrainerSetRightScreen(Screens.SCENARIO)
					break
				case 'exercise-stop':
					moduleTrainerSetLeftScreen(Screens.CREATE_EXERCISE)
					moduleTrainerSetRightScreen(Screens.JOIN_EXERCISE)
					break
				case 'log-update':
					console.log('Trainer Websocket ToDo: handle log-update event ', data)
					break
				default:
					showErrorToast('Unbekannten Nachrichtentypen erhalten: ' + data.messageType)
					console.error('Trainer received unknown message type:', data.messageType, 'with data:', data)
			}
		}
	}

	close() {
		if (this.socket) this.socket.close()
	}

	#sendMessage(message: string) {
		if (connection.trainerConnected && this.socket) {
			this.socket.send(message)
		} else {
			console.log('Trainer WebSocket is not connected.')
		}
	}

	testPassthrough() {
		this.#sendMessage(JSON.stringify({'messageType': 'test-passthrough'}))
	}

	exerciseCreate() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-create'}))
	}

	exerciseStart() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-start'}))
	}

	exerciseStop() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-stop'}))
	}

	areaAdd() {
		this.#sendMessage(JSON.stringify({'messageType': 'area-add'}))
	}

	areaDelete(areaName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'area-delete',
			'areaName': areaName
		}))
	}

	patientAdd(areaName: string, patientName: string, patientCode: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-add',
			'areaName': areaName,
			'patientName': patientName,
			'patientCode': patientCode
		}))
	}

	patientUpdate(patientId: number, patientName: string, patientCode: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-update',
			'patientId': patientId,
			'patientName': patientName,
			'patientCode': patientCode
		}))
	}

	patientDelete(patientId: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-delete',
			'patientId': patientId
		}))
	}
}

const socketTrainer = new SocketTrainer('ws://localhost:8000/ws/trainer/?token=')
export default socketTrainer

export const serverMockEvents = [
	{id: 'failure', data: '{"messageType":"failure","message":"Error encountered"}'},
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{
		id: "available-patients",
		data: '{"messageType":"available-patients","availablePatients":{"availablePatients":['+
			'{"patientCode":1,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 30 Jahre alt","patientBiometrics":"Größe: 196cm, Gewicht: 76kg"},'+
			'{"patientCode":2,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 47 Jahre alt","patientBiometrics":"Größe: 164cm, Gewicht: 65kg"},'+
			'{"patientCode":3,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 20 Jahre alt","patientBiometrics":"Größe: 192cm, Gewicht: 77kg"},'+
			'{"patientCode":4,'+
			'"triage":"Y","patientInjury":"Gebprelltes Bein","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 13 Jahre alt","patientBiometrics":"Größe: 165cm, Gewicht: 54kg"},'+
			'{"patientCode":5,'+
			'"triage":"G","patientInjury":"Butender Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 53 Jahre alt","patientBiometrics":"Größe: 180cm, Gewicht: 71kg"},'+
			'{"patientCode":6,'+
			'"triage":"Y","patientInjury":"Verschobene Schulter","patientHistory":"Gehbehindert",'+
			'"patientPersonalDetails":"männlich, 49 Jahre alt","patientBiometrics":"Größe: 170cm, Gewicht: 67kg"},'+
			'{"patientCode":7,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 162cm, Gewicht: 67kg"},'+
			'{"patientCode":8,'+
			'"triage":"Y","patientInjury":"Verlorener Finger","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"männlich, 43 Jahre alt","patientBiometrics":"Größe: 161cm, Gewicht: 56kg"},'+
			'{"patientCode":9,'+
			'"triage":"G","patientInjury":"Aufgschürfter Ellenbogen","patientHistory":"Bluthochdruck",'+
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 182cm, Gewicht: 75kg"},'+
			'{"patientCode":10,'+
			'"triage":"Y","patientInjury":"Gebrochene Nase","patientHistory":"Grippe",'+
			'"patientPersonalDetails":"männlich, 39 Jahre alt","patientBiometrics":"Größe: 173cm, Gewicht: 61kg"}'+
			']}}'
	},
	{
		id: 'exercise',
		data: '{"messageType":"exercise","exercise":{"exerciseId":123456,"areas":[' +
			'{"areaName":"Intensiv","patients":[{"patientId":5,"patientName":"Anna Müller","patientCode":1,"triage":"Y"},'+
			'{"patientId":3,"patientName":"Frank Huber",' +
			'"patientCode":2,"triage":"G"}],"personnel":[{"personnelId":1,"personnelName":"Sebastian Lieb"}],"devices":' +
			'[{"deviceId":1,"deviceName":"Treadmill"}]},{"areaName":"ZNA","patients":' +
			'[{"patientId":2,"patientName":"Luna Patel","patientCode":3,"triage":"R"},' + 
			'{"patientId":6,"patientName":"Friedrich Gerhard","patientCode":4,"triage":"Y"}],'+
			'"personnel":[{"personnelId":2,"personnelName":"Hannah Mayer"}],"devices":[{"deviceId":2,"deviceName":"Dumbbells"}]},' +
			'{"areaName":"Wagenhalle","patients":[{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
			'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}],' +
			'"personnel":[{"personnelId":3,"personnelName":"Coach Flex"}],' +
			'"devices":[{"deviceId":3,"deviceName":"Beatmungsgerät"}]}]}}'
	},
	{id: 'exercise-start', data: '{"messageType":"exercise-start"}'},
	{id: 'exercise-stop', data: '{"messageType":"exercise-stop"}'},
	{
		id: 'log-update',
		data: '{"messageType":"log-update","logEntry":[' +
			'{"logMessage":"Patient admitted","logTime":' + Date.UTC(2024, 2, 20, 14, 32, 20, 0) +
			',"areaName":"EmergencyRoom","patientId":123,"personnelId":456,"deviceId":789},' +
			'{"logMessage":"Treatment started","logTime":' + Date.UTC(2024, 2, 20, 14, 32, 46, 0) +
			',"areaName":"Operating Theater","patientId":123,"personnelId":456,"deviceId":789},' +
			'{"logMessage":"Patient stabilized","logTime":' + Date.UTC(2024, 2, 20, 14, 33, 8, 0) +
			',"areaName":"ICU","patientId":123,"personnelId":456,"deviceId":789}]}'
	}
]
