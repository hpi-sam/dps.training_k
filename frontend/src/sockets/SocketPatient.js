import {connectionStore} from "@/sockets/ConnectionStore.js";
import {usePatientStore} from "@/stores/Patient.js";

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
			console.log('Patient received message:', message.data);
		};
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
			'message-type': 'authentication',
			'token': `${token}`
		}));
	}

	testPassthrough() {
		this.#sendMessage(JSON.stringify({'message-type': 'test-passthrough'}));
	}

	actionAdd(name) {
		this.#sendMessage(JSON.stringify({
			'message-type': 'action-add',
			'name': `${name}`
		}));
	}
}

// Export an instance of SocketClient
const socketPatient = new SocketPatient('ws://localhost:8000/ws/patient/');
export default socketPatient;
