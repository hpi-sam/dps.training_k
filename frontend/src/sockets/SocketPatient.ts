import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {ScreenPosition, Screens, setScreen} from "@/components/ModulePatient.vue"

class SocketPatient {
	private readonly url: string
	socket: WebSocket | null = null

	constructor(url: string) {
		this.url = url
	}

	connect(): void {
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
					usePatientStore().loadStatusFromJSON(data.state as State)
					break
				case 'exercise':
					useExerciseStore().createFromJSON(data.exercise as Exercise)
					usePatientStore().patientName = useExerciseStore().getPatient(usePatientStore().patientId)?.patientName || ''
					usePatientStore().areaName = useExerciseStore().getAreaOfPatient(usePatientStore().patientId)?.areaName || ''
					usePatientStore().triage = useExerciseStore().getPatient(usePatientStore().patientId)?.triage || '-'
					break
				case 'exercise-start':
					setScreen(Screens.STATUS, ScreenPosition.LEFT)
					setScreen(Screens.ACTIONS, ScreenPosition.RIGHT)
					break
				case 'exercise-stop':
					setScreen(Screens.INACTIVE, ScreenPosition.FULL)
					break
				case 'delete':
					console.log('Patient Websocket ToDo: handle delete event ', data)
					break
				case 'information':
					console.log('Patient Websocket ToDo: handle information event ', data)
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
}

const socketPatient = new SocketPatient('ws://localhost:8000/ws/patient/?token=')
export default socketPatient

export const serverMockEvents = [
	{id: 'failure', data: '{"messageType":"failure","message":"Error encountered"}'},
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{
		id: 'state',
		data: '{"messageType":"state","state":{"phaseNumber":"123","airway":"Normal","breathing":"Regular","circulation":"Stable",' +
			'"consciousness":"Alert","pupils":"Reactive","psyche":"Calm","skin":"Warm"}}'
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
	{id: 'delete', data: '{"messageType":"delete"}'},
	{
		id: 'information',
		data: '{"messageType":"information","patientInjury":"Fractured limb","patientHistory":"No known allergies",' +
			'"patientPersonalDetails":"John Doe, Male, 30 years old","patientBiometrics":"Height: 180cm, Weight: 75kg"}'
	},
]
