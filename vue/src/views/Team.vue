<template>
    <div>
        <div class="flex flex-col gap-1 mb-6">
            <p class="text-sm font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Tým</p>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-slate-100 tracking-tight">Management týmu</h1>
            <p class="text-sm text-slate-500 dark:text-slate-400">Přehled a správa členů vašeho týmu.</p>
        </div>

        <div class="rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden">
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800">
                <h2 class="text-base font-bold text-slate-800 dark:text-slate-100">Členové týmu</h2>
                <span class="inline-flex items-center rounded-full bg-blue-50 dark:bg-blue-500/10 px-2.5 py-1 text-xs font-semibold text-blue-700 dark:text-blue-300">
                    {{ teamMembers.length }} {{ teamMembers.length === 1 ? 'člen' : 'členů' }}
                </span>
            </div>

            <ul class="divide-y divide-slate-100 dark:divide-slate-800">
                <li v-for="member in teamMembers" :key="member.id"
                    class="flex items-center gap-4 px-6 py-4 hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">
                    <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300 text-sm font-bold uppercase">
                        {{ member.user.username.slice(0, 2) }}
                    </div>
                    <div class="min-w-0 flex-1">
                        <p class="text-sm font-semibold text-slate-800 dark:text-slate-100 truncate">{{ member.user.username }}</p>
                    </div>
                    <span v-if="member.leader"
                        class="inline-flex items-center gap-1 rounded-full bg-amber-50 dark:bg-amber-500/10 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:text-amber-300 ring-1 ring-amber-200 dark:ring-amber-500/30">
                        <IconCrown :size="14" />
                        Správce
                    </span>
                    <span v-else class="inline-flex items-center rounded-full bg-slate-100 dark:bg-slate-700 px-2.5 py-1 text-xs font-medium text-slate-500 dark:text-slate-400">
                        Člen
                    </span>
                    <button v-if="member.user.id !== mainStore.user.id" type="button"
                        class="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-red-50 dark:hover:bg-red-500/10 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                        @click="deleteMember(member)">
                        <IconTrash :size="16" />
                    </button>
                </li>

                <li v-if="teamMembers.length === 0" class="px-6 py-10 text-center text-sm text-slate-400">
                    Tým zatím nemá žádné členy.
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { useMainStore } from '../store'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { IconCrown, IconTrash } from '@tabler/icons-vue';

const route = useRoute();
const mainStore = useMainStore();

onMounted(() => {
    loadTeamMembers()
    loadTeam()
})

const selectedTeam = ref(null)
const teamMembers = ref([])
const loadTeamMembers = () => {
    mainStore.api.get(`/team/${route.params.id}/members/`).then((response) => {
        teamMembers.value = response.data.members
    })
}

const deleteMember = (member) => {
    if (member.leader) {
        alert('Nelze odstranit správce týmu')
    }
}

const loadTeam = () => {
    selectedTeam.value = mainStore.selectedTeam
}

</script>

<style scoped></style>
