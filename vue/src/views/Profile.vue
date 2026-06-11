<template>
    <div class="relative min-h-[calc(100vh-2rem)] bg-gradient-to-br from-slate-100 via-white to-slate-200">
        <div class="flex h-full box-border items-center justify-center px-4 py-8">
            <main class="w-full max-w-4xl rounded-[2rem] bg-white p-8 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 sm:p-10">
                <div class="mb-8">
                    <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Profil</p>
                    <h2 class="mt-4 text-3xl font-extrabold text-slate-950 sm:text-4xl">Vaše informace</h2>
                </div>

                <div class="grid gap-8 md:grid-cols-[0.9fr_1.1fr]">
                    <div class="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-8 text-center">
                        <div class="mx-auto flex h-44 w-44 items-center justify-center rounded-full bg-white shadow-sm">
                            <IconUserCircle class="h-24 w-24 text-slate-500" />
                        </div>
                        <p class="mt-6 text-sm font-semibold text-slate-700">Profilový obrázek</p>
                        <p class="mt-2 text-sm text-slate-500">Váš účet nemá nahraný vlastní avatar.</p>
                    </div>

                    <div class="rounded-[1.5rem] bg-slate-50 p-8 shadow-sm">
                        <div v-if="mainStore.user" class="space-y-6">
                            <div>
                                <p class="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Uživatelské jméno</p>
                                <p class="mt-2 text-xl font-semibold text-slate-950">{{ mainStore.user.username }}</p>
                            </div>
                            <div v-if="mainStore.user.email">
                                <p class="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Email</p>
                                <p class="mt-2 text-xl font-semibold text-slate-950">{{ mainStore.user.email }}</p>
                            </div>
                        </div>
                        <div v-else class="rounded-2xl bg-white p-6 text-center text-slate-500">
                            Načítání uživatele...
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
</template>

<script setup>
import { useMainStore } from '../store'
import { IconUserCircle } from '@tabler/icons-vue';

const mainStore = useMainStore()
</script>

<style scoped>
</style>
