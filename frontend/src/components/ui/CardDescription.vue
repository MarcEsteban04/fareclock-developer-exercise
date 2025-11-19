<script setup lang="ts">
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
}

defineProps<Props>();
</script>

<template>
  <div
    data-slot="card-description"
    :class="cn('text-muted-foreground text-sm', $attrs.class)"
  >
    <slot />
  </div>
</template>

