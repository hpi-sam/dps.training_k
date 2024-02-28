import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {showErrorToast, showWarningToast} from "@/App.vue"

class SocketPatient {
	private readonly url: string
	socket: WebSocket | null = null

	constructor(url: string) {
		this.url = url
	}

	connect(): void {
		this.socket = new WebSocket(this.url)

		this.socket.onopen = () => {
			console.log('Patient WebSocket connection established')
			connection.patientConnected = true
			this.authentication(usePatientStore().token)
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
				case 'test-passthrough':
					showWarningToast(data.message || '')
					break
				case 'load-stopped':
					console.log('Patient Websocket ToDo: handle load-stopped event ', data)
					break
				case 'state':
					usePatientStore().loadStatusFromJSON(data.state as State)
					break
				case 'exercise':
					useExerciseStore().createFromJSON(data.exercise as Exercise)
					usePatientStore().areaName = useExerciseStore().getArea(usePatientStore().patientCode)?.name || ''
					break
				case 'exercise-start':
					console.log('Patient Websocket ToDo: handle exercise-start event ', data)
					break
				case 'exercise-stop':
					console.log('Patient Websocket ToDo: handle exercise-stop event ', data)
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

	authentication(token: string) {
		this.sendMessage(JSON.stringify({
			'messageType': 'authentication',
			'token': token,
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

	actionAdd(name: string) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-add',
			'name': name,
		}))
	}
}

const socketPatient = new SocketPatient('ws://localhost:8000/ws/patient/')
export default socketPatient

export const serverMockEvents = [
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{id: 'load-stopped', data: '{"messageType":"load-stopped","patientName":"John Doe","areaName":"Rehabilitation"}'},
	{
		id: 'state',
		data: '{"messageType":"state","state":{"phaseNumber":"123","airway":"Normal","breathing":"Regular","circulation":"Stable",' +
			'"consciousness":"Alert","pupils":"Reactive","psyche":"Calm","skin":"Warm"}}'
	},
	{
		id: 'exercise',
		data: '{"messageType":"exercise","exercise":{"exerciseCode":"123456","areas":[{"name":"Area1",' +
			'"patients":[{"name":"John Doe","patientCode":"JD123","patientId":"39","patientDatabaseId":101}],' +
			'"personnel":[{"name":"Dr. Smith","role":"Therapist","personnelDatabaseId":201}],' +
			'"devices":[{"name":"DeviceA","deviceDatabaseId":301}]},{"name":"Area2",' +
			'"patients":[{"name":"Jane Doe","patientCode":"JD456","patientId":"33","patientDatabaseId":102}],' +
			'"personnel":[{"name":"Nurse Riley","role":"Nurse","personnelDatabaseId":202}],' +
			'"devices":[{"name":"DeviceB","deviceDatabaseId":302}]}]}}'
	},
	{id: 'exercise-start', data: '{"messageType":"exercise-start"}'},
	{id: 'exercise-stop', data: '{"messageType":"exercise-stop"}'},
]
