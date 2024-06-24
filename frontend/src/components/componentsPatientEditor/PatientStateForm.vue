<script setup>
const createPatient = async (fields) => {
  await new Promise((r) => setTimeout(r, 1000))
  alert(JSON.stringify(fields))
}
</script>

<template>
	<!-- eslint-disable max-len -->
	<!-- eslint-disable vue/max-len -->
	<h1>Zustand</h1>
	<FormKit
		v-slot="{ value }"
		type="form"
		submit-label="Patient erstellen"
		@submit="createPatient"
	>
		<FormKit
			id="airway"
			name="airway"
			type="select"
			label="Atemwege"
			placeholder="Wähle den Zustand der Atemwege"
			:options="['freie Atemwege', 'künstlicher Atemweg', 'Atemwegsverlegung']"
			validation="required"
		/>

		<FormKit
			id="breathingRate"
			name="breathingRate"
			type="number"
			label="Atemfrequenz"
			placeholder="Atemzüge pro Minute"
			validation="required|min:0"
		/>

		<FormKit
			id="oxygenSaturation"
			name="oxygenSaturation"
			type="number"
			label="Sauerstoffsättigung"
			placeholder="SpO2 in %"
			validation="required|min:0"
		/>

		<FormKit
			id="breathing"
			name="breathing"
			type="select"
			label="Atmung"
			placeholder="Wähle den Zustand der Atmung"
			:options="['normale Atmung', 'vertiefte Atmung', 'flache Atmung', 'Beatmung', 'Atemstillstand']"
		/>

		<FormKit
			id="breathingSound"
			name="breathingSound"
			type="checkbox"
			label="Giemen und Brummen"
		/>

		<FormKit
			id="breathingLoudness"
			name="breathingLoudness"
			type="select"
			label="Atemgeräusche"
			placeholder="Sind Atemgeräusche hörbar?"
			:options="['normales AG hörbar', 'sehr leises AG hörbar', 'nur einseitiges AG hörbar', 'kein AG hörbar']"
		/>

		<FormKit
			id="heartRate"
			name="heartRate"
			type="number"
			label="Herzfrequenz"
			placeholder="Herzschläge pro Minute"
			validation="required|min:0"
		/>

		<FormKit
			id="pulsePalpable"
			name="pulsePalpable"
			type="select"
			label="Puls tastbar"
			placeholder="Ist der Puls tastbar?"
			:options="['peripher kräftig tastbar', 'peripher tastbar', 'nur zentral noch tastbar', 'zentral nicht tastbar']"
		/>

		<FormKit
			id="rivaRocci"
			name="rivaRocci"
			type="text"
			label="Riva-Rocci"
			placeholder="z.B. '115/75'"
			validation="required"
		/>

		<FormKit
			id="consciousness"
			name="consciousness"
			type="select"
			label="Bewusstsein"
			placeholder="Wähle den Zustand des Bewusstseins"
			:options="[
				'wach, orientiert',
				'wach, nicht orientiert',
				'somnolent',
				'keine Reaktion',
				'narkotisiert',
				'bewusstlos, gezielte Abwehr',
				'bewusstlos, Beugeabwehr',
				'bewusstlos, Beugekrämpfe auf Schmerzreiz',
				'bewusstlos, Streckkrämpfe auf Schmerzreiz'
			]"
		/>

		<FormKit
			id="pupils"
			name="pupils"
			type="select"
			label="Pupillen"
			placeholder="Wähle den Zustand der Pupillen"
			:options="['mittelweit', 'weit', 'weit, entrundet']"
		/>

		<FormKit
			id="psyche"
			name="psyche"
			type="select"
			label="Psyche"
			placeholder="Wähle den Zustand der Psyche"
			:options="['unauffällig', 'aufgeregt', 'sehr aufgeregt', 'hysterisch', 'verlangsamt', 'teilnahmslos']"
		/>

		<FormKit
			id="skinFinding"
			name="skinFining"
			type="select"
			label="Befund der Haut"
			placeholder="Wie ist der Befund der Haut?"
			:options="['kalt', 'trocken', 'feucht']"
		/>

		<FormKit
			id="skinDiscoloration"
			name="skinDiscoloration"
			type="select"
			label="Verfärbung der Haut"
			placeholder="Wie ist die Verfärbung der Haut?"
			:options="['rosig', 'blass', 'grau', 'grau/marmoriert', 'marmoriert', 'sichtbare Zyanose', 'leichte Zyanose', 'schwere Zyanose']"
		/>

		<FormKit
			id="bgaOxy"
			name="bgaOxy"
			type="select"
			label="Blutgaseanalyse für Oxygenierungsleistung"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 600, label: 'schwere Hypoxie' },
				{ value: 601, label: 'leichte Hypoxie' },
				{ value: 602, label: 'gute Oxygenierung' },
				{ value: 604, label: 'mäßige Hypoxie' },
				{ value: 613, label: 'nicht verwertbar' }
			]"
		/>

		<FormKit
			id="bgaSbh"
			name="bgaSbh"
			type="select"
			label="Blutgaseanalyse für Säure-Base-Haushalt"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 650, label: 'resp. Alkalose' },
				{ value: 651, label: 'kompensierte resp. Alkalose' },
				{ value: 652, label: 'kompensierte metabol. Alkalose' },
				{ value: 653, label: 'metabol. Alkalose' },
				{ value: 656, label: 'ausgeglichener SBH' },
				{ value: 657, label: 'kompensierte resp. Azidose' },
				{ value: 658, label: 'kompensierte metab. Azidose' },
				{ value: 659, label: 'resp. Azidose' },
				{ value: 661, label: 'metabol. Azidose' }
			]"
		/>

		<FormKit
			id="hb"
			name="hb"
			type="select"
			label="Hämoglobin"
			placeholder="Wähle einen Wert"
			:options="[
				{ value: 426, label: '2' },
				{ value: 414, label: '2.5' },
				{ value: 410, label: '3' },
				{ value: 409, label: '3.5' },
				{ value: 425, label: '4' },
				{ value: 429, label: '4.5' },
				{ value: 428, label: '5' },
				{ value: 404, label: '5.5' },
				{ value: 407, label: '6' },
				{ value: 417, label: '6.5' },
				{ value: 419, label: '7' },
				{ value: 406, label: '7.5' },
				{ value: 413, label: '8' },
				{ value: 415, label: '8.5' },
				{ value: 408, label: '9' },
				{ value: 400, label: '9.5' },
				{ value: 422, label: '10' },
				{ value: 403, label: '11' },
				{ value: 401, label: '12' },
				{ value: 405, label: '13' },
				{ value: 421, label: '14' },
				{ value: 423, label: '15' },
				{ value: 402, label: '16' },
				{ value: 412, label: '17' }
			]"
		/>

		<FormKit
			id="bz"
			name="bz"
			type="select"
			label="Blutzucker"
			placeholder="Wähle einen Wert"
			:options="[
				{ value: 947, label: '15' },
				{ value: 945, label: '20' },
				{ value: 956, label: '25' },
				{ value: 918, label: '30' },
				{ value: 935, label: '35' },
				{ value: 951, label: '40' },
				{ value: 933, label: '45' },
				{ value: 915, label: '50' },
				{ value: 924, label: '55' },
				{ value: 913, label: '60' },
				{ value: 950, label: '65' },
				{ value: 929, label: '70' },
				{ value: 936, label: '75' },
				{ value: 930, label: '80' },
				{ value: 927, label: '85' },
				{ value: 942, label: '90' },
				{ value: 916, label: '95' },
				{ value: 934, label: '100' },
				{ value: 953, label: '105' },
				{ value: 928, label: '110' },
				{ value: 954, label: '115' },
				{ value: 920, label: '120' },
				{ value: 906, label: '125' },
				{ value: 912, label: '130' },
				{ value: 926, label: '135' },
				{ value: 919, label: '140' },
				{ value: 955, label: '145' },
				{ value: 922, label: '150' },
				{ value: 908, label: '155' },
				{ value: 904, label: '160' },
				{ value: 909, label: '165' },
				{ value: 923, label: '175' },
				{ value: 914, label: '180' },
				{ value: 937, label: '185' },
				{ value: 910, label: '190' },
				{ value: 932, label: '195' },
				{ value: 939, label: '205' },
				{ value: 944, label: '215' },
				{ value: 941, label: '225' },
				{ value: 952, label: '235' },
				{ value: 917, label: '245' },
				{ value: 943, label: '255' },
				{ value: 957, label: '295' },
				{ value: 949, label: '305' },
				{ value: 925, label: '315' },
				{ value: 946, label: '325' },
				{ value: 921, label: '335' },
				{ value: 958, label: '345' },
				{ value: 911, label: '355' },
				{ value: 938, label: '365' },
				{ value: 931, label: '375' },
				{ value: 948, label: '385' },
				{ value: 905, label: '395' },
				{ value: 907, label: 'low' },
				{ value: 940, label: 'high' }
			]"
		/>

		<FormKit
			id="clotting"
			name="clotting"
			type="select"
			label="Gerinnung"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 100, label: 'leichte Einschränkung' },
				{ value: 104, label: 'Normalwerte' },
				{ value: 106, label: 'schwere Einschränkung' }
			]"
		/>

		<FormKit
			id="liver"
			name="liver"
			type="select"
			label="Leber"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 110, label: 'Normalwerte' },
				{ value: 111, label: 'leichte Einschränkung' },
				{ value: 112, label: 'schwere Einschränkung' }
			]"
		/>

		<FormKit
			id="kidney"
			name="kidney"
			type="select"
			label="Niere"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 122, label: 'Normalwerte' },
				{ value: 123, label: 'leichte Einschränkung' },
				{ value: 120, label: 'schwere Einschränkung' }
			]"
		/>

		<FormKit
			id="infarct"
			name="infarct"
			type="select"
			label="Infarkt"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 131, label: 'negativ' },
				{ value: 134, label: 'grenzwertig positiv' },
				{ value: 130, label: 'stark positiv' }
			]"
		/>

		<FormKit
			id="lactate"
			name="lactate"
			type="select"
			label="Laktat"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 140, label: 'negativ' },
				{ value: 144, label: 'grenzwertig positiv' },
				{ value: 141, label: 'stark positiv' }
			]"
		/>

		<FormKit
			id="extremities"
			name="extremities"
			type="select"
			label="Extremitäten Röntgen"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 511, label: 'Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;' },
				{ value: 512, label: 'Dislozierte Handgelenksfraktur; sonst keine Frakturen' },
				{ value: 520, label: 'Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 523, label: 'HüftTEP; sonst keine Auffälligkeiten' },
				{ value: 527, label: 'Extremitäten: Oberschenkelfraktur bds. im mittleren Drittel;' },
				{ value: 559, label: 'Spiralfraktur rechter Oberarm; sonst keine Frakturen' },
				{ value: 566, label: 'Oberschenkelfraktur re;' },
				{ value: 573, label: 'komplette Unterarmfraktur li. mit dezenter Verschiebung;' },
				{ value: 579, label: 'Extremitäten: Normalbefund; keine Frakturzeichen; mehrere Fremdkörper in beiden Händen;' },
				{ value: 591, label: 'fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.;' },
				{ value: 600, label: 'nicht dislozierte Sprunggelengsfraktur; sonst Extr. OB.' },
				{ value: 608, label: 'Sprunggelenksfraktur mit deutlicher Dislokation' },
				{ value: 625, label: 'Trümmerfraktur des distalen US re.; komplette proximale Unterarmfraktur re.' },
				{ value: 637, label: 'Oberschenkeltrummerfraktur re.' },
				{ value: 649, label: 'Oberschenkelschaftfraktur li mit Fehlstellung' },
				{ value: 664, label: 'Oberarmamputation li.; sonst keine Frakturzeichen oder Fremdkörper;' },
				{ value: 680, label: 'komplette Unterarmfraktur re.' }
			]"
		/>

		<FormKit
			id="thorax"
			name="thorax"
			type="select"
			label="Thorax Röntgen"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 305, label: 'Lunge noch deutlich überwässert; Pleuraergüsse bds.' },
				{ value: 306, label: 'Thorax: Normalbefund;' },
				{ value: 312, label: 'inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand' },
				{ value: 314, label: 'minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung' },
				{ value: 324, label: 'Rippenserienfraktur re. 4-7; Lunge seitengleich ventiliert' },
				{ value: 340, label: 'Pneumothorax re. ca. 2 cm' },
				{ value: 342, label: 'Rippenserienfraktur re. 3-7 ohne Pneu' },
				{ value: 347, label: 'Thorax: deutliche Überblähung der peripheren Lungenanteile, \
				vereinzelt kleinere Bullä; keine Frakturen, gleiche Belüftung' },
				{ value: 361, label: 'Thorax: großes Herz, geringgradige Stauung der Lunge, Belüftung seitengleich' },
				{ value: 375, label: 'sgl Belüftung; beginnende Infiltrate bds. Basal, kleine Ergüsse' },
				{ value: 376, label: 'inhomogene Verschattungen, bds zentrale Infiltrate' },
				{ value: 377, label: 'Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen' },
				{ value: 381, label: 'Rippenserienfraktur re. 4-7; Mantelpneu re. ca 3 cm; wenig Blut \
				im unteren Resessus re.; beginnendes Hautemphysem re. lateral; Lunge seitengleich ventiliert' },
				{ value: 382, label: 'Thorax: Lobärpneumonie links; deutliche Überblähung der peripheren \
				Lungenanteile, vereinzelt kleinere Bullä; seitengleiche Belüftung' },
				{ value: 401, label: 'Rippenserienfraktur re. 4-7; Mantelpneu re. ca 1,5 cm; wenig Blut \
				im unteren Resessus re.; Lunge seitengleich ventiliert' },
				{ value: 414, label: 'leichte Stauungszeichen hilär' },
				{ value: 435, label: 'Sternumfraktur im mittleren Drittel' },
				{ value: 445, label: 'Thorax: seitengleiche Belüftung; keine Ergüsse; kein Pneu; Rippenserienfraktur rechts lateral 3-6;' },
				{ value: 446, label: 'Pleuraergüsse bds, Lunge inhomogen verschattet, Belüftung seitengleich, Thoraxskelet oB;' },
				{ value: 457, label: 'linke Lunge deutlich überbläht, Mediastinum dezent nach links \
				verschoben; mehrere große Bullae; basal bds Infiltrate, Herz grenzwertig groß wie bei Rechtsbelastung' },
				{ value: 471, label: 'seitengleiche Belüftung; keine Ergüsse; kein Pneu; nicht dislozierte, sternumnahe Fraktur 4.Rippe li.;' },
				{ value: 479, label: 'Schrittmacheraggregat links subclavikulär, Kabel an loco tipico, \
				Lunge dezent parahilär gestaut, keine Ergüsse;' },
				{ value: 485, label: 'Rippenserienfraktur re. 4-7; kompletter Pneumothorax re. mit Verlagerung \
				des gesamten Mediastinums; ausgedehntes Hautemphysem; Lunge nur links ventiliert' }
			]"
		/>

		<FormKit
			id="trauma"
			name="trauma"
			type="select"
			label="Trauma CT"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 100, label: 'deutlich vergrößertes Herz, Aorta elongiert, Belüftung oB. Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 105, label: 'inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales vermutlich gekapseltes Hämatom abdominal ca 2 L' },
				{ value: 106, label: 'Thorax: Normalbefund; Spiralfraktur rechter Oberarm; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 108, label: 'leichte Stauungszeichen hilär komplette Unterarmfraktur re.' },
				{ value: 112, label: 'Rippenserienfraktur re. 4-7; Mantelpneu re. ca 3 cm; wenig Blut im unteren Resessus re.; beginnendes Hautemphysem re. lateral; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;' },
				{ value: 121, label: 'Thorax: Normalbefund; komplette Unterarmfraktur li. mit dezenter Verschiebung. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 123, label: 'inhomogene Verschattungen, bds zentrale Infiltrate. Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales gekapseltes Hämatom abdominal mind 2 L' },
				{ value: 130, label: 'seitengleiche Belüftung; keine Ergüsse; kein Pneu; nicht dislozierte, sternumnahe Fraktur 4.Rippe li.; Oberarmamputation li.; sonst keine Frakturzeichen oder Fremdkörper; HWS: oB.; Becken: oB.;' },
				{ value: 135, label: 'Rippenserienfraktur re. 4-7; Mantelpneu re. ca 1,5 cm; wenig Blut im unteren Resessus re.; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;' },
				{ value: 136, label: 'inhomogene Verschattungen, bds zentrale Infiltrate Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; kleines zentrales Hämatom abdominal ca. 300 ml' },
				{ value: 137, label: 'Rippenserienfraktur re. 4-7; kompletter Pneumothorax re. mit Verlagerung des gesamten Mediastinums; ausgedehntes Hautemphysem; Lunge nur links ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;' },
				{ value: 148, label: 'Lunge noch deutlich überwässert; Pleuraergüsse bds. Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 152, label: 'sgl Belüftung; beginnende Infiltrate bds. Basal, kleine Ergüsse Extremitäten: Normalbefund; keine Frakturzeichen; mind. 1 L Aszites; Pankreas aufgelockert, mehrere Pseudozysten' },
				{ value: 159, label: 'Thorax: Normalbefund; Oberschenkelfraktur re; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 161, label: 'minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung; Metallcerclage wie nach Sternotomie;' },
				{ value: 162, label: 'Thorax: deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; keine Frakturen, gleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 173, label: 'Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 2 l Blut im Abdomen; Leber fraglich rupturiert.' },
				{ value: 174, label: 'Thorax: großes Herz, geringgradige Stauung der Lunge, Belüftung seitengleich HüftTEP; sonst keine Auffälligkeiten' },
				{ value: 175, label: 'sgl Belüftung; beginnende Infiltrate bds. Basal Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 176, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; dezente Mittelllinienverschiebung; beginnendes Hirnödem linkshemisphärisch;' },
				{ value: 185, label: 'inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales ausgedehntes Hämatom abdominal mind 2 - 2,5 L' },
				{ value: 189, label: 'Rippenserienfraktur re. 4-7; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;' },
				{ value: 191, label: 'Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 3 l Blut im Abdomen; Leber fraglich rupturiert.' },
				{ value: 196, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; Dünndarmschlingen aufgetrieben, Darmwand im Ileumbereich deutlich verdickt, ca. 200 ml freie Flüssigkeit' },
				{ value: 205, label: 'Thorax: Normalbefund; Dislozierte Handgelenksfraktur; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 207, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1 l Blut im Abdomen; Leber fraglich rupturiert.' },
				{ value: 209, label: 'minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung Oberschenkeltrummerfraktur re.' },
				{ value: 221, label: 'Sternumfraktur im mittleren Drittel Sprunggelenksfraktur mit deutlicher Dislokation' },
				{ value: 228, label: 'Thorax: Normalbefund; nicht dislozierte Sprunggelengsfraktur; sonst Extr. OB. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: Nasenbeinfraktu; fragliche Orbitabodenfraktur re.; fragliche Fissur Occipital; keine ICB, keine Raumforderung;' },
				{ value: 236, label: 'linke Lunge deutlich überbläht, Mediastinum dezent nach links verschoben; mehrere große Bullae; basal bds Infiltrate, Herz grenzwertig groß wie bei Rechtsbelastung Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 237, label: 'Thorax: seitengleiche Belüftung; keine Ergüsse; kein Pneu; Rippenserienfraktur rechts lateral 3-6; Extremitäten: Oberschenkelfraktur bds. im mittleren Drittel;' },
				{ value: 238, label: 'Pleuraergüsse bds, Lunge inhomogen verschattet, Belüftung seitengleich, Thoraxskelet oB; Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 242, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 243, label: 'Schrittmacheraggregat links subclavikulär, Kabel an loco tipico, Lunge dezent parahilär gestaut, keine Ergüsse; Extremitäten: Normalbefund; keine Frakturzeichen;' },
				{ value: 248, label: 'Rippenserienfraktur re. 3-7 ohne Pneu Trümmerfraktur des distalen US re.; komplette proximale Unterarmfraktur re.' },
				{ value: 260, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; mehrere Fremdkörper in beiden Händen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;' },
				{ value: 269, label: 'Pneumothorax re. ca. 2 cm Oberschenkelschaftfraktur li mit Fehlstellung' },
				{ value: 273, label: 'Thorax: Lobärpneumonie links; deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; seitengleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; Pneumonische Infiltrate links und beginnend rechts, kleiner Pleuraerguss re.' },
				{ value: 274, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1,5 l Blut im Abdomen; Leber fraglich rupturiert.' },
				{ value: 281, label: 'Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; keine Mittelllinienverschiebung; kein Hirnödem;' }
			]"
		/>

		<FormKit
			id="ultraschall"
			name="ultraschall"
			type="select"
			label="Ultraschall"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 502, label: 'schlechte Untersuchungsbedingungen; mind 2-3 L freie Flüssigkeit im gesamten Abdomen' },
				{ value: 509, label: 'Leber inhomogen, keine Aszites' },
				{ value: 513, label: 'wenig freie Flüssigkeit im kleinen Becken' },
				{ value: 519, label: 'freie Flüssigkeit im kleinen Becken (ca 100 ml)' },
				{ value: 522, label: 'fraglich kleines Hämatom im mittleren Abdomenbereich' },
				{ value: 541, label: 'schlechte Untersuchungsbedingungen; Darmwand im Ileumbereich deutlich verdickt, ca. 500 ml freie Flüssigkeit im Douglas und um die Leber' },
				{ value: 559, label: 'deutlich freie Flüssigkeit im kleinen Becken (> 500 ml) und um die Leber' },
				{ value: 565, label: 'massiv freie Flüssigkeit im gesamten Abdomen (> 2000 ml)' },
				{ value: 566, label: 'Schlechte Untersuchungsbedingugen. Freie Flüssigkeit auszuschließen.' },
				{ value: 571, label: 'reichlich Aszites; Leber oB.; Pankreas aufgelockert, mehrere Pseudozysten' },
				{ value: 585, label: 'Abdomen o.B.; V.a. Pneumothorax re.' },
				{ value: 589, label: 'keine Pleuraergüsse; keine freie Flüssigkeit im Abdomen; Bauch- und Beckenorgane o.B.' },
				{ value: 591, label: 'großes Hämatom im mittleren Abdomenbereich, viel gekapselte Flüssigkeit um die Aorta' },
				{ value: 614, label: 'freie Flüssigkeit im kleinen Becken und um die Milz' },
				{ value: 615, label: 'Abdomen; Normalbefund; keine pathologischen Veränderungen; Thorax: keine Ergüsse sichtbar' },
				{ value: 621, label: 'Abdomen o.B.; Schwangerschaft mit vitalem Kind' },
				{ value: 624, label: 'schlechte Untersuchungsbedingungen; viel freie Flüssigkeit im Becken und um die Leber' },
				{ value: 626, label: 'schlechte Untersuchungsbedingungen; massive freie Flüssigkeit im gesamten Abdomen' },
				{ value: 647, label: 'Abdomen; Normalbefund; keine pathologischen Veränderungen;' },
				{ value: 658, label: 'sehr großes Hämatom im mittleren Abdomenbereich, massiv Flüssigkeit um die Aorta' },
				{ value: 665, label: 'schlechte Untersuchungsbedingungen; mind 1,5 L freie Flüssigkeit im Becken und um die Leber' },
				{ value: 686, label: 'deutlich verkleinerte Leber mit erhöhter Dichte, mind 1,5 L Aszites' }
			]"
		/>

		<FormKit
			id="ekg"
			name="ekg"
			type="select"
			label="EKG"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 701, label: 'Absolute Arrhythmie,Linksschenkelblock' },
				{ value: 702, label: 'Sinusrhythmus,ST-Streckensenkungen' },
				{ value: 703, label: 'Schrittmacherrythmus' },
				{ value: 707, label: 'AV-Block III' },
				{ value: 709, label: 'Sinusrhythmus,Rechtsschenkelblock' },
				{ value: 714, label: 'breite Kammerkomplexe' },
				{ value: 716, label: 'Asystolie' },
				{ value: 719, label: 'Kammerflimmern' },
				{ value: 721, label: 'ST-Streckenhebungen, Hinterwandinfarkt' },
				{ value: 722, label: 'Sinusrhythmus' },
				{ value: 725, label: 'Sinusrhythmus,vereinzelt Salven' },
				{ value: 726, label: 'Absolute Arrhythmie,ST-Streckensenkungen' },
				{ value: 728, label: 'Absolute Arrhythmie,Rechtsschenkelblock' },
				{ value: 730, label: 'Absolute Arrhythmie,vereinzelt Salven' },
				{ value: 737, label: 'Sinusrhythmus,vereinzelt sVES' },
				{ value: 739, label: 'Absolute Arrhythmie,vereinzelt VES' },
				{ value: 746, label: 'Sinusrhythmus,Linksschenkelblock' },
				{ value: 747, label: 'Absolute Arrhythmie' },
				{ value: 748, label: 'Sinusrhythmus,vereinzelt VES' }
			]"
		/>

		<FormKit
			id="zvd"
			name="zvd"
			type="select"
			label="ZVD"
			placeholder="Wähle ein Ergebnis"
			:options="[
				{ value: 816, label: -15 },
				{ value: 806, label: -14 },
				{ value: 825, label: -13 },
				{ value: 811, label: -12 },
				{ value: 835, label: -11 },
				{ value: 815, label: -10 },
				{ value: 817, label: -9 },
				{ value: 829, label: -8 },
				{ value: 828, label: -7 },
				{ value: 827, label: -6 },
				{ value: 802, label: -5 },
				{ value: 831, label: -4 },
				{ value: 814, label: -3 },
				{ value: 823, label: -2 },
				{ value: 838, label: -1 },
				{ value: 822, label: 0 },
				{ value: 805, label: 1 },
				{ value: 837, label: 2 },
				{ value: 810, label: 3 },
				{ value: 821, label: 4 },
				{ value: 813, label: 5 },
				{ value: 804, label: 6 },
				{ value: 836, label: 7 },
				{ value: 833, label: 8 },
				{ value: 812, label: 9 },
				{ value: 824, label: 10 },
				{ value: 820, label: 11 },
				{ value: 801, label: 12 },
				{ value: 807, label: 13 },
				{ value: 803, label: 14 },
				{ value: 832, label: 15 },
				{ value: 800, label: 16 },
				{ value: 808, label: 17 },
				{ value: 834, label: 18 },
				{ value: 809, label: 19 },
				{ value: 830, label: 20 },
				{ value: 819, label: 21 },
				{ value: 818, label: 22 },
				{ value: 826, label: 23 }
			]"
		/>
        
		<pre wrap>{{ value }}</pre>
	</FormKit>
</template><script setup>
const castRangeToNumber = (node) => {
  // We add a check to add the cast only to range inputs
  if (node.props.type !== 'range') return

  node.hook.input((value, next) => next(Number(value)))
}

const createPatient = async (fields) => {
  await new Promise((r) => setTimeout(r, 1000))
  alert(JSON.stringify(fields))
}
</script>

<template>
	<h1>Zustand</h1>
	<FormKit
		v-slot="{ value }"
		type="form"
		:plugins="[castRangeToNumber]"
		submit-label="Patient erstellen"
		@submit="createPatient"
	>
		<FormKit
			id="airway"
			name="airway"
			type="select"
			label="Atemwege"
			placeholder="Wähle den Zustand der Atemwege"
			:options="['freie Atemwege', 'künstlicher Atemweg', 'Atemwegsverlegung']"
			validation="required"
		/>

		<FormKit
			id="breathingRate"
			name="breathingRate"
			type="number"
			label="Atemfrequenz"
			placeholder="Atemzüge pro Minute"
			validation="required|min:0"
		/>

		<FormKit
			id="oxygenSaturation"
			name="oxygenSaturation"
			type="number"
			label="Sauerstoffsättigung"
			placeholder="SpO2 in %"
			validation="required|min:0"
		/>

		<FormKit
			id="breathing"
			name="breathing"
			type="select"
			label="Atmung"
			placeholder="Wähle den Zustand der Atmung"
			:options="['normale Atmung', 'vertiefte Atmung', 'flache Atmung', 'Beatmung', 'Atemstillstand']"
		/>

		<FormKit
			id="breathingSound"
			name="breathingSound"
			type="checkbox"
			label="Giemen und Brummen"
		/>

		<FormKit
			id="breathingLoudness"
			name="breathingLoudness"
			type="select"
			label="Atemgeräusche"
			placeholder="Sind Atemgeräusche hörbar?"
			:options="['normales AG hörbar', 'sehr leises AG hörbar', 'nur einseitiges AG hörbar', 'kein AG hörbar']"
		/>

		<FormKit
			id="heartRate"
			name="heartRate"
			type="number"
			label="Herzfrequenz"
			placeholder="Herzschläge pro Minute"
			validation="required|min:0"
		/>
		<pre wrap>{{ value }}</pre>
	</FormKit>
</template>