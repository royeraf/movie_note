import { ref, watch } from 'vue';

export function useTheme() {
  const isDark = ref(localStorage.getItem('theme') !== 'light');

  const toggleTheme = () => {
    isDark.value = !isDark.value;
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
  };

  watch(isDark, (val) => {
    if (val) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, { immediate: true });

  return {
    isDark,
    toggleTheme
  };
}
