<script setup>
import { RouterView } from "vue-router";
import TranslationKeys from "@/components/TranslationKeys.vue";
import HeaderMenu from "@/components/HeaderMenu.vue";
</script>

<template>
  <TranslationKeys>
    <header>
      <div class="header-menu-container">
        <HeaderMenu />
      </div>
    </header>
    <RouterView />
  </TranslationKeys>
</template>

<style lang="scss" scoped>


.header-menu-container {
  height: var(--px-60);
  align-content: center;
  background-color: var(--color-background-white, #ffffff);
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 1px 3px var(--color-card-shadow, rgba(0,0,0,0.06));
  position: fixed;
  width: 100%;
  z-index: 4;
}

</style>