<script setup>
import { inject } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { MEDIA_BASE_URL } from '@/settings.js';
import Footer from '@/components/Footer.vue';

const { t } = inject('translations');

const { result, loading, error } = useQuery(gql`
  query {
    allGalleryAlbums {
      title
      slug
      description
      coverImage
      date
    }
  }
`);

const formatDate = (d) => {
  if (!d) return '';
  try {
    return new Intl.DateTimeFormat('ru', { dateStyle: 'long' }).format(new Date(d));
  } catch { return d; }
};
</script>

<template>
  <div class="gallery-page">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.gallery', 'Фотогалерея') }}</h1>
    </div>

    <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
    <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

    <div v-else class="container">
      <div v-if="result.allGalleryAlbums?.length" class="albums-grid">
        <router-link
          v-for="album in result.allGalleryAlbums"
          :key="album.slug"
          :to="{ name: 'album', params: { slug: album.slug } }"
          class="album-card"
        >
          <div class="album-cover">
            <img
              v-if="album.coverImage"
              :src="`${MEDIA_BASE_URL}${album.coverImage}`"
              :alt="album.title"
              class="album-img"
            />
            <div v-else class="album-placeholder">📷</div>
          </div>
          <div class="album-info">
            <h3 class="album-title">{{ album.title }}</h3>
            <p v-if="album.date" class="album-date">{{ formatDate(album.date) }}</p>
            <p v-if="album.description" class="album-desc">{{ album.description }}</p>
          </div>
        </router-link>
      </div>
      <p v-else class="state-msg">{{ t('gallery.empty', 'Альбомов пока нет') }}</p>
    </div>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.gallery-page {
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

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--px-24, 24px);
}

.album-card {
  display: flex;
  flex-direction: column;
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  color: var(--color-text);
  transition: transform 0.3s, box-shadow 0.3s;
}

.album-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.album-cover {
  width: 100%;
  aspect-ratio: 16/10;
  overflow: hidden;
  background: var(--color-background-soft);
}

.album-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.album-card:hover .album-img {
  transform: scale(1.05);
}

.album-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  background: var(--color-background-mute);
}

.album-info {
  padding: var(--px-16, 16px) var(--px-20, 20px);
}

.album-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--color-heading);
  margin: 0 0 var(--px-4, 4px);
}

.album-date {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin: 0 0 var(--px-8, 8px);
}

.album-desc {
  font-size: 0.85rem;
  color: var(--color-text);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 640px) {
  .albums-grid {
    grid-template-columns: 1fr;
  }
}
</style>
