<script setup>
import { ref, computed, inject, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { MEDIA_BASE_URL } from '@/settings.js';
import Button from '@/components/Button.vue';

const { t } = inject('translations');
const route = useRoute();
const router = useRouter();
const slug = route.params.slug;

const { result, loading, error } = useQuery(
  gql`
    query GetAlbum($slug: String!) {
      galleryAlbumBySlug(slug: $slug) {
        title
        description
        date
        photos {
          id
          image
          caption
        }
      }
    }
  `,
  { slug }
);

const album = computed(() => result.value?.galleryAlbumBySlug);
const photos = computed(() => album.value?.photos || []);

// Lightbox
const lightboxIndex = ref(null);
const lightboxOpen = computed(() => lightboxIndex.value !== null);
const lightboxPhoto = computed(() =>
  lightboxOpen.value ? photos.value[lightboxIndex.value] : null
);

const openLightbox = (i) => { lightboxIndex.value = i; };
const closeLightbox = () => { lightboxIndex.value = null; };
const prevPhoto = () => {
  if (lightboxIndex.value > 0) lightboxIndex.value--;
  else lightboxIndex.value = photos.value.length - 1;
};
const nextPhoto = () => {
  if (lightboxIndex.value < photos.value.length - 1) lightboxIndex.value++;
  else lightboxIndex.value = 0;
};

const onKeydown = (e) => {
  if (!lightboxOpen.value) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') prevPhoto();
  if (e.key === 'ArrowRight') nextPhoto();
};
onMounted(() => window.addEventListener('keydown', onKeydown));
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown));

const goBack = () => {
  if (window.history.length > 1) router.back();
  else router.push({ name: 'gallery' });
};

const formatDate = (d) => {
  if (!d) return '';
  try {
    return new Intl.DateTimeFormat('ru', { dateStyle: 'long' }).format(new Date(d));
  } catch { return d; }
};
</script>

<template>
  <div v-if="loading" class="state-msg">{{ t('service.loading') }}</div>
  <div v-else-if="error" class="state-msg state-error">{{ error.message }}</div>

  <div v-else-if="album" class="album-page">
    <div class="album-shell">
      <Button size="small" variant="outline" class="back-btn" @click="goBack">
        ← {{ t('button.back', 'Назад') }}
      </Button>

      <header class="album-header">
        <h1 class="album-title">{{ album.title }}</h1>
        <p v-if="album.date" class="album-date">{{ formatDate(album.date) }}</p>
        <p v-if="album.description" class="album-desc">{{ album.description }}</p>
      </header>

      <div v-if="photos.length" class="photos-grid">
        <div
          v-for="(photo, i) in photos"
          :key="photo.id"
          class="photo-item"
          @click="openLightbox(i)"
        >
          <img
            :src="`${MEDIA_BASE_URL}${photo.image}`"
            :alt="photo.caption || album.title"
            class="photo-thumb"
            loading="lazy"
          />
          <p v-if="photo.caption" class="photo-caption">{{ photo.caption }}</p>
        </div>
      </div>
      <p v-else class="state-msg">{{ t('gallery.no_photos', 'Фотографий пока нет') }}</p>
    </div>

    <!-- LIGHTBOX -->
    <Teleport to="body">
      <div v-if="lightboxOpen" class="lightbox-overlay" @click.self="closeLightbox">
        <button class="lb-close" @click="closeLightbox" aria-label="Close">✕</button>
        <button class="lb-prev" @click="prevPhoto" aria-label="Previous">‹</button>
        <button class="lb-next" @click="nextPhoto" aria-label="Next">›</button>

        <div class="lb-content">
          <img
            :src="`${MEDIA_BASE_URL}${lightboxPhoto.image}`"
            :alt="lightboxPhoto.caption || ''"
            class="lb-image"
          />
          <p v-if="lightboxPhoto.caption" class="lb-caption">{{ lightboxPhoto.caption }}</p>
          <p class="lb-counter">{{ lightboxIndex + 1 }} / {{ photos.length }}</p>
        </div>
      </div>
    </Teleport>
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

.album-page {
  min-height: 100vh;
  background: var(--color-background);
  padding: 0 0 var(--px-80);
}

.album-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--px-120, 120px) var(--px-32, 32px) var(--px-40, 40px);
}

.back-btn { margin-bottom: var(--px-24, 24px); }

.album-header {
  margin-bottom: var(--px-32, 32px);
}

.album-title {
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  font-weight: 700;
  color: var(--color-heading);
  margin: 0 0 var(--px-8, 8px);
}

.album-date {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0 0 var(--px-8, 8px);
}

.album-desc {
  color: var(--color-text);
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.5;
}

/* Grid */
.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--px-12, 12px);
}

.photo-item {
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  background: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  transition: transform 0.3s, box-shadow 0.3s;
}

.photo-item:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.photo-thumb {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
}

.photo-caption {
  padding: var(--px-8, 8px) var(--px-12, 12px);
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin: 0;
  text-align: center;
}

/* Lightbox */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.92);
  display: flex;
  align-items: center;
  justify-content: center;
}

.lb-close,
.lb-prev,
.lb-next {
  position: absolute;
  background: none;
  border: none;
  color: #fff;
  font-size: 2rem;
  cursor: pointer;
  z-index: 10;
  padding: 12px;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.lb-close:hover, .lb-prev:hover, .lb-next:hover { opacity: 1; }

.lb-close { top: 16px; right: 16px; font-size: 1.5rem; }
.lb-prev { left: 16px; top: 50%; transform: translateY(-50%); font-size: 3rem; }
.lb-next { right: 16px; top: 50%; transform: translateY(-50%); font-size: 3rem; }

.lb-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 90vw;
  max-height: 90vh;
}

.lb-image {
  max-width: 90vw;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 4px;
}

.lb-caption {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  margin-top: 12px;
  text-align: center;
}

.lb-counter {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.8rem;
  margin-top: 6px;
}

@media (max-width: 640px) {
  .album-shell {
    padding-top: var(--px-96, 96px);
  }
  .photos-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: var(--px-8, 8px);
  }
}
</style>
