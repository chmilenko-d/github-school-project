<script setup>

import SectionList from "../components/SectionList.vue";
import Footer from '../components/Footer.vue';

import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue'

const { t } = inject('translations')

const { result, loading, error } = useQuery(gql`
  query {
    allSections {
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
  <div v-else class="all-sections-container">
    <div class="page-header">
      <h1 class="page-title">{{ t('nav.sections', 'Разделы') }}</h1>
    </div>
    <SectionList :sections="result.allSections" />
    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.all-sections-container {
  padding-top: var(--px-60);
}

.page-header {
  padding: var(--px-32, 32px);
  text-align: center;
}

.page-title {
  font-size: clamp(1.6rem, 4vw, 2.2rem);
  color: var(--color-heading);
  font-weight: 700;
}
</style>