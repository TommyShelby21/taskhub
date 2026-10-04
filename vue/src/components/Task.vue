<template>
    <div class="flex text-white font-semibold cursor-grab task"
        :class="fill ? 'h-full flex-col px-3 py-1.5 rounded-xl overflow-hidden' : 'items-center px-4 py-2 rounded-4xl'"
        draggable="true" @dragstart="onDragStart(task.id)" @dragend="emit('draggedTaskId', null)">
        <div class="flex items-center min-w-0">
            <span class="me-2 h-2.5 w-2.5 shrink-0 rounded-full ring-2 ring-white/70" :class="priority.dotClass"
                :title="`Priorita: ${priority.label}`"></span>
            <span class="me-2 text-white truncate">{{ task.name }}</span>
            <IconInfoCircleFilled class="cursor-pointer shrink-0" @click="openDetail"
                style="width: 20px; height: 20px;" />
        </div>
        <span v-if="subtitle" class="text-xs font-medium text-white/80">{{ subtitle }}</span>
    </div>
    <Modal v-if="openedTaskDetail" @close="openedTaskDetail = false" @delete="deleteTask(task.id)" @submit="saveTask"
        :title="'Detail úkolu'" :deleteButton="true" :submitButton="true">
        <template #modal-content>
            <div class="flex flex-col gap-4">
                <div class="space-y-2">
                    <label class="block text-sm font-semibold text-slate-700">Název</label>
                    <input type="text" v-model="editedName" placeholder="Název úkolu"
                        class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200" />
                </div>
                <div class="space-y-2">
                    <label class="block text-sm font-semibold text-slate-700">Popis</label>
                    <textarea v-model="editedDescription" rows="4" placeholder="Popis úkolu"
                        class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 shadow-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 resize-none"></textarea>
                </div>
                <div class="space-y-2">
                    <label class="block text-sm font-semibold text-slate-700">Priorita</label>
                    <div class="flex gap-2">
                        <button v-for="option in PRIORITIES" :key="option.value" type="button"
                            @click="editedPriority = option.value"
                            class="flex flex-1 items-center justify-center gap-2 rounded-2xl border px-3 py-2 text-sm font-medium transition"
                            :class="editedPriority === option.value
                                ? 'border-slate-400 bg-slate-100 text-slate-900 ring-2 ring-slate-200'
                                : 'border-slate-200 bg-slate-50 text-slate-500 hover:bg-slate-100'">
                            <span class="h-2.5 w-2.5 rounded-full" :class="option.dotClass"></span>
                            {{ option.label }}
                        </button>
                    </div>
                </div>
                <div class="space-y-2">
                    <label class="block text-sm font-semibold text-slate-700">Členové</label>
                    <multiselect v-model="editedMembers" :options="memberOptions" :multiple="true"
                        :close-on-select="false" :clear-on-select="false" :preserve-search="true"
                        track-by="id" label="label" placeholder="Vyhledejte a vyberte členy"
                        select-label="" selected-label="" deselect-label="Odebrat"
                        :loading="loadingMembers" class="custom-multiselect w-full">
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
                <div class="flex flex-wrap items-center gap-x-4 gap-y-1 pt-2 border-t border-slate-100 text-xs text-slate-400">
                    <span v-if="task.created_by" class="flex items-center gap-1">
                        <IconUserCircle :size="14" />
                        Vytvořil: <span class="font-medium text-slate-500">{{ task.created_by.username }}</span>
                    </span>
                    <span v-if="task.created_at" class="flex items-center gap-1">
                        <IconClock :size="14" />
                        {{ formattedCreatedAt }}
                    </span>
                </div>
            </div>
        </template>
    </Modal>
</template>
<script setup>
import { ref, computed, defineEmits } from 'vue';
import { IconInfoCircleFilled, IconUserCircle, IconClock } from '@tabler/icons-vue';
import Modal from '../components/Modal.vue';
import { useMainStore } from '../store';
import { useRoute } from 'vue-router';
import { PRIORITIES, getPriority } from '../priorities';
import Multiselect from 'vue-multiselect';

const mainStore = useMainStore();
const route = useRoute();

const props = defineProps({
    task: {
        type: Object,
        required: true
    },
    // Stretch to fill the parent (used for multi-hour blocks in the calendar)
    fill: {
        type: Boolean,
        default: false
    },
    subtitle: {
        type: String,
        default: ''
    }
});

const emit = defineEmits(['draggedTaskId', 'deleteTask', 'taskUpdated']);

const draggedTaskId = ref(null);
function onDragStart(taskId) {
    draggedTaskId.value = taskId;
    emit('draggedTaskId', taskId);
}

// Open Task
const openedTaskDetail = ref(false)
const editedName = ref('')
const editedDescription = ref('')
const editedPriority = ref('')

const editedMembers = ref([])

// Team members are loaded when the detail opens; ids are TeamMember ids
const teamMembers = ref([])
const loadingMembers = ref(false)
const memberOptions = computed(() => teamMembers.value.map(member => ({
    id: member.id,
    label: member.user.username
})))

function loadMembers() {
    loadingMembers.value = true
    return mainStore.api.get(`/team/${route.params.id}/members/`)
        .then((response) => {
            teamMembers.value = response.data.members
        })
        .catch((error) => {
            console.error('Loading team members failed', error)
        })
        .finally(() => {
            loadingMembers.value = false
        })
}

const priority = computed(() => getPriority(props.task.priority))

function openDetail() {
    editedName.value = props.task.name
    editedDescription.value = props.task.description
    editedPriority.value = priority.value.value
    editedMembers.value = []
    loadMembers().then(() => {
        const assignedIds = props.task.team_members ?? []
        editedMembers.value = memberOptions.value.filter(option => assignedIds.includes(option.id))
    })
    openedTaskDetail.value = true
}

const formattedCreatedAt = computed(() => {
    if (!props.task.created_at) return ''
    return new Date(props.task.created_at).toLocaleDateString('cs-CZ', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
})

const saveTask = () => {
    mainStore.api.put(`/team/${route.params.id}/task/update/`, {
        taskId: props.task.id,
        name: editedName.value,
        description: editedDescription.value,
        priority: editedPriority.value,
        users: editedMembers.value.map(member => member.id)
    })
        .then(() => {
            openedTaskDetail.value = false
            emit('taskUpdated')
        })
        .catch((error) => {
            console.error('Task update failed', error)
        })
}

const deleteTask = (taskId) => {
    mainStore.api.put(`/team/${route.params.id}/task/delete/`, { taskId })
        .then(() => {
            openedTaskDetail.value = false
            emit('deleteTask')
        })
        .catch((error) => {
            console.error('Task delete failed', error)
        })
}

</script>
<style scoped>
.task {
    background-color: var(--main-color);
}
</style>
