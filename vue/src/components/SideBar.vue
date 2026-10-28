<template>
    <!-- Mobile top bar -->
    <div
        class="sm:hidden fixed top-0 left-0 right-0 z-40 flex items-center justify-between px-4 h-14 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
        <div class="flex items-center gap-2">
            <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
                <IconLayoutKanban :size="18" stroke="2" />
            </div>
            <span class="font-bold text-slate-900 dark:text-slate-100 tracking-tight">TaskHub</span>
        </div>
        <div class="flex items-center gap-1">
            <ThemeToggle />
            <button type="button"
                class="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/60 transition-colors"
                @click="toggleSidebar()">
                <IconMenu2 :size="20" />
            </button>
        </div>
    </div>

    <!-- Mobile backdrop -->
    <div v-if="sidebarOpened" class="sm:hidden fixed inset-0 z-40 bg-slate-900/40 dark:bg-black/60 backdrop-blur-[1px]"
        @click="toggleSidebar()"></div>

    <aside :class="[
        'fixed top-0 left-0 w-72 h-full transition-transform duration-200 ease-out z-50 flex flex-col',
        sidebarOpened ? 'translate-x-0' : '-translate-x-full',
        'sm:translate-x-0'
    ]">
        <div class="h-full px-4 py-5 overflow-y-auto flex flex-col flex-1 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700">

            <div class="flex items-center justify-between mb-8 px-2">
                <div class="flex items-center gap-2.5">
                    <div
                        class="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm shadow-blue-600/30">
                        <IconLayoutKanban :size="20" stroke="2" />
                    </div>
                    <span class="text-lg font-bold text-slate-900 dark:text-slate-100 tracking-tight">TaskHub</span>
                </div>
                <div class="flex items-center gap-1">
                    <ThemeToggle class="hidden sm:flex" />
                    <button type="button"
                        class="sm:hidden flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700/60 transition-colors"
                        @click="toggleSidebar()">
                        <IconX :size="18" />
                    </button>
                </div>
            </div>

            <nav class="flex flex-col flex-grow gap-1">
                <p class="px-3 mb-1 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Menu</p>

                <router-link :to="{ path: '/' }" class="nav-link" active-class="nav-link-active" exact>
                    <IconLayoutDashboard :size="19" stroke="1.8" />
                    <span>Nástěnka</span>
                </router-link>

                <router-link v-if="selectedTeam" :to="{ path: '/team' + (selectedTeam ? '/' + selectedTeam : '') }"
                    class="nav-link" active-class="nav-link-active">
                    <IconUsersGroup :size="19" stroke="1.8" />
                    <span>Management týmu</span>
                </router-link>

                <router-link v-if="selectedTeam" :to="{ path: `/team/${selectedTeam}/task-organizator` }"
                    class="nav-link" active-class="nav-link-active">
                    <IconListCheck :size="19" stroke="1.8" />
                    <span>Organizace úkolů</span>
                </router-link>

                <router-link :to="{ path: '/profile' }" class="nav-link" active-class="nav-link-active">
                    <IconUserCircle :size="19" stroke="1.8" />
                    <span>Můj účet</span>
                </router-link>

                <router-link v-if="!mainStore.demoUser" :to="{ path: '/add-team' }" class="nav-link"
                    active-class="nav-link-active">
                    <IconPlus :size="19" stroke="1.8" />
                    <span>Vytvořit nový tým</span>
                </router-link>
            </nav>

            <div class="mt-6 px-1">
                <label for="team"
                    class="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 px-2">
                    Aktivní tým
                </label>
                <div v-if="loading" class="px-2 text-sm text-slate-400">Načítání…</div>
                <div v-else class="relative">
                    <select id="team" class="team-select w-full appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 pl-3.5 pr-9 py-2.5 transition-colors"
                        v-model="selectedTeam" @change="selectTeam()">
                        <option disabled :value="null">Vyberte tým...</option>
                        <option v-for="team in availableTeams" :key="team.id" :value="team.id">{{ team.name }}</option>
                    </select>
                    <IconChevronDown :size="16"
                        class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" />
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800">
                <div class="flex items-center gap-3 px-2 mb-3">
                    <div
                        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-blue-100 dark:bg-blue-500/20 text-blue-700 dark:text-blue-300 text-sm font-bold uppercase">
                        {{ userInitials }}
                    </div>
                    <div class="min-w-0">
                        <p class="text-sm font-semibold text-slate-800 dark:text-slate-100 truncate">{{ mainStore.user?.username ||
                            'Uživatel' }}</p>
                        <p class="text-xs text-slate-400 truncate">{{ mainStore.user?.email || '' }}</p>
                    </div>
                </div>
                <button @click="logout"
                    class="w-full flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-semibold text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700/60 hover:text-red-600 dark:hover:text-red-400 rounded-xl transition-colors">
                    <IconLogout :size="17" stroke="1.8" />
                    <span>Odhlásit se</span>
                </button>
            </div>

        </div>
    </aside>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue';
import { useMainStore } from '../store';
import {
    IconLayoutKanban,
    IconLayoutDashboard,
    IconUserCircle,
    IconUsersGroup,
    IconListCheck,
    IconPlus,
    IconChevronDown,
    IconLogout,
    IconMenu2,
    IconX,
} from '@tabler/icons-vue';
import ThemeToggle from './ThemeToggle.vue';

const sidebarOpened = ref(false); // Controls visibility on mobile
const availableTeams = ref([]);
const selectedTeam = ref(null);
const loading = ref(false)

const mainStore = useMainStore();

const userInitials = computed(() => {
    const name = mainStore.user?.username || '';
    return name.slice(0, 2) || '??';
});

onMounted(() => {
    loading.value = true
    loadData();
    loading.value = false
});

const toggleSidebar = () => {
    sidebarOpened.value = !sidebarOpened.value;
};

const logout = () => {
    mainStore.api.post('/auth/logout/', {}).then(() => {
        window.location.href = '/login';
        mainStore.setUser(null);
        mainStore.setSelectedTeam(null);
    });
}
const loadData = async () => {
    mainStore.api.get('/available_user_teams/').then((response) => {
        availableTeams.value = response.data.teams;
    });
    mainStore.api.get(`/profile/${mainStore.user.id}/`).then((response) => {
        mainStore.setSelectedTeam(response.data.user?.selected_team || null)
        mainStore.setDemoUser(response.data.user?.demo || null)
        selectedTeam.value = mainStore.selectedTeam
    });
}

const selectTeam = () => {
    mainStore.api.post('/profile/set_user_profile/', { team: selectedTeam.value }).then((response) => {
        mainStore.setSelectedTeam(selectedTeam.value);
        window.location.reload();
    });
}

</script>

<style scoped>
.team-select {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    background-image: none;
}

.team-select::-ms-expand {
    display: none;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.6rem 0.75rem;
    border-radius: 0.65rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: #475569;
    transition: background-color 0.15s ease, color 0.15s ease;
}

.nav-link:hover {
    background-color: #f1f5f9;
    color: #1e293b;
}

.nav-link-active {
    background-color: #eff6ff;
    color: #2563eb;
    font-weight: 600;
}

.dark .nav-link {
    color: #94a3b8;
}

.dark .nav-link:hover {
    background-color: #1e293b;
    color: #f1f5f9;
}

.dark .nav-link-active {
    background-color: rgb(59 130 246 / 0.15);
    color: #93c5fd;
}
</style>
