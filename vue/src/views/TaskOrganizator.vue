<template>
    <div>
        <div class="flex flex-col gap-1 mb-6">
            <p class="text-sm font-semibold text-blue-600 uppercase tracking-wider">Tým</p>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Organizace úkolů</h1>
            <p class="text-sm text-slate-500">Vytvářejte úkoly a přetahujte je do plánu týdne.</p>
        </div>

        <div class="rounded-3xl bg-white border border-slate-200 shadow-sm p-6 mb-6">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-base font-bold text-slate-800">Backlog úkolů</h2>
                <button class="btn btn_main" @click="openTaskModal">
                    <IconPlus :size="18" stroke="2" />
                    Přidat úkol
                </button>
            </div>

            <div v-if="teamTasks.length > 0" class="flex flex-wrap gap-3">
                <Task v-for="task in teamTasks" :key="task.id" :task="task"
                    @draggedTaskId="(id) => draggedTaskId = id" @deleteTask="loadTasks" @taskUpdated="loadTasks" />
            </div>
            <div v-else class="rounded-2xl border border-dashed border-slate-200 bg-slate-50/60 px-6 py-10 text-center text-sm text-slate-400">
                Zatím žádné úkoly. Přidejte první pomocí tlačítka výše.
            </div>
        </div>

        <!-- Add task Modal -->
        <Modal v-if="openedTaskModal" @close="openedTaskModal = false" @submit="submitNewTask" :title="'Přidat úkol'" :submitButton="true">
            <template #modal-content>
                <div class="grid gap-4">
                    <div>
                        <label for="name" class="block text-sm font-medium text-slate-700">Název:</label>
                        <input type="text" placeholder="Zadejte název úkolu"
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 mt-1"
                            v-model="addTask.name">
                    </div>
                    <div>
                        <label for="description" class="block text-sm font-medium text-slate-700">Popis:</label>
                        <input type="text" placeholder="Zadejte popis úkolu"
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 mt-1"
                            v-model="addTask.description">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700">Priorita:</label>
                        <div class="flex gap-2 mt-1">
                            <button v-for="option in PRIORITIES" :key="option.value" type="button"
                                @click="addTask.priority = option.value"
                                class="flex flex-1 items-center justify-center gap-2 rounded-2xl border px-3 py-2.5 text-sm font-medium transition"
                                :class="addTask.priority === option.value
                                    ? 'border-slate-400 bg-slate-100 text-slate-900 ring-2 ring-slate-200'
                                    : 'border-slate-200 bg-slate-50 text-slate-500 hover:bg-slate-100'">
                                <span class="h-2.5 w-2.5 rounded-full" :class="option.dotClass"></span>
                                {{ option.label }}
                            </button>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700">Přiřadit členy</label>
                        <multiselect v-model="addTaskMembers" :options="memberOptions" :multiple="true"
                            :close-on-select="false" :clear-on-select="false" :preserve-search="true"
                            track-by="id" label="label" placeholder="Vyhledejte a vyberte členy"
                            select-label="" selected-label="" deselect-label="Odebrat"
                            class="custom-multiselect w-full mt-1">
                            <template #option="{ option }">
                                <div class="flex items-center gap-2">
                                    <IconUserCircle :size="20" stroke="1.8" class="text-slate-400" />
                                    <span>{{ option.label }}</span>
                                </div>
                            </template>
                            <template #noResult>Žádný člen neodpovídá hledání.</template>
                            <template #noOptions>Tým nemá žádné členy.</template>
                        </multiselect>
                    </div>
                </div>
            </template>
        </Modal>

        <!-- Assign members to task Modal -->
        <Modal v-if="openedTaskDetail" @close="openedTaskDetail = false" :title="'Detail úkolu'"
            @submit="assignMembers()" :submitButton="true">
            <template #next-header>
                <div class="flex cursor-pointer btn btn_main justify-center items-center"
                    @click="addingMembers = !addingMembers">
                    <IconPlus :size="18" stroke="2" class="me-2" />
                    <span>Přiřadit členy</span>
                </div>
            </template>
            <template #modal-content>
                <div class="grid gap-4">
                    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div v-if="openedTask.team_members.length > 0" v-for="team_member in openedTask.team_members"
                            :key="team_member.id" class="col-span-1 flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                            <IconUserCircle :size="32" stroke="1.8" class="text-slate-600" />
                            <span class="font-medium text-slate-700">{{ team_member.user.username }}</span>
                        </div>
                        <div v-else class="col-span-1 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                            <span class="text-slate-500">Žádní členové nejsou přiřazeni.</span>
                        </div>
                        <div v-if="addingMembers" class="mb-4 w-full">
                            <multiselect v-model="assignedTeamMembers" :options="processedTeamMembers" :multiple="true"
                                :close-on-select="false" :preserve-search="true" track-by="id" label="label"
                                placeholder="Vyberte členy týmu" select-label="Vybrat" deselect-label="Odstranit"
                                class="custom-multiselect w-full">
                            </multiselect>
                        </div>
                    </div>
                    <div>
                        <span class="block text-xl font-semibold text-slate-900">{{ openedTask.name }}</span>
                        <p class="mt-2 text-slate-600">{{ openedTask.description }}</p>
                    </div>
                </div>
            </template>
        </Modal>

        <div class="rounded-3xl bg-white border border-slate-200 shadow-sm p-6">
            <ActualTasksTable :draggedTaskId="draggedTaskId" :teamTasks="teamTasks"
                @clearDraggedTaskId="draggedTaskId = null" @onDragStart="(id) => draggedTaskId = id" @deleteTask="loadTasks" />
        </div>
    </div>

