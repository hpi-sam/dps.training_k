import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "@/stores/Availables"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {ScreenPosition, Screens, setScreen} from "@/components/ModulePatient.vue"

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
				case 'exercise':
					exerciseStore.createFromJSON(data.exercise as Exercise)
					patientStore.initializePatientFromExercise()
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
		data: '{"messageType":"state","state":{"phaseNumber":"123","airway":"Normal","breathing":"Regelmäßig","circulation":"Stabil",' +
			'"consciousness":"Bewusstlos","pupils":"Geweitet","psyche":"Ruhig","skin":"Blass"}}'
	},
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
	{id: 'delete', data: '{"messageType":"delete"}'},
	{
		id: 'information',
		data: '{"messageType":"information","patientInjury":"Fractured limb","patientHistory":"No known allergies",' +
			'"patientPersonalDetails":"John Doe, Male, 30 years old","patientBiometrics":"Height: 180cm, Weight: 75kg"}'
	},
]
