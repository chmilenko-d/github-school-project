<script setup>
import { RouterLink, useRoute } from "vue-router";
import LanguageSwitcher from "@/components/LanguageSwitcher.vue";
import { inject, ref, watch } from 'vue';
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { MEDIA_BASE_URL } from "@/settings.js";

const { t } = inject('translations');
const route = useRoute();

const isActive = (path) => {
  if (path === '/') return route.path === '/';
  const normalizedPath = path.replace(/s$/, "");
  return route.path.startsWith(normalizedPath);
};

// Загрузка контактов школы
const { result: contactResult } = useQuery(gql`
  query {
    contactInfo {
      schoolName
      shortName
      logo
    }
  }
`);

// Мобильное состояние
const open = ref(false);

// Закрывать меню при смене маршрута
watch(() => route.fullPath, () => { open.value = false; });
</script>

<template>
  <nav class="header-menu" :class="{ 'is-open': open }">
    <!-- Логотип и название школы -->
    <RouterLink to="/" class="school-brand">
      <img
        v-if="contactResult?.contactInfo?.logo"
        :src="`${MEDIA_BASE_URL}${contactResult.contactInfo.logo}`"
        alt="Логотип"
        class="school-logo"
      />
      <span class="school-name">
        {{ contactResult?.contactInfo?.shortName || contactResult?.contactInfo?.schoolName || t('service.school_name', 'Школа') }}
      </span>
    </RouterLink>

    <button
      class="menu-toggle"
      type="button"
      aria-label="Menu"
      :aria-expanded="open"
      @click="open = !open"
    >
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </button>

    <div class="header-menu-content" :class="{ 'show': open }">
      <RouterLink :class="{ active: isActive('/') }" to="/">{{ t('button.home', 'Главная') }}</RouterLink>
      <RouterLink :class="{ active: isActive('/news') }" to="/news">{{ t('button.news', 'Новости') }}</RouterLink>
      <RouterLink :class="{ active: isActive('/teachers') }" to="/teachers">{{ t('nav.teachers', 'Учителя') }}</RouterLink>
      <RouterLink :class="{ active: isActive('/documents') }" to="/documents">{{ t('nav.documents', 'Документы') }}</RouterLink>
      <RouterLink :class="{ active: isActive('/gallery') }" to="/gallery">{{ t('nav.gallery', 'Галерея') }}</RouterLink>
      <RouterLink :class="{ active: isActive('/contacts') }" to="/contacts">{{ t('nav.contacts', 'Контакты') }}</RouterLink>

      <div class="lang-switcher-wrapper">
        <LanguageSwitcher />
      </div>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
.header-menu {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 var(--px-20);
}

/* Логотип + название школы */
.school-brand {
  position: absolute;
  left: var(--px-20);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: var(--px-10);
  text-decoration: none;
  color: var(--color-heading);
  z-index: 10;
}

.school-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
  border-radius: 4px;
}

.school-name {
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}

/* Бургер */
.menu-toggle {
  display: none;
  position: relative;
  width: var(--px-44);
  height: var(--px-44);
  background: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: var(--px-10);
  cursor: pointer;
  padding: 0;
  gap: var(--px-4);
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: background .25s, border-color .25s;
  z-index: 30;
}
.menu-toggle:hover {
  background: var(--color-border);
  border-color: var(--color-border-hover);
}
.menu-toggle .bar {
  width: 60%;
  height: 2px;
  background: var(--color-heading);
  border-radius: 2px;
  transition: transform .35s, opacity .35s;
}
.header-menu.is-open .menu-toggle .bar:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}
.header-menu.is-open .menu-toggle .bar:nth-child(2) {
  opacity: 0;
}
.header-menu.is-open .menu-toggle .bar:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}

/* Десктоп */
.header-menu-content {
  display: flex;
  justify-content: center;
  gap: var(--px-20);
  align-items: center;
  transition: opacity .3s ease;
}

.header-menu-content a {
  font-weight: 500;
  font-size: var(--font-size-normal);
  color: var(--color-text);
  padding: 0 var(--px-6);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: border-color 0.2s ease, background-color .25s, color .2s;
  line-height: 1;
  height: var(--px-40);
  display: flex;
  align-items: center;
  border-radius: var(--px-6);
}

.header-menu-content a.active {
  border-bottom: 2px solid var(--color-primary);
  color: var(--color-primary);
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.header-menu-content a:hover {
  background-color: var(--color-primary-light, #dbeafe);
  color: var(--color-primary);
}

.lang-switcher-wrapper {
  position: absolute;
  right: var(--px-20);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
}

/* Мобильное поведение */
@media (max-width: 860px) {
  .menu-toggle {
    display: inline-flex;
    margin-left: var(--px-4);
  }

  .header-menu {
    justify-content: flex-start;
    width: 100%;
  }

  .header-menu-content {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    flex-direction: column;
    align-items: stretch;
    gap: var(--px-8);
    padding: var(--px-20) var(--px-20) var(--px-28);
    background: var(--color-background-white, #ffffff);
    border: 1px solid var(--color-border);
    border-radius: var(--px-16);
    box-shadow: 0 14px 42px -18px rgba(0,0,0,0.15);
    opacity: 0;
    pointer-events: none;
    transform: translateY(var(--px-10));
  }

  .header-menu-content.show {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
    transition: opacity .35s, transform .4s;
    z-index: 20;
  }

  .header-menu-content a {
    width: 100%;
    justify-content: flex-start;
    padding: var(--px-10) var(--px-12);
    border-bottom: 2px solid transparent;
    background: var(--color-background-soft);
    color: var(--color-text);
  }
  .header-menu-content a + a {
    margin-top: var(--px-4);
  }
  .header-menu-content a.active {
    background: var(--color-primary-light);
    border-bottom: 2px solid var(--color-primary);
    color: var(--color-primary);
  }

  .lang-switcher-wrapper {
    position: relative;
    right: auto;
    top: auto;
    transform: none;
    width: 100%;
    margin-top: var(--px-12);
    justify-content: flex-start;
    padding-top: var(--px-8);
    border-top: 1px solid var(--color-border);
  }
}

/* Очень маленькие экраны */
@media (max-width: 420px) {
  .header-menu-content {
    padding: var(--px-16) var(--px-16) var(--px-24);
  }
  .header-menu-content a {
    font-size: calc(var(--font-size-normal) * .95);
  }
}
</style>