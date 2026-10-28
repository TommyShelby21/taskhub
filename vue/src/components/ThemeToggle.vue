<template>
    <button type="button" @click="toggleDark()" :title="isDark ? 'Světlý režim' : 'Tmavý režim'"
        :aria-label="isDark ? 'Přepnout na světlý režim' : 'Přepnout na tmavý režim'"
        class="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition-colors">
        <IconSun v-if="isDark" :size="19" stroke="1.8" />
        <IconMoon v-else :size="19" stroke="1.8" />
    </button>
</template>
<script setup>
import { IconSun, IconMoon } from '@tabler/icons-vue';
import { isDark, toggleDark } from '../theme';
</script>
