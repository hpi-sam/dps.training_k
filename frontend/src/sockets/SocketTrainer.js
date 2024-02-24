import {connection} from "@/stores/Connection.js";
import {useTrainerStore} from "@/stores/Trainer.js";
import {useExerciseStore} from "@/stores/Exercise.js";
import {showErrorToast, showWarningToast} from "@/App.vue";
import {setLeftScreen as moduleTrainerSetLeftScreen, setRightScreen as moduleTrainerSetRightScreen} from "@/components/ModuleTrainer.vue"

class SocketTrainer {
	constructor(url) {
		this.url = url;
		this.socket = null;
	}

	connect() {
		this.socket = new WebSocket(this.url);

		this.socket.onopen = () => {
			console.log('Trainer WebSocket connection established');
			connection.trainerConnected = true;
			this.authentication(useTrainerStore().token)
		};

		this.socket.onclose = () => {
			console.log('Trainer WebSocket connection closed');
			connection.trainerConnected = false;
		};

		this.socket.onerror = (error) => {
			console.error('Trainer WebSocket error:', error);
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
				case 'exercise':
					useExerciseStore().createFromJSON(data.exercise)
					moduleTrainerSetLeftScreen('ScreenExerciseCreation')
					moduleTrainerSetRightScreen('ScreenResourceCreation')
					break;
				case 'exercise-start':
					console.log('Trainer Websocket ToDo: handle exercise-start event ', data)
					break;
				case 'exercise-stop':
					console.log('Trainer Websocket ToDo: handle exercise-stop event ', data)
					break;
				default:
					showErrorToast('Unbekannten Nachrichtentypen erhalten: ' + data.messageType)
					console.error('Trainer received unknown message type:', data.messageType, 'with data:', data)
			}
		}
	}

	close() {
		if (this.socket) this.socket.close();
	}

	#sendMessage(message) {
		if (connection.trainerConnected && this.socket) {
			this.socket.send(message);
		} else {
			console.log('Trainer WebSocket is not connected.');
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

	exerciseCreate() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-create'}))
	}

	exerciseStart() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-start'}))
	}

	exerciseStop() {
		this.#sendMessage(JSON.stringify({'messageType': 'exercise-stop'}))
	}
}

const socketTrainer = new SocketTrainer('ws://localhost:8000/ws/trainer/');
export default socketTrainer;

export const serverMockEvents = [
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{
		id: 'exercise',
		data: '{"messageType":"exercise","exercise":{"exerciseCode":"123456","areas":[{"name":"Area1",' +
			'"patients":[{"name":"John Doe","patientCode":"JD123","patientId":"39","patientDatabaseId":101}],' +
			'"personnel":[{"name":"Dr. Smith","role":"Therapist","personnelDatabaseId":201}],' +
			'"devices":[{"name":"DeviceA","deviceDatabaseId":301}]},{"name":"Area2",' +
			'"patients":[{"name":"Jane Doe","patientCode":"JD456","patientId":"33","patientDatabaseId":102}],' +
			'"personnel":[{"name":"Nurse Riley","role":"Nurse","personnelDatabaseId":202}],' +
			'"devices":[{"name":"DeviceB","deviceDatabaseId":302}]}]}}'
	},
	{id: 'exercise-start', data: '{"messageType":"exercise-start"}'},
	{id: 'exercise-stop', data: '{"messageType":"exercise-stop"}'},
];
