import {connection} from "@/stores/Connection"
import {useTrainerStore} from "@/stores/Trainer"
import {useExerciseStore} from "@/stores/Exercise"
import {Modules, setModule, showErrorToast, showWarningToast} from "@/App.vue"
import {useAvailablesStore} from "@/stores/Availables"
import {useLogStore} from "@/stores/Log"
import {commonMockEvents} from "./commonMockEvents"
import type {AvailableAction, AvailableMaterial, AvailablePatient, Exercise, LogEntry, MessageData} from "@/sockets/MessageData"

class SocketTrainer {
	private readonly url: string
	socket: WebSocket | null = null

	constructor(url: string) {
		this.url = url
	}

	connect() {
		const exerciseStore = useExerciseStore()

		this.socket = new WebSocket(this.url + useTrainerStore().token)

		this.socket.onopen = () => {
			console.log('Trainer WebSocket connection established')
			connection.trainerConnected = true
			socketTrainer.exerciseCreate()
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
				case 'warning':
					showWarningToast(data.message || '')
					break
				case 'test-passthrough':
					showWarningToast(data.message || '')
					break
				case 'available-actions':
					useAvailablesStore().loadAvailableActions(data.availableActions as AvailableAction[])
					break
				case 'available-materials':
					useAvailablesStore().loadAvailableMaterials(data.availableMaterials as AvailableMaterial[])
					break
				case 'available-patients':
					useAvailablesStore().loadAvailablePatients(data.availablePatients as AvailablePatient[])
					break
				case 'exercise':
					useExerciseStore().createFromJSON(data.exercise as Exercise)
					if (exerciseStore.status == '') {
						exerciseStore.status = 'not-started'
						setModule(Modules.TRAINER)
					}
					break
				case 'exercise-start':
					exerciseStore.status = 'running'
					break
				case 'exercise-pause':
					exerciseStore.status = 'paused'
					break
				case 'exercise-resume':
					exerciseStore.status = 'running'
					break
				case 'exercise-end':
					exerciseStore.status = 'ended'
					break
				case 'log-update':
					useLogStore().addLogEntries(data.logEntries as LogEntry[])
					break
				case 'set-speed':
					useExerciseStore().speed = data.speed
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

	exercisePause() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-pause'}))
	}

	exerciseResume() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-resume'}))
	}

	exerciseEnd() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-end'}))
	}

	areaAdd() {
		this.#sendMessage(JSON.stringify({'messageType': 'area-add'}))
	}

	areaDelete(areaId: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'area-delete',
			'areaId': areaId
		}))
	}

	areaRename(areaId: number, areaName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'area-rename',
			'areaId': areaId,
			'areaName': areaName
		}))
	}

	patientAdd(areaId: number, patientName: string, code: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-add',
			'areaId': areaId,
			'patientName': patientName,
			'code': code
		}))
	}

	patientUpdate(patientId: string, code: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-update',
			'patientId': patientId,
			'code': code
		}))
	}

	patientDelete(patientId: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-delete',
			'patientId': patientId
		}))
	}

	patientRename(patientId: string, patientName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'patient-rename',
			'patientId': patientId,
			'patientName': patientName
		}))
	}

	personnelAdd(areaId: number, personnelName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'personnel-add',
			'areaId': areaId,
			'personnelName': personnelName
		}))
	}

	personnelDelete(personnelId: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'personnel-delete',
			'personnelId': personnelId
		}))
	}

	personnelRename(personnelId: number, personnelName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'personnel-rename',
			'personnelId': personnelId,
			'personnelName': personnelName
		}))
	}

	materialAdd(areaId: number, materialName: string) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'material-add',
			'areaId': areaId,
			'materialName': materialName
		}))
	}

	materialDelete(materialId: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'material-delete',
			'materialId': materialId
		}))
	}

	setSpeed(speed: number) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'set-speed',
			'speed': speed
		}))
	}
}

const socketTrainer = new SocketTrainer(import.meta.env.VITE_SERVER_URL_WS + '/ws/trainer/?token=')
export default socketTrainer

export const serverMockEvents = [
	{
		id: "available-material",
		data: '{"messageType":"available-materials","availableMaterials":[' +
			'{"materialName":"Beatmungsgerät","materialType":"DE"},' +
			'{"materialName":"Blutdruckmessgerät","materialType":"DE"},' +
			'{"materialName":"Defibrillator","materialType":"DE"},' +
			'{"materialName":"Endoskop","materialType":"DE"},' +
			'{"materialName":"Herz-Lungen-Maschine","materialType":"DE"},' +
			'{"materialName":"Blut 0 negativ","materialType":"BL"},' +
			'{"materialName":"Blut 0 positiv","materialType":"BL"},' +
			'{"materialName":"Blut A negativ","materialType":"BL"},' +
			'{"materialName":"Blut A positiv","materialType":"BL"},' +
			'{"materialName":"Blut B negativ","materialType":"BL"},' +
			'{"materialName":"Blut B positiv","materialType":"BL"},' +
			'{"materialName":"Blut AB negativ","materialType":"BL"},' +
			'{"materialName":"Blut AB positiv","materialType":"BL"}' +
			']}'
	},
	{
		id: 'log-update-1',
		data: '{"messageType":"log-update","logEntries":[' +
			'{"logId":"0","logMessage":"Patient wurde ins Krankenhaus eingeliefert. ' +
			'Der Patient befindet sich in einem kritischen Zustand und benötigt sofortige Aufmerksamkeit.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 32, 20, 0) +
			',"areaId":2,"patientId":"123456","personnelIds":[]},' +
			'{"logId":"1","logMessage":"Behandlung des Patienten begonnen. ' +
			'Dem Patienten werden die notwendigen Medikamente verabreicht und er steht unter ständiger Überwachung.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 31, 46, 0) +
			',"areaId":1,"patientId":"123456","personnelIds":[11, 12]},' +
			'{"logId":"2","logMessage":"Patient nach der Erstbehandlung stabilisiert. ' +
			'Der Patient reagiert nun gut auf die Behandlung und wird beobachtet.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 33, 8, 0) +
			',"areaId":2,"patientId":"754262","personnelIds":[13]}]}'
	},
	{
		id: 'log-update-2',
		data: '{"messageType":"log-update","logEntries":[' +
			'{"logId":"4","logMessage":"Patient zur Zentralen Notaufnahme transportiert. ' +
			'Der Patient wird für weitere Tests und Behandlungen verlegt.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 31, 10, 0) +
			',"areaId":1,"patientId":"623422","personnelIds":[14]},' +
			'{"logId":"5","logMessage":"Behandlung aufgrund unvorhergesehener Komplikationen abgebrochen. ' +
			'Der Patient wird auf einen alternativen Behandlungsplan vorbereitet.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 33, 8, 0) +
			',"areaId":2,"patientId":"123456","personnelIds":[]},' +
			'{"logId":"6","logMessage":"Blut für den Patienten angefordert. ' +
			'Der Patient benötigt eine Bluttransfusion, um seinen Zustand zu stabilisieren.",' +
			'"logTime":' + Date.UTC(2024, 2, 20, 14, 32, 8, 0) +
			',"areaId":1,"patientId":"623422","personnelIds":[15, 11]}]}'
	},
	{
		id: 'set-speed',
		data: '{"messageType":"set-speed","speed":2.5}'
	},
	...commonMockEvents
]
