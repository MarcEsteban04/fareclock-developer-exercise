/**
 * Date and timezone utility functions
 */

/**
 * Format an ISO 8601 datetime string according to the preferred timezone
 */
export function formatDateTime(
  isoString: string,
  timezone: string,
  options: Intl.DateTimeFormatOptions = {}
): string {
  const date = new Date(isoString);
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: timezone,
    ...options,
  };
  return new Intl.DateTimeFormat('en-US', defaultOptions).format(date);
}

/**
 * Format date only (without time)
 */
export function formatDate(isoString: string, timezone: string): string {
  const date = new Date(isoString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    timeZone: timezone,
  }).format(date);
}

/**
 * Format time only
 */
export function formatTime(isoString: string, timezone: string): string {
  const date = new Date(isoString);
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: timezone,
  }).format(date);
}

/**
 * Format datetime for input fields (local datetime-local format)
 */
export function formatDateTimeLocal(isoString: string, timezone: string): string {
  const date = new Date(isoString);
  // Convert to the target timezone
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });

  const parts = formatter.formatToParts(date);
  const year = parts.find((p) => p.type === 'year')?.value;
  const month = parts.find((p) => p.type === 'month')?.value;
  const day = parts.find((p) => p.type === 'day')?.value;
  const hour = parts.find((p) => p.type === 'hour')?.value;
  const minute = parts.find((p) => p.type === 'minute')?.value;

  return `${year}-${month}-${day}T${hour}:${minute}`;
}

/**
 * Convert local datetime-local string to ISO 8601 in the target timezone
 * This function treats the input as if it's already in the target timezone
 * 
 * Strategy: We need to create a UTC date that, when displayed in the target timezone,
 * shows the same date/time as the input. We do this by:
 * 1. Creating a date object from the input (interpreted as local browser time)
 * 2. Getting what that same moment looks like in the target timezone
 * 3. Calculating the offset and adjusting
 */
export function localToISO(dateTimeLocal: string, timezone: string): string {
  // Parse the local datetime string
  const [datePart, timePart] = dateTimeLocal.split('T');
  if (!datePart) {
    throw new Error('Invalid date format');
  }

  const dateParts = datePart.split('-').map(Number);
  const timeParts = (timePart || '00:00').split(':').map(Number);
  
  const year = dateParts[0] ?? 0;
  const month = dateParts[1] ?? 1;
  const day = dateParts[2] ?? 1;
  const hour = timeParts[0] ?? 0;
  const minute = timeParts[1] ?? 0;

  // Now we need to find what UTC time would display as this time in the target timezone
  // Get the timezone offset for the target timezone at this date
  // Create a formatter for the target timezone
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });

  // Try different UTC times until we find one that formats to our target
  // Start with the local date as UTC
  let testDate = new Date(Date.UTC(year, month - 1, day, hour, minute, 0));
  let iterations = 0;
  const maxIterations = 10;

  while (iterations < maxIterations) {
    const parts = formatter.formatToParts(testDate);
    const formattedYear = parseInt(parts.find((p) => p.type === 'year')?.value || '0');
    const formattedMonth = parseInt(parts.find((p) => p.type === 'month')?.value || '0');
    const formattedDay = parseInt(parts.find((p) => p.type === 'day')?.value || '0');
    const formattedHour = parseInt(parts.find((p) => p.type === 'hour')?.value || '0');
    const formattedMinute = parseInt(parts.find((p) => p.type === 'minute')?.value || '0');

    if (
      formattedYear === year &&
      formattedMonth === month &&
      formattedDay === day &&
      formattedHour === hour &&
      formattedMinute === minute
    ) {
      return testDate.toISOString();
    }

    // Calculate the difference and adjust
    const hourDiff = hour - formattedHour;
    const minuteDiff = minute - formattedMinute;
    const totalMinutesDiff = hourDiff * 60 + minuteDiff;

    testDate = new Date(testDate.getTime() + totalMinutesDiff * 60000);
    iterations++;
  }

  // Fallback: return the date as-is (not ideal but better than error)
  return testDate.toISOString();
}


/**
 * Get common IANA timezone options
 */
export function getCommonTimezones(): Array<{ value: string; label: string }> {
  return [
    { value: 'America/New_York', label: 'Eastern Time (ET)' },
    { value: 'America/Chicago', label: 'Central Time (CT)' },
    { value: 'America/Denver', label: 'Mountain Time (MT)' },
    { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
    { value: 'America/Phoenix', label: 'Arizona Time' },
    { value: 'America/Anchorage', label: 'Alaska Time' },
    { value: 'Pacific/Honolulu', label: 'Hawaii Time' },
    { value: 'UTC', label: 'UTC' },
    { value: 'Europe/London', label: 'London (GMT)' },
    { value: 'Europe/Paris', label: 'Paris (CET)' },
    { value: 'Europe/Berlin', label: 'Berlin (CET)' },
    { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
    { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
    { value: 'Asia/Dubai', label: 'Dubai (GST)' },
    { value: 'Australia/Sydney', label: 'Sydney (AEST)' },
    { value: 'America/Toronto', label: 'Toronto (ET)' },
    { value: 'America/Vancouver', label: 'Vancouver (PT)' },
    { value: 'America/Mexico_City', label: 'Mexico City (CST)' },
    { value: 'America/Sao_Paulo', label: 'São Paulo (BRT)' },
    { value: 'Asia/Singapore', label: 'Singapore (SGT)' },
    { value: 'Asia/Hong_Kong', label: 'Hong Kong (HKT)' },
  ];
}

