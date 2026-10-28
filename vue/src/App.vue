<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 box-border">
    <SideBar v-if="showNavbar" />
    <div :class="showNavbar ? 'sm:ml-72 px-4 pb-4 pt-20 sm:px-8 sm:pb-8 sm:pt-8' : ''">
      <div :class="showNavbar ? 'max-w-6xl mx-auto' : ''">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import SideBar from './components/SideBar.vue';
import { useRoute } from 'vue-router'
import { useMainStore } from './store';

const store = useMainStore();

const route = useRoute();

const showNavbar = computed(() =>
  route.meta.navbar !== false
)
</script>

<style scoped></style>
