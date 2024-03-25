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
			'"triage":"Y","patientInjury":"broken arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"Female, 30 years old","patientBiometrics":"Height:196cm, Weight: 76kg"},'+
			'{"patientCode":2,'+
			'"triage":"G","patientInjury":"twisted ankle","patientHistory":"No known allergies",'+
			'"patientPersonalDetails":"Male, 47 years old","patientBiometrics":"Height:164cm, Weight: 65kg"},'+
			'{"patientCode":3,'+
			'"triage":"R","patientInjury":"head injury","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"Female, 20 years old","patientBiometrics":"Height:192cm, Weight: 77kg"},'+
			'{"patientCode":4,'+
			'"triage":"Y","patientInjury":"sprained wrist","patientHistory":"gastroesophageal reflux disease",'+
			'"patientPersonalDetails":"Male, 13 years old","patientBiometrics":"Height:165cm, Weight: 54kg"},'+
			'{"patientCode":5,'+
			'"triage":"G","patientInjury":"bruised ribs","patientHistory":"No known allergies",'+
			'"patientPersonalDetails":"Female, 53 years old","patientBiometrics":"Height:180cm, Weight: 71kg"},'+
			'{"patientCode":6,'+
			'"triage":"Y","patientInjury":"shoulder dislocation","patientHistory":"paralyzed",'+
			'"patientPersonalDetails":"Male, 49 years old","patientBiometrics":"Height:170cm, Weight: 67kg"},'+
			'{"patientCode":7,'+
			'"triage":"R","patientInjury":"head trauma","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"Female, 23 years old","patientBiometrics":"Height:162cm, Weight: 67kg"},'+
			'{"patientCode":8,'+
			'"triage":"Y","patientInjury":"bruised ribs","patientHistory":"reflux disease",'+
			'"patientPersonalDetails":"Male, 43 years old","patientBiometrics":"Height:161cm, Weight: 56kg"},'+
			'{"patientCode":9,'+
			'"triage":"G","patientInjury":"sprained wrist","patientHistory":"hearth disease",'+
			'"patientPersonalDetails":"Female, 23 years old","patientBiometrics":"Height:182cm, Weight: 75kg"},'+
			'{"patientCode":10,'+
			'"triage":"Y","patientInjury":"shoulder broken","patientHistory":"illness",'+
			'"patientPersonalDetails":"Male, 39 years old","patientBiometrics":"Height:173cm, Weight: 61kg"}'+
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
