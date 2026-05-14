<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: String,
  size: {
    type: Number,
    default: 24,
  },
});

const iconPath = computed(() => {
  return `/images/icons/${props.name}.svg`;
});
</script>


<template>
  <img :src="iconPath" :alt="`${props.name} icon`" :style="{ width: `var(--px-${props.size})`, height: `var(--px-${props.size})` }" class="icon" />
</template>

<style scoped>
.icon {
  display: inline-block;
}
</style>