<script setup lang="ts">
import { computed, useAttrs } from 'vue';
import type { ClassValue } from 'clsx';
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
  type?: string;
  modelValue?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
});

const emit = defineEmits<{
  'update:modelValue': [value: string | number];
}>();

const value = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val ?? ''),
});

const attrs = useAttrs();

const baseClasses = [
  'file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
  'focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]',
  'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
] as const;

const inputClass = computed(() =>
  cn(baseClasses, attrs.class as ClassValue)
);
</script>

<template>
  <input
    :type="type"
    data-slot="input"
    :class="inputClass"
    :value="value"
    @input="value = ($event.target as HTMLInputElement).value"
    v-bind="$attrs"
  />
</template>

