// Vue Pinia Store Template with TypeScript
// Usage: Complex state management (global cache, real-time sync)

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// Composition API style (recommended for Vue 3)
export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<{ id: string; name: string } | null>(null);
  const theme = ref<'light' | 'dark'>('light');
  const isLoading = ref(false);

  // Getters (computed)
  const isAuthenticated = computed(() => user.value !== null);
  const displayName = computed(() => user.value?.name ?? 'Guest');

  // Actions
  async function login(credentials: { email: string; password: string }) {
    isLoading.value = true;
    try {
      // API call here
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
      const userData = await response.json();
      user.value = userData;
    } finally {
      isLoading.value = false;
    }
  }

  function logout() {
    user.value = null;
  }

  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
  }

  return {
    // State
    user,
    theme,
    isLoading,
    // Getters
    isAuthenticated,
    displayName,
    // Actions
    login,
    logout,
    toggleTheme,
  };
});
