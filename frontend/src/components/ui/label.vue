<script setup lang="ts">
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  for?: string;
}

defineProps<Props>();
</script>

<template>
  <label
    data-slot="label"
    :for="for"
    :class="cn(
      'flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
      $attrs.class
    )"
  >
    <slot />
  </label>
</template>

