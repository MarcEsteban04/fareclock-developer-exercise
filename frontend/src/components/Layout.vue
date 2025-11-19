<script setup lang="ts">
import { inject, onMounted, ref, computed } from 'vue';
import { useTimezone } from '@/composables/useTimezone';

const { timezone, fetchTimezone } = useTimezone();

const currentPage = inject<{ value: string }>('currentPage', { value: 'shifts' });
const setPage = inject<(page: string) => void>('setPage', () => {});

const mobileMenuOpen = ref(false);

const navLinks = [
  { id: 'shifts', label: 'Shifts', description: 'Schedule overview' },
  { id: 'workers', label: 'Workers', description: 'Team roster' },
  { id: 'settings', label: 'Settings', description: 'Timezone preferences' },
];

const activeLink = computed(() => navLinks.find((link) => link.id === currentPage.value) ?? navLinks[0]);

function handleNavigation(page: string) {
  setPage?.(page);
  mobileMenuOpen.value = false;
}

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value;
}

onMounted(() => {
  fetchTimezone();
});
</script>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <div class="pointer-events-none absolute inset-x-0 top-0 -z-10 flex justify-center overflow-hidden">
      <div class="h-64 w-[70rem] bg-gradient-to-r from-sky-200 via-violet-200 to-amber-200 blur-3xl opacity-70"></div>
    </div>

    <!-- Header -->
    <header class="sticky top-0 z-40 w-full border-b border-slate-100 bg-white/90 backdrop-blur">
      <div class="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-emerald-400 text-base font-bold text-white shadow-lg">
            F
          </div>
          <div>
            <p class="text-xs uppercase tracking-[0.3em] text-slate-400">Fareclock</p>
            <p class="text-lg font-semibold text-slate-900">Shift Planner</p>
          </div>
        </div>

        <nav class="hidden md:flex items-center gap-2">
          <button
            v-for="link in navLinks"
            :key="link.id"
            @click="handleNavigation(link.id)"
            :aria-current="currentPage.value === link.id ? 'page' : undefined"
            :class="[
              'group flex flex-col rounded-xl border px-4 py-2 text-left transition-all duration-200',
              currentPage.value === link.id
                ? 'border-sky-500/80 bg-sky-50 text-slate-900 shadow-[0_0_25px_rgba(14,165,233,0.25)]'
                : 'border-slate-100 text-slate-500 hover:border-slate-300 hover:bg-white hover:text-slate-900'
            ]"
          >
            <span class="text-sm font-semibold">{{ link.label }}</span>
            <span class="text-xs text-slate-400 group-hover:text-slate-500">{{ link.description }}</span>
          </button>
        </nav>

        <div class="hidden md:flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-xs text-slate-500">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3" />
            <circle cx="12" cy="12" r="9" stroke-width="2"></circle>
          </svg>
          <span>{{ timezone || 'Loading timezone…' }}</span>
        </div>

        <!-- Mobile menu button -->
        <button
          @click="toggleMobileMenu"
          class="md:hidden rounded-full border border-slate-200 p-2 text-slate-700 hover:bg-slate-100"
          aria-label="Toggle navigation"
        >
          <svg v-if="!mobileMenuOpen" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-slate-100 bg-white">
        <nav class="container mx-auto space-y-1 px-4 py-4">
          <button
            v-for="link in navLinks"
            :key="link.id"
            @click="handleNavigation(link.id)"
            :class="[
              'w-full rounded-xl border px-4 py-3 text-left text-sm font-medium transition-colors',
              currentPage.value === link.id
                ? 'border-sky-500/80 bg-sky-50 text-slate-900'
                : 'border-slate-100 text-slate-500 hover:border-slate-200 hover:bg-slate-50'
            ]"
          >
            <div class="flex items-center justify-between">
              <span>{{ link.label }}</span>
              <span class="text-xs text-slate-400">{{ link.description }}</span>
            </div>
          </button>
        </nav>
      </div>
    </header>

    <!-- Main content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <section class="mb-8 rounded-2xl border border-white shadow-[0_10px_40px_rgba(15,23,42,0.08)] bg-gradient-to-br from-white to-slate-50 p-6 text-slate-600">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.4em] text-slate-400">Current view</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-900">{{ activeLink?.label ?? 'Shifts' }}</h2>
            <p class="text-sm text-slate-500">{{ activeLink?.description ?? 'Schedule overview' }}</p>
          </div>
          <div class="flex flex-wrap gap-3">
            <span class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6l3 3" />
              </svg>
              {{ timezone || 'UTC' }}
            </span>
            <span class="inline-flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm text-slate-600">
              <span class="h-2 w-2 rounded-full bg-emerald-400"></span>
              Real-time validation enabled
            </span>
          </div>
        </div>
      </section>

      <slot />
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-200 bg-white/70 py-6 text-center text-sm text-slate-500">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8">
        <p>Fareclock • Designed for high-volume shift operations • Timezone: {{ timezone || 'UTC' }}</p>
      </div>
    </footer>
  </div>
</template>

