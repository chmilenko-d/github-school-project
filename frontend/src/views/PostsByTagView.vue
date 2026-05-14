<script setup>
import PostList from "../components/PostList.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue'

const { t } = inject('translations')

const route = useRoute();
const tag = route.params.tag;
const { result, loading, error } = useQuery(gql`
  query {
    postsByTag(
      tag: "${tag}"
    ) {
        title
        slug
        author {
          user {
            username
            firstName
            lastName
          }
        }
      }
    }
`);
</script>

<template>
  <div v-if="loading">{{ t('service.loading')}}</div>
  <div v-else-if="error" class="warn">{{ error.message }}</div>
  <section v-else :set="tagPosts = result.postsByTag">
    <h2>Posts Tagged With "{{ tag }}"</h2>
    <PostList v-if="tagPosts.length > 0" :posts="tagPosts" />
    <p v-else>No posts found for this tag</p>
  </section>
</template>

<style lang="scss" scoped>
section {
  padding-top: var(--px-120);
  padding-bottom: var(--px-120);
  max-width: var(--px-1200);
  margin: 0 auto;
  min-height: 100vh;
  background-color: var(--color-background);
}

h2 {
  font-size: clamp(1.4rem, 4vw, 2rem);
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: var(--px-32);
  text-align: center;
}

p {
  color: var(--color-text-muted);
  text-align: center;
  font-size: var(--font-size-normal);
}

@media (max-width: 640px) {
  section {
    padding: var(--px-96) var(--px-20) var(--px-60);
  }
}
</style>