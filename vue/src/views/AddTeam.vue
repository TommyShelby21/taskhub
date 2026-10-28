<template>
    <div>
        <div class="flex flex-col gap-1 mb-6">
            <p class="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Tým</p>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">Vytvořit nový tým</h1>
            <p class="text-sm text-slate-500 dark:text-slate-400">Zadejte název týmu a vytvořte nové pracovní prostředí.</p>
        </div>

        <div class="rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-sm p-6 sm:p-8 max-w-lg">
            <div class="space-y-6">
                <div v-if="success"
                    class="rounded-2xl bg-emerald-50 dark:bg-emerald-500/10 p-4 text-center text-sm text-emerald-700 dark:text-emerald-300 ring-1 ring-emerald-200 dark:ring-emerald-500/30">
                    Tým byl úspěšně vytvořen
                </div>

                <div class="space-y-4">
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-slate-700 dark:text-slate-200">Název týmu</label>
                        <input type="text" placeholder="Zadejte název týmu"
                            class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-4 py-3 text-slate-900 dark:text-slate-100 outline-none transition focus:border-slate-400 dark:focus:border-slate-500 focus:ring-2 focus:ring-slate-200 dark:focus:ring-slate-700"
                            v-model="teamName" />
                    </div>
                    <button class="btn btn_main w-full rounded-2xl px-5 py-3 text-base" @click="createTeam()">
                        Vytvořit tým
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { useMainStore } from '../store'
import { onMounted, ref } from 'vue'

const mainStore = useMainStore();

// Add Team
const teamName = ref('')
const success = ref(false)

const createTeam = () => {
    mainStore.api.post(`/team/add`, { name: teamName.value }).then((response) => {
        success.value = true
        teamName.value = ''

    }).catch(err => {
        console.error(err)
    })
}

</script>
<style scoped></style>
