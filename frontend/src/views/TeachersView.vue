<script setup>
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue';
import { MEDIA_BASE_URL } from "@/settings.js";
import Footer from '@/components/Footer.vue';

const { t } = inject('translations');

const { result, loading, error } = useQuery(gql`
  query {
    allTeachers {
      fullName
      slug
      position
      subject
      photo
    }
  }
`);
</script>

<template>
  <div class="teachers-page">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.teachers', 'Педагогический состав') }}</h1>
    </div>

    <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
    <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

    <div v-else class="container">
      <div class="teachers-grid">
        <router-link
          v-for="teacher in result.allTeachers"
          :key="teacher.slug"
          :to="{ name: 'teacher', params: { slug: teacher.slug } }"
          class="teacher-card"
        >
          <div class="teacher-photo-wrap">
            <img
              v-if="teacher.photo"
              :src="`${MEDIA_BASE_URL}${teacher.photo}`"
              :alt="teacher.fullName"
              class="teacher-photo"
            />
            <div v-else class="teacher-photo-placeholder">
              <span>{{ teacher.fullName?.charAt(0) }}</span>
            </div>
          </div>
          <div class="teacher-info">
            <h3 class="teacher-name">{{ teacher.fullName }}</h3>
            <p v-if="teacher.position" class="teacher-position">{{ teacher.position }}</p>
            <p v-if="teacher.subject" class="teacher-subject">{{ teacher.subject }}</p>
          </div>
        </router-link>
      </div>
    </div>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.teachers-page {
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--px-32, 32px) var(--px-48, 48px);
}

.state-msg {
  text-align: center;
  padding: var(--px-48, 48px);
  color: var(--color-text-muted);
}
.state-error { color: #dc2626; }

.teachers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--px-24, 24px);
}

.teacher-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 16px;
  padding: var(--px-24, 24px) var(--px-20, 20px);
  text-decoration: none;
  color: var(--color-text);
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}

.teacher-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: var(--color-primary-light);
}

.teacher-photo-wrap {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: var(--px-16, 16px);
  background: var(--color-background-soft);
  flex-shrink: 0;
}

.teacher-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.teacher-photo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 2.5rem;
  font-weight: 700;
}

.teacher-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 var(--px-4, 4px);
}

.teacher-position {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  margin: 0 0 var(--px-4, 4px);
}

.teacher-subject {
  font-size: 0.85rem;
  color: var(--color-primary);
  font-weight: 500;
  margin: 0;
}

@media (max-width: 640px) {
  .teachers-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: var(--px-16, 16px);
  }
  .teacher-photo-wrap {
    width: 100px;
    height: 100px;
  }
}
</style>
