<template>
	<div class="node" :class="{ selected: data.selected }" :style="nodeStyles()" data-testid="node">
		<!-- Inputs-->
		<div v-for="[key, input] in inputs()" :key="'input' + key + seed" class="input" :data-testid="'input-' + key">
			<Ref
				class="input-socket"
				:emit="emit"
				:data="{ type: 'socket', side: 'input', key: key, nodeId: data.id, payload: input.socket }"
				data-testid="input-socket"
			/>
			<div v-show="!input.control || !input.showControl" class="input-title" data-testid="input-title">
				{{ input.label }}
			</div>
			<Ref
				v-show="input.control && input.showControl"
				class="input-control"
				:emit="emit"
				:data="{ type: 'control', payload: input.control }"
				data-testid="input-control"
			/>
		</div>
		<div class="title" data-testid="title">
			{{ data.label }}
		</div>
		<!-- Outputs-->
		<div v-for="[key, output] in outputs()" :key="'output' + key + seed" class="output" :data-testid="'output-' + key">
			<div class="output-title" data-testid="output-title">
				{{ output.label }}
			</div>
			<Ref
				class="output-socket"
				:emit="emit"
				:data="{ type: 'socket', side: 'output', key: key, nodeId: data.id, payload: output.socket }"
				data-testid="output-socket"
			/>
		</div>
	</div>
</template>


<script lang="js">
import { defineComponent } from 'vue'
import { Ref } from 'rete-vue-plugin'


function sortByIndex(entries) {
  entries.sort((a, b) => {
    const ai = a[1] && a[1].index || 0
    const bi = b[1] && b[1].index || 0

    return ai - bi
  })
  return entries
}

export default defineComponent({
  components: {
    Ref
  },
  props: ['data', 'emit', 'seed'],
  methods: {
    nodeStyles() {
      return {
        width: Number.isFinite(this.data.width) ? `${this.data.width}px` : '',
        height: Number.isFinite(this.data.height) ? `${this.data.height}px` : ''
      }
    },
    inputs() {
      return sortByIndex(Object.entries(this.data.inputs))
    },
    controls() {
      return sortByIndex(Object.entries(this.data.controls))
    },
    outputs() {
      return sortByIndex(Object.entries(this.data.outputs))
    }
  }
})
</script>

<style lang="scss" scoped>
@use "sass:math";
@import "./vars";

.node {
    background: $node-color;
    border: 2px solid #4e58bf;
  border-radius: 100%;
  cursor: pointer;
  box-sizing: border-box;
  width: $node-width;
  height: auto;
  padding-bottom: 6px;
  position: relative;
  user-select: none;
  line-height: initial;
  font-family: Arial;

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;


  &:hover {
    background: lighten($node-color, 4%);
  }

  &.selected {
    background: $node-color-selected;
    border-color: #e3c000;
  }

  .title {
    color: white;
    font-family: sans-serif;
    font-size: 18px;
    padding: 8px;
    text-align: center;
  }

  .input {
    text-align: left;
    position: absolute;
    left: 0;
  }

  .output {
    text-align: right;
    position: absolute;
    right: 0;
  }

  .output-socket {
    text-align: right;
    margin-right: -(math.div($socket-size, 2) + $socket-margin);
    display: inline-block;
  }

  .input-socket {
    text-align: left;
    margin-left: -(math.div($socket-size, 2) + $socket-margin);
    display: inline-block;
  }

  .input-title,
  .output-title {
    vertical-align: middle;
    color: white;
    display: inline-block;
    font-family: sans-serif;
    font-size: 14px;
    margin: $socket-margin;
    line-height: $socket-size;
  }

  .input-control {
    z-index: 1;
    width: calc(100% - #{$socket-size + 2*$socket-margin});
    vertical-align: middle;
    display: inline-block;
  }

  .control {
    padding: $socket-margin math.div($socket-size, 2) + $socket-margin;
  }
}
</style>
