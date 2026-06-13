<template>
    <div class="fixed inset-0 flex items-center justify-center z-50">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/40" @click="$emit('close')"></div>

        <!-- Modal Content -->
        <div class="modal rounded-2xl shadow-[0_30px_70px_-40px_rgba(15,23,42,0.4)] max-w-md p-6 z-10 transition transform duration-300 w-full grid grid-cols-12"
            style="max-width: 550px;">
            <div class="col-span-6">
                <h2 class="text-xl font-bold text-slate-900" v-if="title">{{ title }}</h2>
            </div>
            <div class="col-span-6 flex justify-end">
                <slot name="next-header"></slot>
            </div>
            <!-- Named slot for modal content -->
            <div class="col-span-12 mt-5">
                <slot name="modal-content"></slot>
            </div>

            <div class="flex justify-end mt-4 gap-2 col-span-12">
                <button @click="$emit('delete')" class="btn btn_delete px-4 py-2 rounded" v-if="deleteButton">
                    Smazat
                </button>
                <button @click="$emit('close')" class="btn btn_cancel px-4 py-2 rounded">
                    Zavřít
                </button>
                <button @click="$emit('submit')" class="btn btn_submit px-4 py-2 rounded" v-if="submitButton">
                    Potvrdit
                </button>
            </div>
        </div>
    </div>
</template>
<script setup>
defineProps({
    title: String,
    deleteButton: {
        type: Boolean,
        default: false
    },
    submitButton: {
        type: Boolean,
        default: false
    }
})

</script>
<style scoped>
.modal {
    background-color: var(--white);
    color: var(--text-color);
    border: 1px solid #e2e8f0;
}
</style>