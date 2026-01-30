<script setup lang="ts">
import { X, AlertTriangle } from 'lucide-vue-next';

defineProps<{
    show: boolean;
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
}>();

const emit = defineEmits<{
    (e: 'confirm'): void;
    (e: 'cancel'): void;
}>();
</script>

<template>
    <Transition name="modal">
        <div v-if="show"
            class="fixed inset-0 z-[70] flex items-center justify-center p-4 backdrop-blur-xl bg-black/60 dark:bg-black/70"
            @click.self="emit('cancel')">
            <div
                class="relative w-full max-w-md rounded-2xl md:rounded-3xl overflow-hidden shadow-2xl border border-black/10 dark:border-white/10 bg-white dark:bg-slate-900 animate-in">

                <!-- Header -->
                <div class="flex items-start gap-3 p-5 md:p-6 border-b border-black/5 dark:border-white/10">
                    <div class="p-2 rounded-xl bg-red-500/10 dark:bg-red-500/20">
                        <AlertTriangle :size="20" class="text-red-600 dark:text-red-500" />
                    </div>
                    <div class="flex-1">
                        <h3 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white mb-1">{{ title }}</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">{{ message }}</p>
                    </div>
                    <button @click="emit('cancel')"
                        class="p-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white shrink-0">
                        <X :size="18" />
                    </button>
                </div>

                <!-- Actions -->
                <div class="flex gap-3 p-5 md:p-6 bg-gray-50 dark:bg-white/5">
                    <button @click="emit('cancel')"
                        class="flex-1 h-11 md:h-12 rounded-xl text-sm font-medium bg-white dark:bg-white/10 border border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/20 transition-colors">
                        {{ cancelText || 'Cancelar' }}
                    </button>
                    <button @click="emit('confirm')"
                        class="flex-1 h-11 md:h-12 rounded-xl text-sm font-bold bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 text-white transition-colors shadow-lg shadow-red-500/20 dark:shadow-red-500/30">
                        {{ confirmText || 'Eliminar' }}
                    </button>
                </div>
            </div>
        </div>
    </Transition>
</template>
