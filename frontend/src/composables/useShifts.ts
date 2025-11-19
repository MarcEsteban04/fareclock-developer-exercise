import { ref, computed } from 'vue';
import { apiService } from '@/services/api';
import type { Shift } from '@/types';

const shifts = ref<Shift[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

export function useShifts() {
  const fetchShifts = async (workerId?: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.getShifts(workerId);
      if (response.error) {
        error.value = response.error.message;
      } else if (response.data) {
        shifts.value = response.data;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch shifts';
    } finally {
      loading.value = false;
    }
  };

  const createShift = async (shift: Omit<Shift, 'id' | 'duration'>) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.createShift(shift);
      if (response.error) {
        error.value = response.error.message;
        return null;
      } else if (response.data) {
        shifts.value.push(response.data);
        return response.data;
      }
      return null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create shift';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const updateShift = async (id: string, shift: Partial<Omit<Shift, 'id' | 'duration'>>) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.updateShift(id, shift);
      if (response.error) {
        error.value = response.error.message;
        return null;
      } else if (response.data) {
        const index = shifts.value.findIndex((s) => s.id === id);
        if (index !== -1) {
          shifts.value[index] = response.data;
        }
        return response.data;
      }
      return null;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update shift';
      return null;
    } finally {
      loading.value = false;
    }
  };

  const deleteShift = async (id: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.deleteShift(id);
      if (response.error) {
        error.value = response.error.message;
        return false;
      } else {
        shifts.value = shifts.value.filter((s) => s.id !== id);
        return true;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete shift';
      return false;
    } finally {
      loading.value = false;
    }
  };

  return {
    shifts: computed(() => shifts.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    fetchShifts,
    createShift,
    updateShift,
    deleteShift,
  };
}

