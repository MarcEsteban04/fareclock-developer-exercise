<script setup lang="ts">
interface Props {
  class?: string;
}

defineProps<Props>();
</script>

<template>
  <thead :class="$attrs.class">
    <slot />
  </thead>
</template>

