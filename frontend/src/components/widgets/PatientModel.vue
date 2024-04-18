<script setup lang="ts">
    import { ref } from 'vue'
</script>
<script lang="ts">
const positions = [
        // head
        { name: 'head', x: 322, y: 50 },
        { name: 'right head', x: 370, y: 70 },
        { name: 'right eye', x: 360, y: 130 },
        { name: 'nose', x: 322, y: 170 },
        { name: 'neck', x: 322, y: 320 },
        // arm
        { name: 'right collarbone', x: 400, y: 320 },
        { name: 'right shoulder', x: 450, y: 350 },
        { name: 'right upper arm', x: 470, y: 430 },
        { name: 'right arm', x: 500, y: 500 },
        { name: 'right elbow', x: 500, y: 500 },
        { name: 'right forearm', x: 540, y: 580 },
        { name: 'right hand', x: 590, y: 680 },
        // body thorax rip flank pelvis, lower abdomen 
        { name: 'thorax', x: 322, y: 420 },
        { name: 'right thorax', x: 390, y: 420 },
        { name: 'rips', x: 390, y: 580 },
        { name: 'right rip', x: 390, y: 580 },
        { name: 'right flank', x: 440, y: 580 },
        { name: 'abdomen', x: 322, y: 680 },
        { name: 'pelvis', x: 420, y: 720 },
        { name: 'right pelvis', x: 420, y: 720 },
        { name: 'lower abdomen', x: 322, y: 740 },
        { name: 'after', x: 322, y: 810 },
    ]

const svgRef = ref<SVGElement | null>(null)

export function addInjury(position: string, injury: string) {
    let x = 0
    let y = 0
    let rightPosition = ''
    if (position.startsWith('left')) {
        rightPosition = position.replace('left', 'right');
        ({ x, y } = positions.find(p => p.name === rightPosition) || { x: 0, y: 0 })
        x = 322 - (x - 322)
    } else {
        ({ x, y } = positions.find(p => p.name === position) || { x: 0, y: 0 })
    }
    switch (injury) {
        case 'wave':
            addWave(x, y)
            break
        case 'hash':
            addHash(x, y)
            break
    }
}

export function addWave(x: number, y: number) {
    const scale = 0.3
    const waveWidth = (180 - 10) * scale
    const waveHeight = (180 - 10) * scale
    const wave = document.createElementNS('http://www.w3.org/2000/svg', 'path')
    wave.setAttribute('d', `M${(10*scale)+x-waveWidth/2} ${y}
    Q ${(52.5*scale)+x-waveWidth/2} ${(10*scale)+y-waveHeight/2}, ${(95*scale)+x-waveWidth/2} ${y}
    T ${(180*scale)+x-waveWidth/2} ${y}`)
    wave.setAttribute('stroke', 'red')
    wave.setAttribute('stroke-width', '10')
    wave.setAttribute('fill', 'transparent')
    svgRef.value?.appendChild(wave)
}

export function addHash(x: number, y: number) {
  const scale = 0.4
  const hashWidth = (90 - 10) * scale
  const hashHeight = (100 - 0) * scale

  const lines = [
    { x1: 10, y1: 20, x2: 90, y2: 20 },
    { x1: 10, y1: 80, x2: 90, y2: 80 },
    { x1: 30, y1: 0, x2: 30, y2: 100 },
    { x1: 70, y1: 0, x2: 70, y2: 100 },
  ]

  lines.forEach(({ x1, y1, x2, y2 }) => {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    line.setAttribute('x1', ((x1 * scale) + x - hashWidth / 2).toString())
    line.setAttribute('y1', ((y1 * scale) + y - hashHeight / 2).toString())
    line.setAttribute('x2', ((x2 * scale) + x - hashWidth / 2).toString())
    line.setAttribute('y2', ((y2 * scale) + y - hashHeight / 2).toString())
    line.setAttribute('stroke', 'lightgray')
    line.setAttribute('stroke-width', (scale * 20).toString())
    svgRef.value?.appendChild(line)
  })
}

const injury = ref('')
const position = ref('')

</script>

<template>
	<svg
		ref="svgRef"
		width="150px"
		height="100%"
		viewBox="0 0 644 1280"
	>
		<g
			transform="translate(0,1280) scale(0.1,-0.1)"
			fill="black"
		>
			<!--Head-->
			<path
				d="M3080 12790 c-327 -46 -587 -175 -815 -404 -217 -218 -344 -468 -392
      -771 -19 -122 -13 -381 12 -495 91 -413 359 -762 732 -953 211 -108 390 -151
      633 -151 173 0 285 17 434 65 485 158 855 587 941 1093 22 130 22 332 0 461
      -96 568 -528 1016 -1093 1135 -111 24 -350 34 -452 20z"
			/>
			<!--Body-->
			<path
				d="

      M
      2047 9855
      
      c
      -137 -38 -239 -123 -328 -275
      -96 -164 -1692 -3429 -1708 -3492
      -60 -249 108 -497 406 -597
      45 -15 88 -21 152 -21
      152 0 257 44 352 148
      49 53 89 130 398 763
      190 387 348 708 353 713
      4 6 8 -1470 8 -3280
      0 -2783 3 -3299 14 -3355
      43 -203 214 -381 421 -440
      32 -9 100 -14 190 -14
      121 0 150 3 213 24
      142 46 269 152 336 280
      71 136 66 -22 66 2098
      
      l
      0 1913
      330 0
      330 0
      0 -1908
      
      c
      0 -2101 -4 -1955 62 -2092
      22 -46 55 -89 112 -145
      128 -127 249 -175 446 -175
      184 0 315 48 432 158
      77 73 120 136 157 230
      
      l
      26 67
      5 3330
      5 3330
      121 -245
      
      c
      66 -135 208 -423 314 -640
      106 -217 206 -414 221 -437
      103 -150 317 -226 504 -178
      80 21 198 77 262 126
      143 108 222 320 180 484
      -9 35 -206 448 -469 985
      -250 509 -623 1269 -829 1690
      -374 765 -374 765 -439 830
      -68 68 -127 103 -213 126
      -75 20 -2358 19 -2430 -1
      
      z
      "
			/>
		</g>
	</svg>
	<form @submit.prevent="addInjury(position, injury)">
		<select v-model="position">
			<option v-for="(item, index) in positions" :key="index" :value="item.name">
				{{ item.name }}
			</option>
		</select>
		<select v-model="injury">
			<option value="wave">
				Wave
			</option>
			<option value="hash">
				Hash
			</option>
		</select>
		<button type="submit">
			Add Injury
		</button>
		<button @click="addInjury('left hand', 'wave')">
			Add Left Hand Injury
		</button>
	</form>
</template>

<style scoped>
    svg {
        display: inline-block;
        width: 25%;
    }
</style>