import { Worker } from 'worker_threads';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url))
const NUM_EXERCISES = 2

let results = [];
let workerCount = 0;

function startWorker(userIndex) {
	const workerPath = resolve(__dirname, 'assignMaterial.js');

	return new Promise((resolve, reject) => {
		const worker = new Worker(workerPath, {
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
		await Promise.race([
			startWorker(i),
			new Promise((_, reject) =>
				setTimeout(() => reject(new Error('Timeout')), 90000)
			)
		])
			.catch((e) => {
				if (!e.message.includes('Timeout')) throw e;
				results.push({
					i,
					responseTime: 0,
					success: false,
					error: "manual timeout"
				})
			});
	}

	console.log(`Total workers executed: ${workerCount}`);
	console.log('Performance results:', results);

	const avgResponseTime = results.reduce((acc, curr) => acc + curr.responseTime, 0) / results.length;
	const variance = results.reduce((acc, curr) => acc + Math.pow(curr.responseTime - avgResponseTime, 2), 0) / results.length;
	const stdDeviation = Math.sqrt(variance);
	console.log(`Average response time: ${avgResponseTime.toFixed(4)} ms`);
	console.log(`Variance: ${variance.toFixed(4)} ms^2`);
	console.log(`Standard deviation: ${stdDeviation.toFixed(4)} ms`);

	const failedJobs = results.reduce((acc, curr) => {
		return acc + (curr.success === false ? 1 : 0);
	}, 0);
	console.log(`Failed jobs: ${failedJobs}`);
}

runStressTest();
