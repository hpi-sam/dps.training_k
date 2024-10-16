import { Worker } from 'worker_threads';

const NUM_EXERCISES = 2

let results = [];
let workerCount = 0;

function startWorker(userIndex) {
	return new Promise((resolve, reject) => {
		const worker = new Worker('./phaseChange.js', {
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
				setTimeout(() => reject(new Error('Timeout')), 60000)
			)
		])
			.catch(() => {
				results.push({
					i,
					responseTime_total: 0,
					responseTime_base: 0,
					responseTime_cv: 0,
					success: false
				})
			});
	}

	console.log(`Total workers executed: ${workerCount}`);
	console.log('Performance results:', results);

	const avgResponseTime_total = results.reduce((acc, curr) => acc + curr.responseTime_total, 0) / results.length;
	const variance_total = results.reduce((acc, curr) => acc + Math.pow(curr.responseTime_total - avgResponseTime_total, 2), 0) / results.length;
	const stdDeviation_total = Math.sqrt(variance_total);
	console.log(`Average response time total: ${avgResponseTime_total.toFixed(4)} ms`);
	console.log(`Variance total: ${variance_total.toFixed(4)} ms^2`);
	console.log(`Standard deviation total : ${stdDeviation_total.toFixed(4)} ms`);

	const avgResponseTime_base = results.reduce((acc, curr) => acc + curr.responseTime_base, 0) / results.length;
	const variance_base = results.reduce((acc, curr) => acc + Math.pow(curr.responseTime_base - avgResponseTime_base, 2), 0) / results.length;
	const stdDeviation_base = Math.sqrt(variance_base);
	console.log(`Average response time base: ${avgResponseTime_base.toFixed(4)} ms`);
	console.log(`Variance base: ${variance_base.toFixed(4)} ms^2`);
	console.log(`Standard deviation base : ${stdDeviation_base.toFixed(4)} ms`);

	const avgResponseTime_cv = results.reduce((acc, curr) => acc + curr.responseTime_cv, 0) / results.length;
	const variance_cv = results.reduce((acc, curr) => acc + Math.pow(curr.responseTime_cv - avgResponseTime_cv, 2), 0) / results.length;
	const stdDeviation_cv = Math.sqrt(variance_cv);
	console.log(`Average response time cv: ${avgResponseTime_cv.toFixed(4)} ms`);
	console.log(`Variance cv: ${variance_cv.toFixed(4)} ms^2`);
	console.log(`Standard deviation cv : ${stdDeviation_cv.toFixed(4)} ms`);

	const failedJobs = results.reduce((acc, curr) => {
		return acc + (curr.success === false ? 1 : 0);
	}, 0);
	console.log(`Failed jobs: ${failedJobs}`);
}

runStressTest();
