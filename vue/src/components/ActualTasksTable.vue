<template>
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 mt-6">
        <div class="flex items-center gap-3 current_time_div shadow-sm border border-blue-100">
            <span class="text-blue-700">{{ formattedCurrentDate }}</span>
        </div>
        <div class="flex items-center gap-2">
            <button class="btn btn_secondary hover:bg-slate-200 transition-colors" @click="previousWeek">
                <span class="text-xl">‹</span>
            </button>
            <button class="btn btn_secondary hover:bg-slate-200 transition-colors" @click="nextWeek">
                <span class="text-xl">›</span>
            </button>
        </div>
    </div>
    <div class="h-[700px] overflow-x-auto overflow-y-auto rounded-xl border border-slate-200 shadow-sm bg-white">
        <table class="table-fixed w-full border-collapse">
            <thead class="sticky top-0 z-20 bg-slate-50 border-b border-slate-200">
                <tr>
                    <th
                        class="w-20 px-4 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider bg-slate-50 border-r border-slate-200">
                        Čas</th>
                    <th class="px-4 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider border-r border-slate-200 last:border-r-0"
                        v-for="day in weekDays" :key="day">{{ day.label }}</th>
                </tr>
            </thead>
            <tbody class="text-sm">
                <tr v-for="hour in hours" :key="hour" class="border-b border-slate-100 last:border-0">
                    <td class="px-2 py-3 font-medium bg-slate-50 text-slate-600 text-center border-r border-slate-200">
                        {{ hour }}</td>
                    <td v-for="day in weekDays" :key="day.index"
                        class="px-2 py-4 hover:bg-blue-50/50 cursor-pointer border-r border-slate-100 last:border-r-0 transition-colors"
                        @dragover.prevent @drop="onDrop(day, hour)">

                        <div v-for="task in tasksForCell(day.index, hour)" :key="task.id" class="mb-1 last:mb-0">
                            <Task :task="task.task" draggable="true" @dragstart="onDragStart(task.task.id)"
                                @deleteTask="handleTaskDelete" />
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

</template>
<script setup>
import { ref, computed, watch } from 'vue'
import { useMainStore } from '../store'
import { useRoute } from 'vue-router'
import Task from '../components/Task.vue';

const mainStore = useMainStore()
const route = useRoute()

const emit = defineEmits(['clearDraggedTaskId', 'onDragStart', 'deleteTask'])

const props = defineProps({
    draggedTaskId: Number,
    teamTasks: Array
})

// Update current date
const currentDate = ref(new Date())
const assignedTasks = ref([])


watch(
    () => mainStore.selectedTeam,
    (newTeam) => {
        if (newTeam) {
            loadData()
        }
    },
    { immediate: true }
)

function loadData() {
    if (mainStore.selectedTeam) {
        mainStore.api.get(`/team/${mainStore.selectedTeam}/assigned_tasks`)
            .then((response) => {
                assignedTasks.value = response.data.assigned_tasks.filter(at => !at.task.is_hidden);
            })
    }
}

const formattedCurrentDate = computed(() => {
    return currentDate.value.toLocaleDateString('cs-CZ', {
        weekday: 'long',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
})


function nextWeek() {
    const newDate = new Date(currentDate.value)
    newDate.setDate(newDate.getDate() + 7)
    currentDate.value = newDate
    loadData()
}

function previousWeek() {
    const newDate = new Date(currentDate.value)
    newDate.setDate(newDate.getDate() - 7)
    currentDate.value = newDate
    loadData()
}

// Get the Monday of the current week
function getStartOfWeek(date) {
    const day = date.getDay() || 7 // Sunday=0 becomes 7
    const monday = new Date(date)
    monday.setDate(date.getDate() - day + 1)
    return monday
}

const weekDays = computed(() => {
    const start = getStartOfWeek(currentDate.value)
    const days = []

    for (let i = 0; i < 7; i++) {
        const d = new Date(start)
        d.setDate(start.getDate() + i)

        const label = d.toLocaleDateString('cs-CZ', {
            weekday: 'long',
            day: '2-digit',
            month: '2-digit'
        })

        days.push({
            date: d,
            label,
            index: i + 1 // matches 1 = Monday, 7 = Sunday
        })
    }

    return days
})

const hours = ref([
    '00:00', '01:00', '02:00', '03:00', '04:00',
    '05:00', '06:00', '07:00',
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00',
    '18:00', '19:00', '20:00', '21:00', '22:00',
    '23:00', '24:00'
]);

function onDrop(day, hour) {
    saveTaskChanges(day, hour, props.draggedTaskId);

    // clear the draggedTaskId
    emit('clearDraggedTaskId');
}

function handleTaskDelete() {
    loadData()
    emit('deleteTask')
}

function tasksForCell(day, hour) {
    const startOfWeek = getStartOfWeek(currentDate.value)
    const endOfWeek = new Date(startOfWeek)
    endOfWeek.setDate(endOfWeek.getDate() + 6)

    return assignedTasks.value.filter(task => {
        const taskDate = new Date(task.datetime)

        // pouze pokud je task v aktuálním týdnu
        if (taskDate < startOfWeek || taskDate > endOfWeek) return false

        const taskDay = taskDate.getUTCDay() === 0 ? 7 : taskDate.getUTCDay() // Sunday = 7
        const taskHour = taskDate.getUTCHours().toString().padStart(2, '0') + ':00'

        return taskDay === day && taskHour === hour
    })
}

const saveTaskChanges = (day, hour, taskId) => {
    const correct_datetime = `${day.date.getFullYear()}-${day.date.getMonth() + 1}-${day.date.getDate()} ${hour}:00`
    const postData = {
        datetime: correct_datetime,
        taskId: taskId
    }
    mainStore.api.put(`/team/${route.params.id}/tasks/update/`, postData).then((response) => {
        loadData()
    })
}

const onDragStart = (taskId) => {
    emit('onDragStart', taskId)
}

</script>
<style scoped>
.current_time_div {
    background-color: #eff6ff;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.75rem 1.25rem;
    border-radius: 0.75rem;
}
</style>