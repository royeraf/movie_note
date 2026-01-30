<script setup lang="ts">
import { X } from 'lucide-vue-next';
import { getPosterUrl } from '../utils/movieUtils';
import type { NormalizedMovie } from '../types';

defineProps<{
    show: boolean;
    movie: NormalizedMovie | null;
    isDark: boolean;
    modalColor: string;
}>();

const emit = defineEmits<{
    (e: 'close'): void;
}>();
</script>

<template>
    <Transition name="modal">
        <div v-if="show"
            class="fixed inset-0 z-[60] flex items-center justify-center p-4 sm:p-6 backdrop-blur-xl bg-black/60"
            @click.self="emit('close')">
            <div class="relative w-full max-w-2xl rounded-[2.5rem] overflow-hidden shadow-2xl border border-white/10 duration-300 ease-out bg-slate-900"
                :style="{
                    backgroundColor: modalColor || (isDark ? '#0f172a' : '#ffffff'),
                }">

                <!-- Ambient Background Layer -->
                <div class="absolute inset-0 opacity-40 pointer-events-none" :style="{
                    background: `radial-gradient(circle at 70% 30%, ${modalColor || 'transparent'}, transparent 100%)`
                }">
                </div>

                <div class="flex flex-col md:flex-row min-h-[400px] relative z-10">
                    <!-- Poster Side -->
                    <div class="w-full md:w-2/5 h-64 md:h-auto relative">
                        <img :src="getPosterUrl(movie.poster)" :alt="movie.title" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-l from-[rgba(var(--bg-card-rgb),0.8)] via-transparent to-transparent"
                            :style="{
                                '--tw-gradient-from': modalColor ? `${modalColor}CC` : 'var(--bg-card-rgb)'
                            }">
                        </div>
                    </div>

                    <!-- Info Side -->
                    <div
                        class="w-full md:w-3/5 p-8 flex flex-col justify-between backdrop-blur-md bg-black/20 dark:bg-black/40">
                        <div>
                            <div class="flex justify-between items-start mb-4">
                                <h2 class="text-3xl font-bold leading-tight line-clamp-2">{{ movie.title }}</h2>
                                <button @click="emit('close')"
                                    class="p-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-full transition-colors text-muted hover:text-main shrink-0">
                                    <X :size="24" />
                                </button>
                            </div>

                            <div class="flex items-center gap-3 mb-6">
                                <span class="px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-bold">{{
                                    movie.year }}</span>
                                <span v-if="movie.status" :class="['px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider',
                                    movie.status === 'watched' ? 'bg-green-500/10 text-green-500' : 'bg-amber-500/10 text-amber-500']">
                                    {{ movie.status === 'watched' ? 'Vista' : 'Pendiente' }}
                                </span>
                            </div>

                            <div class="space-y-4">
                                <div>
                                    <h4 class="text-xs font-bold uppercase tracking-widest text-muted mb-2">Actores</h4>
                                    <p class="text-main font-serif italic text-lg leading-relaxed line-clamp-2">{{
                                        movie.actors }}
                                    </p>
                                </div>

                                <div>
                                    <h4 class="text-xs font-bold uppercase tracking-widest text-muted mb-2">Sinopsis
                                    </h4>
                                    <p class="text-muted leading-relaxed text-sm line-clamp-4">{{ movie.description }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-8">
                            <button @click="emit('close')"
                                class="w-full btn btn-primary h-12 rounded-2xl justify-center text-sm font-bold shadow-xl">
                                Cerrar Detalles
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Transition>
</template>
