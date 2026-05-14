<script setup>
import { ref, computed, inject } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { MEDIA_BASE_URL } from '@/settings.js';
import Footer from '@/components/Footer.vue';

const { t } = inject('translations');

const { result: catResult } = useQuery(gql`
  query { allDocumentCategories { name slug } }
`);

const { result: docResult, loading, error } = useQuery(gql`
  query {
    allDocuments {
      title
      description
      file
      category { name slug }
    }
  }
`);

const activeCategory = ref(null);

const categories = computed(() => catResult.value?.allDocumentCategories || []);
const documents = computed(() => {
  const all = docResult.value?.allDocuments || [];
  if (!activeCategory.value) return all;
  return all.filter(d => d.category?.slug === activeCategory.value);
});

const fileIcon = (file) => {
  if (!file) return '📄';
  const ext = file.split('.').pop().toLowerCase();
  if (ext === 'pdf') return '📕';
  if (['doc', 'docx'].includes(ext)) return '📘';
  if (['xls', 'xlsx'].includes(ext)) return '📗';
  return '📄';
};
</script>

<template>
  <div class="documents-page">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.documents', 'Документы') }}</h1>
    </div>

    <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
    <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

    <div v-else class="container">
      <!-- Табы категорий -->
      <div v-if="categories.length" class="category-tabs">
        <button
          class="category-tab"
          :class="{ active: !activeCategory }"
          @click="activeCategory = null"
        >
          {{ t('documents.all', 'Все') }}
        </button>
        <button
          v-for="cat in categories"
          :key="cat.slug"
          class="category-tab"
          :class="{ active: activeCategory === cat.slug }"
          @click="activeCategory = cat.slug"
        >
          {{ cat.name }}
        </button>
      </div>

      <!-- Список документов -->
      <div v-if="documents.length" class="documents-list">
        <a
          v-for="doc in documents"
          :key="doc.title"
          :href="doc.file ? `${MEDIA_BASE_URL}${doc.file}` : '#'"
          target="_blank"
          rel="noopener"
          class="document-card"
        >
          <span class="doc-icon">{{ fileIcon(doc.file) }}</span>
          <div class="doc-info">
            <h3 class="doc-title">{{ doc.title }}</h3>
            <p v-if="doc.description" class="doc-desc">{{ doc.description }}</p>
            <span v-if="doc.category" class="doc-category">{{ doc.category.name }}</span>
          </div>
          <span class="doc-download">⬇</span>
        </a>
      </div>
      <p v-else class="state-msg">{{ t('documents.empty', 'Документов пока нет') }}</p>
    </div>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.documents-page {
  padding-top: var(--px-60);
  min-height: 100vh;
  background: var(--color-background);
}

.page-header {
  padding: var(--px-48, 48px) var(--px-32, 32px) var(--px-24, 24px);
  text-align: center;
}

.page-title {
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  font-weight: 700;
  color: var(--color-heading);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 var(--px-32, 32px) var(--px-48, 48px);
}

.state-msg {
  text-align: center;
  padding: var(--px-48, 48px);
  color: var(--color-text-muted);
}
.state-error { color: #dc2626; }

/* Табы */
.category-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: var(--px-8, 8px);
  margin-bottom: var(--px-32, 32px);
  justify-content: center;
}

.category-tab {
  padding: var(--px-8, 8px) var(--px-20, 20px);
  border-radius: 999px;
  border: 1px solid var(--color-border);
  background: var(--color-card-bg);
  color: var(--color-text);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.category-tab.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

/* Список */
.documents-list {
  display: flex;
  flex-direction: column;
  gap: var(--px-12, 12px);
}

.document-card {
  display: flex;
  align-items: center;
  gap: var(--px-16, 16px);
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 12px;
  padding: var(--px-16, 16px) var(--px-20, 20px);
  text-decoration: none;
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.document-card:hover {
  border-color: var(--color-primary-light);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.doc-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.doc-info {
  flex: 1;
  min-width: 0;
}

.doc-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 var(--px-4, 4px);
}

.doc-desc {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin: 0 0 var(--px-4, 4px);
  line-height: 1.4;
}

.doc-category {
  font-size: 0.75rem;
  color: var(--color-primary);
  font-weight: 500;
}

.doc-download {
  font-size: 1.3rem;
  color: var(--color-primary);
  flex-shrink: 0;
  opacity: 0.6;
  transition: opacity 0.2s;
}
.document-card:hover .doc-download { opacity: 1; }

@media (max-width: 640px) {
  .document-card {
    flex-wrap: wrap;
  }
  .doc-download { display: none; }
}
</style>
