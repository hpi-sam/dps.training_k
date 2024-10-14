import { WebSocket } from 'ws';

class EventCallbacks {
	constructor() {
		this.testPassthroughs = []
		this.exercises = []
		this.exerciseStarts = []
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
		};

		this.socket.onclose = () => {
			this.connected = false;
		};

		this.socket.onerror = (error) => {
			console.error('Trainer WebSocket error:', error);
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
					try {
						(this.callbacks.exercises.shift())(data.exercise);
					} catch (e) {
						console.error("TrainerSocket exercise cb not created");
					}
					break;
				case 'exercise-start':
					(this.callbacks.exerciseStarts.shift())();
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
		this.callbacks.testPassthroughs.push(cb);
		this.sendMessage(JSON.stringify({ 'messageType': 'test-passthrough' }));
	}

	exerciseCreate(cb) {
		this.callbacks.exercises.push(cb)
		this.sendMessage(JSON.stringify({ 'messageType': 'exercise-create' }));
	}

	exerciseStart(cb) {
		this.callbacks.exerciseStarts.push(cb)
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

	areaAdd(cb) {
		this.callbacks.exercises.push(cb)
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

	patientAdd(areaId, patientName, code, cb) {
		this.callbacks.exercises.push(cb)
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

	materialAdd(areaId, materialName, cb) {
		this.callbacks.exercises.push(cb)
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