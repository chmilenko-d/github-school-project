<script setup>
import DescriptionList from "../components/DescriptionList.vue";
import { useQuery } from "@vue/apollo-composable";
import { gql } from "@apollo/client/core";
import { inject } from 'vue'

const { t } = inject('translations')

const { result, loading, error } = useQuery(gql`
  query {
    allDescriptions {
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
  <div v-else class="all-descriptions-container">
    <div class="all-descriptions-content">
      <div class="general-title-container">
        <div class="general-title-text">
          {{ t('button.descriptions') }}
        </div>
      </div>
      <!-- проп компонента: если в DescriptionList используется items, поменяйте на :items -->
      <DescriptionList :items="result.allDescriptions" />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.all-descriptions-container {
  padding-top: var(--px-120);
  padding-bottom: var(--px-120);
  background-color: var(--color-background);
  min-height: 100vh;

}

.all-descriptions-content {
  width: 100%;
  max-width: var(--px-1200);
  margin: 0 auto;
  padding: 0 var(--px-32);
}

.general-title-container {
  width: 100%;
  position: relative;
}

.general-title-text {
  font-size: var(--font-size-header);
  font-weight: 700;
  color: var(--color-heading);
  text-align: center;
  margin-bottom: var(--px-40);
}

/* Mobile */
@media (max-width: 860px) {
  .all-descriptions-container {
    padding-top: var(--px-96);
  }
  .all-descriptions-content {
    padding: 0 var(--px-24);
  }
  .general-title-text {
    font-size: clamp(1.6rem, 6.5vw, 2.2rem);
    margin-bottom: var(--px-32);
  }
}

@media (max-width: 480px) {
  .all-descriptions-container {
    padding-top: var(--px-88);
  }
  .all-descriptions-content {
    padding: 0 var(--px-18);
  }
  .general-title-text {
    font-size: clamp(1.4rem, 8vw, 1.9rem);
    margin-bottom: var(--px-28);
  }
}
</style>