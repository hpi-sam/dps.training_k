import {connection} from "@/stores/Connection"
import {usePatientStore} from "@/stores/Patient"
import {useExerciseStore} from "@/stores/Exercise"
import {useAvailablesStore} from "@/stores/Availables"
import {showErrorToast, showWarningToast} from "@/App.vue"
import {ScreenPosition, Screens, setScreen} from "@/components/ModulePatient.vue"
import {allowNewActions} from "@/components/widgets/ActionConfig.vue"
import {useRessourceAssignmentsStore} from "@/stores/RessourceAssignments"

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
		data: '{"messageType":"available-patients","availablePatients":{"availablePatients":[' +
			'{"patientCode":1,' +
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",' +
			'"patientPersonalDetails":"weiblich, 30 Jahre alt","patientBiometrics":"Größe: 196cm, Gewicht: 76kg"},' +
			'{"patientCode":2,' +
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",' +
			'"patientPersonalDetails":"männlich, 47 Jahre alt","patientBiometrics":"Größe: 164cm, Gewicht: 65kg"},' +
			'{"patientCode":3,' +
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",' +
			'"patientPersonalDetails":"weiblich, 20 Jahre alt","patientBiometrics":"Größe: 192cm, Gewicht: 77kg"},' +
			'{"patientCode":4,' +
			'"triage":"Y","patientInjury":"Gebprelltes Bein","patientHistory":"Asthma",' +
			'"patientPersonalDetails":"männlich, 13 Jahre alt","patientBiometrics":"Größe: 165cm, Gewicht: 54kg"},' +
			'{"patientCode":5,' +
			'"triage":"G","patientInjury":"Butender Arm","patientHistory":"Asthma",' +
			'"patientPersonalDetails":"weiblich, 53 Jahre alt","patientBiometrics":"Größe: 180cm, Gewicht: 71kg"},' +
			'{"patientCode":6,' +
			'"triage":"Y","patientInjury":"Verschobene Schulter","patientHistory":"Gehbehindert",' +
			'"patientPersonalDetails":"männlich, 49 Jahre alt","patientBiometrics":"Größe: 170cm, Gewicht: 67kg"},' +
			'{"patientCode":7,' +
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Asthma",' +
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 162cm, Gewicht: 67kg"},' +
			'{"patientCode":8,' +
			'"triage":"Y","patientInjury":"Verlorener Finger","patientHistory":"Diabetes",' +
			'"patientPersonalDetails":"männlich, 43 Jahre alt","patientBiometrics":"Größe: 161cm, Gewicht: 56kg"},' +
			'{"patientCode":9,' +
			'"triage":"G","patientInjury":"Aufgschürfter Ellenbogen","patientHistory":"Bluthochdruck",' +
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 182cm, Gewicht: 75kg"},' +
			'{"patientCode":10,' +
			'"triage":"Y","patientInjury":"Gebrochene Nase","patientHistory":"Grippe",' +
			'"patientPersonalDetails":"männlich, 39 Jahre alt","patientBiometrics":"Größe: 173cm, Gewicht: 61kg"}' +
			']}}'
	},
	{
		id: 'available-actions',
		data: '{"messageType":"available-actions","availableActions":{"availableActions":[' +
			'{"actionName":"Blutdruck messen","actionType":"treatment"},{"actionName":"Blutprobe untersuchen","actionType":"lab"},' +
			'{"actionName":"Beatmungsmaske anlegen","actionType":"treatment"},' +
			'{"actionName":"Infusion anlegen","actionType":"treatment"},{"actionName":"Blut abnehmen","actionType":"treatment"},' +
			'{"actionName":"Medikament verabreichen","actionType":"treatment"},' +
			'{"actionName":"Ruheposition einnehmen","actionType":"treatment"},{"actionName":"Röntgen","actionType":"lab"},' +
			'{"actionName":"Wundversorgung","actionType":"treatment"},{"actionName":"Stabile Seitenlage","actionType":"treatment"},' +
			'{"actionName":"Schienung anlegen","actionType":"treatment"},{"actionName":"Vitalwerte messen","actionType":"treatment"}' +
			']}}'
	},
	{
		id: 'exercise',
		data: '{"messageType":"exercise","exercise":{"exerciseId":"abcdef","areas":[' +
			'{"areaName":"Intensiv",' +
			'"patients":[' +
			'{"patientId":5,"patientName":"Anna Müller","patientCode":1,"triage":"Y"},' +
			'{"patientId":3,"patientName":"Frank Huber","patientCode":2,"triage":"G"}' +
			'],' +
			'"personnel":[' +
			'{"personnelId":10,"personnelName":"Sebastian Lieb"},' +
			'{"personnelId":1,"personnelName":"Albert Spahn"},' +
			'{"personnelId":4,"personnelName":"Anna Neumann"}' +
			'],' +
			'"material":[' +
			'{"materialId":1,"materialName":"Beatmungsgerät"},' +
			'{"materialId":2,"materialName":"Defibrillator"}' +
			']' +
			'},' +
			'{"areaName":"ZNA",' +
			'"patients":[' +
			'{"patientId":2,"patientName":"Luna Patel","patientCode":3,"triage":"R"},' +
			'{"patientId":6,"patientName":"Friedrich Gerhard","patientCode":4,"triage":"Y"}' +
			'],' +
			'"personnel":[' +
			'{"personnelId":11,"personnelName":"Hannah Mayer"},' +
			'{"personnelId":3,"personnelName":"Jens Schweizer"},' +
			'{"personnelId":2,"personnelName":"Lena Schulze"},' +
			'{"personnelId":7,"personnelName":"Günther Beutle"},' +
			'{"personnelId":8,"personnelName":"Julian Mohn"},' +
			'{"personnelId":9,"personnelName":"Elisabeth Bauer"}' +
			'],' +
			'"material":[' +
			'{"materialId":3,"materialName":"Defibrillator"},' +
			'{"materialId":4,"materialName":"EKG-Monitor"},' +
			'{"materialId":7,"materialName":"Pulsoximeter"},' +
			'{"materialId":8,"materialName":"EEG"},' +
			'{"materialId":9,"materialName":"Narkosegerät"}' +
			']' +
			'},' +
			'{"areaName":"Wagenhalle",' +
			'"patients":[' +
			'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
			'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}' +
			'],' +
			'"personnel":[' +
			'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
			'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
			'],' +
			'"material":[' +
			'{"materialId":5,"materialName":"EKG-Gerät"},' +
			'{"materialId":6,"materialName":"Blutdruckmessgerät"},' +
			'{"materialId":10,"materialName":"Beatmungsgerät"}' +
			']' +
			'}]}}'
	},
	{id: 'exercise-start', data: '{"messageType":"exercise-start"}'},
	{id: 'exercise-stop', data: '{"messageType":"exercise-stop"}'},
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
	}
]
