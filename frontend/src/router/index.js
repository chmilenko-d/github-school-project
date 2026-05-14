import { createRouter, createWebHistory } from "vue-router";
import AuthorView from "../views/AuthorView.vue";
import AllPostsView from "../views/AllPostsView.vue";
import AllSectionsView from "../views/AllSectionsView.vue";
import AllDescriptionsView from "../views/AllDescriptionsView.vue";
import HomeView from "../views/HomeView.vue";
import PostView from "../views/PostView.vue";
import SectionView from "../views/SectionView.vue";
import DescriptionView from "../views/DescriptionView.vue";
import PostsByTagView from "../views/PostsByTagView.vue";
import TeachersView from "../views/TeachersView.vue";
import TeacherView from "../views/TeacherView.vue";
import DocumentsView from "../views/DocumentsView.vue";
import ContactsView from "../views/ContactsView.vue";
import PageView from "../views/PageView.vue";
import GalleryView from "../views/GalleryView.vue";
import AlbumView from "../views/AlbumView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() {
    return { top: 0 };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/news",
      name: "news",
      component: AllPostsView,
    },
    {
      path: "/news/:slug",
      name: "post",
      component: PostView,
    },
    {
      path: "/sections",
      name: "sections",
      component: AllSectionsView,
    },
    {
      path: "/section/:slug",
      name: "section",
      component: SectionView,
    },
    {
      path: "/descriptions",
      name: "descriptions",
      component: AllDescriptionsView,
    },
    {
      path: "/description/:slug",
      name: "description",
      component: DescriptionView,
    },
    {
      path: "/teachers",
      name: "teachers",
      component: TeachersView,
    },
    {
      path: "/teachers/:slug",
      name: "teacher",
      component: TeacherView,
    },
    {
      path: "/documents",
      name: "documents",
      component: DocumentsView,
    },
    {
      path: "/contacts",
      name: "contacts",
      component: ContactsView,
    },
    {
      path: "/gallery",
      name: "gallery",
      component: GalleryView,
    },
    {
      path: "/gallery/:slug",
      name: "album",
      component: AlbumView,
    },
    {
      path: "/page/:slug",
      name: "page",
      component: PageView,
    },
    {
      path: "/tag/:tag",
      name: "tag",
      component: PostsByTagView,
    },
    {
      path: "/author/:username",
      name: "author",
      component: AuthorView,
    },
    // Редиректы со старых URL
    {
      path: "/posts",
      redirect: "/news",
    },
    {
      path: "/post/:slug",
      redirect: to => `/news/${to.params.slug}`,
    },
  ],
});

export default router;