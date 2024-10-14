import { WebSocket } from 'ws'; // Use require for WebSocket


export class SocketPatient {
	constructor(url) {
		this.url = url;
		this.socket = null;
		this.connected = false;
	}

	connect(token) {
		this.socket = new WebSocket(this.url + token);

		this.socket.onopen = () => {
			console.log('Patient WebSocket connection established');
			this.connected = true;
		};

		this.socket.onclose = () => {
			console.log('Patient WebSocket connection closed');
			this.connected = false;
		};

		this.socket.onerror = (error) => {
			console.error('Patient WebSocket error:', error);
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
					break;
				case 'state':
					break;
				case 'continuous-variable':
					break;
				case 'available-patients':
					break;
				case 'available-actions':
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
				case 'delete':
					console.log('Patient WebSocket ToDo: handle delete event ', data);
					break;
				case 'information':
					console.log('Patient WebSocket ToDo: handle information event ', data);
					break;
				case 'action-confirmation':
					break;
				case 'action-declination':
					break;
				case 'action-result':
					console.log('Patient WebSocket ToDo: handle action-result event ', data);
					break;
				case 'resource-assignments':
					break;
				case 'action-list':
					break;
				case 'visible-injuries':
					break;
				case 'action-check':
					break;
				case 'patient-relocating':
					break;
				case 'patient-back':
					break;
				default:
					console.error('Patient received unknown message type:', data.messageType, 'with data:', data);
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
			console.log('Patient WebSocket is not connected.');
		}
	}

	actionAdd(actionName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-add',
			'actionName': actionName,
		}));
	}

	testPassthrough() {
		this.sendMessage(JSON.stringify({ 'messageType': 'test-passthrough' }));
	}

	triage(triage) {
		this.sendMessage(JSON.stringify({
			'messageType': 'triage',
			'triage': triage,
		}));
	}

	releasePersonnel(personnelId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-release',
			'personnelId': personnelId,
		}));
	}

	assignPersonnel(personnelId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-assign',
			'personnelId': personnelId,
		}));
	}

	releaseMaterial(materialId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-release',
			'materialId': materialId,
		}));
	}

	assignMaterial(materialId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-assign',
			'materialId': materialId,
		}));
	}

	cancelAction(actionId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-cancel',
			'actionId': actionId,
		}));
	}

	movePatient(areaId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'patient-move',
			'areaId': areaId,
		}));
	}

	movePersonnel(personnelId, areaId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-move',
			'personnelId': personnelId,
			'areaId': areaId,
		}));
	}

	moveMaterial(materialId, areaId) {
		this.sendMessage(JSON.stringify({
			'messageType': 'material-move',
			'materialId': materialId,
			'areaId': areaId,
		}));
	}

	actionCheck(actionName) {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-check',
			'actionName': actionName,
		}));
	}

	stopActionCheck() {
		this.sendMessage(JSON.stringify({
			'messageType': 'action-check-stop',
		}));
	}
}