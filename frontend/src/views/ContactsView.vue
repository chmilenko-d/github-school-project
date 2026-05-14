<script setup>
import { computed, inject } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import Footer from '@/components/Footer.vue';

const { t } = inject('translations');

const { result, loading, error } = useQuery(gql`
  query {
    contactInfo {
      schoolName
      shortName
      address
      phone
      email
      directorName
      workHours
      mapEmbedUrl
      telegramUrl
      vkUrl
    }
  }
`);

const contact = computed(() => result.value?.contactInfo);
</script>

<template>
  <div class="contacts-page">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.contacts', 'Контакты') }}</h1>
    </div>

    <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
    <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

    <div v-else-if="contact" class="container">
      <div class="contacts-grid">
        <!-- Карточка контактов -->
        <div class="contact-card">
          <h2 class="card-title">{{ contact.schoolName }}</h2>

          <div v-if="contact.directorName" class="contact-row">
            <span class="contact-icon">👤</span>
            <div>
              <span class="contact-label">{{ t('contacts.director', 'Директор') }}</span>
              <span class="contact-value">{{ contact.directorName }}</span>
            </div>
          </div>

          <div v-if="contact.address" class="contact-row">
            <span class="contact-icon">📍</span>
            <div>
              <span class="contact-label">{{ t('contacts.address', 'Адрес') }}</span>
              <span class="contact-value">{{ contact.address }}</span>
            </div>
          </div>

          <div v-if="contact.phone" class="contact-row">
            <span class="contact-icon">📞</span>
            <div>
              <span class="contact-label">{{ t('contacts.phone', 'Телефон') }}</span>
              <a :href="`tel:${contact.phone}`" class="contact-value contact-link">{{ contact.phone }}</a>
            </div>
          </div>

          <div v-if="contact.email" class="contact-row">
            <span class="contact-icon">✉️</span>
            <div>
              <span class="contact-label">Email</span>
              <a :href="`mailto:${contact.email}`" class="contact-value contact-link">{{ contact.email }}</a>
            </div>
          </div>

          <div v-if="contact.workHours" class="contact-row">
            <span class="contact-icon">🕐</span>
            <div>
              <span class="contact-label">{{ t('contacts.work_hours', 'Режим работы') }}</span>
              <span class="contact-value">{{ contact.workHours }}</span>
            </div>
          </div>

          <!-- Соцсети -->
          <div v-if="contact.vkUrl || contact.telegramUrl" class="social-links">
            <a v-if="contact.vkUrl" :href="contact.vkUrl" target="_blank" rel="noopener" class="social-btn">
              ВКонтакте
            </a>
            <a v-if="contact.telegramUrl" :href="contact.telegramUrl" target="_blank" rel="noopener" class="social-btn">
              Telegram
            </a>
          </div>
        </div>

        <!-- Карта -->
        <div v-if="contact.mapEmbedUrl" class="map-card">
          <iframe
            :src="contact.mapEmbedUrl"
            width="100%"
            height="100%"
            style="border:0; min-height: 400px;"
            allowfullscreen=""
            loading="lazy"
          ></iframe>
        </div>
      </div>
    </div>

    <div v-else class="state-msg">{{ t('contacts.empty', 'Контактная информация пока не добавлена') }}</div>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.contacts-page {
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
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 var(--px-32, 32px) var(--px-48, 48px);
}

.state-msg {
  text-align: center;
  padding: var(--px-48, 48px);
  color: var(--color-text-muted);
}
.state-error { color: #dc2626; }

.contacts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--px-24, 24px);
  align-items: start;
}

.contact-card {
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 16px;
  padding: var(--px-32, 32px);
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 var(--px-24, 24px);
}

.contact-row {
  display: flex;
  gap: var(--px-12, 12px);
  align-items: flex-start;
  padding: var(--px-12, 12px) 0;
  border-bottom: 1px solid var(--color-border);
}

.contact-row:last-of-type { border-bottom: none; }

.contact-icon {
  font-size: 1.3rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.contact-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 2px;
}

.contact-value {
  display: block;
  font-size: 0.95rem;
  color: var(--color-text);
}

.contact-link {
  color: var(--color-primary);
  text-decoration: none;
}
.contact-link:hover { text-decoration: underline; }

.social-links {
  display: flex;
  gap: var(--px-12, 12px);
  margin-top: var(--px-20, 20px);
  padding-top: var(--px-16, 16px);
  border-top: 1px solid var(--color-border);
}

.social-btn {
  padding: var(--px-8, 8px) var(--px-20, 20px);
  border-radius: 999px;
  background: var(--color-primary);
  color: #fff;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: background 0.2s;
}
.social-btn:hover { background: var(--color-primary-hover); }

.map-card {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--color-card-border);
  min-height: 400px;
}

@media (max-width: 860px) {
  .contacts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
