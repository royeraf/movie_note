<script setup lang="ts">
defineProps<{
    stats: {
        total: number;
        watched: number;
        toWatch: number;
        favorites: number;
    };
}>();
</script>

<template>
    <div
        class="inline-flex items-center gap-2.5 md:gap-6 px-3.5 md:px-6 py-2 md:py-3 bg-black/5 dark:bg-white/5 rounded-xl md:rounded-2xl border border-black/5 dark:border-white/5 backdrop-blur-md w-auto">
        <div class="flex flex-col items-center">
            <span class="text-[9px] md:text-xs text-muted uppercase tracking-wide md:tracking-widest font-bold">Total</span>
            <span class="text-lg md:text-xl font-bold text-primary mt-0.5">{{ stats.total }}</span>
        </div>
        <div class="w-px h-8 md:h-9 bg-black/10 dark:bg-white/10"></div>
        <div class="flex flex-col items-center">
            <span class="text-[9px] md:text-xs text-muted uppercase tracking-wide md:tracking-widest font-bold whitespace-nowrap">Por Ver</span>
            <span class="text-lg md:text-xl font-bold text-amber-500 mt-0.5">{{ stats.toWatch }}</span>
        </div>
        <div class="w-px h-8 md:h-9 bg-black/10 dark:bg-white/10"></div>
        <div class="flex flex-col items-center">
            <span class="text-[9px] md:text-xs text-muted uppercase tracking-wide md:tracking-widest font-bold">Vistas</span>
            <span class="text-lg md:text-xl font-bold text-green-500 mt-0.5">{{ stats.watched }}</span>
        </div>
        <div class="w-px h-8 md:h-9 bg-black/10 dark:bg-white/10"></div>
        <div class="flex flex-col items-center">
            <span class="text-[9px] md:text-xs text-muted uppercase tracking-wide md:tracking-widest font-bold">Favoritos</span>
            <span class="text-lg md:text-xl font-bold text-red-500 mt-0.5">{{ stats.favorites }}</span>
        </div>
    </div>
</template>
