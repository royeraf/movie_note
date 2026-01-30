<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { Search, Library, Clapperboard, Sun, Moon, Heart } from 'lucide-vue-next';

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
import ConfirmDialog from './components/ConfirmDialog.vue';

// Utils
import { extractColor, normalizeMovie } from './utils/movieUtils';

const { isDark, toggleTheme } = useTheme();
const { myMovies, stats, fetchMyMovies, addMovie, updateMovieData, deleteMovie } = useMovies();
const { searchQuery, searchResults, loading, searchColorSelections, searchMovies } = useSearch();

const selectedMovie = ref<NormalizedMovie | null>(null);
const showModal = ref(false);
const modalColor = ref('');
const currentTab = ref<'search' | 'my-list' | 'favorites'>('my-list');
const filterStatus = ref<'all' | 'to-watch' | 'watched'>('all');
const showConfirmDialog = ref(false);
const movieToDelete = ref<string | null>(null);

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

const favoriteMovies = computed(() => {
  return myMovies.value.filter(m => m.is_favorite);
});

const isAlreadyInList = (id: string) => {
  return myMovies.value.some(m => m.imdb_id === id);
};

const toggleFavorite = async (imdbId: string) => {
  const movie = myMovies.value.find(m => m.imdb_id === imdbId);
  if (movie) {
    await updateMovieData(imdbId, { is_favorite: !movie.is_favorite });
  }
};

const handleDeleteClick = (imdbId: string) => {
  movieToDelete.value = imdbId;
  showConfirmDialog.value = true;
};

const confirmDelete = async () => {
  if (movieToDelete.value) {
    await deleteMovie(movieToDelete.value);
    showConfirmDialog.value = false;
    movieToDelete.value = null;
  }
};

const cancelDelete = () => {
  showConfirmDialog.value = false;
  movieToDelete.value = null;
};

onMounted(fetchMyMovies);
</script>

