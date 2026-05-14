<!-- DescriptionList.vue -->
<script setup>
import AuthorLink from "./AuthorLink.vue";
import Button from "@/components/Button.vue";
import { gql } from "@apollo/client/core";
import { useQuery } from "@vue/apollo-composable";
import { MEDIA_BASE_URL } from "@/settings.js";
import { inject } from 'vue'
import { RouterLink } from 'vue-router'

const { t } = inject('translations')

const { result, loading, error } = useQuery(gql`
  query GetAllDescriptions {
    allDescriptions {
      title
      subtitle
      body
      slug
      image
      backgroundImage
      publishDate
      smallDescription
      metaDescription
      customCssClass
      author {
        user {
          username
          firstName
          lastName
        }
      }
      tags {
        name
      }
    }
  }
`);
</script>

<template>
  <div v-if="loading">{{ t('service.loading') }}</div>
  <div v-else-if="error" class="warn"> {{ error.message }}</div>
  <div v-else class="description-list-container">
    <RouterLink
      v-for="description in result.allDescriptions"
      :key="description.slug"
      :to="{ name: 'description', params: { slug: description.slug } }"
      class="description-article"
      :class="description.customCssClass"
    >
      <div
        v-if="description.backgroundImage"
        :style="{ backgroundImage: `url(${MEDIA_BASE_URL}${description.backgroundImage})` }"
        class="description-background"
      />
      <div class="description-media" v-if="description.image">
        <img :src="`${MEDIA_BASE_URL}${description.image}`" :alt="description.title" class="description-image"/>
      </div>
      <div class="description-block">
        <div class="title-container">
          <div class="title-text">
            {{ description.title }}
          </div>
        </div>
        <div class="body-container">
          <div v-html="description.smallDescription" class="body-text" />
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style lang="scss" scoped>
.description-list-container {
  width: 100%;
  display: grid;
  gap: var(--px-30) var(--px-30);
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  align-items: stretch;
  margin: 0 auto;
  padding: var(--px-10) 0;
}

/* Card */
.description-article {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  text-decoration: none;
  background: var(--color-card-bg, #ffffff);
  border: 1px solid var(--color-card-border, #e2e8f0);
  border-radius: var(--px-16);
  box-shadow: 0 1px 3px var(--color-card-shadow, rgba(0,0,0,0.06));
  width: 100%;
  min-height: 340px;
  color: var(--color-text);
  transition: transform .4s cubic-bezier(.22,.9,.3,1),
              box-shadow .4s,
              border-color .3s;
}

.description-article::before {
  display: none;
}

.description-article::after {
  display: none;
}

.description-article:hover {
  transform: translateY(-4px);
  border-color: var(--color-primary-light, #dbeafe);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.description-article:hover::before { opacity: 0; }
.description-article:hover::after { opacity: 0; }

.description-background {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  opacity: .12;
  transition: transform 1.1s ease;
}

.description-article:hover .description-background {
  transform: scale(1.05);
}

.description-media {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  z-index: 1;
  background: var(--color-background-soft);
}

.description-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  mix-blend-mode: normal;
  transition: transform 1.1s ease;
}

.description-article:hover .description-image {
  transform: scale(1.06);
}

.description-block {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  gap: var(--px-14);
  padding: var(--px-20) var(--px-20) var(--px-24);
  flex: 1;
}

.title-container { padding: 0; }

.body-container { padding: 0; }

.title-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 600;
  font-size: var(--font-size-header);
  letter-spacing: .5px;
  text-transform: none;
  margin: 0;
  line-height: 1.25;
  color: var(--color-heading);
}

.body-text {
  font-size: var(--font-size-normal);
  font-weight: 400;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--color-text);
  margin: 0;
}

@media (max-width: 640px) {
  .description-list-container {
    display: flex;
    flex-direction: column;
    gap: var(--px-20);
  }
  .description-article {
    min-height: 280px;
  }
  .description-block {
    padding: var(--px-18) var(--px-18) var(--px-22);
  }
  .title-text {
    font-size: 0.95rem;
  }
  .body-text {
    -webkit-line-clamp: 5;
    font-size: calc(var(--font-size-small) * 0.9);
  }
}
</style>