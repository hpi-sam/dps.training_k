import { Worker } from 'worker_threads';

const NUM_EXERCISES = 100

let results = [];
let workerCount = 0;

function startWorker(userIndex) {
	return new Promise((resolve, reject) => {
		const worker = new Worker('./assignMaterial.js', {
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
	for (let i = 0; i < NUM_EXERCISES; i++) {
		console.log("Processing iteration " + i)
		await startWorker(i);
	}

	console.log(`Total workers executed: ${workerCount}`);
	console.log('Performance results:', results);

	const avgResponseTime = results.reduce((acc, curr) => acc + curr.responseTime, 0) / results.length;
	const variance = results.reduce((acc, curr) => acc + Math.pow(curr.responseTime - avgResponseTime, 2), 0) / results.length;
	console.log(`Average response time: ${avgResponseTime.toFixed(4)} ms`);
	console.log(`Variance: ${variance.toFixed(4)} ms^2`);
}

runStressTest();
