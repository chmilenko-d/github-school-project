<script setup>
import PostList from "../components/PostList.vue";
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue'

const { t } = inject('translations')

const { result, loading, error } = useQuery(gql`
  query {
    allPosts {
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
  <div v-else-if="error" class="warn"></div>
  <div v-else class="all-posts-container">
    <PostList/>
  </div>
</template>

<style lang="scss" scoped>
.all-posts-container {
  padding-top: var(--px-120);
  padding-bottom: var(--px-120);
  width: 100%;
  background-color: var(--color-background);
  min-height: 100vh;
}
</style>