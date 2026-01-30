import { ref, computed } from 'vue';
import axios from 'axios';
import type { Movie } from '../types';

const API_BASE = '/api';

export function useMovies() {
  const myMovies = ref<Movie[]>([]);
  const loading = ref(false);

  const fetchMyMovies = async () => {
    loading.value = true;
    try {
      const res = await axios.get(`${API_BASE}/movies`);
      myMovies.value = res.data;
    } catch (e) {
      console.error("Error fetching movies", e);
    } finally {
      loading.value = false;
    }
  };

  const addMovie = async (movie: any, status: 'to-watch' | 'watched' = 'to-watch', color: string | null = null) => {
    try {
      await axios.post(`${API_BASE}/movies`, {
        imdb_id: movie.imdbID,
        title: movie.Title,
        poster_path: movie.Poster === 'N/A' ? null : movie.Poster,
        release_year: movie.Year,
        status: status,
        color: color,
        actors: movie.Actors,
        description: movie.Plot || movie.description
      });
      await fetchMyMovies();
    } catch (e) {
      console.error("Error adding movie", e);
    }
  };

  const updateMovieData = async (imdb_id: string, updates: { status?: string, color?: string }) => {
    try {
      await axios.patch(`${API_BASE}/movies/${imdb_id}`, null, { params: updates });
      await fetchMyMovies();
    } catch (e) {
      console.error("Error updating movie", e);
    }
  };

  const deleteMovie = async (imdb_id: string) => {
    try {
      await axios.delete(`${API_BASE}/movies/${imdb_id}`);
      await fetchMyMovies();
    } catch (e) {
      console.error("Error deleting", e);
    }
  };

  const stats = computed(() => {
    const total = myMovies.value.length;
    const watched = myMovies.value.filter(m => m.status === 'watched').length;
    const toWatch = total - watched;
    return { total, watched, toWatch };
  });

  return {
    myMovies,
    loading,
    fetchMyMovies,
    addMovie,
    updateMovieData,
    deleteMovie,
    stats
  };
}
