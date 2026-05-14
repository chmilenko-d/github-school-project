<script setup>
import { ref, provide } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'

const translations = ref({})
const loading = ref(true)

const { onResult } = useQuery(gql`
  query GetAllTranslationKeys {
    allTranslationKeys {
      key
      value
    }
  }
`)

onResult(result => {
  const data = result.data?.allTranslationKeys || []
  translations.value = Object.fromEntries(
    data.map(item => [item.key, item.value])
  )
  loading.value = false
})

const t = (key, fallback = key) => {
  return translations.value[key] || fallback
}

provide('translations', { translations, loading, t })
</script>

<template>
  <div v-if="loading" class="translations-loading">
    Loading translations...
  </div>
  <slot v-else />
</template>

<style scoped>
.translations-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: var(--font-size-normal);
  color: #666;
}
</style>