import { WebSocket } from 'ws';

class EventCallbacks {
	constructor() {
		this.testPassthroughs = []
		this.resourceAssignments = []
		this.actionConfirmationsDeclinations = []
		this.actionLists = []
		this.states = []
		this.continuousVariables = []
	}
}

export class SocketPatient {
	constructor(url) {
		this.url = url;
		this.socket = null;
		this.connected = false;
		this.callbacks = new EventCallbacks()
	}

	connect(token, cb) {
		this.socket = new WebSocket(this.url + token);

		this.socket.onopen = () => {
			this.callbacks.states.push(() => {})
			this.callbacks.continuousVariables.push(() => {})
			this.callbacks.actionLists.push(() => {})
			this.callbacks.resourceAssignments.push(() => {})
			this.connected = true;
			cb()
		};

		this.socket.onclose = () => {
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
					(this.callbacks.testPassthroughs.shift())(data.message)
					break;
				case 'state':
					(this.callbacks.states.shift())(data.state)
					break;
				case 'continuous-variable':
					(this.callbacks.continuousVariables.shift())(data.continuousState)
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
					break;
				case 'information':
					break;
				case 'action-confirmation':
					(this.callbacks.actionConfirmationsDeclinations.shift())(true)
					break;
				case 'action-declination':
					(this.callbacks.actionConfirmationsDeclinations.shift())(false)
					break;
				case 'resource-assignments':
					try {
						(this.callbacks.resourceAssignments.shift())(data.resourceAssignments)
					} catch (e) {
						console.error("PatientSocket resource-assignments cb not created");
					}
					break;
				case 'action-list':
					try {
						(this.callbacks.actionLists.shift())(data.actions)
					} catch (e) {
						console.error("PatientSocket action-list cb not created");
					}
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

	actionAdd(actionName, cb_conf, cb_list) {
		this.callbacks.actionConfirmationsDeclinations.push(cb_conf);
		this.callbacks.actionLists.push(() => {}); // IP
		this.callbacks.actionLists.push(() => {}); // IP #2???
		this.callbacks.actionLists.push(cb_list); // FI
		this.sendMessage(JSON.stringify({
			'messageType': 'action-add',
			'actionName': actionName,
		}));
	}

	testPassthrough(cb) {
		this.callbacks.testPassthroughs.push(cb);
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

	assignPersonnel(personnelId, cb) {
		this.callbacks.resourceAssignments.push(cb);
		this.sendMessage(JSON.stringify({
			'messageType': 'personnel-assign',
			'personnelId': personnelId,
		}));
	}

	releaseMaterial(materialId, cb) {
		this.callbacks.resourceAssignments.push(cb);
		this.sendMessage(JSON.stringify({
			'messageType': 'material-release',
			'materialId': materialId,
		}));
	}

	assignMaterial(materialId, cb) {
		this.callbacks.resourceAssignments.push(cb);
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

	addStateCb(cb_st) {
		this.callbacks.states.push(cb_st);
	}

	addContinuousVariableCb(cb) {
		this.callbacks.continuousVariables.push(cb);
	}
}