<template>
  <div class="min-h-screen">
    <!-- Sticky Header -->
    <header class="sticky top-0 z-40 backdrop-blur-lg border-b border-black/5 dark:border-white/5 py-3 md:py-4 px-4 md:px-6">
      <div class="max-w-6xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-2 md:gap-3">
          <Clapperboard class="text-primary" :size="28" />
          <h1
            class="text-xl md:text-2xl lg:text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            MovieNote
          </h1>
        </div>

        <button @click="toggleTheme"
          class="p-2 md:p-2.5 rounded-xl border border-black/5 dark:border-white/10 hover:bg-black/5 dark:hover:bg-white/5 transition-all text-muted shrink-0">
          <Sun v-if="isDark" :size="18" class="md:w-5 md:h-5" />
          <Moon v-else :size="18" class="md:w-5 md:h-5" />
        </button>
      </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 md:px-6 py-6 md:py-8 lg:py-12">
      <!-- Title Section -->
      <div class="mb-6 md:mb-10 lg:mb-12">
        <p class="text-muted text-sm md:text-base lg:text-lg max-w-2xl leading-relaxed">
          Tu santuario personal de cine. Descubre nuevas historias y organiza las que ya te han marcado (Con códigos de
          color).
        </p>
      </div>

      <!-- Search Bar -->
      <div class="relative max-w-xl mb-6 md:mb-10 lg:mb-12 group">
        <Search
          class="absolute left-3 md:left-4 top-1/2 -translate-y-1/2 text-slate-600 dark:text-slate-400 group-focus-within:text-primary transition-colors"
          :size="18" />
        <input v-model="searchQuery" @keyup.enter="handleSearch" type="text"
          class="w-full bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/10 rounded-xl md:rounded-2xl py-3 md:py-3.5 lg:py-4 pl-10 md:pl-12 pr-24 md:pr-28 text-sm md:text-base lg:text-lg outline-none focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all font-sans [&::placeholder]:text-slate-500 dark:[&::placeholder]:text-slate-400"
          :style="{ color: isDark ? '#ffffff' : '#0f172a' }"
          placeholder="Busca una película..." />
        <div v-if="loading" class="absolute right-14 md:right-16 top-1/2 -translate-y-1/2">
          <div class="animate-spin h-4 w-4 md:h-5 md:w-5 border-2 border-primary border-t-transparent rounded-full"></div>
        </div>
        <button @click="handleSearch" :disabled="!searchQuery.trim() || loading"
          class="absolute right-2 md:right-3 top-1/2 -translate-y-1/2 btn btn-primary h-9 md:h-10 px-3 md:px-4 rounded-lg md:rounded-xl text-xs md:text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-all">
          Buscar
        </button>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex gap-2 md:gap-4 mb-6 md:mb-8">
        <button @click="currentTab = 'my-list'" class="flex-1 md:flex-none btn text-xs md:text-sm"
          :class="currentTab === 'my-list' ? 'btn-primary' : 'btn-outline text-muted'">
          <Library :size="16" class="md:w-[18px] md:h-[18px]" />
          <span class="hidden min-[360px]:inline">Mi Colección</span>
          <span class="min-[360px]:hidden">Mis Pelis</span>
        </button>
        <button @click="currentTab = 'favorites'" class="flex-1 md:flex-none btn text-xs md:text-sm"
          :class="currentTab === 'favorites' ? 'btn-primary' : 'btn-outline text-muted'">
          <Heart :size="16" class="md:w-[18px] md:h-[18px]" />
          <span>Favoritos</span>
        </button>
        <button v-if="searchResults.length > 0" @click="currentTab = 'search'" class="flex-1 md:flex-none btn text-xs md:text-sm"
          :class="currentTab === 'search' ? 'btn-primary' : 'btn-outline text-muted'">
          <Search :size="16" class="md:w-[18px] md:h-[18px]" />
          <span>Resultados</span>
        </button>
      </div>

      <!-- Content Views -->
      <div v-if="currentTab === 'my-list'" class="animate-in">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 md:gap-6 mb-6 md:mb-8">
          <div class="flex flex-wrap gap-2">
            <button @click="filterStatus = 'all'"
              :class="['px-3 md:px-4 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all', filterStatus === 'all' ? 'bg-primary/20 text-primary border border-primary/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Todas</button>
            <button @click="filterStatus = 'to-watch'"
              :class="['px-3 md:px-4 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all whitespace-nowrap', filterStatus === 'to-watch' ? 'bg-amber-500/20 text-amber-600 dark:text-amber-500 border border-amber-500/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Por
              Ver</button>
            <button @click="filterStatus = 'watched'"
              :class="['px-3 md:px-4 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all', filterStatus === 'watched' ? 'bg-green-500/20 text-green-600 dark:text-green-500 border border-green-500/30' : 'bg-black/5 dark:bg-white/5 text-muted hover:text-main']">Vistas</button>
          </div>

          <MovieStats :stats="stats" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
          <MovieCard v-for="movie in filteredMovies" :key="movie.imdb_id" :movie="movie" is-saved
            @open-detail="openDetail" @update-status="(id, status) => updateMovieData(id, { status })"
            @update-color="(id, color) => updateMovieData(id, { color })" @toggle-favorite="toggleFavorite"
            @delete="handleDeleteClick" />
        </div>

        <div v-if="filteredMovies.length === 0"
          class="flex flex-col items-center justify-center py-16 md:py-20 text-muted glass-card border-dashed">
          <Clapperboard :size="40" class="md:w-12 md:h-12 mb-3 md:mb-4 opacity-10" />
          <p class="text-sm md:text-base font-medium">Lista vacía</p>
        </div>
      </div>

      <!-- Favorites Section -->
      <div v-if="currentTab === 'favorites'" class="animate-in">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 md:gap-6 mb-6 md:mb-8">
          <h2 class="text-xl md:text-2xl font-bold flex items-center gap-2 md:gap-3">
            <Heart :size="24" class="text-red-500 fill-red-500" />
            <span>Mis Favoritos</span>
          </h2>
          <MovieStats :stats="stats" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
          <MovieCard v-for="movie in favoriteMovies" :key="movie.imdb_id" :movie="movie" is-saved
            @open-detail="openDetail" @update-status="(id, status) => updateMovieData(id, { status })"
            @update-color="(id, color) => updateMovieData(id, { color })" @toggle-favorite="toggleFavorite"
            @delete="handleDeleteClick" />
        </div>

        <div v-if="favoriteMovies.length === 0"
          class="flex flex-col items-center justify-center py-16 md:py-20 text-muted glass-card border-dashed">
          <Heart :size="40" class="md:w-12 md:h-12 mb-3 md:mb-4 opacity-10" />
          <p class="text-sm md:text-base font-medium">No tienes películas favoritas aún</p>
          <p class="text-xs md:text-sm text-muted mt-2">Marca tus películas favoritas con el ícono de corazón</p>
        </div>
      </div>

      <!-- Search Section -->
      <div v-if="currentTab === 'search'" class="animate-in">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">
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

    <ConfirmDialog :show="showConfirmDialog" title="¿Eliminar película?"
      :message="`¿Estás seguro de que deseas eliminar '${myMovies.find(m => m.imdb_id === movieToDelete)?.title || 'esta película'}' de tu lista? Esta acción no se puede deshacer.`"
      confirm-text="Eliminar" cancel-text="Cancelar" @confirm="confirmDelete" @cancel="cancelDelete" />
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
