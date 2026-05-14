<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps({
  to: {
    type: [String, Object],
    default: null
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'small',
    validator: (value) => ['small', 'normal', 'big'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const isRouterLink = props.to && typeof props.to === 'object'
const isLink = props.to && typeof props.to === 'string'
const resolvedComponent = isRouterLink
  ? RouterLink
  : (isLink ? 'a' : 'button')

function onClick(e) {
  if (props.disabled || props.loading) {
    e && e.preventDefault()
    return
  }
  emit('click', e)
}
</script>

<template>
  <component
    :is="resolvedComponent"
    :to="isRouterLink ? to : undefined"
    :href="isLink ? to : undefined"
    :disabled="disabled || loading"
    :class="[
      'btn',
      `btn--${variant}`,
      {
        'btn--disabled': disabled || loading,
        'btn--loading': loading
      },
      `btn--${size}`
    ]"
    :aria-busy="loading"
    @click="onClick"
  >
    <span v-if="loading" class="btn__spinner"></span>
    <span v-else-if="icon" class="btn__icon">{{ icon }}</span>
    <slot />
  </component>
</template>

<style lang="scss" scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--px-4);
  padding: var(--px-4) var(--px-8);
  border: none;
  border-radius: var(--px-4);
  font-family: 'Montserrat', sans-serif;
  font-size: var(--font-size-small);
  font-weight: 300;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  min-height: var(--px-12);
  text-transform: uppercase;
}

.btn--small {
  font-size: var(--font-size-small);
  padding: var(--px-4) var(--px-8);
}

.btn--normal {
  font-size: var(--font-size-normal);
  padding: var(--px-6) var(--px-12);
}

.btn--big {
  font-size: var(--font-size-big);
  padding: var(--px-8) var(--px-16);
}

.btn--primary {
  background: var(--color-primary);
  color: #ffffff;
}

.btn--primary:hover:not(.btn--disabled) {
  background: var(--color-primary-hover);
}

.btn--secondary {
  background: #64748b;
  color: white;
}

.btn--secondary:hover:not(.btn--disabled) {
  background: #475569;
}

.btn--outline {
  background: transparent;
  color: var(--color-primary);
  border: var(--px-1) solid var(--color-primary);
}

.btn--outline:hover:not(.btn--disabled) {
  background: var(--color-primary-light, #dbeafe);
  color: var(--color-primary-hover);
}

.btn--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--loading {
  pointer-events: none;
}

.btn__spinner {
  display: inline-block;
  width: var(--px-12);
  height: var(--px-12);
  border: var(--px-1) solid rgba(37, 99, 235, 0.3);
  border-top: var(--px-1) solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.btn__icon {
  font-size: 1.2em;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>