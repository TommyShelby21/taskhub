<template>
    <div class="main_div">
        <div>
            <h1 style="font-size: 26px; font-weight: 700;">Management týmu</h1>
        </div>
        <div class="mt-10">
            <div>
                <h2 style="font-size: 20px; font-weight: 500;">Členové týmu:</h2>
                <div class="mt-5">
                    <table class="table-auto border-collapse border border-gray-300 w-full">
                        <thead>
                            <tr>
                                <th class="py-2 border-b border-gray-300 text-center">Jméno</th>
                                <th class="py-2 border-b border-gray-300 text-center">Správce</th>
                                <th class="py-2 border-b border-gray-300 text-center"></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="member in teamMembers" :key="member.id">
                                <td class="py-2 border-b border-gray-300 text-center">{{ member.user.username }}</td>
                                <td class="py-2 border-b border-gray-300 text-center">{{ member.leader ? 'Ano' : 'Ne' }}
                                </td>
                                <td class="py-2 border-b border-gray-300 text-center">
                                    <button type="button" class="btn" @click="deleteMember(member)">
                                        <IconXboxX stroke={2} style="color: red; height: 30px; width: 30px" />
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useMainStore } from '../store'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { IconXboxX } from '@tabler/icons-vue';

const route = useRoute();
const mainStore = useMainStore();

onMounted(() => {
    loadTeamMembers()
    loadTeam()
})

const selectedTeam = ref(null)
const teamMembers = ref([])
const loadTeamMembers = () => {
    mainStore.api.get(`/team/${route.params.id}/members`).then((response) => {
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
    console.log(selectedTeam.value)
}

</script>

<style scoped></style>