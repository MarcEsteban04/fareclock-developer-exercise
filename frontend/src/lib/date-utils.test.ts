import { describe, expect, it } from 'vitest';
import {
  formatDate,
  formatTime,
  formatDateTime,
  formatDateTimeLocal,
  localToISO,
} from './date-utils';

const ISO_SAMPLE = '2025-11-18T15:56:00.000Z';

describe('date-utils formatting helpers', () => {
  it('formats full datetime with timezone', () => {
    expect(formatDateTime(ISO_SAMPLE, 'UTC')).toBe('Nov 18, 2025, 03:56 PM');
    expect(formatDateTime(ISO_SAMPLE, 'America/New_York')).toBe('Nov 18, 2025, 10:56 AM');
  });

  it('formats date-only strings consistently', () => {
    expect(formatDate(ISO_SAMPLE, 'UTC')).toBe('Nov 18, 2025');
  });

  it('formats time-only strings consistently', () => {
    expect(formatTime(ISO_SAMPLE, 'America/Los_Angeles')).toBe('07:56 AM');
  });

  it('formats ISO into datetime-local input value', () => {
    expect(formatDateTimeLocal(ISO_SAMPLE, 'UTC')).toBe('2025-11-18T15:56');
    expect(formatDateTimeLocal(ISO_SAMPLE, 'America/New_York')).toBe('2025-11-18T10:56');
  });
});

describe('localToISO', () => {
  it('converts local datetime strings into ISO respecting timezone', () => {
    const localInput = '2025-11-18T10:00';
    const result = localToISO(localInput, 'America/New_York');
    expect(result).toBe('2025-11-18T15:00:00.000Z');
  });

  it('handles half-hour offset zones', () => {
    const localInput = '2025-05-10T09:30';
    const result = localToISO(localInput, 'Asia/Kolkata');
    expect(result).toBe('2025-05-10T04:00:00.000Z');
  });
});
