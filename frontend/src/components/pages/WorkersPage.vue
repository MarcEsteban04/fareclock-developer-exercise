<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useWorkers } from '@/composables/useWorkers';
import Card from '@/components/ui/card.vue';
import CardHeader from '@/components/ui/CardHeader.vue';
import CardTitle from '@/components/ui/CardTitle.vue';
import CardDescription from '@/components/ui/CardDescription.vue';
import CardContent from '@/components/ui/CardContent.vue';
import Button from '@/components/ui/button.vue';
import Input from '@/components/ui/input.vue';
import Label from '@/components/ui/label.vue';
import Table from '@/components/ui/table.vue';
import TableHeader from '@/components/ui/TableHeader.vue';
import TableBody from '@/components/ui/TableBody.vue';
import TableRow from '@/components/ui/TableRow.vue';
import TableHead from '@/components/ui/TableHead.vue';
import TableCell from '@/components/ui/TableCell.vue';
import Dialog from '@/components/ui/dialog.vue';

const { workers, loading, error, fetchWorkers, createWorker, updateWorker, deleteWorker } = useWorkers();

const dialogOpen = ref(false);
const editingWorker = ref<{ id: string; name: string } | null>(null);
const workerName = ref('');
const deletingId = ref<string | null>(null);
const successMessage = ref<string | null>(null);
const confirmDialog = ref<{ open: boolean; workerId: string | null; workerName: string | null }>({
  open: false,
  workerId: null,
  workerName: null,
});

const showSuccess = (message: string) => {
  successMessage.value = message;
  setTimeout(() => {
    successMessage.value = null;
  }, 3500);
};

onMounted(() => {
  fetchWorkers();
});

const openCreateDialog = () => {
  editingWorker.value = null;
  workerName.value = '';
  dialogOpen.value = true;
};

const openEditDialog = (worker: { id: string; name: string }) => {
  editingWorker.value = worker;
  workerName.value = worker.name;
  dialogOpen.value = true;
};

const handleSave = async () => {
  if (!workerName.value.trim()) return;

  if (editingWorker.value) {
    await updateWorker(editingWorker.value.id, workerName.value.trim());
  } else {
    const created = await createWorker(workerName.value.trim());
    if (created) {
      showSuccess('Worker added successfully.');
    }
  }

  if (!error.value) {
    dialogOpen.value = false;
    workerName.value = '';
    editingWorker.value = null;
  }
};

const openDeleteDialog = (worker: { id: string; name: string }) => {
  confirmDialog.value = {
    open: true,
    workerId: worker.id,
    workerName: worker.name,
  };
};

const closeDeleteDialog = () => {
  confirmDialog.value = { open: false, workerId: null, workerName: null };
};

const confirmDelete = async () => {
  if (!confirmDialog.value.workerId) return;
  deletingId.value = confirmDialog.value.workerId;
  const success = await deleteWorker(confirmDialog.value.workerId);
  deletingId.value = null;
  if (success) {
    showSuccess('Worker deleted successfully.');
    closeDeleteDialog();
  }
};
</script>

<template>
  <div class="space-y-6">
    <transition name="fade">
      <div
        v-if="successMessage"
        class="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 shadow-sm"
      >
        <div class="flex items-center gap-2">
          <span class="inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
          {{ successMessage }}
        </div>
      </div>
    </transition>

    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">Workers</h2>
        <p class="text-muted-foreground mt-2">
          Manage your team members and their information.
        </p>
      </div>
      <Button @click="openCreateDialog" size="lg">
        <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Worker
      </Button>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>All Workers</CardTitle>
        <CardDescription>
          {{ workers.length }} worker{{ workers.length !== 1 ? 's' : '' }} in your system
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="text-muted-foreground">Loading workers...</div>
        </div>

        <div v-else-if="error" class="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
          <p class="text-sm text-destructive">{{ error }}</p>
        </div>

        <div v-else-if="workers.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
          <div class="rounded-full bg-muted p-6 mb-4">
            <svg class="h-12 w-12 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2">No workers yet</h3>
          <p class="text-muted-foreground mb-4">Get started by adding your first worker.</p>
          <Button @click="openCreateDialog">Add Worker</Button>
        </div>

        <div v-else class="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow v-for="worker in workers" :key="worker.id">
                <TableCell>
                  <div class="font-medium">{{ worker.name }}</div>
                </TableCell>
                <TableCell>
                  <div class="flex items-center gap-2">
                    <Button
                      @click="openEditDialog(worker)"
                      variant="ghost"
                      size="sm"
                    >
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      Edit
                    </Button>
                    <Button
                      @click="openDeleteDialog(worker)"
                      variant="ghost"
                      size="sm"
                      :disabled="deletingId === worker.id"
                    >
                      <svg class="h-4 w-4 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      Delete
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>

    <!-- Create/Edit Dialog -->
    <Dialog :open="dialogOpen" @update:open="dialogOpen = $event">
      <div class="space-y-4">
        <div>
          <h3 class="text-lg font-semibold">
            {{ editingWorker ? 'Edit Worker' : 'Add New Worker' }}
          </h3>
          <p class="text-sm text-muted-foreground mt-1">
            {{ editingWorker ? 'Update the worker information.' : 'Enter the name of the new worker.' }}
          </p>
        </div>

        <div class="space-y-2">
          <Label for="worker-name">Name</Label>
          <Input
            id="worker-name"
            v-model="workerName"
            placeholder="Enter worker name"
            @keyup.enter="handleSave"
          />
        </div>

        <div v-if="error" class="p-3 rounded-lg bg-destructive/10 border border-destructive/20">
          <p class="text-sm text-destructive">{{ error }}</p>
        </div>

        <div class="flex justify-end gap-3">
          <Button
            variant="outline"
            @click="dialogOpen = false"
          >
            Cancel
          </Button>
          <Button
            @click="handleSave"
            :disabled="!workerName.trim() || loading"
          >
            {{ editingWorker ? 'Update' : 'Create' }}
          </Button>
        </div>
      </div>
    </Dialog>

    <!-- Delete confirmation -->
    <Dialog :open="confirmDialog.open" @update:open="closeDeleteDialog">
      <div class="space-y-4">
        <div>
          <h3 class="text-lg font-semibold">Delete worker</h3>
          <p class="text-sm text-muted-foreground">
            This will also remove any shifts for <span class="font-medium">{{ confirmDialog.workerName }}</span>.
          </p>
        </div>
        <div class="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
          This action cannot be undone.
        </div>
        <div class="flex justify-end gap-3">
          <Button variant="outline" @click="closeDeleteDialog">Cancel</Button>
          <Button variant="destructive" @click="confirmDelete" :disabled="deletingId === confirmDialog.workerId">
            Delete
          </Button>
        </div>
      </div>
    </Dialog>
  </div>
</template>

