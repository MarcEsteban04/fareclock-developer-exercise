<script setup lang="ts">
import { computed, watch } from 'vue';
import { cn } from '@/lib/utils';

interface Props {
  open?: boolean;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  open: false,
});

const emit = defineEmits<{
  'update:open': [value: boolean];
}>();

const isOpen = computed({
  get: () => props.open,
  set: (val) => emit('update:open', val),
});

function close() {
  isOpen.value = false;
}

// Close on Escape key
watch(isOpen, (newVal) => {
  if (newVal) {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
    };
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }
});
</script>

<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center"
        @click.self="close"
      >
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" />
        
        <!-- Dialog -->
        <div
          :class="cn(
            'relative z-50 w-full max-w-lg bg-background rounded-lg border shadow-lg p-6 mx-4',
            $attrs.class as any
          )"
        >
          <slot :close="close" />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dialog-enter-active,
.dialog-leave-active {
  transition: opacity 0.2s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}
</style>

<script lang="ts">
export const DialogHeader = {
  name: 'DialogHeader',
  template: `
    <div :class="cn('flex flex-col space-y-1.5 text-center sm:text-left', $attrs.class as any)">
      <slot />
    </div>
  `,
  setup() {
    return { cn };
  },
};

export const DialogTitle = {
  name: 'DialogTitle',
  template: `
    <h2 :class="cn('text-lg font-semibold leading-none tracking-tight', $attrs.class as any)">
      <slot />
    </h2>
  `,
  setup() {
    return { cn };
  },
};

export const DialogDescription = {
  name: 'DialogDescription',
  template: `
    <p :class="cn('text-sm text-muted-foreground', $attrs.class as any)">
      <slot />
    </p>
  `,
  setup() {
    return { cn };
  },
};

export const DialogContent = {
  name: 'DialogContent',
  template: `
    <div :class="cn('flex flex-col space-y-4', $attrs.class as any)">
      <slot />
    </div>
  `,
  setup() {
    return { cn };
  },
};

export const DialogFooter = {
  name: 'DialogFooter',
  template: `
    <div :class="cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', $attrs.class as any)">
      <slot />
    </div>
  `,
  setup() {
    return { cn };
  },
};
</script>

