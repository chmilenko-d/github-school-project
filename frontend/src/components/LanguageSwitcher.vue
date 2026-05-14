<!-- LanguageSwitcher.vue -->
<template>
  <div class="lang-switcher">
    <button
      @click="setLang('en')"
      :class="{ active: currentLang === 'en' }"
      class="lang-btn"
      aria-label="Switch to English"
    >
      EN
    </button>
    <button
      @click="setLang('ru')"
      :class="{ active: currentLang === 'ru' }"
      class="lang-btn"
      aria-label="Переключиться на русский"
    >
      RU
    </button>
  </div>
</template>

<script>
import {apolloClient} from "@/apollo.js";

export default {
  data() {
    return {
      currentLang: 'ru'
    }
  },
  mounted() {
    this.currentLang = localStorage.getItem('lang') || this.getCookie('django_language') || 'ru'
  },
  methods: {
    async setLang(lang) {
      this.currentLang = lang

      localStorage.setItem('lang', lang)
      this.setCookie('django_language', lang, 365)
      this.setCookie('csrftoken', this.getCookie('csrftoken'), 365)  // важно для CSRF

      await fetch('/api/myapp/set-language/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCookie('csrftoken')
        },
        body: JSON.stringify({ language: lang })
      })
      window.dispatchEvent(new CustomEvent('language-changed', { detail: { lang } }));
      apolloClient.reFetchObservableQueries(true)

    },

    setCookie(name, value, days) {
      const d = new Date()
      d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000)
      document.cookie = `${name}=${value};path=/;expires=${d.toUTCString()}`
    },

    getCookie(name) {
      const value = `; ${document.cookie}`
      const parts = value.split(`; ${name}=`)
      if (parts.length === 2) return parts.pop().split(';').shift()
    }
  }
}
</script>

<style lang="scss" scoped>
.lang-switcher {
  display: flex;
  gap: var(--px-6);
  background: var(--color-background-soft);
  padding: var(--px-4);
  border-radius: var(--px-12);
  border: var(--px-1) solid var(--color-border);
}

.lang-btn {
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  font-size: var(--font-size-small);
  font-weight: 500;
  padding: var(--px-6) var(--px-10);
  border-radius: var(--px-8);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.lang-btn.active {
  background: var(--color-primary);
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 var(--px-2) var(--px-8) rgba(37, 99, 235, 0.25);
}

.lang-btn:hover:not(.active) {
  background: var(--color-background-mute);
  color: var(--color-heading);
}
</style>