</template>
<script setup>
import { computed, ref } from 'vue';
import { useMainStore } from '../store';
import { onMounted } from 'vue'
import { useRoute } from 'vue-router';
import Modal from '../components/Modal.vue';
import ActualTasksTable from '../components/ActualTasksTable.vue';
import Task from '../components/Task.vue';
import { IconUserCircle, IconPlus } from '@tabler/icons-vue';
import Multiselect from 'vue-multiselect'
import { PRIORITIES, DEFAULT_PRIORITY } from '../priorities';

const mainStore = useMainStore();
const route = useRoute();

onMounted(() => {
    loadTasks()
})

const draggedTaskId = ref(null);

// Load Tasks
const teamTasks = ref([])
function loadTasks() {
    mainStore.api.get(`/team/${route.params.id}/tasks/`).then((response) => {
        teamTasks.value = response.data.tasks.filter(t => !t.is_hidden)
    });
}

// Open Task
const openedTaskModal = ref(false)
function openTaskModal() {
    openedTaskModal.value = true
}

const openedTaskDetail = ref(false)
const openedTask = ref({})
const openTaskDetail = (taskId) => {
    openedTask.value = teamTasks.value.find(task => task.id === taskId)
    openedTaskDetail.value = true
}

// Add Task
const addTask = ref({
    name: '',
    description: '',
    users: []
})
const addTaskMembers = ref([])
function submitNewTask() {
    const payload = { ...addTask.value, users: addTaskMembers.value.map(member => member.id) }
    mainStore.api.post(`/team/${route.params.id}/tasks/add/`, payload).then((response) => {
        loadTasks()
        openedTaskModal.value = false;
        addTask.value = {
            name: '',
            description: '',
            priority: DEFAULT_PRIORITY,
            users: []
        }
        addTaskMembers.value = []
    })
}

// Load Team Members
const teamMembers = ref([])
onMounted(() => {
    mainStore.api.get(`/team/${route.params.id}/members/`).then((response) => {
        teamMembers.value = response.data.members;
    });
})
// Options for the add-task form use TeamMember ids, which the backend expects
const memberOptions = computed(() => teamMembers.value.map(member => ({
    id: member.id,
    label: member.user.username
})))
const processedTeamMembers = computed(() => {
    return teamMembers.value.map(member => ({
        ...member,
        id: member.user.id,
        label: member.user.username
    }))
})

// Add Members to Task
const addingMembers = ref(false)
const assignedTeamMembers = ref([])
const assignMembers = () => {
    let payload = {
        taskId: openedTask.value.id,
        teamMembers: assignedTeamMembers.value.map(member => member.id)
    }
    mainStore.api.post(`/team/${route.params.id}/tasks/assign/`, payload).then((response) => {
        loadTasks()
        addingMembers.value = false
    })
}


</script>
