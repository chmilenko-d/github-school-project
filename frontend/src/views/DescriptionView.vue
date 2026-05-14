<script setup>
import AuthorLink from "../components/AuthorLink.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import {MEDIA_BASE_URL} from "@/settings.js";
import { inject } from 'vue'

const { t } = inject('translations')

const dateFormatter = new Intl.DateTimeFormat("en-US", { dateStyle: "full" });
const displayableDate = (date) => dateFormatter.format(new Date(date));

const route = useRoute();
const slug = route.params.slug;
const { result, loading, error } = useQuery(
  gql`
    query GetDescriptionBySlug($slug: String!) {
      descriptionBySlug(slug: $slug) {
        title
        subtitle
        publishDate
        published
        metaDescription
        slug
        image
        backgroundImage
        body
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
  `,
  { slug }
);

</script>


<template>
  <div v-if="loading">{{ t('service.loading')}}</div>
  <div v-else-if="error" class="warn">{{ error.message }}</div>
  <div v-else class="description-view-container">
    <article :set="description = result.descriptionBySlug">
      <header class="title-container">
        <h1>{{ description.title }}</h1>
        <h2>{{ description.subtitle }}</h2>
        <p>{{ description.metaDescription }}</p>
      </header>
      <figure v-if="description.image">
        <img
          :src="`${MEDIA_BASE_URL}${description.image}`"
          :alt="description.title"
          style="max-width: 100%; height: auto;"
        />
      </figure>

      <section v-html="description.body" class="description-body-container"></section>
      <div class="post-properties-container">
        <div class="date-container">
        <p>{{ t('service.published_on')}} {{ displayableDate(description.publishDate) }}</p>
        </div>
      </div>
    </article>
  </div>
</template>


<style lang="scss" scoped>
.description-view-container {
  padding-top: var(--px-120);
  padding-bottom: var(--px-120);
  width: 100%;
  background-color: var(--color-background);
  min-height: 100vh;
}

article {
  max-width: var(--px-1000);
  margin: 0 auto;
  //padding: var(--px-20) var(--px-30);
}

.description-body-container {
  font-size: var(--font-size-normal);
}
.title-container {
  margin-bottom: var(--px-20);
  h1 {
    text-transform: uppercase;
  }
}

.post-properties-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: var(--font-size-normal);
  color: var(--color-text-muted, #64748b);
  margin-top: var(--px-20);
}
</style>