<template>
    <div class="relative min-h-[calc(100vh-2rem)] bg-gradient-to-br from-slate-100 via-white to-slate-200">
        <div class="flex h-full box-border items-center justify-center px-4 py-8">
            <main
                class="w-full max-w-2xl rounded-[2rem] bg-white p-8 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 sm:p-10">
                <div class="mb-8">
                    <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Registrace</p>
                    <h2 class="mt-4 text-3xl font-extrabold text-slate-950 sm:text-4xl">
                        Vytvořte svůj nový účet
                    </h2>
                    <p class="mt-3 text-sm leading-6 text-slate-600 sm:text-base">
                        Zadejte své údaje a začněte používat TashHub pro efektivní týmovou práci.
                    </p>
                </div>

                <div class="space-y-5">
                    <div class="space-y-2">
                        <label for="email" class="text-sm font-semibold text-slate-700">Email</label>
                        <input type="text" id="email"
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                            placeholder="Zadejte svůj email" v-model="email" />
                    </div>

                    <div class="space-y-2">
                        <label for="username" class="text-sm font-semibold text-slate-700">Uživatelské jméno</label>
                        <input type="text" id="username"
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                            placeholder="Zadejte své uživatelské jméno" v-model="username" />
                    </div>

                    <div class="space-y-2">
                        <label for="password" class="text-sm font-semibold text-slate-700">Heslo</label>
                        <input type="password" id="password"
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                            placeholder="Zadejte své heslo" v-model="password" />
                    </div>

                    <button type="button" class="btn btn_submit w-full rounded-2xl text-base" @click="registerUser()">
                        Zaregistrovat se
                    </button>
                </div>

                <div
                    class="mt-6 flex flex-col gap-3 border-t border-slate-200 pt-6 text-sm sm:flex-row sm:items-center sm:justify-between">
                    <p class="text-slate-600">Již máš účet?
                        <router-link :to="{ name: 'Login' }" class="font-semibold text-slate-900 hover:text-slate-700">
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