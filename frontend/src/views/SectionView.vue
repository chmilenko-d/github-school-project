<script setup>
import { ref, inject, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'
import { MEDIA_BASE_URL } from '@/settings.js'
import Button from '@/components/Button.vue'

const { t } = inject('translations') || { t: (k,d)=>d||k }

function getCurrentLang() {
  return (
    localStorage.getItem('lang') ||
    document.cookie.match(/django_language=([^;]+)/)?.[1] ||
    'ru'
  )
}

const currentLang = ref(getCurrentLang())

function onLangChanged() {
  currentLang.value = getCurrentLang()
}

onMounted(() => window.addEventListener('language-changed', onLangChanged))
onBeforeUnmount(() => window.removeEventListener('language-changed', onLangChanged))

const formatDate = (d) => {
  if (!d) return ''
  try {
    return new Intl.DateTimeFormat(currentLang.value, { dateStyle: 'long' }).format(new Date(d))
  } catch {
    return d
  }
}

const route = useRoute()
const slug = route.params.slug

const { result, loading, error } = useQuery(
  gql`
    query GetSectionBySlug($slug: String!) {
      sectionBySlug(slug: $slug) {
        title
        subtitle
        publishDate
        published
        metaDescription
        slug
        image
        backgroundImage
        body
        author {
          user {
            username
            firstName
            lastName
          }
        }
        tags { name }
      }
    }
  `,
  { slug }
)

const section = computed(() => result.value?.sectionBySlug)

const router = useRouter()
const goBack = () => {
  if (window.history.length > 1) router.back()
  else router.push({ name: 'home' }).catch(()=>{})
}
</script>

<template>
  <div v-if="loading" class="state-loading">{{ t('service.loading') }}</div>
  <div v-else-if="error" class="state-error">{{ error.message }}</div>

  <div v-else-if="section" class="section-view">
    <div
      v-if="section.backgroundImage"
      class="section-bg"
      :style="{ backgroundImage: `url(${MEDIA_BASE_URL}${section.backgroundImage})` }"
      aria-hidden="true"
    ></div>
    <div class="section-bg-overlay" aria-hidden="true"></div>

    <div class="section-shell">
      <header class="section-header">
        <Button size="small" variant="outline" class="back-btn" @click="goBack">
          {{ t('button.back_to_home', 'Назад') }}
        </Button>
        <h1 class="section-title">{{ section.title }}</h1>
        <h2 v-if="section.subtitle" class="section-subtitle">
          {{ section.subtitle }}
        </h2>
        <div class="meta-row">
          <span v-if="section.publishDate" class="meta-date">
            {{ t('service.published_on', 'Опубликовано') }}: {{ formatDate(section.publishDate) }}
          </span>
          <span v-if="section.tags?.length" class="meta-tags">
            <span v-for="tag in section.tags" :key="tag.name" class="tag">{{ tag.name }}</span>
          </span>
        </div>
      </header>

      <figure v-if="section.image" class="section-figure">
        <img
          :src="`${MEDIA_BASE_URL}${section.image}`"
            :alt="section.title"
          class="section-image"
          loading="lazy"
        />
      </figure>

      <article class="section-body prose" v-html="section.body"></article>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.section-view {
  position: relative;
  width: 100%;
  min-height: 100dvh;
  padding: 0 0 var(--px-80);
  display: flex;
  flex-direction: column;
  color: var(--color-text);
  background: var(--color-background);
}

.section-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 360px;
  background-size: cover;
  background-position: center;
  z-index: 0;
  filter: brightness(.85) contrast(1.05);
}

.section-bg-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 360px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), var(--color-background));
  pointer-events: none;
  z-index: 1;
}

.section-shell {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: var(--px-140) var(--px-40) var(--px-40);
  display: flex;
  flex-direction: column;
  gap: var(--px-40);
}

.section-header {
  display: flex;
  flex-direction: column;
  gap: var(--px-20);
}

.back-btn {
  align-self: flex-start;
}

.section-title {
  margin: 0;
  font-size: clamp(1.9rem, 4.2vw, 3rem);
  line-height: 1.15;
  font-weight: 700;
  letter-spacing: .6px;
  color: var(--color-heading);
}

.section-subtitle {
  margin: 0;
  font-size: clamp(1.05rem, 2.2vw, 1.4rem);
  font-weight: 400;
  color: var(--color-text-muted);
  line-height: 1.35;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--px-12) var(--px-20);
  font-size: var(--font-size-small);
  letter-spacing: .5px;
  text-transform: uppercase;
  color: var(--color-text-light, #94a3b8);
}

.meta-date { white-space: nowrap; }

.meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--px-8);
}

.tag {
  background: var(--color-primary-light, #dbeafe);
  color: var(--color-primary);
  padding: var(--px-4) var(--px-10);
  border-radius: var(--px-20);
  font-size: calc(var(--font-size-small) - 1px);
  letter-spacing: .5px;
  transition: background .25s;
}
.tag:hover {
  background: var(--color-primary);
  color: #ffffff;
}

.section-figure {
  margin: 0;
  border-radius: var(--px-20);
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.section-image {
  width: 100%;
  height: 100%;
  max-height: 540px;
  object-fit: cover;
  display: block;
  transition: transform 1.1s ease;
}

.section-figure:hover .section-image {
  transform: scale(1.04);
}

.section-body {
  font-size: var(--font-size-normal);
  line-height: 1.65;
  display: flex;
  flex-direction: column;
  gap: var(--px-20);
  color: var(--color-text);
}

.section-body :deep(h2),
.section-body :deep(h3) {
  margin-top: var(--px-32);
  margin-bottom: var(--px-12);
  line-height: 1.25;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .5px;
}

.section-body :deep(p) {
  margin: 0 0 var(--px-18);
}

.section-body :deep(a) {
  color: var(--color-primary);
  position: relative;
  text-decoration: none;
}
.section-body :deep(a)::after {
  content: "";
  position: absolute;
  left: 0; bottom: -2px;
  width: 100%; height: 1px;
  background: currentColor;
  opacity: .35;
  transition: opacity .25s;
}
.section-body :deep(a:hover)::after {
  opacity: .9;
}

.state-loading,
.state-error {
  padding: var(--px-80) var(--px-24);
  text-align: center;
  font-size: var(--font-size-normal);
  opacity: .85;
}
.state-error { color: #dc2626; }

/* Mobile */
@media (max-width: 760px) {
  .section-shell {
    padding: var(--px-110) var(--px-20) var(--px-40);
    gap: var(--px-32);
  }
  .section-title {
    font-size: clamp(1.6rem, 7vw, 2.3rem);
  }
  .section-subtitle {
    font-size: clamp(.95rem, 4vw, 1.15rem);
  }
  .section-image {
    max-height: 340px;
  }
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--px-10);
  }
  .back-btn {
    position: relative;
    top: 0;
  }
}

@media (max-width: 480px) {
  .section-shell {
    padding-top: var(--px-96);
  }
  .section-body {
    font-size: calc(var(--font-size-normal) * .95);
    line-height: 1.55;
  }
}
</style>