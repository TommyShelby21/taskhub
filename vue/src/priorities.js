export const PRIORITIES = [
    { value: 'low', label: 'Nízká', dotClass: 'bg-emerald-400' },
    { value: 'medium', label: 'Střední', dotClass: 'bg-amber-400' },
    { value: 'high', label: 'Vysoká', dotClass: 'bg-red-500' },
]

export const DEFAULT_PRIORITY = 'medium'

export function getPriority(value) {
    return PRIORITIES.find(p => p.value === value) ?? PRIORITIES.find(p => p.value === DEFAULT_PRIORITY)
}
