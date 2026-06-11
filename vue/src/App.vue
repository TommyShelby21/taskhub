<template>
  <div class="min-h-screen box-border p-4">
    <SideBar v-if="showNavbar" />
    <div :class="showNavbar ? 'sm:ml-64 md:ml-64' : ''">
      <router-view />
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
