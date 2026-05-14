<script setup>
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue';

const { t } = inject('translations');

const { result: contactResult } = useQuery(gql`
  query {
    contactInfo {
      schoolName
      address
      phone
      email
      workHours
      vkUrl
      telegramUrl
      mapEmbedUrl
    }
  }
`);
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-links">
        <div class="footer-column">
          <h3>{{ t('footer.about', 'О школе') }}</h3>
          <router-link to="/news">{{ t('button.news', 'Новости') }}</router-link>
          <router-link to="/teachers">{{ t('nav.teachers', 'Учителя') }}</router-link>
          <router-link to="/documents">{{ t('nav.documents', 'Документы') }}</router-link>
          <router-link to="/gallery">{{ t('nav.gallery', 'Галерея') }}</router-link>
        </div>

        <div v-if="contactResult?.contactInfo" class="footer-column">
          <h3>{{ t('footer.contacts', 'Контакты') }}</h3>
          <span v-if="contactResult.contactInfo.address" class="footer-info">
            📍 {{ contactResult.contactInfo.address }}
          </span>
          <a v-if="contactResult.contactInfo.phone" :href="`tel:${contactResult.contactInfo.phone}`" class="footer-info">
            📞 {{ contactResult.contactInfo.phone }}
          </a>
          <a v-if="contactResult.contactInfo.email" :href="`mailto:${contactResult.contactInfo.email}`" class="footer-info">
            ✉️ {{ contactResult.contactInfo.email }}
          </a>
          <span v-if="contactResult.contactInfo.workHours" class="footer-info">
            🕐 {{ contactResult.contactInfo.workHours }}
          </span>
        </div>

        <div v-if="contactResult?.contactInfo" class="footer-column">
          <h3>{{ t('footer.social', 'Мы в соцсетях') }}</h3>
          <a v-if="contactResult.contactInfo.vkUrl" :href="contactResult.contactInfo.vkUrl" target="_blank" rel="noopener">
            ВКонтакте
          </a>
          <a v-if="contactResult.contactInfo.telegramUrl" :href="contactResult.contactInfo.telegramUrl" target="_blank" rel="noopener">
            Telegram
          </a>
        </div>
      </div>

      <!-- Карта -->
      <div v-if="contactResult?.contactInfo?.mapEmbedUrl" class="footer-map">
        <iframe
          :src="contactResult.contactInfo.mapEmbedUrl"
          width="100%"
          height="250"
          style="border:0; border-radius: 8px;"
          allowfullscreen=""
          loading="lazy"
        ></iframe>
      </div>

      <div class="footer-text">
        <p>&copy; {{ new Date().getFullYear() }} {{ contactResult?.contactInfo?.schoolName || t('service.school_name', 'Школьный сайт') }}</p>
      </div>
    </div>
  </footer>
</template>

<style lang="scss" scoped>
.footer {
  background-color: var(--color-footer-bg, #0f172a);
  color: var(--color-footer-text, #cbd5e1);
  padding: var(--px-48, 48px) 0 var(--px-32, 32px);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--px-32, 32px);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--px-32, 32px);
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: var(--px-48, 48px);
  flex-wrap: wrap;
  width: 100%;
}

.footer-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--px-8, 8px);
  min-width: 200px;
}

.footer-column h3 {
  font-size: var(--font-size-normal);
  margin-bottom: var(--px-8, 8px);
  color: #ffffff;
  font-weight: 600;
}

.footer-column a,
.footer-info {
  color: var(--color-footer-text, #cbd5e1);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  gap: var(--px-8, 8px);
  line-height: 1.6;
}

.footer-column a:hover {
  color: #ffffff;
}

.footer-map {
  width: 100%;
  max-width: 600px;
  border-radius: 8px;
  overflow: hidden;
}

.footer-text {
  font-size: 0.85rem;
  opacity: 0.6;
  margin-top: var(--px-12, 12px);
}

@media (max-width: 640px) {
  .footer-links {
    flex-direction: column;
    gap: var(--px-32, 32px);
    align-items: center;
  }
  .footer-column {
    align-items: center;
    text-align: center;
  }
}
</style>