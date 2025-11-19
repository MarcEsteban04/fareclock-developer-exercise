/**
 * API service for communicating with the backend
 */

import type { Worker, Shift, TimezoneSetting, ApiResponse } from '@/types';

// Mapping helpers between backend (snake_case) and frontend (camelCase)
function toFrontendWorker(w: any): Worker {
  return {
    id: w.id,
    name: w.name,
    createdAt: w.created_at,
    updatedAt: w.updated_at,
  };
}

function toFrontendShift(s: any): Shift {
  return {
    id: s.id,
    workerId: s.worker_id,
    start: s.start,
    end: s.end,
    duration: s.duration,
    createdAt: s.created_at,
    updatedAt: s.updated_at,
  } as Shift;
}

function toBackendShiftPayload(input: any): any {
  const payload: any = {};
  if (input.workerId !== undefined) payload.worker_id = input.workerId;
  if (input.worker_id !== undefined) payload.worker_id = input.worker_id;
  if (input.start !== undefined) payload.start = input.start;
  if (input.end !== undefined) payload.end = input.end;
  return payload;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

function extractErrorMessage(status: number, statusText: string, payload?: any): string {
  if (payload) {
    if (typeof payload.detail === 'string') {
      return payload.detail;
    }

    if (Array.isArray(payload.detail)) {
      const messages = payload.detail
        .map((item: { msg?: string; message?: string } | undefined) => item?.msg || item?.message)
        .filter(Boolean);
      if (messages.length) {
        return messages.join('\n');
      }
    }

    if (payload.message) {
      return payload.message;
    }
  }

  return `HTTP ${status}: ${statusText}`;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => undefined);
        return {
          error: {
            message: extractErrorMessage(
              response.status,
              response.statusText,
              errorPayload,
            ),
            code: String(response.status),
            details: errorPayload,
          },
        };
      }

      const hasBody = response.headers.get('content-length') !== '0' && response.status !== 204;
      const data = hasBody ? await response.json() : null;
      return { data: data as T };
    } catch (error) {
      return {
        error: {
          message: error instanceof Error ? error.message : 'Network error occurred',
        },
      };
    }
  }

  // Timezone endpoints
  async getTimezone(): Promise<ApiResponse<TimezoneSetting>> {
    return this.request<TimezoneSetting>('/api/timezone');
  }

  async setTimezone(timezone: string): Promise<ApiResponse<TimezoneSetting>> {
    return this.request<TimezoneSetting>('/api/timezone', {
      method: 'POST',
      body: JSON.stringify({ timezone }),
    });
  }

  // Worker endpoints
  async getWorkers(): Promise<ApiResponse<Worker[]>> {
    const res = await this.request<any[]>('/api/workers');
    if (res.error) return { error: res.error };
    const mapped = (res.data || []).map(toFrontendWorker);
    return { data: mapped };
  }

  async getWorker(id: string): Promise<ApiResponse<Worker>> {
    const res = await this.request<any>(`/api/workers/${id}`);
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendWorker(res.data) : undefined };
  }

  async createWorker(name: string): Promise<ApiResponse<Worker>> {
    const res = await this.request<any>('/api/workers', {
      method: 'POST',
      body: JSON.stringify({ name }),
    });
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendWorker(res.data) : undefined };
  }

  async updateWorker(id: string, name: string): Promise<ApiResponse<Worker>> {
    const res = await this.request<any>(`/api/workers/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ name }),
    });
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendWorker(res.data) : undefined };
  }

  async deleteWorker(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/workers/${id}`, {
      method: 'DELETE',
    });
  }

  // Shift endpoints
  async getShifts(workerId?: string): Promise<ApiResponse<Shift[]>> {
    const query = workerId ? `?worker_id=${encodeURIComponent(workerId)}` : '';
    const res = await this.request<any[]>(`/api/shifts${query}`);
    if (res.error) return { error: res.error };
    const mapped = (res.data || []).map(toFrontendShift);
    return { data: mapped };
  }

  async getShift(id: string): Promise<ApiResponse<Shift>> {
    const res = await this.request<any>(`/api/shifts/${id}`);
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendShift(res.data) : undefined };
  }

  async createShift(shift: Omit<Shift, 'id' | 'duration'>): Promise<ApiResponse<Shift>> {
    const payload = toBackendShiftPayload(shift as any);
    const res = await this.request<any>('/api/shifts', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendShift(res.data) : undefined };
  }

  async updateShift(
    id: string,
    shift: Partial<Omit<Shift, 'id' | 'duration'>>
  ): Promise<ApiResponse<Shift>> {
    const payload = toBackendShiftPayload(shift as any);
    const res = await this.request<any>(`/api/shifts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
    if (res.error) return { error: res.error };
    return { data: res.data ? toFrontendShift(res.data) : undefined };
  }

  async deleteShift(id: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/shifts/${id}`, {
      method: 'DELETE',
    });
  }

  // Helpers to map backend (snake_case) <-> frontend (camelCase)
  
  
}

export const apiService = new ApiService();

