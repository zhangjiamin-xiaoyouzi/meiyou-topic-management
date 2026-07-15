<template>
  <div class="modal-root" @click.self="$emit('close')">
    <div :class="['modal-panel', sizeClass]">
      <div class="modal-head">
        <div>
          <div class="modal-title">{{ title }}</div>
          <div v-if="description" class="modal-description">{{ description }}</div>
        </div>
        <button class="close-button" type="button" @click="$emit('close')">✕</button>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'default'
  }
})

defineEmits(['close'])

const sizeClass = computed(() => {
  if (props.size === 'narrow') {
    return 'modal-panel-narrow'
  }
  if (props.size === 'wide') {
    return 'modal-panel-wide'
  }
  return ''
})
</script>

<style scoped>
.modal-root {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(16, 20, 32, 0.42);
  backdrop-filter: blur(4px);
}

.modal-panel {
  width: min(760px, calc(100vw - 32px));
  max-height: calc(100vh - 40px);
  overflow: auto;
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 24px 80px rgba(25, 29, 43, 0.22);
  padding: 22px;
}

.modal-panel-narrow {
  width: min(420px, calc(100vw - 32px));
}

.modal-panel-wide {
  width: min(880px, calc(100vw - 32px));
}

.modal-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 22px;
  font-weight: 600;
  color: #1f2430;
}

.modal-description {
  margin-top: 6px;
  color: #83889a;
  font-size: 13px;
  line-height: 1.5;
}

.close-button {
  width: 28px;
  height: 28px;
  border: 1px solid transparent;
  border-radius: 12px;
  color: #8d93a6;
  background: none;
  cursor: pointer;
}

.close-button:hover {
  border-color: #e8e8ef;
  background: #f7f8fb;
  color: #1f2430;
}
</style>