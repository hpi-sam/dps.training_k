<script setup lang="ts">
    import { ref } from 'vue'
    import { svg }  from '@/assets/Svg'
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
        // body
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
        // leg
        { name: 'right thigh', x: 420, y: 920},
        { name: 'right knee', x: 420, y: 1040},
        { name: 'right leg', x: 420, y: 1040},
        { name: 'right lower leg', x: 420, y: 1130},
        { name: 'right foot', x: 420, y: 1240},
    ]

const svgRef = ref<SVGElement | null>(null)

export function addInjury(injuryType: string, position: string) {
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
    switch (injuryType) {
        case 'blood':
            addWave(x, y)
            break
        case 'fracture':
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

</script>

<template>
	<svg
		ref="svgRef"
		width="150px"
		height="100%"
		viewBox="0 0 644 1280"
	>
		<g transform="translate(0,1280) scale(0.1,-0.1)" fill="black">
			<path :d="svg.patientHead" />
			<path :d="svg.patientBody" />
		</g>
	</svg>
</template>

<style scoped>
    svg {
        display: inline-block;
        width: 25%;
    }
</style>