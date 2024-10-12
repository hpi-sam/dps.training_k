import { Worker } from 'worker_threads';
import now from 'performance-now';

const TEST_DURATION = 1000; // in ms
const NUM_EXERCISES = 2
export const NUM_TRAINER_PER_EXERCISE = 5; // = NUM_AREAS
export const NUM_PATIENTS_PER_AREA = 10
export const NUM_PERSONNEL_PER_PATIENT = 5

let results = [];
let workerCount = 0;

function startWorker(userIndex) {
	return new Promise((resolve, reject) => {
		const worker = new Worker('./exercise.js', {
			workerData: { userIndex }
		});

		worker.on('message', (result) => {
			results.push(result); // Gather results from worker
			resolve(result);
		});

		worker.on('error', reject);
		worker.on('exit', (code) => {
			if (code !== 0) {
				reject(new Error(`Worker stopped with exit code ${code}`));
			}
		});
	});
}

async function runStressTest() {

	const workerPromises = [];
	for (let i = 0; i < NUM_EXERCISES; i++) {
		workerPromises.push(startWorker());
	}
	await Promise.all(workerPromises);


	// results
	console.log(`Total workers executed: ${workerCount}`);
	console.log('Performance results:', results);

	const avgResponseTime = results.reduce((acc, curr) => acc + curr.responseTime, 0) / results.length;
	console.log(`Average response time: ${avgResponseTime.toFixed(2)} ms`);
}

runStressTest();
