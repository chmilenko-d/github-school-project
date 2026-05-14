<script setup>
import SectionList from "../components/SectionList.vue";
import PostList from "../components/PostList.vue";
import Button from "../components/Button.vue";
import Footer from '../components/Footer.vue';

import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { computed, inject } from 'vue'
import { MEDIA_BASE_URL } from "@/settings.js";

const { t } = inject('translations')

// Секции для главной
const { result: sectionsResult, loading: sectionsLoading } = useQuery(gql`
  query {
    allSections {
      title
      slug
      image
      subtitle
      author {
        user { username firstName lastName }
      }
    }
  }
`);

// Контактная информация (название, hero-фото)
const { result: contactResult } = useQuery(gql`
  query {
    contactInfo {
      schoolName
      shortName
      heroImage
      logo
    }
  }
`);

// Активные объявления
const { result: announcementsResult } = useQuery(gql`
  query {
    activeAnnouncements {
      title
      body
      priority
      startDate
      endDate
    }
  }
`);

// Последние описания (быстрые ссылки)
const { result: descriptionsResult } = useQuery(gql`
  query {
    allDescriptions {
      title
      slug
      image
      smallDescription
    }
  }
`);

const schoolName = computed(() =>
  contactResult.value?.contactInfo?.schoolName || t('service.school_name', 'Школьный сайт')
);
const heroImage = computed(() => {
  const img = contactResult.value?.contactInfo?.heroImage;
  return img ? `${MEDIA_BASE_URL}${img}` : null;
});

const announcements = computed(() => announcementsResult.value?.activeAnnouncements || []);
const descriptions = computed(() => descriptionsResult.value?.allDescriptions || []);

const priorityClass = (p) => {
  if (p === 'URGENT') return 'announcement-urgent';
  if (p === 'IMPORTANT') return 'announcement-important';
  return 'announcement-normal';
};
const priorityLabel = (p) => {
  if (p === 'URGENT') return '🔴 Срочное';
  if (p === 'IMPORTANT') return '🟡 Важное';
  return '';
};
</script>

<template>
  <div v-if="sectionsLoading" class="loading-state">{{ t('service.loading') }}</div>
  <div v-else class="home-container">
    <!-- HERO -->
    <div class="hero-section" :style="heroImage ? { backgroundImage: `url(${heroImage})` } : {}">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="hero-title">{{ schoolName }}</h1>
        <p class="hero-subtitle">{{ t('service.subtitle1', 'Добро пожаловать на наш сайт!') }}</p>
        <div class="button-group">
          <Button variant="primary" size="normal" :to="{ name: 'news' }">
            {{ t('button.news', 'Новости') }}
          </Button>
          <Button variant="outline" size="normal" :to="{ name: 'sections' }">
            {{ t('button.sections', 'Разделы') }}
          </Button>
        </div>
      </div>
    </div>

    <!-- ОБЪЯВЛЕНИЯ -->
    <section v-if="announcements.length" class="announcements-section">
      <div class="container">
        <h2 class="section-title">{{ t('home.announcements', 'Объявления') }}</h2>
        <div class="announcements-list">
          <div
            v-for="(ann, i) in announcements"
            :key="i"
            class="announcement-card"
            :class="priorityClass(ann.priority)"
          >
            <div class="announcement-header">
              <span v-if="priorityLabel(ann.priority)" class="announcement-badge">
                {{ priorityLabel(ann.priority) }}
              </span>
              <h3 class="announcement-title">{{ ann.title }}</h3>
            </div>
            <div class="announcement-body" v-html="ann.body"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ПОСЛЕДНИЕ НОВОСТИ -->
    <section class="news-section">
      <div class="container">
        <h2 class="section-title">{{ t('home.latest_news', 'Последние новости') }}</h2>
        <PostList />
        <div class="section-footer">
          <Button variant="outline" size="normal" :to="{ name: 'news' }">
            {{ t('button.all_news', 'Все новости') }} →
          </Button>
        </div>
      </div>
    </section>

    <!-- РАЗДЕЛЫ -->
    <section v-if="sectionsResult?.allSections?.length" class="sections-on-home">
      <div class="container">
        <h2 class="section-title">{{ t('home.sections', 'Разделы') }}</h2>
        <SectionList :sections="sectionsResult.allSections" />
      </div>
    </section>

    <!-- БЫСТРЫЕ ССЫЛКИ (описания) -->
    <section v-if="descriptions.length" class="quick-links-section">
      <div class="container">
        <h2 class="section-title">{{ t('home.quick_links', 'Полезные ссылки') }}</h2>
        <div class="quick-links-grid">
          <router-link
            v-for="desc in descriptions"
            :key="desc.slug"
            :to="{ name: 'description', params: { slug: desc.slug } }"
            class="quick-link-card"
          >
            <img
              v-if="desc.image"
              :src="`${MEDIA_BASE_URL}${desc.image}`"
              :alt="desc.title"
              class="quick-link-image"
            />
            <div class="quick-link-info">
              <h3>{{ desc.title }}</h3>
              <p v-if="desc.smallDescription">{{ desc.smallDescription }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.loading-state {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: var(--px-60);
}

.home-container {
  width: 100%;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--px-32, 32px);
}

