export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(' ');
}

export function formatGoal(goal: string): string {
  return goal.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatDate(value: string): string {
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(new Date(value));
}

export function percentage(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function apiErrorMessage(error: unknown, fallback = 'Something went wrong. Please try again.'): string {
  const response = (error as { response?: { data?: { detail?: unknown } } })?.response;
  const detail = response?.data?.detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item && typeof item === 'object' && 'msg' in item) return String(item.msg);
        return 'The submitted information is invalid.';
      })
      .join(' ');
  }
  if (typeof detail === 'string') return detail;
  if (error instanceof Error && error.message) return error.message;
  return fallback;
}
