import { ref } from 'vue';
import axios from 'axios';

const API_BASE = '/api';

export function useSearch() {
  const searchQuery = ref('');
  const searchResults = ref<any[]>([]);
  const loading = ref(false);
  const searchColorSelections = ref<Record<string, string>>({});

  const searchMovies = async () => {
    if (!searchQuery.value) return;
    loading.value = true;
    try {
      const res = await axios.get(`${API_BASE}/search`, { params: { query: searchQuery.value } });
      searchResults.value = res.data.Search || [];
      searchColorSelections.value = {};
    } catch (e) {
      console.error("Error searching", e);
    } finally {
      loading.value = false;
    }
  };

  const clearSearch = () => {
    searchQuery.value = '';
    searchResults.value = [];
    searchColorSelections.value = {};
  };

  return {
    searchQuery,
    searchResults,
    loading,
    searchColorSelections,
    searchMovies,
    clearSearch
  };
}
