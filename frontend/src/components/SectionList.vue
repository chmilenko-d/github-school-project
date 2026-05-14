<!-- SectionList.vue -->
<script setup>
import AuthorLink from "./AuthorLink.vue";
import Button from "@/components/Button.vue";
import { gql } from "@apollo/client/core";
import {useQuery} from "@vue/apollo-composable";
import {MEDIA_BASE_URL} from "@/settings.js";
import { inject } from 'vue'

const { t } = inject('translations')

const { result, loading, error } = useQuery(gql`
  query GetAllSections {
    allSections {
      title
      subtitle
      body
      slug
      link
      image
      backgroundImage
      publishDate
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
  <div v-else class="section-list-container">
    <div v-for="section in result.allSections" :key="section.slug"  :class="['section-article', section.customCssClass]">
      <div v-if="section.backgroundImage" :style="{ backgroundImage: `url(${MEDIA_BASE_URL}${section.backgroundImage})` }" class="section-background"/>
      <img v-if="section.image" :src="`${MEDIA_BASE_URL}${section.image}`" :alt="section.title" class="section-image"/>
      <div class="section-block">
        <div class="title-container">
          <div class="title-text">
            {{ section.title }}
          </div>
        </div>
        <div class="subtitle-container">
          <div class="subtitle-text">
            {{ section.subtitle }}
          </div>
        </div>
        <div class="body-container">
          <div v-html="section.body" class="body-text">
          </div>
          <Button variant="outline" :to="`${section.link || 'section/' + section.slug}`">
            {{ t('button.read_more')}}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.section-list-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--px-40) var(--px-32);
  display: flex;
  flex-direction: column;
  gap: var(--px-48);
}

.section-article {
  width: 100%;
  position: relative;
  display: flex;
  gap: var(--px-32);
  background: var(--color-card-bg, #ffffff);
  border: 1px solid var(--color-card-border, #e2e8f0);
  border-radius: var(--px-16);
  overflow: hidden;
  box-shadow: 0 1px 3px var(--color-card-shadow, rgba(0,0,0,0.06));
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.section-article:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.section-background {
  display: none;
}

.section-image {
  width: 340px;
  min-height: 240px;
  object-fit: cover;
  flex-shrink: 0;
}

.section-block {
  display: flex;
  flex-direction: column;
  gap: var(--px-16);
  padding: var(--px-24);
  flex: 1;
}

.title-container {
  position: static;
  width: auto;
  height: auto;
  right: auto;
  top: auto;
}

.subtitle-container {
  display: none;
  position: static;
  width: auto;
  height: auto;
}

.title-text {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
  font-size: var(--font-size-header);
  text-transform: none;
  position: static;
  left: auto;
  width: auto;
  margin: 0;
  color: var(--color-heading);
  line-height: 1.3;
}

.body-container {
  position: static;
  width: auto;
  right: auto;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 0;
  backdrop-filter: none;
  box-shadow: none;
  top: auto;
  transform: none;
  display: flex;
  flex-direction: column;
  gap: var(--px-12);
}

.body-text {
  font-size: var(--font-size-normal);
  font-weight: 400;
  color: var(--color-text);
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.6;
}

/* Override all marketing CSS classes */
.section-article.right-section,
.section-article.left-section,
.section-article.world-section,
.section-article.squad-section,
.section-article.cdk-section {
  display: flex;
  flex-direction: row;

  .title-container,
  .body-container,
  .title-text,
  .section-image {
    position: static;
    left: auto;
    right: auto;
    top: auto;
    transform: none;
    width: auto;
    height: auto;
    margin: 0;
  }

  .section-image {
    width: 340px;
    min-height: 240px;
    object-fit: cover;
  }

  .title-text {
    color: var(--color-heading);
  }

  .subtitle-container {
    display: none;
  }

  .section-block {
    position: static;
  }

  .body-container {
    background: transparent;
    border: none;
    box-shadow: none;
    backdrop-filter: none;
    padding: 0;
    display: flex;
  }

  .section-background {
    display: none;
  }
}

/* Mobile */
@media (max-width: 860px) {
  .section-list-container {
    padding: var(--px-20) var(--px-16);
    gap: var(--px-24);
  }

  .section-article,
  .section-article.left-section,
  .section-article.right-section,
  .section-article.world-section,
  .section-article.squad-section,
  .section-article.cdk-section {
    flex-direction: column;
    gap: 0;
  }

  .section-image {
    width: 100% !important;
    min-height: auto;
    max-height: 220px;
  }

  .section-block {
    padding: var(--px-16);
  }

  .title-text {
    font-size: clamp(1.1rem, 5vw, 1.4rem) !important;
  }
}

@media (max-width: 480px) {
  .section-image {
    max-height: 180px;
  }
  .section-block {
    padding: var(--px-12);
  }
}
</style>