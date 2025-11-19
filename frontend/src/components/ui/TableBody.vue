<script setup lang="ts">
interface Props {
  class?: string;
}

defineProps<Props>();
</script>

<template>
  <tbody :class="$attrs.class">
    <slot />
  </tbody>
</template>

