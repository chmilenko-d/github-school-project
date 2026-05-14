// <script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'
import { apolloClient } from '@/apollo.js'
import {MEDIA_BASE_URL} from "@/settings.js";
import { inject } from 'vue'
import Button from '@/components/Button.vue'

const { t } = inject('translations')

const dateFormatter = new Intl.DateTimeFormat("en-US", { dateStyle: "full" });
const displayableDate = (date) => dateFormatter.format(new Date(date));

const GET_POSTS = gql`
  query GetAllPosts($offset: Int!, $limit: Int!) {
    allPosts(offset: $offset, limit: $limit) {
      title
      subtitle
      slug
      image
      publishDate
      smallDescription
      views
      metaDescription
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
`

const posts = ref([])
const limit = ref(5)
const hasMore = ref(true)
const isFetching = ref(false)
const offset = ref(0)

const { result, fetchMore, onResult, onError, loading, refetch } = useQuery(
  GET_POSTS,
  () => ({ offset: offset.value, limit: limit.value }),
)
let scrollPosition = 0;
onResult((data) => {
  console.log(data);
  const allPosts = data?.data?.allPosts
  if (Array.isArray(allPosts)) {
    if (offset.value === 0) {
      posts.value = allPosts
    } else {
      posts.value = [...posts.value, ...allPosts]
    }
    hasMore.value = allPosts.length >= limit.value
  }
  Promise.resolve().then(() => {
          window.scrollTo(0, scrollPosition)
          isFetching.value = false
        })
})

const reloadPosts = async () => {
  isFetching.value = true
  posts.value = []
  offset.value = 0
  hasMore.value = true

  try {
    await apolloClient.cache.evict({
      fieldName: 'allPosts'
    })
    apolloClient.cache.gc()

    await refetch({offset: 0, limit: limit.value})
  } catch (err) {
    console.error('Ошибка:', err)
  } finally {
    isFetching.value = false
  }
}

const throttle = (func, delay) => {
  let inThrottle
  return function () {
    if (!inThrottle) {
      func.apply(this, arguments)
      inThrottle = true
      setTimeout(() => (inThrottle = false), delay)
    }
  }
}

const handleScroll = throttle(() => {
  if (isFetching.value || !hasMore.value) return

  const { scrollTop, clientHeight, scrollHeight } = document.documentElement
  if (scrollTop + clientHeight >= scrollHeight - 500) {
    isFetching.value = true
    scrollPosition = scrollTop
    offset.value = posts.value.length
  }
}, 300)

onMounted(() => {
  reloadPosts()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('language-changed', reloadPosts)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('language-changed', reloadPosts)
})

</script>

<template>
  <div v-if="loading">{{ t('service.loading')}}</div>
  <div v-else-if="error" class="warn">{{ error.message }}</div>

  <div v-else class="post-list-container">
    <div v-for="post in posts" :key="post.slug" class="post-article">
      <div class="post-properties-container">
        <div class="date-container">
          <p>{{ t('service.published_on')}} {{ displayableDate(post.publishDate) }}</p>
        </div>
        <div class="views-container">
          <p v-if="post.views">{{ t('service.views')}}: {{ post.views }}</p>
        </div>
      </div>
      <div class="post-block">
        <div v-if="post.image" :style="{ backgroundImage: `url(${MEDIA_BASE_URL}${post.image})` }" class="post-image"/>
        <div class="post-text-container">
          <div class="title-container">
            <div class="title-text">{{ post.title }}</div>
          </div>
          <div class="body-container">
            <div v-html="post.smallDescription" class="small-description-text"></div>
          </div>
        </div>
        <div class="button-container">
          <Button variant="outline" size="small" :to="{ name: 'post', params: { slug: post.slug } }">
            {{ t('button.read_more')}}
          </Button>
        </div>
      </div>

    </div>
  </div>
  <div v-if="!hasMore" class="end">{{ t('service.noposts')}}</div>
</template>

<style lang="scss" scoped>
.post-list-container {
  margin: auto;
  display: flex;
  flex-direction: column;
  width: fit-content;
  min-height: 100vh;
}
.post-article {
  width: var(--px-800);
  display: flex;
  //padding: var(--px-20) var(--px-30);
  flex-direction: column;
  margin-bottom: var(--px-40);
}

.post-properties-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: var(--font-size-normal);
  color: var(--color-text-muted, #64748b);
  margin-bottom: var(--px-12);
}

.button-container {
  //margin-top: var(--px-12);
  padding: var(--px-16) var(--px-20);
  padding-top: 0;
}

.post-block {
  background-color: var(--color-card-bg, #ffffff);
  border: 1px solid var(--color-card-border, #e2e8f0);
  border-radius: var(--px-6);
  box-shadow: 0 1px 3px var(--color-card-shadow, rgba(0,0,0,0.06));
  overflow: hidden;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.post-block:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.post-text-container {
  padding: var(--px-12) var(--px-24);
  .title-container {
  }

  .body-container {
      z-index: 2;
  }

  .title-text {
      font-family: 'Montserrat', sans-serif;
      font-weight: 700;
      font-size: var(--font-size-small-header);
      text-transform: none;
      color: var(--color-heading);
  }
}

.image-container {
  position: relative;
}
.image-shadow {
  position: absolute;
  top: 0;
  left:0;
  width: 100%;
  height: 100%;
  box-shadow: 0 0 var(--px-40) rgba(0, 0, 0, 0.5) inset;
}
.post-image {
  width: 100%;
  z-index: 1;
  height: var(--px-380);
  background: center;
  background-size: cover;
}

.body-text {
  font-size: var(--font-size-normal);
  //font-weight: 300;
}

.small-description-text {
  font-size: var(--font-size-normal);
  font-weight: initial;
  margin-top: var(--px-12);
}

.end {
  margin: auto;
  font-size: var(--font-size-normal);
  color: var(--color-text-muted, #64748b);
  padding: var(--px-20) var(--px-40);
  text-align: center;
}

@media (max-width: 640px) {
  .post-article {
    width: 100%;
    margin-bottom: var(--px-40);
  }
}

</style>