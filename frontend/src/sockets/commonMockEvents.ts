export const commonMockEvents = [
	{id: 'failure', data: '{"messageType":"failure","message":"Error encountered"}'},
	{id: 'test-passthrough', data: '{"messageType":"test-passthrough","message":"received test-passthrough event"}'},
	{
		id: "available-patients",
		data: '{"messageType":"available-patients","availablePatients":[' +
			'{"code":1001,' +
			'"personalDetails":"Annkatrin Rohde 01.05.1989 Aulgasse 75, 53721 Siegburg",' +
			'"injury":"Schürfwunden beide Arme und Kopf; nicht mehr wesentlich blutend; leichte Bewegungseinschränkung im li. Ellbogengelenk",' +
			'"biometrics":"weiblich; ca. 27; braune Augen, braune Haare, 1,60 m",' +
			'"triage":"-",' +
			'"consecutiveUniqueNumber":-1,' +
			'"mobility":"initial gehfähig",' +
			'"preexistingIllnesses":"v. Jahren unklare Anämie; v. 2 J. OSG- Fraktur re.",' +
			'"permanentMedication":"keine Medikamente",' +
			'"currentCaseHistory":"kommt selbst zu Fuß ins KrHs: bisher keine medizinische Versorgung, Taschentuch auf Wunde.",' +
			'"pretreatment":"keine keine"},' +
			'{"code":1004,' +
			'"personalDetails":"Helena Raedder 15.03.1964 Albert-Einstein-Str. 34, 06122 Halle",' +
			'"injury":"ca. 8 cm große, weit klaffende Kopfplatzwunde re. temporal, blutet noch; im Wundgrund vermutlich Knochensplitter sichtbar.",' +
			'"biometrics":"weiblich; ca. 52; blond, braune Augen, Brille, 1,82 m",' +
			'"triage":"G",' +
			'"consecutiveUniqueNumber":5225,' +
			'"mobility":"initial gehfähig",' +
			'"preexistingIllnesses":"funktionelle Herzbeschwerden; beginnender Bechterew",' +
			'"permanentMedication":"Schlafmittel",' +
			'"currentCaseHistory":"wird vom Rettungsdienst gebracht: habe eine Deckenplatte vor den Kopf bekommen; Verband durchgeblutet; ' +
			'nicht bewusstlos gewesen.",' +
			'"pretreatment":" Wundversorgung,"}' +
			']}'
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
			'{"areaName":"Intensiv",' +
				'"patients":[' +
					'{"patientId":5,"patientName":"Anna Müller","code":1,"triage":"Y"},' +
					'{"patientId":3,"patientName":"Frank Huber","code":2,"triage":"G"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":10,"personnelName":"Sebastian Lieb"},' +
					'{"personnelId":1,"personnelName":"Albert Spahn"}' +
				'],' +
				'"material":[' +
					'{"materialId":1,"materialName":"Beatmungsgerät","materialType":"device"},' +
					'{"materialId":2,"materialName":"Defibrillator","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"ZNA",' +
				'"patients":[' +
					'{"patientId":123456,"patientName":"Luna Patel","code":1004,"triage":"R"},' +
					'{"patientId":6,"patientName":"Friedrich Gerhard","code":4,"triage":"Y"},' +
					'{"patientId":7,"patientName":"Hans Schmidt","code":4,"triage":"Y"},' +
					'{"patientId":8,"patientName":"Johannes Müller","code":4,"triage":"Y"},' +
					'{"patientId":9,"patientName":"Sophie Schneider","code":4,"triage":"Y"},' +
					'{"patientId":10,"patientName":"Lisa Fischer","code":4,"triage":"Y"},' +
					'{"patientId":11,"patientName":"Julia Meyer","code":4,"triage":"Y"},' +
					'{"patientId":12,"patientName":"Max Weber","code":4,"triage":"Y"},' +
					'{"patientId":13,"patientName":"Lukas Wagner","code":4,"triage":"Y"},' +
					'{"patientId":14,"patientName":"Laura Becker","code":4,"triage":"Y"},' +
					'{"patientId":15,"patientName":"Anna Schäfer","code":4,"triage":"Y"},' +
					'{"patientId":16,"patientName":"David Hoffmann","code":4,"triage":"Y"},' +
					'{"patientId":17,"patientName":"Sarah Bauer","code":4,"triage":"Y"},' +
					'{"patientId":18,"patientName":"Michael Schulz","code":4,"triage":"Y"},' +
					'{"patientId":19,"patientName":"Stefan Lehmann","code":4,"triage":"Y"},' +
					'{"patientId":20,"patientName":"Christina Krüger","code":4,"triage":"Y"},' +
					'{"patientId":21,"patientName":"Andreas Koch","code":4,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":11,"personnelName":"Hannah Mayer"},' +
					'{"personnelId":3,"personnelName":"Jens Schweizer"},' +
					'{"personnelId":2,"personnelName":"Lena Schulze"},' +
					'{"personnelId":7,"personnelName":"Günther Beutle"},' +
					'{"personnelId":8,"personnelName":"Julian Mohn"},' +
					'{"personnelId":9,"personnelName":"Elisabeth Bauer"},' +
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
				'],' +
				'"material":[' +
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
					'{"materialId":4,"materialName":"EKG-Monitor","materialType":"device"},' +
					'{"materialId":7,"materialName":"Pulsoximeter","materialType":"device"},' +
					'{"materialId":8,"materialName":"EEG","materialType":"device"},' +
					'{"materialId":9,"materialName":"Narkosegerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle2",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle3",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle4",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle5",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle6",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle7",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle8",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle9",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle10",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle11",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle12",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle13",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle14",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle15",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'},' +
			'{"areaName":"Wagenhalle16",' +
				'"patients":[' +
					'{"patientId":1,"patientName":"Isabelle Busch","code":5,"triage":"G"},' +
					'{"patientId":4,"patientName":"Jasper Park","code":6,"triage":"Y"}' +
				'],' +
				'"personnel":[' +
					'{"personnelId":5,"personnelName":"Finn Heizmann"},' +
					'{"personnelId":6,"personnelName":"Ursula Seiler"}' +
				'],' +
				'"material":[' +
					'{"materialId":5,"materialName":"EKG-Gerät","materialType":"device"},' +
					'{"materialId":6,"materialName":"Blutdruckmessgerät","materialType":"device"},' +
					'{"materialId":10,"materialName":"Beatmungsgerät","materialType":"device"}' +
				']' +
			'}' +
		']}}'
	},
	{id: 'exercise-started', data: '{"messageType":"exercise-started"}'},
	{id: 'exercise-paused', data: '{"messageType":"exercise-paused"}'},
	{id: 'exercise-resumed', data: '{"messageType":"exercise-resumed"}'},
	{id: 'exercise-ended', data: '{"messageType":"exercise-ended"}'},
]