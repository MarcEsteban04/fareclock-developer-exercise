<script setup lang="ts">
import { cn } from '@/lib/utils';

interface Props {
  class?: string;
}

defineProps<Props>();
</script>

<template>
  <div :class="cn('relative w-full overflow-auto', $attrs.class as any)">
    <table :class="cn('w-full caption-bottom text-sm', $attrs.class as any)">
      <slot />
    </table>
  </div>
</template>

<script lang="ts">
export const TableHeader = {
  name: 'TableHeader',
  template: `
    <thead :class="($attrs.class as any)">
      <slot />
    </thead>
  `,
};

export const TableBody = {
  name: 'TableBody',
  template: `
    <tbody :class="($attrs.class as any)">
      <slot />
    </tbody>
  `,
};

export const TableRow = {
  name: 'TableRow',
  template: `
    <tr :class="cn('border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted', $attrs.class as any)">
      <slot />
    </tr>
  `,
  setup() {
    return { cn };
  },
};

export const TableHead = {
  name: 'TableHead',
  template: `
    <th :class="cn('h-10 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0', $attrs.class as any)">
      <slot />
    </th>
  `,
  setup() {
    return { cn };
  },
};

export const TableCell = {
  name: 'TableCell',
  template: `
    <td :class="cn('p-4 align-middle [&:has([role=checkbox])]:pr-0', $attrs.class as any)">
      <slot />
    </td>
  `,
  setup() {
    return { cn };
  },
};
</script>

