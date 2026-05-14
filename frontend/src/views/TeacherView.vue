<script setup>
import { useRoute, useRouter } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { computed, inject } from 'vue';
import { MEDIA_BASE_URL } from '@/settings.js';
import Button from '@/components/Button.vue';

const { t } = inject('translations');
const route = useRoute();
const router = useRouter();
const slug = route.params.slug;

const { result, loading, error } = useQuery(
  gql`
    query GetTeacher($slug: String!) {
      teacherBySlug(slug: $slug) {
        fullName
        position
        subject
        education
        qualification
        experienceYears
        bio
        photo
        email
      }
    }
  `,
  { slug }
);

const teacher = computed(() => result.value?.teacherBySlug);

const goBack = () => {
  if (window.history.length > 1) router.back();
  else router.push({ name: 'teachers' });
};
</script>

<template>
  <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
  <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

  <div v-else-if="teacher" class="teacher-detail">
    <div class="teacher-shell">
      <Button size="small" variant="outline" class="back-btn" @click="goBack">
        ← {{ t('button.back', 'Назад') }}
      </Button>

      <div class="teacher-top">
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
        <div class="teacher-heading">
          <h1 class="teacher-name">{{ teacher.fullName }}</h1>
          <p v-if="teacher.position" class="teacher-position">{{ teacher.position }}</p>
        </div>
      </div>

      <div class="teacher-details">
        <div v-if="teacher.subject" class="detail-row">
          <span class="detail-label">{{ t('teacher.subject', 'Предмет') }}</span>
          <span class="detail-value">{{ teacher.subject }}</span>
        </div>
        <div v-if="teacher.education" class="detail-row">
          <span class="detail-label">{{ t('teacher.education', 'Образование') }}</span>
          <span class="detail-value">{{ teacher.education }}</span>
        </div>
        <div v-if="teacher.qualification" class="detail-row">
          <span class="detail-label">{{ t('teacher.qualification', 'Квалификация') }}</span>
          <span class="detail-value">{{ teacher.qualification }}</span>
        </div>
        <div v-if="teacher.experienceYears" class="detail-row">
          <span class="detail-label">{{ t('teacher.experience', 'Стаж') }}</span>
          <span class="detail-value">{{ teacher.experienceYears }} {{ t('teacher.years', 'лет') }}</span>
        </div>
        <div v-if="teacher.email" class="detail-row">
          <span class="detail-label">Email</span>
          <a :href="`mailto:${teacher.email}`" class="detail-value detail-link">{{ teacher.email }}</a>
        </div>
      </div>

      <article v-if="teacher.bio" class="teacher-bio prose" v-html="teacher.bio"></article>
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

.teacher-detail {
  min-height: 100vh;
  padding: 0 0 var(--px-80);
  background: var(--color-background);
}

.teacher-shell {
  max-width: 860px;
  margin: 0 auto;
  padding: var(--px-120, 120px) var(--px-32, 32px) var(--px-40, 40px);
  display: flex;
  flex-direction: column;
  gap: var(--px-32, 32px);
}

.back-btn {
  align-self: flex-start;
}

.teacher-top {
  display: flex;
  align-items: center;
  gap: var(--px-24, 24px);
}

.teacher-photo-wrap {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-background-soft);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
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
  font-size: 3.5rem;
  font-weight: 700;
}

.teacher-name {
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 var(--px-4, 4px);
}

.teacher-position {
  font-size: 1.05rem;
  color: var(--color-text-muted);
  margin: 0;
}

.teacher-details {
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 12px;
  padding: var(--px-24, 24px);
  display: flex;
  flex-direction: column;
  gap: var(--px-12, 12px);
}

.detail-row {
  display: flex;
  gap: var(--px-12, 12px);
  align-items: baseline;
  padding-bottom: var(--px-8, 8px);
  border-bottom: 1px solid var(--color-border);
}

.detail-row:last-child { border-bottom: none; padding-bottom: 0; }

.detail-label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  min-width: 140px;
  flex-shrink: 0;
}

.detail-value {
  font-size: 0.95rem;
  color: var(--color-text);
}

.detail-link {
  color: var(--color-primary);
  text-decoration: none;
}
.detail-link:hover { text-decoration: underline; }

.teacher-bio {
  font-size: var(--font-size-normal);
  line-height: 1.65;
  color: var(--color-text);

  :deep(p) { margin: 0 0 var(--px-16, 16px); }
  :deep(a) { color: var(--color-primary); }
}

@media (max-width: 640px) {
  .teacher-shell {
    padding-top: var(--px-96, 96px);
  }
  .teacher-top {
    flex-direction: column;
    text-align: center;
  }
  .teacher-photo-wrap {
    width: 120px;
    height: 120px;
  }
  .detail-row {
    flex-direction: column;
    gap: var(--px-4, 4px);
  }
  .detail-label {
    min-width: auto;
  }
}
</style>
