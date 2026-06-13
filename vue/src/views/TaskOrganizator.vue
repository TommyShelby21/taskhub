<template>
    <div>
        <h1 style="font-size: 26px; font-weight: 700;">Organizace úkolů v týmu</h1>
    </div>
    <div class="mt-4">
        <div class="flex">
            <h2 class="me-5" style="font-size: 20px; font-weight: 500;">Aktuální úkoly:</h2>
            <button class="btn btn_main" @click="openTaskModal">Přidat úkol</button>
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
                        <label class="block text-sm font-medium text-slate-700">Přiřadit členy</label>
                        <select
                            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 mt-1"
                            multiple v-model="addTask.users">
                            <option v-for="member in teamMembers" :key="member.id" :value="member.id">{{ member.user.username }}</option>
                        </select>
                    </div>
                </div>
            </template>
        </Modal>
        <div class="flex gap-5 mt-3">
            <div v-for="task in teamTasks" :key="task.id">
                <Task :task="task" @draggedTaskId="(id) => draggedTaskId = id" @deleteTask="loadTasks" />
            </div>
        </div>
        <!-- Assign members to task Modal -->
        <Modal v-if="openedTaskDetail" @close="openedTaskDetail = false" :title="'Detail úkolu'"
            @submit="assignMembers()" :submitButton="true">
            <template #next-header>
                <div class="flex cursor-pointer btn btn_main justify-center items-center"
                    @click="addingMembers = !addingMembers">
                    <IconPlus stroke={2} class="me-2" />
                    <span>Přiřadit členy</span>
                </div>
            </template>
            <template #modal-content>
                <div class="grid gap-4">
                    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <div v-if="openedTask.team_members.length > 0" v-for="team_member in openedTask.team_members"
                            :key="team_member.id" class="col-span-1 flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                            <IconUserCircle stroke={2} class="w-10 h-10 text-slate-600" />
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
        <div class="mt-5">
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
import { IconUserCircle } from '@tabler/icons-vue';
import { IconPlus } from '@tabler/icons-vue';
import Multiselect from 'vue-multiselect'

const mainStore = useMainStore();
const route = useRoute();

onMounted(() => {
    loadTasks()
})

const draggedTaskId = ref(null);

// Load Tasks
const teamTasks = ref([])
function loadTasks() {
    mainStore.api.get(`/team/${route.params.id}/tasks`).then((response) => {
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
function submitNewTask() {
    mainStore.api.post(`/team/${route.params.id}/tasks/add/`, addTask.value).then((response) => {
        loadTasks()
        openedTaskModal.value = false;
        addTask.value = {
            name: '',
            description: '',
            users: []
        }
    })
}

// Load Team Members
const teamMembers = ref([])
onMounted(() => {
    mainStore.api.get(`/team/${route.params.id}/members`).then((response) => {
        teamMembers.value = response.data.members;
    });
})
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
    mainStore.api.post(`/team/${route.params.id}/tasks/assign`, payload).then((response) => {
        loadTasks()
        addingMembers.value = false
    })
}


</script>
<style scoped></style>