<template>
    <div>
        <div class="flex flex-col gap-1 mb-6">
            <p class="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Profil</p>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">Vaše informace</h1>
            <p class="text-sm text-slate-500 dark:text-slate-400">Přehled údajů spojených s vaším účtem.</p>
        </div>

        <div class="rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-sm p-6 sm:p-8">
            <div class="grid gap-8 md:grid-cols-[0.9fr_1.1fr]">
                <div class="rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 p-8 text-center">
                    <div class="mx-auto flex h-32 w-32 items-center justify-center rounded-full bg-white dark:bg-slate-900 shadow-sm">
                        <IconUserCircle class="h-16 w-16 text-slate-400" stroke="1.5" />
                    </div>
                    <p class="mt-6 text-sm font-semibold text-slate-700 dark:text-slate-200">Profilový obrázek</p>
                    <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">Váš účet nemá nahraný vlastní avatar.</p>
                </div>

                <div class="rounded-2xl bg-slate-50 dark:bg-slate-800 p-8">
                    <div v-if="user" class="space-y-6">
                        <div>
                            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Uživatelské jméno</p>
                            <p class="mt-2 text-xl font-semibold text-slate-900 dark:text-slate-100">{{ user.username }}</p>
                        </div>
                        <div v-if="user.email">
                            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">Email</p>
                            <p class="mt-2 text-xl font-semibold text-slate-900 dark:text-slate-100">{{ user.email }}</p>
                        </div>
                    </div>
                    <div v-else class="rounded-xl bg-white dark:bg-slate-900 p-6 text-center text-slate-500 dark:text-slate-400">
                        Načítání uživatele...
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useMainStore } from '../store'
import { IconUserCircle } from '@tabler/icons-vue';

const { user } = useMainStore()
</script>

<style scoped></style>
