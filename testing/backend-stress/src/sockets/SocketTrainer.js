import { WebSocket } from 'ws'; // Use require for WebSocket
import { commonMockEvents } from './commonMockEvents.js'; // Use require for commonMockEvents

class EventCallbacks {
	constructor() {
		this.testPassthroughs = []
	}
}

export class SocketTrainer {
	constructor(url) {
		this.url = url;
		this.socket = null;
		this.connected = false;
		this.callbacks = new EventCallbacks()
	}

	connect(token, cb) {
		this.socket = new WebSocket(this.url + token);

		this.socket.onopen = () => {
			cb()
			this.connected = true;
			this.exerciseCreate();
		};

		this.socket.onclose = () => {
			//console.log('Trainer WebSocket connection closed');
			this.connected = false;
		};

		this.socket.onerror = (error) => {
			//console.error('Trainer WebSocket error:', error);
		};

		this.socket.onmessage = (message) => {
			let data;
			try {
				data = JSON.parse(message.data);
			} catch (e) {
				console.error('Error parsing message data:', e);
				console.error('Problematic message data:', message.data);
				return;
			}

			switch (data.messageType) {
				case 'failure':
					break;
				case 'warning':
					break;
				case 'test-passthrough':
					(this.callbacks.testPassthroughs.shift())(data.message)
					break;
				case 'available-actions':
					break;
				case 'available-materials':
					break;
				case 'available-patients':
					break;
				case 'exercise':
					break;
				case 'exercise-start':
					break;
				case 'exercise-pause':
					break;
				case 'exercise-resume':
					break;
				case 'exercise-end':
					break;
				case 'log-update':
					break;
				case 'set-speed':
					break;
				default:
					console.error('Trainer received unknown message type:', data.messageType, 'with data:', data);
			}
		};
	}

	close() {
		if (this.socket) this.socket.close();
	}

	sendMessage(message) {
		if (this.connected && this.socket) {
			this.socket.send(message);
		} else {
			console.log('Trainer WebSocket is not connected.');
		}
	}

	testPassthrough(cb) {
		this.sendMessage(JSON.stringify({ 'messageType': 'test-passthrough' }));
		this.callbacks.testPassthroughs.push(cb);
	}

	exerciseCreate() {
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-create' }));
	}

	exerciseStart() {
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-start' }));
	}

	exercisePause() {
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-pause' }));
	}

	exerciseResume() {
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-resume' }));
	}

	exerciseEnd() {
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-end' }));
	}

	areaAdd() {
		this.sendMessage(JSON.stringify({ 'messageType': 'area-add' }));
	}

	areaDelete(areaId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'area-delete',
			'areaId': areaId
		}));
	}

	areaRename(areaId, areaName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'area-rename',
			'areaId': areaId,
			'areaName': areaName
		}));
	}

	patientAdd(areaId, patientName, code) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-add',
			'areaId': areaId,
			'patientName': patientName,
			'code': code
		}));
	}

	patientUpdate(patientId, code) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-update',
			'patientId': patientId,
			'code': code
		}));
	}

	patientDelete(patientId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-delete',
			'patientId': patientId
		}));
	}

	patientRename(patientId, patientName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-rename',
			'patientId': patientId,
			'patientName': patientName
		}));
	}

	personnelAdd(areaId, personnelName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-add',
			'areaId': areaId,
			'personnelName': personnelName
		}));
	}

	personnelDelete(personnelId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-delete',
			'personnelId': personnelId
		}));
	}

	personnelRename(personnelId, personnelName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-rename',
			'personnelId': personnelId,
			'personnelName': personnelName
		}));
	}

	materialAdd(areaId, materialName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-add',
			'areaId': areaId,
			'materialName': materialName
		}));
	}

	materialDelete(materialId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-delete',
			'materialId': materialId
		}));
	}

	setSpeed(speed) {
		this.sendMessage(JSON.stringify({
			'messageType': 'set-speed',
			'speed': speed
		}));
	}
}

const serverMockEvents = [
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
];
