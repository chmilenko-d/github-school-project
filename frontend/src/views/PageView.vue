<script setup>
import { useRoute } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { computed, inject } from 'vue';

const { t } = inject('translations');
const route = useRoute();
const slug = route.params.slug;

const { result, loading, error } = useQuery(
  gql`
    query GetPage($slug: String!) {
      staticPageBySlug(slug: $slug) {
        title
        body
        metaDescription
        dateModified
      }
    }
  `,
  { slug }
);

const page = computed(() => result.value?.staticPageBySlug);
</script>

<template>
  <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
  <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

  <div v-else-if="page" class="page-view">
    <div class="page-shell">
      <header class="page-header">
        <h1 class="page-title">{{ page.title }}</h1>
      </header>
      <article class="page-body prose" v-html="page.body"></article>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.state-msg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: var(--px-60);
  color: var(--color-text-muted);
}
.state-error { color: #dc2626; }

.page-view {
  min-height: 100vh;
  background: var(--color-background);
  padding: 0 0 var(--px-80);
}

.page-shell {
  max-width: 860px;
  margin: 0 auto;
  padding: var(--px-120, 120px) var(--px-32, 32px) var(--px-40, 40px);
}

.page-header {
  margin-bottom: var(--px-32, 32px);
}

.page-title {
  font-size: clamp(1.6rem, 4vw, 2.5rem);
  font-weight: 700;
  color: var(--color-heading);
}

.page-body {
  font-size: var(--font-size-normal);
  line-height: 1.7;
  color: var(--color-text);

  :deep(h2), :deep(h3) {
    margin-top: var(--px-32, 32px);
    margin-bottom: var(--px-12, 12px);
    font-weight: 600;
    color: var(--color-heading);
  }

  :deep(p) {
    margin: 0 0 var(--px-16, 16px);
  }

  :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }

  :deep(a) {
    color: var(--color-primary);
    text-decoration: none;
  }
  :deep(a:hover) { text-decoration: underline; }

  :deep(ul), :deep(ol) {
    padding-left: var(--px-24, 24px);
    margin: 0 0 var(--px-16, 16px);
  }

  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: var(--px-16, 16px) 0;
  }

  :deep(th), :deep(td) {
    border: 1px solid var(--color-border);
    padding: var(--px-8, 8px) var(--px-12, 12px);
    text-align: left;
  }

  :deep(th) {
    background: var(--color-background-soft);
    font-weight: 600;
  }
}

@media (max-width: 640px) {
  .page-shell {
    padding-top: var(--px-96, 96px);
    padding-left: var(--px-20, 20px);
    padding-right: var(--px-20, 20px);
  }
}
</style>
