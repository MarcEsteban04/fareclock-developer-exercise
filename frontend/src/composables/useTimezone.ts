import { ref, computed } from 'vue';
import { apiService } from '@/services/api';

const timezone = ref<string>('UTC');
const loading = ref(false);
const error = ref<string | null>(null);

export function useTimezone() {
  const fetchTimezone = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.getTimezone();
      if (response.error) {
        error.value = response.error.message;
      } else if (response.data) {
        timezone.value = response.data.timezone;
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch timezone';
    } finally {
      loading.value = false;
    }
  };

  const updateTimezone = async (newTimezone: string) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.setTimezone(newTimezone);
      if (response.error) {
        error.value = response.error.message;
        return false;
      } else if (response.data) {
        timezone.value = response.data.timezone;
        return true;
      }
      return false;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update timezone';
      return false;
    } finally {
      loading.value = false;
    }
  };

  return {
    timezone: computed(() => timezone.value),
    loading: computed(() => loading.value),
    error: computed(() => error.value),
    fetchTimezone,
    updateTimezone,
  };
}

