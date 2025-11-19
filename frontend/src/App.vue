<script setup lang="ts">
import { ref, computed, provide } from 'vue';
import Layout from './components/Layout.vue';
import ShiftsPage from './components/pages/ShiftsPage.vue';
import WorkersPage from './components/pages/WorkersPage.vue';
import TimezoneSettings from './components/pages/TimezoneSettings.vue';

const currentPage = ref('shifts');

const setPage = (page: string) => {
  if (['shifts', 'workers', 'settings'].includes(page)) {
    currentPage.value = page;
  }
};

provide('currentPage', currentPage);
provide('setPage', setPage);

const currentComponent = computed(() => {
  switch (currentPage.value) {
    case 'workers':
      return WorkersPage;
    case 'settings':
      return TimezoneSettings;
    default:
      return ShiftsPage;
  }
});
</script>

<template>
  <Layout>
    <component :is="currentComponent" />
  </Layout>
</template>
