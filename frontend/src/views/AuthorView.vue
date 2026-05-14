<script setup>
import PostList from "../components/PostList.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue'

const { t } = inject('translations')

const route = useRoute();
const username = route.params.username;
const { result, loading, error } = useQuery(gql`
  query {
    authorByUsername(
      username: "${username}"
    ) {
        website
        bio
        user {
          firstName
          lastName
          username
        }
        postSet {
          title
          slug
        }
        sectionSet {
          title
          slug
        }
      }
  }
`);
</script>

<template>
  <div v-if="loading">{{ t('service.loading')}}</div>
  <div v-else-if="error">{{ error.message }}</div>
  <section v-else :set="author = result.authorByUsername">
    <h2>{{ author.user.username }}</h2>
    <template v-if="author.user.firstName && author.user.lastName">
      <h3>{{ author.user.firstName }} {{ author.user.lastName }}</h3>
    </template>
    <p v-if="author.bio">
      {{ author.bio }}
      <template v-if="author.website">
        Learn more about {{ author.user.username }} on their
        <a :href="author.website">website</a>.
      </template>
    </p>
    <h3>Posts</h3>
    <PostList
      v-if="author.postSet"
      :posts="author.postSet"
      :showAuthor="false"
    />
    <p v-else>The author hasn't posted yet.</p>
    <h3>Sections</h3>
    <SectionList
      v-if="author.sectionSet"
      :sections="author.sectionSet"
      :showAuthor="false"
    />
    <p v-else>The author hasn't created sections yet.</p>
  </section>
</template>

<style lang="scss" scoped>
section {
  padding-top: var(--px-120);
  padding-bottom: var(--px-120);
  max-width: var(--px-1000);
  margin: 0 auto;
  min-height: 100vh;
  background-color: var(--color-background);
}

h2 {
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: var(--px-16);
}

h3 {
  font-size: var(--font-size-header);
  font-weight: 600;
  color: var(--color-heading);
  margin-top: var(--px-32);
  margin-bottom: var(--px-16);
}

p {
  color: var(--color-text);
  font-size: var(--font-size-normal);
  line-height: 1.6;
}

a {
  color: var(--color-primary);
  text-decoration: none;
  &:hover {
    color: var(--color-primary-hover);
    text-decoration: underline;
  }
}

@media (max-width: 640px) {
  section {
    padding: var(--px-96) var(--px-20) var(--px-60);
  }
}
</style>