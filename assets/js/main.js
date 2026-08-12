/**
 * Main Application JS
 * Handles Theme Engine (Dark/Light/System) & global initializations.
 * Configured for Tailwind darkMode: 'class'.
 */

(function () {
  'use strict';

  // Apply theme immediately before rendering to prevent FOUC
  function applyTheme() {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    // Default to dark mode if not specified, or if system prefers dark
    const isDark = savedTheme ? savedTheme === 'dark' : systemPrefersDark;

    if (isDark) {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    }
  }

  applyTheme();

  document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    updateCopyrightYear();
  });

  function initThemeToggle() {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    if (!toggleBtns.length) return;

    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.contains('dark');
        const nextTheme = isDark ? 'light' : 'dark';

        if (nextTheme === 'dark') {
          document.documentElement.classList.add('dark');
          document.documentElement.classList.remove('light');
        } else {
          document.documentElement.classList.remove('dark');
          document.documentElement.classList.add('light');
        }

        localStorage.setItem('theme', nextTheme);
        btn.setAttribute('aria-label', `Switch to ${isDark ? 'dark' : 'light'} theme`);
      });
    });
  }

  function updateCopyrightYear() {
    const yearEls = document.querySelectorAll('.current-year');
    const currentYear = new Date().getFullYear();
    yearEls.forEach(el => {
      el.textContent = currentYear;
    });
  }
})();
