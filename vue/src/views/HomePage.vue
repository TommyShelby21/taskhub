<template>
    <div>
        <div class="flex flex-col gap-1 mb-6">
            <p class="text-sm font-semibold text-blue-600 uppercase tracking-wider">{{ formattedDate }}</p>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                Nástěnka
            </h1>
            <p class="text-sm text-slate-500">Tady je přehled úkolů týmu pro tento týden.</p>
        </div>

        <ActualTasksTable />
    </div>
</template>
<script setup>
import { computed } from 'vue';
import ActualTasksTable from '../components/ActualTasksTable.vue';

const formattedDate = computed(() => {
    return new Date().toLocaleDateString('cs-CZ', {
        weekday: 'long',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
});
</script>
<style lang="">

</style>
