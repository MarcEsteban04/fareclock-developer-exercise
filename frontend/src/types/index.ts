/**
 * Core domain types for the Shift Management application
 */

export interface Worker {
  id: string;
  name: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface Shift {
  id: string;
  workerId: string;
  worker?: Worker; // Populated on fetch
  start: string; // ISO 8601 datetime string
  end: string; // ISO 8601 datetime string
  duration: number; // Computed duration in floating point hours (read-only)
  createdAt?: string;
  updatedAt?: string;
}

export interface TimezoneSetting {
  timezone: string; // IANA timezone string
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

