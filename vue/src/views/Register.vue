<template>
    <div class="relative min-h-[calc(100vh-2rem)] bg-gradient-to-br from-slate-100 dark:from-slate-950 via-white dark:via-slate-900 to-slate-200 dark:to-slate-950">
        <div class="absolute top-6 right-6">
            <ThemeToggle />
        </div>
        <div class="flex h-full box-border items-center justify-center px-4 py-8">
            <main
                class="w-full max-w-2xl rounded-[2rem] bg-white dark:bg-slate-900 p-8 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 dark:ring-slate-700 sm:p-10">
                <div class="mb-8">
                    <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Registrace</p>
                    <h2 class="mt-4 text-3xl font-extrabold text-slate-950 dark:text-white sm:text-4xl">
                        Vytvořte svůj nový účet
                    </h2>
                    <p class="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300 sm:text-base">
                        Zadejte své údaje a začněte používat TaskHub pro efektivní týmovou práci.
                    </p>
                </div>

                <div class="space-y-5">
                    <div class="space-y-2">
                        <label for="email" class="text-sm font-semibold text-slate-700 dark:text-slate-200">Email</label>
                        <input type="text" id="email"
                            class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-3 text-slate-900 dark:text-slate-100 shadow-sm outline-none transition focus:border-slate-400 dark:focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:focus:ring-slate-700"
                            placeholder="Zadejte svůj email" v-model="email" />
                    </div>

                    <div class="space-y-2">
                        <label for="username" class="text-sm font-semibold text-slate-700 dark:text-slate-200">Uživatelské jméno</label>
                        <input type="text" id="username"
                            class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-3 text-slate-900 dark:text-slate-100 shadow-sm outline-none transition focus:border-slate-400 dark:focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:focus:ring-slate-700"
                            placeholder="Zadejte své uživatelské jméno" v-model="username" />
                    </div>

                    <div class="space-y-2">
                        <label for="password" class="text-sm font-semibold text-slate-700 dark:text-slate-200">Heslo</label>
                        <input type="password" id="password"
                            class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-3 text-slate-900 dark:text-slate-100 shadow-sm outline-none transition focus:border-slate-400 dark:focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:focus:ring-slate-700"
                            placeholder="Zadejte své heslo" v-model="password" />
                    </div>

                    <button type="button" class="btn btn_submit w-full rounded-2xl text-base" @click="registerUser()">
                        Zaregistrovat se
                    </button>
                </div>

                <div
                    class="mt-6 flex flex-col gap-3 border-t border-slate-200 dark:border-slate-700 pt-6 text-sm sm:flex-row sm:items-center sm:justify-between">
                    <p class="text-slate-600 dark:text-slate-300">Již máš účet?
                        <router-link :to="{ name: 'Login' }" class="font-semibold text-slate-900 dark:text-slate-100 hover:text-slate-700 dark:hover:text-slate-200">
                            Přihlásit se
                        </router-link>
                    </p>
                </div>
            </main>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { useMainStore } from '../store'
import ThemeToggle from '../components/ThemeToggle.vue';

const mainStore = useMainStore()

const email = ref('');
const username = ref('');
const password = ref('');

function registerUser() {
    mainStore.api.post('/auth/register/', {
        email: email.value,
        username: username.value,
        password: password.value,
    })
}

</script>
<style lang="">

</style>