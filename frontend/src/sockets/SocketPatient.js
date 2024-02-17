import {connectionStore} from "@/sockets/ConnectionStore.js";
import {usePatientStore} from "@/stores/Patient.js";
import {showErrorToast, showWarningToast} from "@/App.vue";


class SocketPatient {
	constructor(url) {
		this.url = url;
		this.socket = null;
	}

	connect() {
		this.socket = new WebSocket(this.url);

		this.socket.onopen = () => {
			console.log('Patient WebSocket connection established');
			connectionStore.patientConnected = true;
			this.authentication(usePatientStore().token)
		};

		this.socket.onclose = () => {
			console.log('Patient WebSocket connection closed');
			connectionStore.patientConnected = false;
		};

		this.socket.onerror = (error) => {
			console.error('Patient WebSocket error:', error);
		};

		this.socket.onmessage = (message) => {
			let data
			try {
				data = JSON.parse(message.data)
			} catch (e) {
				console.error('Error parsing message data:', e);
				console.error('Problematic message data:', message.data);
				return
			}

			switch (data.messageType) {
				case 'test-passthrough':
					showWarningToast(data.message)
					break;
				case 'load-stopped':
					console.log('Patient Websocket ToDo: handle load-stopped event ', data)
					break;
				case 'state':
					console.log('Patient Websocket ToDo: handle state event ', data)
					break;
				case 'exercise':
					console.log('Patient Websocket ToDo: handle exercise event ', data)
					break;
				case 'exercise-start':
					console.log('Patient Websocket ToDo: handle exercise-start event ', data)
					break;
				case 'exercise-stop':
					console.log('Patient Websocket ToDo: handle exercise-stop event ', data)
					break;
				default:
					showErrorToast('Unbekannten Nachrichtentypen erhalten:' + data.messageType)
					console.error('Patient received unknown message type:', data.messageType, 'with data:', data)
			}
		}
	}

	close() {
		if (this.socket) this.socket.close();
	}

	#sendMessage(message) {
		if (connectionStore.patientConnected && this.socket) {
			this.socket.send(message);
		} else {
			console.log('Patient WebSocket is not connected.');
		}
	}

	authentication(token) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'authentication',
			'token': `${token}`
		}));
	}

	testPassthrough() {
		this.#sendMessage(JSON.stringify({'messageType': 'test-passthrough'}));
	}

	actionAdd(name) {
		this.#sendMessage(JSON.stringify({
			'messageType': 'action-add',
			'name': `${name}`
		}));
	}
}

// Export an instance of SocketClient
const socketPatient = new SocketPatient('ws://localhost:8000/ws/patient/');
export default socketPatient;
