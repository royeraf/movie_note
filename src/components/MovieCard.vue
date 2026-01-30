<script setup lang="ts">
import { Check, Clock, Trash2, Info, Plus } from 'lucide-vue-next';
import { COLORS } from '../constants';
import { getPosterUrl, getColorClass } from '../utils/movieUtils';

interface Props {
    movie: any;
    isSaved?: boolean;
    selectedColor?: string | null;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    (e: 'open-detail', movie: any): void;
    (e: 'update-status', imdbId: string, status: string): void;
    (e: 'update-color', imdbId: string, color: string): void;
    (e: 'delete', imdbId: string): void;
    (e: 'add-movie', movie: any, status: 'to-watch' | 'watched'): void;
    (e: 'select-color', imdbId: string, color: string): void;
}>();

const handleUpdateStatus = () => {
    const newStatus = props.movie.status === 'watched' ? 'to-watch' : 'watched';
    emit('update-status', props.movie.imdb_id, newStatus);
};
</script>

<template>
    <div class="movie-card-horizontal group relative overflow-hidden rounded-3xl transition-all hover:scale-[1.02] hover:shadow-2xl active:scale-[0.98] min-h-[200px] border"
        :class="getColorClass(isSaved ? movie.color : selectedColor)">

        <!-- Full Background Poster -->
        <div class="absolute inset-0 z-0">
            <img :src="getPosterUrl(isSaved ? movie.poster_path : movie.Poster)"
                :alt="isSaved ? movie.title : movie.Title"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
            <!-- Legibility Gradient Overlay -->
            <div
                class="absolute inset-0 bg-gradient-to-r from-[rgba(var(--bg-card-rgb),0.95)] via-[rgba(var(--bg-card-rgb),0.8)] to-[rgba(var(--bg-card-rgb),0.1)] dark:from-[rgba(var(--bg-card-rgb),0.9)] dark:via-[rgba(var(--bg-card-rgb),0.7)]">
            </div>
        </div>

        <div class="relative z-10 flex flex-col justify-between h-full p-5 md:p-6 min-h-[220px]">
            <div class="max-w-[70%]">
                <h3
                    class="font-bold text-lg md:text-xl mb-1 line-clamp-1 truncate group-hover:text-primary transition-colors">
                    {{ isSaved ? movie.title : movie.Title }}
                </h3>
                <p class="text-muted text-sm font-medium mb-2">{{ isSaved ? movie.release_year : movie.Year }}</p>
                <p class="text-muted text-xs italic line-clamp-2 min-h-[2rem] leading-relaxed mb-4 font-serif">
                    {{ isSaved ? movie.actors : movie.Actors }}
                </p>

                <!-- Color Selection -->
                <div class="flex gap-4 mb-4 relative z-20">
                    <button v-for="c in COLORS" :key="c.id"
                        @click.stop="isSaved ? emit('update-color', movie.imdb_id, c.id) : emit('select-color', movie.imdbID, c.id)"
                        class="relative w-9 h-9 rounded-full transition-all active:scale-95 flex items-center justify-center p-[3px]"
                        :class="[(isSaved ? movie.color === c.id : selectedColor === c.id) ? `ring-2 ${c.ring} scale-110 opacity-100` : 'opacity-40 hover:opacity-100']">

                        <div class="w-full h-full rounded-full shadow-lg" :class="c.class"></div>

                        <div v-if="(isSaved ? movie.color === c.id : selectedColor === c.id)"
                            class="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-white flex items-center justify-center shadow-xl animate-in scale-110">
                            <Check :size="12" stroke-width="4" :class="c.text" />
                        </div>
                    </button>
                </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-3 mt-4 w-full relative z-20">
                <template v-if="isSaved">
                    <button @click.stop="handleUpdateStatus"
                        class="flex-1 btn btn-primary h-11 text-[10px] md:text-xs rounded-xl shadow-lg shadow-primary/20 whitespace-nowrap justify-center">
                        <component :is="movie.status === 'watched' ? Clock : Check" :size="14" />
                        {{ movie.status === 'watched' ? 'Re-ver' : 'Ya la vi' }}
                    </button>
                    <button @click.stop="emit('open-detail', movie)"
                        class="w-11 h-11 flex items-center justify-center btn btn-outline bg-white/10 dark:bg-black/20 rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md group/info shrink-0">
                        <Info :size="14" class="text-muted group-hover/info:text-primary transition-colors" />
                    </button>
                    <button @click.stop="emit('delete', movie.imdb_id)"
                        class="w-11 h-11 flex items-center justify-center btn btn-outline bg-white/10 dark:bg-black/20 rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md group/trash shrink-0">
                        <Trash2 :size="14" class="text-muted group-hover/trash:text-red-500 transition-colors" />
                    </button>
                </template>

                <template v-else>
                    <div class="flex flex-col gap-2 w-full">
                        <div v-if="!movie.isAlreadyInList" class="grid grid-cols-2 gap-3 w-full">
                            <button @click.stop="emit('add-movie', movie, 'to-watch')"
                                class="btn btn-primary h-11 text-[10px] md:text-xs rounded-xl shadow-lg shadow-primary/20 whitespace-nowrap justify-center">
                                <Plus :size="14" /> Añadir
                            </button>
                            <div class="flex gap-2">
                                <button @click.stop="emit('add-movie', movie, 'watched')"
                                    class="flex-1 btn btn-outline bg-white/10 dark:bg-black/20 h-11 text-[10px] md:text-xs rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md whitespace-nowrap justify-center">
                                    <Check :size="14" /> Ya la vi
                                </button>
                                <button @click.stop="emit('open-detail', movie)"
                                    class="w-11 h-11 flex items-center justify-center btn btn-outline bg-white/10 dark:bg-black/20 rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md group/info shrink-0">
                                    <Info :size="14"
                                        class="text-muted group-hover/info:text-primary transition-colors" />
                                </button>
                            </div>
                        </div>
                        <div v-else class="flex gap-2 w-full">
                            <button disabled
                                class="flex-1 btn btn-outline bg-white/5 dark:bg-black/10 h-11 text-[10px] md:text-xs opacity-40 cursor-not-allowed rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md justify-center">
                                <Check :size="14" /> En tu lista
                            </button>
                            <button @click.stop="emit('open-detail', movie)"
                                class="w-11 h-11 flex items-center justify-center btn btn-outline bg-white/10 dark:bg-black/20 rounded-xl border-black/5 dark:border-white/5 backdrop-blur-md group/info shrink-0">
                                <Info :size="14" class="text-muted group-hover/info:text-primary transition-colors" />
                            </button>
                        </div>
                    </div>
                </template>
            </div>

            <!-- Status Badge (Saved Only) -->
            <div v-if="isSaved" class="absolute top-4 right-4">
                <span :class="['px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider backdrop-blur-md border border-white/20 shadow-xl',
                    movie.status === 'watched' ? 'bg-green-500/80 text-white' : 'bg-amber-500/80 text-white']">
                    {{ movie.status === 'watched' ? 'Vista' : 'Pend' }}
                </span>
            </div>
        </div>
    </div>
</template>
