<template>
    <button v-if="!sidebarOpened" type="button" class="sm:hidden m-2 bg-blue-500 px-5 py-2 text-white rounded-4xl"
        @click="toggleSidebar()">
        <span>Otevrit sidebar</span>
    </button>

    <aside :class="[
        'fixed top-0 left-0 w-64 h-full transition-transform z-50 flex flex-col',
        sidebarOpened ? 'translate-x-0' : '-translate-x-full',
        'sm:translate-x-0' // Always open on sm and up
    ]">
        <div class="h-full px-4 py-6 overflow-y-auto flex flex-col flex-1 sidebar bg-white">
            <div class="mb-8 px-2">
                <h1 class="text-xl font-bold text-blue-600 tracking-tight">TaskHub</h1>
            </div>
            <ul class="flex flex-col flex-grow gap-1">
                <li>
                    <router-link :to="{ path: '/' }" class="flex items-center p-2.5 rounded-lg link transition-colors">
                        <span class="ms-3">Nástěnka</span>
                    </router-link>
                </li>
                <li>
                    <router-link :to="{ path: '/profile' }"
                        class="flex items-center p-2.5 rounded-lg link transition-colors">
                        <span class="ms-3">Můj účet</span>
                    </router-link>
                </li>
                <li v-if="selectedTeam">
                    <router-link :to="{ path: '/team' + (selectedTeam ? '/' + selectedTeam : '') }"
                        class="flex items-center p-2.5 rounded-lg link transition-colors">
                        <span class="ms-3">Management týmu</span>
                    </router-link>
                </li>
                <li v-if="selectedTeam">
                    <router-link :to="{ path: `/team/${selectedTeam}/task-organizator` }"
                        class="flex items-center p-2.5 rounded-lg link transition-colors">
                        <span class="ms-3">Organizace úkolů</span>
                    </router-link>
                </li>
                <li v-if="mainStore.demoUser">
                    <router-link :to="{ path: '/add-team' }"
                        class="flex items-center p-2.5 rounded-lg link transition-colors">
                        <span class="ms-3">Vytvořit nový tým</span>
                    </router-link>
                </li>

                <li v-if="sidebarOpened">
                    <button @click="toggleSidebar" class="bg-blue-500 px-5 py-2 rounded-4xl">
                        Zavřít sidebar
                    </button>
                </li>
            </ul>
            <div class="mb-6 px-2">
                <label for="team"
                    class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Vyberte tým</label>
                <select
                    class="w-full bg-slate-50 border border-slate-200 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5"
                    v-model="selectedTeam" @change="selectTeam()">
                    <option disabled value="null">Vyberte tým...</option>
                    <option v-for="team in availableTeams" :key="team.id" :value="team.id">{{ team.name }}</option>
                </select>
            </div>

            <div class="mt-auto pt-4 border-t border-slate-100">
                <button @click="logout"
                    class="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
                    <span>Odhlásit se</span>
                </button>
            </div>

        </div>
    </aside>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue';
import { useMainStore } from '../store';

const sidebarOpened = ref(false); // Controls visibility on mobile
const availableTeams = ref([]);
const selectedTeam = ref(null);

const mainStore = useMainStore();

onMounted(() => {
    selectedTeam.value = mainStore.selectedTeam
});

const toggleSidebar = () => {
    sidebarOpened.value = !sidebarOpened.value;
};

const logout = () => {
    mainStore.api.post('/api/logout/', {}).then(() => {
        window.location.href = '/login';
        mainStore.setUser(null);
        mainStore.setSelectedTeam(null);
    });
}
const loadData = async () => {
    mainStore.api.get('/available_user_teams/').then((response) => {
        availableTeams.value = response.data.teams;
    });
    mainStore.api.get(`/user/${mainStore.user.id}/`).then((response) => {
        mainStore.setSelectedTeam(response.data.user?.selected_team || null)
        mainStore.setDemoUser(response.data.user?.demo || null)
    });
}

const selectTeam = () => {
    mainStore.api.post('/profile/set_user_profile/', { team: selectedTeam.value }).then((response) => {
        console.log("Nastaven vybraný tým:", selectedTeam.value);
        mainStore.setSelectedTeam(selectedTeam.value);
        window.location.reload();
    });
}

watch(() => mainStore.user, (newUser) => {
    if (newUser) {
        loadData();
    }
}, { immediate: true }
);

</script>

<style scoped>
.sidebar {
    color: var(--text-color);
    font-weight: 500;
}

.link {
    color: #64748b;
}

.link:hover,
.router-link-active {
    color: #2563eb;
    background-color: #eff6ff;
}

.router-link-active {
    font-weight: 600;
}
</style>