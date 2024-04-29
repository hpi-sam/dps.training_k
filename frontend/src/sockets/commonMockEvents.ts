export const commonMockEvents = [
	{id: 'failure', data: '{"messageType":"failure","message":"Error encountered"}'},
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{
		id: "available-patients",
		data: '{"messageType":"available-patients","availablePatients":{"availablePatients":['+
			'{"patientCode":1,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 30 Jahre alt","patientBiometrics":"Größe: 196cm, Gewicht: 76kg"},'+
			'{"patientCode":2,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 47 Jahre alt","patientBiometrics":"Größe: 164cm, Gewicht: 65kg"},'+
			'{"patientCode":3,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 20 Jahre alt","patientBiometrics":"Größe: 192cm, Gewicht: 77kg"},'+
			'{"patientCode":4,'+
			'"triage":"Y","patientInjury":"Gebprelltes Bein","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 13 Jahre alt","patientBiometrics":"Größe: 165cm, Gewicht: 54kg"},'+
			'{"patientCode":5,'+
			'"triage":"G","patientInjury":"Butender Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 53 Jahre alt","patientBiometrics":"Größe: 180cm, Gewicht: 71kg"},'+
			'{"patientCode":6,'+
			'"triage":"Y","patientInjury":"Verschobene Schulter","patientHistory":"Gehbehindert",'+
			'"patientPersonalDetails":"männlich, 49 Jahre alt","patientBiometrics":"Größe: 170cm, Gewicht: 67kg"},'+
			'{"patientCode":7,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 162cm, Gewicht: 67kg"},'+
			'{"patientCode":8,'+
			'"triage":"Y","patientInjury":"Verlorener Finger","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"männlich, 43 Jahre alt","patientBiometrics":"Größe: 161cm, Gewicht: 56kg"},'+
			'{"patientCode":9,'+
			'"triage":"G","patientInjury":"Aufgschürfter Ellenbogen","patientHistory":"Bluthochdruck",'+
			'"patientPersonalDetails":"weiblich, 23 Jahre alt","patientBiometrics":"Größe: 182cm, Gewicht: 75kg"},'+
			'{"patientCode":10,'+
			'"triage":"Y","patientInjury":"Gebrochene Nase","patientHistory":"Grippe",'+
			'"patientPersonalDetails":"männlich, 39 Jahre alt","patientBiometrics":"Größe: 173cm, Gewicht: 61kg"},'+
			'{"patientCode":11,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"weiblich, 29 Jahre alt","patientBiometrics":"Größe: 190cm, Gewicht: 78kg"},'+
			'{"patientCode":12,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 35 Jahre alt","patientBiometrics":"Größe: 174cm, Gewicht: 62kg"},'+
			'{"patientCode":13,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 45 Jahre alt","patientBiometrics":"Größe: 185cm, Gewicht: 72kg"},'+
			'{"patientCode":14,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 27 Jahre alt","patientBiometrics":"Größe: 180cm, Gewicht: 70kg"},'+
			'{"patientCode":15,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 33 Jahre alt","patientBiometrics":"Größe: 177cm, Gewicht: 69kg"},'+
			'{"patientCode":16,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 41 Jahre alt","patientBiometrics":"Größe: 167cm, Gewicht: 64kg"},'+
			'{"patientCode":17,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 25 Jahre alt","patientBiometrics":"Größe: 186cm, Gewicht: 73kg"},'+
			'{"patientCode":18,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 37 Jahre alt","patientBiometrics":"Größe: 168cm, Gewicht: 65kg"},'+
			'{"patientCode":19,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"weiblich, 49 Jahre alt","patientBiometrics":"Größe: 176cm, Gewicht: 70kg"},'+
			'{"patientCode":20,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"männlich, 31 Jahre alt","patientBiometrics":"Größe: 179cm, Gewicht: 71kg"},'+
			'{"patientCode":21,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 39 Jahre alt","patientBiometrics":"Größe: 175cm, Gewicht: 68kg"},'+
			'{"patientCode":22,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 43 Jahre alt","patientBiometrics":"Größe: 170cm, Gewicht: 67kg"},'+
			'{"patientCode":23,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 19 Jahre alt","patientBiometrics":"Größe: 183cm, Gewicht: 74kg"},'+
			'{"patientCode":24,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 41 Jahre alt","patientBiometrics":"Größe: 171cm, Gewicht: 66kg"},'+
			'{"patientCode":25,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"weiblich, 47 Jahre alt","patientBiometrics":"Größe: 174cm, Gewicht: 68kg"},'+
			'{"patientCode":26,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"männlich, 33 Jahre alt","patientBiometrics":"Größe: 172cm, Gewicht: 67kg"},'+
			'{"patientCode":27,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"weiblich, 35 Jahre alt","patientBiometrics":"Größe: 173cm, Gewicht: 67kg"},'+
			'{"patientCode":28,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"männlich, 49 Jahre alt","patientBiometrics":"Größe: 175cm, Gewicht: 68kg"},'+
			'{"patientCode":29,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"weiblich, 21 Jahre alt","patientBiometrics":"Größe: 177cm, Gewicht: 69kg"},'+
			'{"patientCode":30,'+
			'"triage":"Y","patientInjury":"Gebrochener Arm","patientHistory":"Asthma",'+
			'"patientPersonalDetails":"männlich, 37 Jahre alt","patientBiometrics":"Größe: 176cm, Gewicht: 68kg"},'+
			'{"patientCode":31,'+
			'"triage":"G","patientInjury":"Verdrehter Knöchel","patientHistory":"Keine Allergien",'+
			'"patientPersonalDetails":"weiblich, 51 Jahre alt","patientBiometrics":"Größe: 178cm, Gewicht: 69kg"},'+
			'{"patientCode":32,'+
			'"triage":"R","patientInjury":"Kopfverletzung","patientHistory":"Diabetes",'+
			'"patientPersonalDetails":"männlich, 35 Jahre alt","patientBiometrics":"Größe: 179cm, Gewicht: 70kg"}'+
			']}}'
	},
	{
		id: "available-material",
		data: '{"messageType":"available-material","availableMaterialList":{"availableMaterialList":['+
			'{"materialName":"Beatmungsgerät","materialType":"device"},'+
			'{"materialName":"Blutdruckmessgerät","materialType":"device"},'+
			'{"materialName":"Defibrillator","materialType":"device"},'+
			'{"materialName":"Endoskop","materialType":"device"},'+
			'{"materialName":"Herz-Lungen-Maschine","materialType":"device"},'+
			'{"materialName":"Blut 0 negativ","materialType":"blood"},'+
			'{"materialName":"Blut 0 positiv","materialType":"blood"},'+
			'{"materialName":"Blut A negativ","materialType":"blood"},'+
			'{"materialName":"Blut A positiv","materialType":"blood"},'+
			'{"materialName":"Blut B negativ","materialType":"blood"},'+
			'{"materialName":"Blut B positiv","materialType":"blood"},'+
			'{"materialName":"Blut AB negativ","materialType":"blood"},'+
			'{"materialName":"Blut AB positiv","materialType":"blood"}'+
			']}}'
	},
	{
		id: 'exercise',
		data: '{"messageType":"exercise","exercise":{"exerciseId":123456,"areas":[' +
			'{"areaName":"Intensiv",'+
				'"patients":['+
					'{"patientId":5,"patientName":"Anna Müller","patientCode":1,"triage":"Y"},'+
					'{"patientId":3,"patientName":"Frank Huber","patientCode":2,"triage":"G"}'+
				'],'+
				'"personnel":['+
					'{"personnelId":10,"personnelName":"Sebastian Lieb"},'+
					'{"personnelId":1,"personnelName":"Albert Spahn"}'+
				'],'+
				'"material":['+
					'{"materialId":1,"materialName":"Beatmungsgerät","materialType":"device"},'+
					'{"materialId":2,"materialName":"Defibrillator","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"ZNA",'+
				'"patients":['+
					'{"patientId":2,"patientName":"Luna Patel","patientCode":3,"triage":"R"},' + 
					'{"patientId":6,"patientName":"Friedrich Gerhard","patientCode":4,"triage":"Y"},'+
					'{"patientId":7,"patientName":"Hans Schmidt","patientCode":4,"triage":"Y"},' +
					'{"patientId":8,"patientName":"Johannes Müller","patientCode":4,"triage":"Y"},' +
					'{"patientId":9,"patientName":"Sophie Schneider","patientCode":4,"triage":"Y"},' +
					'{"patientId":10,"patientName":"Lisa Fischer","patientCode":4,"triage":"Y"},' +
					'{"patientId":11,"patientName":"Julia Meyer","patientCode":4,"triage":"Y"},' +
					'{"patientId":12,"patientName":"Max Weber","patientCode":4,"triage":"Y"},' +
					'{"patientId":13,"patientName":"Lukas Wagner","patientCode":4,"triage":"Y"},' +
					'{"patientId":14,"patientName":"Laura Becker","patientCode":4,"triage":"Y"},' +
					'{"patientId":15,"patientName":"Anna Schäfer","patientCode":4,"triage":"Y"},' +
					'{"patientId":16,"patientName":"David Hoffmann","patientCode":4,"triage":"Y"},' +
					'{"patientId":17,"patientName":"Sarah Bauer","patientCode":4,"triage":"Y"},' +
					'{"patientId":18,"patientName":"Michael Schulz","patientCode":4,"triage":"Y"},' +
					'{"patientId":19,"patientName":"Stefan Lehmann","patientCode":4,"triage":"Y"},' +
					'{"patientId":20,"patientName":"Christina Krüger","patientCode":4,"triage":"Y"},' +
					'{"patientId":21,"patientName":"Andreas Koch","patientCode":4,"triage":"Y"}' +
				'],'+
				'"personnel":['+
					'{"personnelId":11,"personnelName":"Hannah Mayer"},'+
					'{"personnelId":3,"personnelName":"Jens Schweizer"},'+
					'{"personnelId":2,"personnelName":"Lena Schulze"},'+
					'{"personnelId":7,"personnelName":"Günther Beutle"},' +
					'{"personnelId":8,"personnelName":"Julian Mohn"},'+
					'{"personnelId":9,"personnelName":"Elisabeth Bauer"},'+
					'{"personnelId":12,"personnelName":"Hans Schmidt"},' +
					'{"personnelId":13,"personnelName":"Johannes Müller"},' +
					'{"personnelId":14,"personnelName":"Sophie Schneider"},' +
					'{"personnelId":15,"personnelName":"Lisa Fischer"},' +
					'{"personnelId":16,"personnelName":"Julia Meyer"},' +
					'{"personnelId":17,"personnelName":"Max Weber"},' +
					'{"personnelId":18,"personnelName":"Lukas Wagner"},' +
					'{"personnelId":19,"personnelName":"Laura Becker"},' +
					'{"personnelId":20,"personnelName":"Anna Schäfer"},' +
					'{"personnelId":21,"personnelName":"David Hoffmann"},' +
					'{"personnelId":22,"personnelName":"Sarah Bauer"}' +
				'],'+
				'"material":['+
					'{"materialId":3,"materialName":"EKG-Maschine","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"},' +
					'{"materialId":11,"materialName":"Defibrillator","materialType":"device"},' +
					'{"materialId":12,"materialName":"Anästhesiegerät","materialType":"device"},' +
					'{"materialId":13,"materialName":"Elektrochirurgiegerät","materialType":"device"},' +
					'{"materialId":14,"materialName":"Herzschrittmacher","materialType":"device"},' +
					'{"materialId":15,"materialName":"Infusionspumpe","materialType":"device"},' +
					'{"materialId":16,"materialName":"Patientenmonitor","materialType":"device"},' +
					'{"materialId":17,"materialName":"Ultraschallgerät","materialType":"device"},' +
					'{"materialId":18,"materialName":"MRT-Gerät","materialType":"device"},' +
					'{"materialId":19,"materialName":"Röntgengerät","materialType":"device"},' +
					'{"materialId":20,"materialName":"CT-Scanner","materialType":"device"},' +
					'{"materialId":4,"materialName":"EKG-Monitor","materialType":"device"},'+
					'{"materialId":7,"materialName":"Pulsoximeter","materialType":"device"},'+
					'{"materialId":8,"materialName":"EEG","materialType":"device"},'+
					'{"materialId":9,"materialName":"Narkosegerät","materialType":"device"}'+
				']'+
			'},' +
			'{"areaName":"Wagenhalle",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle2",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle3",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle4",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle5",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle6",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle7",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle8",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle9",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle10",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle11",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle12",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle13",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle14",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle15",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'},'+
			'{"areaName":"Wagenhalle16",'+
				'"patients":['+
					'{"patientId":1,"patientName":"Isabelle Busch","patientCode":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","patientCode":6,"triage":"Y"}'+
				'],' +
				'"personnel":['+
					'{"personnelId":5,"personnelName":"Finn Heizmann"},'+
					'{"personnelId":6,"personnelName":"Ursula Seiler"}'+
				'],' +
				'"material":['+
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},'+
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},'+
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}'+
				']'+
			'}'+
			']}}'
	},
	{id: 'exercise-started', data: '{"messageType":"exercise-started"}'},
	{id: 'exercise-paused', data: '{"messageType":"exercise-paused"}'},
	{id: 'exercise-resumed', data: '{"messageType":"exercise-resumed"}'},
	{id: 'exercise-ended', data: '{"messageType":"exercise-ended"}'},
]