/* ── Hero ── */
.hero-section {
  width: 100%;
  min-height: 65vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-hero-bg, #0f172a), #1e3a5f);
  background-size: cover;
  background-position: center;
  position: relative;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.55);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--px-32, 32px);
}

.hero-title {
  font-size: clamp(2rem, 5vw, 3.2rem);
  color: #fff;
  margin-bottom: var(--px-16, 16px);
  font-weight: 700;
}

.hero-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.35rem);
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: var(--px-32, 32px);
  font-weight: 400;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: var(--px-16, 16px);
}

/* ── Секции страницы ── */
.section-title {
  font-size: clamp(1.5rem, 3.5vw, 2rem);
  font-weight: 700;
  color: var(--color-heading);
  text-align: center;
  margin-bottom: var(--px-32, 32px);
}

.section-footer {
  display: flex;
  justify-content: center;
  margin-top: var(--px-32, 32px);
}

/* ── Объявления ── */
.announcements-section {
  padding: var(--px-48, 48px) 0;
  background: var(--color-background);
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: var(--px-16, 16px);
}

.announcement-card {
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 12px;
  padding: var(--px-24, 24px);
  border-left: 4px solid var(--color-primary);
}

.announcement-urgent {
  border-left-color: #dc2626;
  background: #fef2f2;
}

.announcement-important {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.announcement-header {
  display: flex;
  align-items: center;
  gap: var(--px-12, 12px);
  margin-bottom: var(--px-8, 8px);
}

.announcement-badge {
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.announcement-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0;
}

.announcement-body {
  font-size: 0.95rem;
  color: var(--color-text);
  line-height: 1.6;
}

/* ── Новости ── */
.news-section {
  padding: var(--px-48, 48px) 0;
  background: var(--color-background-soft);
}

/* ── Секции ── */
.sections-on-home {
  padding: var(--px-48, 48px) 0;
  background: var(--color-background);
}

/* ── Быстрые ссылки ── */
.quick-links-section {
  padding: var(--px-48, 48px) 0;
  background: var(--color-background-soft);
}

.quick-links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--px-20, 20px);
}

.quick-link-card {
  display: flex;
  flex-direction: column;
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: var(--color-text);
  transition: transform 0.3s, box-shadow 0.3s;
}

.quick-link-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.quick-link-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.quick-link-info {
  padding: var(--px-16, 16px);

  h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-heading);
    margin-bottom: var(--px-8, 8px);
  }

  p {
    font-size: 0.9rem;
    color: var(--color-text-muted);
    line-height: 1.5;
    margin: 0;
  }
}

/* ── Mobile ── */
@media (max-width: 860px) {
  .hero-section {
    min-height: 50vh;
  }
  .button-group {
    flex-direction: column;
    gap: var(--px-12, 12px);
    width: 100%;
    max-width: 320px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 var(--px-16, 16px);
  }
  .quick-links-grid {
    grid-template-columns: 1fr;
  }
}
</style>