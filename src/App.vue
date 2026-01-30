<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Search, Library, Clapperboard, Sun, Moon } from 'lucide-vue-next';

// Types
import type { Movie, OMDBMovie, NormalizedMovie } from './types';

// Composables
import { useTheme } from './composables/useTheme';
import { useMovies } from './composables/useMovies';
import { useSearch } from './composables/useSearch';

// Components
import MovieCard from './components/MovieCard.vue';
import MovieModal from './components/MovieModal.vue';
import MovieStats from './components/MovieStats.vue';

// Utils
import { extractColor, normalizeMovie } from './utils/movieUtils';

const { isDark, toggleTheme } = useTheme();
const { myMovies, stats, fetchMyMovies, addMovie, updateMovieData, deleteMovie } = useMovies();
const { searchQuery, searchResults, loading, searchColorSelections, searchMovies } = useSearch();

const selectedMovie = ref<NormalizedMovie | null>(null);
const showModal = ref(false);
const modalColor = ref('');
const currentTab = ref<'search' | 'my-list'>('my-list');
const filterStatus = ref<'all' | 'to-watch' | 'watched'>('all');

const openDetail = async (movie: Movie | OMDBMovie) => {
  const normalized = normalizeMovie(movie);
  selectedMovie.value = normalized;
  showModal.value = true;

  if (normalized.poster) {
    modalColor.value = await extractColor(normalized.poster);
  }
};

const closeModal = () => {
  showModal.value = false;
  setTimeout(() => {
    selectedMovie.value = null;
    modalColor.value = '';
  }, 300);
};

const handleSearch = async () => {
  await searchMovies();
  if (searchResults.value.length > 0) {
    currentTab.value = 'search';
  }
};

const filteredMovies = computed(() => {
  if (filterStatus.value === 'all') return myMovies.value;
  return myMovies.value.filter(m => m.status === filterStatus.value);
});

const isAlreadyInList = (id: string) => {
  return myMovies.value.some(m => m.imdb_id === id);
};

onMounted(fetchMyMovies);
</script>

<template>
  <div class="min-h-screen">
    <!-- Sticky Header -->
    <header class="sticky top-0 z-40 backdrop-blur-lg border-b border-black/5 dark:border-white/5 py-4 px-6">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-2 md:gap-3">
          <Clapperboard class="text-primary" :size="32" />
          <h1
            class="text-2xl md:text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            MovieNote
          </h1>
        </div>

        <button @click="toggleTheme"
          class="p-2.5 rounded-xl border border-black/5 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/5 transition-all text-muted">
          <Sun v-if="isDark" :size="20" />
          <Moon v-else :size="20" />
        </button>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 md:px-6 py-8 md:py-12">
      <!-- Title Section -->
      <div class="mb-10 md:mb-12">
        <p class="text-muted text-base md:text-lg max-w-2xl">
          Tu santuario personal de cine. Descubre nuevas historias y organiza las que ya te han marcado (Con códigos de
          color).
        </p>
      </div>

      <!-- Search Bar -->
      <div class="relative max-w-xl mb-10 md:mb-12 group">
        <Search
          class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors"
          :size="20" />
        <input v-model="searchQuery" @keyup.enter="handleSearch" type="text"
          class="w-full bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10 rounded-2xl py-3.5 md:py-4 pl-12 pr-6 text-base md:text-lg outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all font-sans"
          placeholder="Busca una película..." />
        <div v-if="loading" class="absolute right-4 top-1/2 -translate-y-1/2">
          <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex gap-2 min-[400px]:gap-4 mb-8">
        <button @click="currentTab = 'my-list'" class="flex-1 min-[400px]:flex-none btn"
          :class="currentTab === 'my-list' ? 'btn-primary' : 'btn-outline text-muted'">
          <Library :size="18" />
          <span class="hidden min-[400px]:inline">Mi Colección</span>
          <span class="min-[400px]:hidden">Colección</span>
        </button>
        <button v-if="searchResults.length > 0" @click="currentTab = 'search'" class="flex-1 min-[400px]:flex-none btn"
          :class="currentTab === 'search' ? 'btn-primary' : 'btn-outline text-muted'">
          <Search :size="18" />
          <span>Resultados</span>
        </button>
      </div>

      <!-- Content Views -->
      <div v-if="currentTab === 'my-list'" class="animate-in">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
          <div class="flex flex-wrap gap-2">
            <button @click="filterStatus = 'all'"
              :class="['px-4 py-1.5 rounded-lg text-sm font-medium transition-all', filterStatus === 'all' ? 'bg-primary/20 text-primary border border-primary/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Todas</button>
            <button @click="filterStatus = 'to-watch'"
              :class="['px-4 py-1.5 rounded-lg text-sm font-medium transition-all', filterStatus === 'to-watch' ? 'bg-amber-500/20 text-amber-600 dark:text-amber-500 border border-amber-500/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Por
              Ver</button>
            <button @click="filterStatus = 'watched'"
              :class="['px-4 py-1.5 rounded-lg text-sm font-medium transition-all', filterStatus === 'watched' ? 'bg-green-500/20 text-green-600 dark:text-green-500 border border-green-500/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Vistas</button>
          </div>

          <MovieStats :stats="stats" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <MovieCard v-for="movie in filteredMovies" :key="movie.imdb_id" :movie="movie" is-saved
            @open-detail="openDetail" @update-status="(id, status) => updateMovieData(id, { status })"
            @update-color="(id, color) => updateMovieData(id, { color })" @delete="deleteMovie" />
        </div>

        <div v-if="filteredMovies.length === 0"
          class="flex flex-col items-center justify-center py-20 text-muted glass-card border-dashed">
          <Clapperboard :size="48" class="mb-4 opacity-10" />
          <p class="text-base font-medium">Lista vacía</p>
        </div>
      </div>

      <!-- Search Section -->
      <div v-if="currentTab === 'search'" class="animate-in">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          <MovieCard v-for="movie in searchResults" :key="movie.imdbID"
            :movie="{ ...movie, isAlreadyInList: isAlreadyInList(movie.imdbID) }"
            :selected-color="searchColorSelections[movie.imdbID]" @open-detail="openDetail"
            @add-movie="(m, s) => addMovie(m, s, searchColorSelections[m.imdbID])"
            @select-color="(id, c) => searchColorSelections[id] = c" />
        </div>
      </div>
    </main>

    <MovieModal :show="showModal" :movie="selectedMovie" :is-dark="isDark" :modal-color="modalColor"
      @close="closeModal" />
  </div>
</template>

<style>
:root {
  --bg-card-rgb: 255, 255, 255;
}

.dark {
  --bg-card-rgb: 15, 23, 42;
}

.movie-card-horizontal {
  background: rgba(var(--bg-card-rgb), 0.5);
  backdrop-filter: blur(28px) saturate(180%);
}

.dark .movie-card-horizontal {
  background: rgba(var(--bg-card-rgb), 0.7);
}

.poster-mask {
  mask-image: linear-gradient(to left, black 85%, transparent 100%);
  -webkit-mask-image: linear-gradient(to left, black 85%, transparent 100%);
}

.font-serif {
  font-family: 'Instrument Serif', serif;
}

.animate-in {
  animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.modal-enter-from .bg-slate-900,
.modal-leave-to .bg-slate-900 {
  transform: scale(0.95) translateY(10px);
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
