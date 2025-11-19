<script setup lang="ts">
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
}

defineProps<Props>();
</script>

<template>
  <div
    data-slot="card-title"
    :class="cn('leading-none font-semibold', $attrs.class)"
  >
    <slot />
  </div>
</template>

