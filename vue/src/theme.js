import { ref, watchEffect } from 'vue'

// Theme is stored in localStorage; the inline script in index.html applies it before first paint
const STORAGE_KEY = 'theme'

function initialDark() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY)
        if (saved) return saved === 'dark'
    } catch { /* storage unavailable */ }
    return window.matchMedia('(prefers-color-scheme: dark)').matches
}

export const isDark = ref(initialDark())

watchEffect(() => {
    document.documentElement.classList.toggle('dark', isDark.value)
})

export function toggleDark() {
    isDark.value = !isDark.value
    try {
        localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
    } catch { /* storage unavailable */ }
}
