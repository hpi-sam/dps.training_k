import {connectionStore} from "@/sockets/ConnectionStore.js";

class SocketTrainer {
	constructor(url) {
		this.url = url;
		this.socket = null;
	}

	connect() {
		this.socket = new WebSocket(this.url);

		this.socket.onopen = () => {
			console.log('Trainer WebSocket connection established');
			connectionStore.trainerConnected = true;
		};

		this.socket.onclose = () => {
			console.log('Trainer WebSocket connection closed');
			connectionStore.trainerConnected = false;
		};

		this.socket.onerror = (error) => {
			console.error('Trainer WebSocket error:', error);
		};

		this.socket.onmessage = (message) => {
			console.log('Trainer received message:', message.data);
		};
	}

	close() {
		if (this.socket) this.socket.close();
	}

	#sendMessage(message) {
		if (connectionStore.trainerConnected && this.socket) {
			this.socket.send(message);
		} else {
			console.log('Trainer WebSocket is not connected.');
		}
	}

	testPassthrough() {
		console.log('Trainer sending test passthrough message')
		this.#sendMessage(JSON.stringify({'message-type': 'test-passthrough'}));
	}
}

// Export an instance of SocketClient
const socketTrainer = new SocketTrainer('ws://localhost:8000/ws/trainer/');
export default socketTrainer;
