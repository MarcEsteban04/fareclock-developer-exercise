import { ref, computed } from 'vue';
import { apiService } from '@/services/api';
import type { Worker } from '@/types';

const workers = ref<Worker[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

export function useWorkers() {
  const fetchWorkers = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.getWorkers();
      if (response.error) {
        error.value = response.error.message;
      } else if (response.data) {
        workers.value = response.data;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch workers';
    } finally {
      loading.value = false;
    }
  };

  const createWorker = async (name: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.createWorker(name);
      if (response.error) {
        error.value = response.error.message;
        return null;
      } else if (response.data) {
        workers.value.push(response.data);
        return response.data;
      }
      return null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create worker';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const updateWorker = async (id: string, name: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.updateWorker(id, name);
      if (response.error) {
        error.value = response.error.message;
        return null;
      } else if (response.data) {
        const index = workers.value.findIndex((w) => w.id === id);
        if (index !== -1) {
          workers.value[index] = response.data;
        }
        return response.data;
      }
      return null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update worker';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const deleteWorker = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.deleteWorker(id);
      if (response.error) {
        error.value = response.error.message;
        return false;
      } else {
        workers.value = workers.value.filter((w) => w.id !== id);
        return true;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete worker';
      return false;
    } finally {
      loading.value = false;
    }
  };

  return {
    workers: computed(() => workers.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    fetchWorkers,
    createWorker,
    updateWorker,
    deleteWorker,
  };
}

