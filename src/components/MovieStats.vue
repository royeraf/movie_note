<script setup lang="ts">
defineProps<{
    stats: {
        total: number;
        watched: number;
        toWatch: number;
    };
}>();
</script>

<template>
    <div
        class="flex items-center gap-6 px-6 py-3 bg-black/5 dark:bg-white/5 rounded-2xl border border-black/5 dark:border-white/5 backdrop-blur-md">
        <div class="flex flex-col items-center">
            <span class="text-xs text-muted uppercase tracking-widest font-bold">Total</span>
            <span class="text-lg font-bold text-primary">{{ stats.total }}</span>
        </div>
        <div class="w-px h-8 bg-black/10 dark:bg-white/10"></div>
        <div class="flex flex-col items-center">
            <span class="text-xs text-muted uppercase tracking-widest font-bold">Por Ver</span>
            <span class="text-lg font-bold text-amber-500">{{ stats.toWatch }}</span>
        </div>
        <div class="w-px h-8 bg-black/10 dark:bg-white/10"></div>
        <div class="flex flex-col items-center">
            <span class="text-xs text-muted uppercase tracking-widest font-bold">Vistas</span>
            <span class="text-lg font-bold text-green-500">{{ stats.watched }}</span>
        </div>
    </div>
</template>
