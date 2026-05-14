<script setup>
import AuthorLink from "../components/AuthorLink.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import { onMounted } from 'vue'
import { gql } from "@apollo/client/core";
import {MEDIA_BASE_URL} from "@/settings.js";
import { inject } from 'vue'

const { t } = inject('translations')

const dateFormatter = new Intl.DateTimeFormat("en-US", { dateStyle: "full" });
const displayableDate = (date) => dateFormatter.format(new Date(date));
const route = useRoute();

onMounted(() => {
  fetch(`/api/myapp/posts/${route.params.slug}/view/`, {
    method: 'POST'
  });
})
const slug = route.params.slug;
const { result, loading, error } = useQuery(
  gql`
    query GetPostBySlug($slug: String!) {
      postBySlug(slug: $slug) {
        title
        subtitle
        publishDate
        published
        metaDescription
        slug
        image
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
  <div v-else class="post-view-container">
    <article :set="post = result.postBySlug">
      <header class="title-container">
        <h1>{{ post.title }}</h1>
        <h2>{{ post.subtitle }}</h2>
        <p>{{ post.metaDescription }}</p>
      </header>
      <figure v-if="post.image">
        <img
          :src="`${MEDIA_BASE_URL}${post.image}`"
          :alt="post.title"
          style="max-width: 100%; height: auto;"
        />
      </figure>

      <section v-html="post.body" class="post-body-container"></section>
      <div class="post-properties-container">
        <div class="date-container">
        <p>{{ t('service.published_on')}} {{ displayableDate(post.publishDate) }}</p>
        </div>
      </div>
    </article>
  </div>
</template>

<style lang="scss" scoped>
.post-view-container {
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

.post-body-container {
  font-size: var(--font-size-normal);
  :deep(p) {
    margin-top: var(--px-24);
    margin-bottom: var(--px-24);
    img {
      width: 100%;
    }
  }
}
.title-container {
  margin-bottom: var(--px-20);
}

.post-properties-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: var(--font-size-normal);
  color: var(--color-text-muted, #64748b);
  margin-top: var(--px-20);
}



@media (max-width: 640px) {

  .post-body-container {
    margin: var(--px-20) var(--px-30);
  }
  .title-container {
    margin: 0 var(--px-30);
    margin-bottom: var(--px-20);
  }

  .post-properties-container{
    margin: 0 var(--px-30);
    margin-top: var(--px-20);
  }
}
</style>