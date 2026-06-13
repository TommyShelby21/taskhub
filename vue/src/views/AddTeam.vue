<template>
    <div class="relative min-h-[calc(100vh-2rem)] bg-gradient-to-br from-slate-100 via-white to-slate-200">
        <div class="flex h-full box-border items-center justify-center px-4 py-8">
            <main
                class="w-full max-w-2xl rounded-[2rem] bg-white p-8 shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] ring-1 ring-slate-200 sm:p-10">
                <div class="mb-8">
                    <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">Tým</p>
                    <h2 class="mt-4 text-3xl font-extrabold text-slate-950 sm:text-4xl">Vytvořit nový tým</h2>
                    <p class="mt-3 text-sm leading-6 text-slate-600 sm:text-base">
                        Zadejte název týmu a vytvořte nové pracovní prostředí.
                    </p>
                </div>

                <div class="space-y-6">
                    <div v-if="success"
                        class="rounded-2xl bg-emerald-50 p-4 text-center text-sm text-emerald-700 ring-1 ring-emerald-200">
                        Tým byl úspěšně vytvořen
                    </div>

                    <div class="space-y-4">
                        <div class="space-y-2">
                            <label class="block text-sm font-semibold text-slate-700">Název týmu</label>
                            <input type="text" placeholder="Zadejte název týmu"
                                class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
                                v-model="teamName" />
                        </div>
                        <button class="btn btn_main w-full rounded-2xl px-5 py-3 text-base" @click="createTeam()">
                            Vytvořit tým
                        </button>
                    </div>
                </div>
            </main>
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
<style scoped>
.add_team {
    padding: 2rem;
    background-color: var(--main-color);
    color: var(--white);
    border-radius: 32px;
}

.form {
    background-color: var(--secondary-color);
    max-width: 700px;
    padding: 1rem;
    border-radius: 32px;
}

label {
    font-weight: 600;
    margin-bottom: 0.4rem;
    opacity: 0.7;
}

input {
    background-color: var(--secondary-color);
    color: var(--black);
    border-radius: 32px;
    padding: 0.5rem 1rem;
    min-height: 44px;
}

input::placeholder {
    font-size: 14px;
}

/* Root */
::v-deep(.custom-multiselect.multiselect) {
    background-color: #000;
    color: #fff;
    border-radius: 32px;
}

/* Control / input area */
::v-deep(.custom-multiselect .multiselect__tags) {
    background-color: #000;
    border: 1px solid #333;
    border-radius: 32px;
    min-height: 44px;
}

/* Placeholder */
::v-deep(.custom-multiselect .multiselect__placeholder) {
    color: #aaa;
}

/* Input text */
::v-deep(.custom-multiselect .multiselect__input) {
    background-color: #000;
    color: #fff;
}

/* Selected single label */
::v-deep(.custom-multiselect .multiselect__single) {
    background-color: #000;
    color: #fff;
}

/* Dropdown */
::v-deep(.custom-multiselect .multiselect__content-wrapper) {
    background-color: #000;
    border: 1px solid #333;
    color: #fff;
    border-radius: 16px;
}

/* Options */
::v-deep(.custom-multiselect .multiselect__option) {
    background-color: #000;
    color: #fff;
}

/* Hover / highlight */
::v-deep(.custom-multiselect .multiselect__option--highlight) {
    background-color: #222;
}

/* Selected option */
::v-deep(.custom-multiselect .multiselect__option--selected) {
    background-color: #111;
    font-weight: 600;
}

/* Tags (multiple select) */
::v-deep(.custom-multiselect .multiselect__tag) {
    background-color: #111;
    color: #fff;
    border-radius: 16px;
}

/* Tag remove icon */
::v-deep(.custom-multiselect .multiselect__tag-icon) {
    color: #aaa;
}

::v-deep(.custom-multiselect .multiselect__tag-icon:hover) {
    background-color: transparent;
    color: #fff;
}

/* Arrow */
::v-deep(.custom-multiselect .multiselect__select::before) {
    border-color: #fff transparent transparent;
}

/* Disabled */
::v-deep(.custom-multiselect.multiselect--disabled) {
    opacity: 0.5;
}
</style>