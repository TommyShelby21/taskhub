<template>
    <div class="relative min-h-[calc(100vh-2rem)] flex items-center justify-center bg-gradient-to-br from-slate-100 via-white to-slate-200">
        <div class="absolute top-6 right-6">
            <button @click="demoLogin()" type="button" class="btn btn_secondary text-sm px-4 py-2 rounded-full shadow-sm">
                Demo režim
            </button>
        </div>

        <div class="w-full max-w-6xl px-4">
            <div class="grid w-full gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:gap-12">
                <section
                    class="hidden rounded-[2rem] bg-white/80 p-10 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 lg:block">
                    <div class="space-y-8">
                        <div
                            class="inline-flex items-center gap-3 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm">
                            <span class="h-2.5 w-2.5 rounded-full bg-teal-400"></span>
                            Pracujte chytře a rychle
                        </div>
                        <div class="space-y-4">
                            <h1 class="text-4xl font-extrabold tracking-tight text-slate-950">
                                Vítejte v TaskHub
                            </h1>
                            <p class="max-w-md text-base leading-7 text-slate-600">
                                Přihlaste se do svého účtu a sledujte projekty, úkoly a tým v přehledném rozhraní.
                            </p>
                        </div>
                        <div class="space-y-4 text-slate-700">
                            <div>
                                <h2 class="text-xl font-semibold">Přehled v reálném čase</h2>
                                <p class="text-sm">Sledujte stav úkolů a týmové aktivity na jednom místě.</p>
                            </div>
                            <div>
                                <h2 class="text-xl font-semibold">Bezpečné přihlášení</h2>
                                <p class="text-sm">Vaše data jsou chráněna pomocí moderních standardů zabezpečení.</p>
                            </div>
                        </div>
                    </div>
                </section>

                <main
                    class="rounded-[2rem] bg-white p-8 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 sm:p-10">
                    <div class="mb-8">
                        <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Přihlášení</p>
                        <h2 class="mt-4 text-3xl font-extrabold text-slate-950 sm:text-4xl">
                            Vstup do vašeho účtu
                        </h2>
                        <p class="mt-3 text-sm leading-6 text-slate-600 sm:text-base">
                            Zadejte svůj email a heslo pro přístup do TaskHub.
                        </p>
                    </div>

                    <div class="space-y-5">
                        <div class="space-y-2">
                            <label for="email" class="text-sm font-semibold text-slate-700">Email</label>
                            <input type="text" id="email"
                                class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                                placeholder="Zadejte svůj email" v-model="username" />
                        </div>

                        <div class="space-y-2">
                            <label for="password" class="text-sm font-semibold text-slate-700">Heslo</label>
                            <input type="password" id="password"
                                class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                                placeholder="Zadejte své heslo" v-model="password" @keyup.enter="loginUser" />
                        </div>

                        <button type="button" class="btn btn_submit w-full rounded-2xl text-base" @click="loginUser()">
                            Přihlásit se
                        </button>
                    </div>

                    <div
                        class="mt-6 flex flex-col gap-3 border-t border-slate-200 pt-6 text-sm sm:flex-row sm:items-center sm:justify-between">
                        <p class="text-slate-600">Ještě nemáš účet?
                            <router-link :to="{ name: 'Register' }"
                                class="font-semibold text-slate-900 hover:text-slate-700">
                                Zaregistrovat se
                            </router-link>
                        </p>
                        <button type="button" class="text-slate-500 hover:text-slate-700">
                            Zapomněli jste heslo?
                        </button>
                    </div>
                </main>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMainStore } from '../store'
import { useRouter } from 'vue-router';

const mainStore = useMainStore()
const router = useRouter();

const username = ref('');
const password = ref('');

function loginUser() {
    mainStore.api.post('/auth/login/', {
        username: username.value,
        password: password.value,
    },
    ).then(response => {
        mainStore.api.get(`/user/${response.data.user.id}/`)
            .then((response) => {
                mainStore.setUser(response.data.user);
            }).catch(err => {
                console.error('Chyba při načítání profilu uživatele:', err);
            });
        router.push({ name: 'HomePage' });
    }).catch(err => {
        console.error(err)
    })
}

function demoLogin() {
    mainStore.api.post('/auth/create-demo/').then(response => {
        mainStore.setUser(response.data.user);
        router.push({ name: 'HomePage' });
    }).catch(err => {
        console.error('Chyba při vytvoření demo účtu:', err);
    });
}

</script>
<style lang="">

</style>